from fastapi import APIRouter, Form
from libs.errors.exceptions import APIError, ErrorCode
from libs.errors.models import StandardResponse
from services.agent_analysis_vision.app.schemas.vision_object import ModelVisionData, RequestVision
from services.agent_analysis_vision.service.vision import vision_info

router = APIRouter(
    prefix="/vision-info",
    tags=["vision-info (v1)"]
)

@router.post("/vision", 
    response_model=StandardResponse[ModelVisionData], 
    summary="Vision", 
    description=("Identificar informações baseado nas imagens passadas."),
    response_model_exclude_none=True,
    operation_id="vision_analyze" 
)


async def vision_analyze(body: RequestVision) -> StandardResponse[ModelVisionData]:
    
    response, success = await vision_info(body.url, body.text_vision)

    if not success:
        raise APIError(
            code        = ErrorCode.CALL_ERROR,
            code_alias  = "EXTRACTION_FAILED",
            system_code = "AGENT_EXTRACTION",
            description = response
        )

    return StandardResponse(
        success = True,
        data    = ModelVisionData(result=response.result, explanation=response.explanation)
    )
