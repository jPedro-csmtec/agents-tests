from __future__ import annotations
from collections import defaultdict
from pathlib import Path
from typing import List, Tuple
import time
from aiohttp import ClientError
import boto3, botocore
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential_jitter

from configurations.config import Config


aws_access_key = Config.AWS_ACCESS_KEY_ID
aws_secret_key = Config.AWS_SECRET_ACCESS_KEY
region = Config.AWS_REGION
bucket = Config.AWS_BUCKET_NAME

TOLERANCIA_Y = 0.005

TEXTRACT = boto3.client(
            'textract',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region
        )

CLIENT = boto3.client("s3", aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=region)

def copy_object_from_s3(source_bucket: str, source_key: str, dest_bucket: str):
    
    params = {
        "Bucket": dest_bucket,
        "Key": source_key,
        "CopySource": {"Bucket": source_bucket, "Key": source_key},
    }
    
    try:
        resp = CLIENT.copy_object(**params)
        #print("Copiado:", source_bucket, "/", source_key, "→", dest_bucket, "/", f"{dest_bucket}/{source_key}")
        print("Passou na função")
        return resp
    except Exception as e:
        raise RuntimeError(f"CopyObject falhou: {e}")
    except ClientError as e:
        raise RuntimeError(f"CopyObject falhou: {e}")

def _is_throttle(err):
    return isinstance(err, botocore.exceptions.ClientError) and \
           err.response["Error"]["Code"] in (
               "ProvisionedThroughputExceededException",
               "ThrottlingException", "LimitExceededException"
           )

def retry_on_throttle():                 
    return retry(
        retry_error_callback=lambda retry_state: retry_state.outcome.result(),
        retry=retry_if_exception(_is_throttle),
        stop=stop_after_attempt(6),      
        wait=wait_exponential_jitter(max=60),
        reraise=True,
    )

@retry_on_throttle()
def _detect_sync(path: Path) -> List[str]:
    with path.open("rb") as f:
        bytes_content = f.read()
        
    resp = TEXTRACT.detect_document_text(Document={"Bytes": bytes_content})
    
    linhas: List[Tuple[float, float, str]] = []
    for block in resp["Blocks"]:
        if block["BlockType"] == "LINE":
            bb = block["Geometry"]["BoundingBox"]
            linhas.append((bb["Top"], bb["Left"], block["Text"].strip()))

    grupos: dict[int, List[Tuple[float, str]]] = defaultdict(list)
    for top, left, texto in linhas:
        faixa_y = round(top / TOLERANCIA_Y)
        grupos[faixa_y].append((left, texto))

    linhas_ordenadas: List[str] = []
    for faixa in sorted(grupos.keys()):
        colunas = sorted(grupos[faixa], key=lambda x: x[0])
        linhas_ordenadas.append(" ".join(txt for _, txt in colunas))

    return linhas_ordenadas

def wait_text_job(job_id: str, poll=2, timeout=900) -> None:
    t0 = time.time()
    while True:
        meta = TEXTRACT.get_document_text_detection(JobId=job_id)
        status = meta["JobStatus"]
        if status == "SUCCEEDED":
            return
        if status in {"FAILED", "PARTIAL_SUCCESS"}:
            raise RuntimeError(f"OCR falhou: {status}")
        if time.time() - t0 > timeout:
            raise TimeoutError("Job Textract excedeu tempo limite.")
        time.sleep(poll)

@retry_on_throttle()
def detect_lines_s3(bucket: str, key: str) -> List[str]:
    job_id = TEXTRACT.start_document_text_detection(
        DocumentLocation={"S3Object": {"Bucket": bucket, "Name": key}}
    )["JobId"]

    wait_text_job(job_id)

    items: List[Tuple[int, float, float, str]] = []
    token = None
    while True:
        page = TEXTRACT.get_document_text_detection(JobId=job_id, NextToken=token) \
               if token else \
               TEXTRACT.get_document_text_detection(JobId=job_id)

        for b in page["Blocks"]:
            if b["BlockType"] == "LINE":
                bb = b["Geometry"]["BoundingBox"]
                items.append((
                    b["Page"],
                    bb["Top"],
                    bb["Left"],
                    b["Text"].strip()
                ))
        token = page.get("NextToken")
        if not token:
            break

    grupos = defaultdict(list)
    for page, top, left, texto in items:
        faixa_y = round(top / TOLERANCIA_Y)
        grupos[(page, faixa_y)].append((left, texto))
        
    linhas_ordenadas: List[str] = []
    for (page, faixa_y) in sorted(grupos.keys()):
        colunas = sorted(grupos[(page, faixa_y)], key=lambda x: x[0])
        linhas_ordenadas.append(" ".join(txt for _, txt in colunas))
    
    return linhas_ordenadas

def smart_detect(path: str | Path, *, s3_bucket: str = None, s3_key: str = None) -> List[str]:
    
    if "s3" not in path:
        path = Path(path)
        size_mb = path.stat().st_size / 1_048_576
        ext = path.suffix.lower()

        if ext in {".jpg", ".jpeg", ".png"} and size_mb <= 10:
            return _detect_sync(path)

    if not s3_bucket:
        s3_bucket = bucket
    if s3_bucket != bucket:
        copy_object_from_s3(s3_bucket, s3_key, bucket)
        s3_bucket = bucket
    if not s3_key:
        s3_key = f"uploads/{path.name}"
        CLIENT.upload_file(str(path), s3_bucket, s3_key)
        
    return detect_lines_s3(s3_bucket, s3_key)
