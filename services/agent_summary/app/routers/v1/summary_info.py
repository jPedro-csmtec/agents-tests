from fastapi import APIRouter, Form
from libs.errors.exceptions import APIError, ErrorCode
from libs.errors.models import StandardResponse
from services.agent_summary.app.schemas.summary_object import RequestSummary, SummaryData
from services.agent_summary.services.summary import summary_call


router = APIRouter(
    prefix="/summary-info",
    tags=["summary-info (v1)"]
)

@router.post("/summary", 
    response_model=StandardResponse[SummaryData], 
    summary="Gerar resumo clínico", 
    description=("Processa relatórios e laudos médicos, destacando pontos principais (exames, tratamentos, "
                 "recomendações), e retorna um sumário conciso e bem estruturado, seguindo o modelo "
                 "especificado para anamnese."),
    response_model_exclude_none=True,
    operation_id="generate_clinical_summary" 
)


async def generate_clinical_summary(body: RequestSummary) -> StandardResponse[SummaryData]:
    
    """
    Função para criar um tratamento para o paciente baseado nas informações fornecidas.
    Args:
        text_summary (str): Texto contendo as informações sobre sintomas, queixas e histórico do paciente.
        agent_resume (Optional[bool]): Seleção opcional do agente a ser utilizado.
    """
    
    response, success = await summary_call(body)

    if not success:
        raise APIError(
            code        = ErrorCode.CALL_ERROR,
            code_alias  = "EXTRACTION_FAILED",
            system_code = "AGENT_EXTRACTION",
            description = response
        )

    return StandardResponse(
        success = True,
        data    = SummaryData(result=response)
    )
