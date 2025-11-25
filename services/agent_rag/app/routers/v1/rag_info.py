from fastapi import APIRouter, Form
from libs.errors.exceptions import APIError, ErrorCode
from libs.errors.models import StandardResponse
from services.agent_rag.app.schemas.rag_object import PostQuery, PostResponse, Query
from services.agent_rag.services.rag_service import rag_info, rag_query

router = APIRouter(
    prefix="/rag-info",
    tags=["rag-info (v1)"]
)

@router.post(
    "/rag",
    response_model=StandardResponse[PostResponse], 
    summary="Recuperar laudo", 
    description=("Encontra o informações relevantes na base, para a"
                 "pergunta enviada enriquecendo o contexto para resposta."),
    response_model_exclude_none=True,
    operation_id="retrieve_relevant_rag" 
    
)

async def retrieve_relevant_rag(payload: PostQuery) -> StandardResponse[PostResponse]:
    
    result, success = await rag_info(payload)

    if not success:
        raise APIError(
            code        = ErrorCode.DATABASE_QUERY_ERROR,
            code_alias  = "EXTRACTION_FAILED",
            system_code = "AGENT_EXTRACTION",
            description = result
        )

    return StandardResponse(
        success = True,
        data    = PostResponse(result=result)
    )


@router.post(
    "/rag-query", 
    response_model=StandardResponse[PostResponse], 
    summary="Geração de query vetorial a partir de contexto", 
    description=("Recebe um bloco de texto (CONTEXTO) contendo documentos ou trechos de informação e retorna, "
                 "em formato de pergunta, a query ideal para busca em um banco vetorial."),
    response_model_exclude_none=True,
    operation_id="rag_analysis" 
    
)

async def rag_analysis(payload: Query) -> StandardResponse[PostResponse]:
    
    result, success = await rag_query(payload.result)

    if not success:
        raise APIError(
            code        = ErrorCode.DATABASE_QUERY_ERROR,
            code_alias  = "EXTRACTION_FAILED",
            system_code = "AGENT_EXTRACTION",
            description = result
        )

    return StandardResponse(
        success = True,
        data    = PostResponse(result=result)
    )