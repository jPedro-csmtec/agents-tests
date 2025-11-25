from fastapi import APIRouter, Form
from libs.errors.exceptions import APIError, ErrorCode
from libs.errors.models import StandardResponse
from services.agent_allergy.app.schemas.allergy_object import AllergyReport, RequestAllergy
from services.agent_allergy.services.allergy import allergy_info


router = APIRouter(
    prefix="/allergy-info",
    tags=["allergy-info (v1)"]
)

@router.post("/allergy", 
    response_model=StandardResponse[AllergyReport], 
    summary="Analise de Alergias", 
    description=("Analisar a partir do texto o principil ativco da alergia identificada."),
    response_model_exclude_none=True,
    operation_id="analyze_allergy" 
)


async def analyze_allergy(body: RequestAllergy) -> StandardResponse[AllergyReport]:
    
    response, success = await allergy_info(body.model_dump())

    if not success:
        raise APIError(
            code        = ErrorCode.CALL_ERROR,
            code_alias  = "EXTRACTION_FAILED",
            system_code = "AGENT_EXTRACTION",
            description = response
        )

    return StandardResponse(
        success = True,
        data    = AllergyReport(allergies=response.allergies)
    )
