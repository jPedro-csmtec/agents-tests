from fastapi import APIRouter, Form
from libs.errors.exceptions import APIError, ErrorCode
from libs.errors.models import StandardResponse
from services.agent_treatment.app.schemas.treatment_object import RequestTreatment, TreatmentData
from services.agent_treatment.services.treatment import treatment_call

router = APIRouter(
    prefix="/treatment-info",
    tags=["treatment-info (v1)"]
)

@router.post("/treatment", 
    response_model=StandardResponse[TreatmentData], 
    summary="Propor estratégia terapêutica", 
    description=("Processa informações de laudos e resultados laboratoriais, sintetiza recomendações "
                 "existentes e cria uma estratégia terapêutica embasada em literatura e guias oficiais."),
    response_model_exclude_none=True,
    operation_id="propose_therapeutic_strategy" 
)


async def propose_therapeutic_strategy(body: RequestTreatment) -> StandardResponse[TreatmentData]:
    
    """
    Função para criar um tratamento para o paciente baseado nas informações fornecidas.
    Args:
        text_treatment (str): Texto contendo as informações sobre sintomas, queixas e histórico do paciente. 
    """
    
    response, success = await treatment_call(body.text_treatment)

    if not success:
        raise APIError(
            code        = ErrorCode.CALL_ERROR,
            code_alias  = "EXTRACTION_FAILED",
            system_code = "AGENT_EXTRACTION",
            description = response
        )

    return StandardResponse(
        success = True,
        data    = TreatmentData(result=response)
    )
