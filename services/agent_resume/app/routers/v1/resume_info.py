from fastapi import APIRouter
from libs.errors.exceptions import APIError, ErrorCode
from libs.errors.models import StandardResponse
from services.agent_resume.app.schemas.resume_object import RequestResume, ResumeData
from services.agent_resume.services.resume import resume_call 

router = APIRouter(
    prefix="/resume-info",
    tags=["resume-info (v1)"]
)

@router.post("/resumes", 
    response_model=StandardResponse[ResumeData], 
    summary="Resumir relatório", 
    description=("Lê relatórios, laudos ou diagnósticos médicos e extrai "
                 "objetivo, metodologia, principais resultados e conclusões "
                 "clínicas."),
    response_model_exclude_none=True,
    operation_id="summarize_medical_report" 
)


async def summarize_medical_report(body: RequestResume) -> StandardResponse[ResumeData]:
    
    """
    Função responsavel com o resumo das informações passadas.
    Args:
        text_resume (str): Texto contendo as informações sobre sintomas, queixas e histórico do paciente.
    """
    
    response, success = await resume_call(body.text_resume)

    if not success:
        raise APIError(
            code        = ErrorCode.CALL_ERROR,
            code_alias  = "EXTRACTION_FAILED",
            system_code = "AGENT_EXTRACTION",
            description = response
        )

    return StandardResponse(
        success = True,
        data    = ResumeData(result=response)
    )
