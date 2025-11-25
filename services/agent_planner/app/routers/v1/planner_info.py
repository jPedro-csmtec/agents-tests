from fastapi import APIRouter, Form
from libs.errors.exceptions import APIError, ErrorCode
from libs.errors.models import StandardResponse
from services.agent_planner.app.schemas.planner_object import IntervationPlannerData, RequestIntervationPlanner
from services.agent_planner.services.intervation_planner import planner_call

router = APIRouter(
    prefix="/planner-info",
    tags=["planner-info (v1)"]
)

@router.post("/planners", 
    response_model=StandardResponse[IntervationPlannerData], 
    summary="Criar plano de cuidado", 
    description=("Analisa laudo ou diagnóstico e retorna objetivo, "
                 "metodologia, resultados e um plano detalhado de próximos "
                 "passos, exames e encaminhamentos para o paciente."),
    response_model_exclude_none=True,
    operation_id="create_care_plan" 
)


async def create_care_plan(body: RequestIntervationPlanner) -> StandardResponse[IntervationPlannerData]:
    
    """
    Função para criar um planejamento de intervenção para o paciente baseado nas informações fornecidas.
    Args:
        text_info (str): Texto contendo as informações sobre sintomas, queixas e histórico do paciente.
    """
    
    response, success = await planner_call(body.text_info)

    if not success:
        raise APIError(
            code        = ErrorCode.CALL_ERROR,
            code_alias  = "EXTRACTION_FAILED",
            system_code = "AGENT_EXTRACTION",
            description = response
        )

    return StandardResponse(
        success = True,
        data    = IntervationPlannerData(result=response)
    )
