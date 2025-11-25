from typing import Any
from fastapi import APIRouter
from libs.errors.exceptions import APIError, ErrorCode
from libs.errors.models import StandardResponse
from services.agent_extraction.app.schemas.extract_document_object import BrazilDocument, ExtractDocument
from services.agent_extraction.app.schemas.extract_object import ExtractData, ExtractObject
from services.agent_extraction.services.extraction import extract_and_clean_json, extract_info

router = APIRouter(
    prefix="/extraction-info",
    tags=["extraction-info (v1)"]
)

@router.post("/extract-document-info",
    response_model=StandardResponse[Any],
    summary="Extrair informações de documentos", 
    description="Extrai e retorna de documentos via link, arquivo ou imagem",
    response_model_exclude_none=True,
    operation_id="extract_document_info"
)
async def extract_document_info(payload: ExtractDocument) -> StandardResponse[Any]:
    result, success = await extract_info(payload.model_dump())
    if not success:
        raise APIError(
            code        = ErrorCode.CALL_ERROR,
            code_alias  = "EXTRACTION_FAILED",
            system_code = "AGENT_EXTRACTION",
            description = result
        )
        
    
    if payload.type == 'brazil_document':
        data = extract_and_clean_json(result)
        result =  BrazilDocument(**data)
    else:
        result = ExtractData(result=result)
    
    return StandardResponse(
        success = True,
        data    = result
    )
    

@router.post(
    "/extract",
    response_model=StandardResponse[ExtractData],
    summary="Extrair informações", 
    description="Extrai e retorna texto/processado de link, arquivo ou imagem",
    response_model_exclude_none=True,
    operation_id="extract_content"
)
async def extract_content(payload: ExtractObject) -> StandardResponse[ExtractData]:
    result, success = await extract_info(payload.model_dump())

    if not success:
        raise APIError(
            code        = ErrorCode.CALL_ERROR,
            code_alias  = "EXTRACTION_FAILED",
            system_code = "AGENT_EXTRACTION",
            description = result
        )
        
    return StandardResponse(
        success = True,
        data    = ExtractData(result=result)
    )
