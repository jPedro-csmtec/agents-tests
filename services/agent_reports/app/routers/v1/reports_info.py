from fastapi import APIRouter, Form
from libs.errors.exceptions import APIError, ErrorCode
from libs.errors.models import StandardResponse
from services.agent_reports.app.schemas.reports_object import ReporttData, RequestReport
from services.agent_reports.services.reports import reports_info

router = APIRouter(
    prefix="/reports-info",
    tags=["reports-info (v1)"]
)

@router.post(
    "/reports",
    response_model=StandardResponse[ReporttData], 
    summary="Recuperar laudo", 
    description=("Encontra o laudo mais relevante conforme o texto de "
                 "entrada e devolve somente os valores extraídos e o "
                 "conteúdo do laudo."),
    response_model_exclude_none=True,
    operation_id="retrieve_relevant_report" 
    
)

async def retrieve_relevant_report(payload: RequestReport) -> StandardResponse[ReporttData]:
    
    result, success = await reports_info(payload.text_report)
    
    if not success:
        raise APIError(
            code        = ErrorCode.CALL_ERROR,
            code_alias  = "EXTRACTION_FAILED",
            system_code = "AGENT_EXTRACTION",
            description = result
        )

    return StandardResponse(
        success = True,
        data    = ReporttData(result=result)
    )
