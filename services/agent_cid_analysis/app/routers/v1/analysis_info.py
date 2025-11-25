from fastapi import APIRouter
from libs.errors.exceptions import APIError, ErrorCode
from libs.errors.models import StandardResponse
from services.agent_cid_analysis.app.schemas.analysis_object import ExtractData, RequestAnalysis
from services.agent_cid_analysis.services.analysis import analysis_info

router = APIRouter(
    prefix="/analysis-info",
    tags=["analysis-info (v1)"]
)

@router.post("/analysis", 
    response_model=StandardResponse[ExtractData], 
    summary="Analisar CID-10", 
    description=("Identifica todos os termos, sinais, sintomas e condições no texto que correspondam a "
     "códigos CID-10, listando possibilidades em caso de ambiguidade e retornando para cada "
     "código a estrutura clínica detalhada conforme especificado."),
    response_model_exclude_none=True,
    operation_id="analyze_cid10_codes" 
)


async def analyze_cid10_codes(body: RequestAnalysis) -> StandardResponse[ExtractData]:
    
    response, success = await analysis_info(body.text_analysis)

    if not success:
        raise APIError(
            code        = ErrorCode.CALL_ERROR,
            code_alias  = "EXTRACTION_FAILED",
            system_code = "AGENT_EXTRACTION",
            description = response
        )

    return StandardResponse(
        success = True,
        data    = ExtractData(cid=response.cid, result=response.result)
    )
