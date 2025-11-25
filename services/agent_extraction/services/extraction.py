import json
from pathlib import Path
import re
import time
from typing import Dict, Tuple
from libs.errors.exceptions import ErrorCode, ExtractionError, ValidationError, NotFoundError
import aiohttp
import aiofiles
import aioboto3
from urllib.parse import urlparse
import tempfile
import os
import base64
import shutil
from configurations.config import Config
from logs.logger import log_function_call
from services.agent_extraction.services.amazon_extraction import smart_detect
from services.agent_extraction.services.mistral_agent import MistralAgent, MistralAgentRunType
# from docling.datamodel.base_models import InputFormat
# from docling.datamodel.pipeline_options import PdfPipelineOptions, AcceleratorOptions, AcceleratorDevice
# from docling.document_converter import DocumentConverter, PdfFormatOption
from botocore.exceptions import ClientError
from PIL import ImageFile, Image
from commonmark import Parser

from PyPDF2 import PdfReader, PdfWriter

from .agent_extraction_document_info import *

SUPPORTED_EXT = {"jpg", "jpeg", "png", "gif", "bmp", "webp", "pdf", "docx"}
SUPPORTED_MODELS = {"docling", "mistral", "awsDocumentExtractOcr"}

IMAGE_RESOLUTION_SCALE = 2.0
ImageFile.LOAD_TRUNCATED_IMAGES = True


@log_function_call
def md_to_json_ast(md_text):
    parser = Parser()
    root   = parser.parse(md_text)

    def node_to_dict(node):
        d = {
            "type":       node.t,
            "literal":    node.literal,
            "destination": node.destination,
            "title":      node.title,
            "level":      node.level
        }
        children = []
        child = node.first_child
        while child:
            children.append(node_to_dict(child))
            child = child.next
        if children:
            d["children"] = children
        return d

    return node_to_dict(root)

@log_function_call
def extract_and_clean_json(raw: str) -> Dict:
    m = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", raw, flags=re.IGNORECASE)
    json_snippet = m.group(1) if m else raw

    json_snippet = json_snippet.strip()

    try:
        unescaped = json_snippet
    except Exception:
        unescaped = json_snippet.replace("\\n", "\n").replace("\\t", "\t")
    
    unescaped = unescaped.lstrip("\ufeff \n\r\t").replace("\n", "")
    
    return json.loads(unescaped)

@log_function_call
def build_key_filename(url: str, filename: str) -> str:
    
    parts = urlparse(url).path.strip("/").split("/")
    #parts[-1] = filename
    return "".join(parts[-1])

@log_function_call
async def download_file(source: dict) -> tuple[str, str]:
    tmpdir = tempfile.mkdtemp()
    file_path = os.path.join(tmpdir, f"{source['name']}.{source['extension']}")
    chunk_size = 64 * 1024
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(source['url']) as response:
                response.raise_for_status()
                async with aiofiles.open(file_path, 'wb') as out_file:
                    async for chunk in response.content.iter_chunked(chunk_size):
                        await out_file.write(chunk)    
        return file_path, tmpdir
    except Exception as e:
        print(f"Error: {e}")
        error_message = f"Error downloading arquivo: {e}"
        return error_message, tmpdir

@log_function_call    
async def download_file_s3(source: dict) -> tuple[str, str]:
    tmpdir   = tempfile.mkdtemp()
    filename = f"{source['name']}.{source['extension']}"
    file_path = os.path.join(tmpdir, filename.replace('/', '\\'))
    chunk_size = 64 * 1024

    parsed = urlparse(source["url"])
    if parsed.scheme == "s3":
        bucket_name = parsed.netloc
    else:
        bucket_name = parsed.netloc.split(".")[0]

    session = aioboto3.Session(
        aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
    )
    
    key_filename = "/".join(source["url"].split("/")[3:])

    async with session.client("s3", region_name=Config.AWS_REGION) as s3_client:
        try:
            #print("Bucket:", bucket_name, "Key:", filename)
            resp = await s3_client.get_object(Bucket=bucket_name, Key=key_filename)
        except ClientError as e:
            code = e.response["Error"]["Code"]
            if code == "NoSuchKey":
                raise FileNotFoundError(f"O objeto '{filename}' não existe no bucket '{bucket_name}'")
            else:
                raise

        body = resp["Body"]
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await body.read(chunk_size):
                await f.write(chunk)

    return file_path, tmpdir

@log_function_call
async def decode_base64(source: dict) -> tuple[str, str]:
    
    tmpdir   = tempfile.mkdtemp()
    file_path = os.path.join(tmpdir, f"{source['name']}.{source['extension']}")

    try:
        b64str = source.get('data') or source.get('url', '')

        missing = len(b64str) % 4
        if missing:
            b64str += "=" * (4 - missing)

        data = base64.b64decode(b64str)

        async with aiofiles.open(file_path, "wb") as f:
            await f.write(data)

        return file_path, tmpdir

    except Exception as e:
        shutil.rmtree(tmpdir, ignore_errors=True)
        raise ValueError(f"Falha ao decodificar Base64: {e}")

@log_function_call
async def apply_docling(path: str, tmpdir: str) -> tuple[str, bool]:

    # chunk_size = 5
    # src = Path(path).resolve()
    # if not src.exists():
    #     return f"Arquivo não encontrado: {src}", {}

    # ext = src.suffix.lower()
    # temp_dir = Path(tempfile.mkdtemp())
    # pdf_input: Path

    # if ext in {".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif"}:
    #     pdf_input = temp_dir / f"{src.stem}.pdf"
    #     try:
    #         Image.open(src).save(pdf_input, "PDF", resolution=300.0)
    #     except Exception as e:
    #         return f"Falha ao converter imagem para PDF: {e}", {}
    # elif ext == ".pdf":
    #     pdf_input = src
    # else:
    #     return f"Extensão não suportada: {ext}", {}

    # try:
        
    #     converter = DocumentConverter()
        
    #     if Config.CUDA_CONFIG == 'True':
    #         converter = DocumentConverter(
    #             format_options={
    #                 InputFormat.PDF: PdfFormatOption(pipeline_options=pdf_opts)
    #             }
    #         )
        
    #     reader = PdfReader(str(pdf_input))
    #     total_pages = len(reader.pages)
    #     text_parts: list[str] = []
        
    #     if total_pages <= chunk_size:
    #         result = await asyncio.to_thread(converter.convert, str(pdf_input))
    #         text_parts.append(result.document.export_to_text())
    #     else:
    #         for start in range(0, total_pages, chunk_size):
    #             writer = PdfWriter()
    #             end = min(start + chunk_size, total_pages)
    #             for page in reader.pages[start:end]:
    #                 writer.add_page(page)

    #             chunk_path = temp_dir / f"chunk_{start//chunk_size}.pdf"
    #             with open(chunk_path, "wb") as f:
    #                 writer.write(f)

    #             result = await asyncio.to_thread(converter.convert, str(chunk_path))
    #             text_parts.append(result.document.export_to_text())
        
    #     full_text = "\n".join(text_parts)
    # except Exception as e:
    #     print(f"Error: {e}")
    #     error_message = f"Error applying Docling: {e}"
    #     return error_message, False
    
    #return full_text, True
    return "Docling extraction is not implemented yet.", False

@log_function_call
async def apply_mistral(payload: dict, path: str, tmpdir: str) -> tuple[str, bool]:
    
    try:
        prompt = ""
        if 'prompt' in payload['options']['modelOptions']:
            prompt = payload['options']['modelOptions']['prompt']
        
        mistral = MistralAgent(agent_name='mistral_agent', system_prompt=prompt,)
        
        model_name = "mistral-ocr-2505"
        type_model = MistralAgentRunType.OCR
        
        if payload['options']['modelOptions']['type_model'] == "DOCUMENT_UNDERSTANDING":
            type_model = MistralAgentRunType.DOCUMENT_UNDERSTANDING
            prompt = payload['options']['modelOptions']['prompt']
            model_name = payload['options']['modelOptions']['model_name']
            
        text = await mistral.run_concurrent("", image_path=path, type=type_model, model_name=model_name)
        
    except Exception as e:
        #print(f"Error: {e}")
        error_message = f"Error applying Mistral: {e}"
        return error_message, False
    
    return text, True

@log_function_call
async def apply_document(payload: dict, path: str, tmpdir: str) -> tuple[str, bool]:
    
    try:
        prompt=""
        if payload['type'] == 'brazil_document':    
            prompt = prompt_brazil_document
            model_name = model_document
        
        mistral = MistralAgent(agent_name='mistral_agent', system_prompt=prompt,)    
        text = await mistral.run_concurrent("", image_path=path, type=MistralAgentRunType.DOCUMENT_UNDERSTANDING, model_name=model_name)
    except Exception as e:
        #print(f"Error: {e}")
        error_message = f"Error applying Mistral: {e}"
        return error_message, False
    
    return text, True

@log_function_call
async def apply_aws_ocr(payload: dict, path: str, tmpdir: str) -> tuple[str, bool]:
    
    try:
        parsed = urlparse(payload['source']["url"])
        key_filename = None
        bucket_name = None
        path = payload['source']["url"]
        key_filename = "/".join(path.split("/")[3:])
        
        if parsed.scheme == "s3":    
            bucket_name = parsed.netloc
        else:
            bucket_name = parsed.netloc.split(".")[0]
        
        inicio = time.time()    
        detection = smart_detect(path, s3_bucket=bucket_name, s3_key=key_filename)
        fim = time.time()
        print(f"File extraction Processing {(fim - inicio)}")
        text="\n".join(detection)   
        
    except Exception as e:
        #print(f"Error: {e}")
        error_message = f"Error applying Aws Document Extraction: {e}"
        return error_message, False
    
    return text, True

@log_function_call
async def _docling_wrapper(payload, path, tmpdir):
    return await apply_docling(path, tmpdir)

@log_function_call
async def _mistral_wrapper(payload, path, tmpdir):
    tipo = payload.get("type", "")
    if tipo == 'default' or tipo == "":
        return await apply_mistral(payload, path, tmpdir)
    else:
        return await apply_document(payload, path, tmpdir)
            
@log_function_call
async def _aws_doc_extract_wrapper(payload, path, tmpdir):
    return await apply_aws_ocr(payload, path, tmpdir)

_DOWNLOAD_FUNCS = {
    's3':     download_file_s3,
    'http':   download_file,
    'base64': decode_base64,
}

_MODEL_FUNCS = {
    'awsDocumentExtractOcr': _aws_doc_extract_wrapper,
    'docling': _docling_wrapper,
    'mistral': _mistral_wrapper,
}

@log_function_call
async def extract_info(payload: dict) -> Tuple[str, bool]:
    
    src = payload.get("source", {})
    if src.get("type") == "base64" and not src.get("data"):
        
        raise ExtractionError(
            "Dados em base64 são obrigatórios para o tipo de fonte base64.",
            code=6,
            system_code="BASE64_DATA_REQUIRED",
            status_code=400,
            about_link=None,
            details=None
        )

    src_ext = src.get("extension", "").lower()
    if src_ext not in SUPPORTED_EXT:
        raise ExtractionError(
            (
                f"Tipo de arquivo {src_ext} não suportado. "
                f"Tipos suportados: {', '.join(sorted(SUPPORTED_EXT))}"
            ),
            code=6,
            system_code="UNSUPPORTED_FILE_TYPE",
            status_code=400
        )

    options = payload.get("options", {})
    model = options.get("model")
    if model not in SUPPORTED_MODELS:
        raise ExtractionError(
            "Tipo de modelo inválido. Tipos suportados: docling, mistral.",
            code=6,
            system_code="INVALID_OPTIONS_MODEL",
            status_code=400
        )

    if model == "mistral":
        opts = options.get("modelOptions") or {}
        if not opts:
            raise ExtractionError(
                "Opções do modelo são obrigatórias para o modelo Mistral.",
                code=6,
                system_code="MISTRAL_OPTIONS_REQUIRED",
                status_code=400
            )
        if opts.get("type_model") == "DOCUMENT_UNDERSTANDING" and not opts.get("prompt", "").strip():
            raise ExtractionError(
                (
                    "Prompt é obrigatório para o modelo Mistral "
                    "com tipo de modelo DOCUMENT_UNDERSTANDING."
                ),
                code=6,
                system_code="MISTRAL_PROMPT_REQUIRED",
                status_code=400
            )
    
    path, tmpdir = "", ""
    
    if model != "awsDocumentExtractOcr":
        download_fn = _DOWNLOAD_FUNCS.get(src.get('type'))
    
        if download_fn is None:
            raise ValueError(f"Fonte inválida: {src.get('type')!r}")
        
        path, tmpdir = await download_fn(src)    
        
    model_fn = _MODEL_FUNCS.get(model)

    if model_fn is None:
        raise ValueError(f"Modelo inválido: {model!r}")
    
    try:
        response_model, success = await model_fn(payload, path, tmpdir)
        
    except Exception as internal_exc:
        raise ExtractionError(
            f"Falha na extração de informações: {str(internal_exc)}",
            code=6,
            system_code="EXTRACTION_INTERNAL_ERROR",
            status_code=500
        )

    if not success:
        raise ExtractionError(
            "Falha na extração de informações.",
            code=6,
            system_code="EXTRACTION_PROCESSING_ERROR",
            status_code=500
        )

    return response_model, success
