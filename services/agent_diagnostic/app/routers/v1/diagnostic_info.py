from fastapi import APIRouter, Form
from libs.errors.exceptions import APIError, ErrorCode
from libs.errors.models import StandardResponse 
from services.agent_diagnostic.app.schemas.diagnostic_object import RequestDiagnostic, ExtractData
from services.agent_diagnostic.services.diagnostic import diagnostic_info

router = APIRouter(
    prefix="/diagnostic-info",
    tags=["diagnostic-info (v1)"]
)

@router.post("/diagnostics", 
    response_model=StandardResponse[ExtractData], 
    summary="Realizar diagnóstico", 
    description=("Extrai dados clínicos (demográficos, sintomas, histórico e exames), classifica a provável "
     "enfermidade conforme critérios ADA/Ministério da Saúde, lista diferenciais e recomenda "
     "exames complementares."),
    response_model_exclude_none=True,
    operation_id="evaluate_patient_diagnostics" 
)


async def evaluate_patient_diagnostics(body: RequestDiagnostic) -> StandardResponse[ExtractData]:
    """
    Função para avaliar o diagnóstico do paciente com base nas informações fornecidas.
    Args:
        text_diagnostic (str): Texto contendo as informações sobre sintomas, queixas e histórico do paciente.
        model (Optional[str]): Entrada opcional de texto contendo a informação de qual modelo será utilizado entre gpt-4o-2024-08-06 ou o3-2025-04-16.
    """
    response, success = await diagnostic_info(body.model_dump())

    if not success:
        raise APIError(
            code        = ErrorCode.CALL_ERROR,
            code_alias  = "EXTRACTION_FAILED",
            system_code = "AGENT_EXTRACTION",
            description = response
        )

    return StandardResponse(
        success = True,
        data    = ExtractData(result=response)
    )
