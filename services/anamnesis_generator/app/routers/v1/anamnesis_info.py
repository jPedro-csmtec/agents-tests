from fastapi import APIRouter, Form
from libs.errors.exceptions import APIError, ErrorCode
from libs.errors.models import StandardResponse
from services.agent_extraction.app.schemas.extract_object import ExtractData
from services.anamnesis_generator.app.schemas.file_object import ExtractionFileInfo
from services.anamnesis_generator.app.schemas.summary_input import SummaryInputData
from services.anamnesis_generator.app.schemas.summary_report import ExtractDataSummary, SummaryReport
from services.anamnesis_generator.service.anamnesis import anamnesis_data, anamnesis_extraction


router = APIRouter(
    prefix="/anamnesis-info",
    tags=["anamnesis-info (v1)"]
)

@router.post("/anamnesis-strunction-data", 
    response_model=StandardResponse[ExtractDataSummary], 
    summary="Recebe conjunto de informações e formata para construção da anamnese", 
    description=("Analisar a partir do texto o principil ativco da alergia identificada."),
    response_model_exclude_none=True,
    operation_id="strunction_anamnesis_data" 
)

async def strunction_anamnesis_data(body: SummaryInputData) -> StandardResponse[ExtractDataSummary]:
    
    result, success = await anamnesis_data(body)

    if not success:
        raise APIError(
            code        = ErrorCode.CALL_ERROR,
            code_alias  = "EXTRACTION_FAILED",
            system_code = "AGENT_STRUNCTION",
            description = result
        )
        
    summary_report = SummaryReport(**result)

    return StandardResponse(
        success = True,
        data    = ExtractDataSummary(summaryReport=summary_report) 
    )


@router.post("/anamnesis-extraction-file", 
    response_model=StandardResponse[ExtractData], 
    summary="Recebe um arquivo de imagem ou documento e faz a extração das informações em formato de texto.", 
    description=("Analisar um arquivo de imagem ou documento e extrair dados em formato de texto."),
    response_model_exclude_none=True,
    operation_id="anamnesis_extraction_file" 
)

async def anamnesis_extraction_file(body: ExtractionFileInfo) -> StandardResponse[ExtractData]:
    
    result, success = await anamnesis_extraction(body)

    if not success:
        raise APIError(
            code        = ErrorCode.CALL_ERROR,
            code_alias  = "EXTRACTION_FAILED",
            system_code = "AGENT_EXTRACTION",
            description = result
        )

    return StandardResponse(
        success = True,
        data    = ExtractData(result=result)
    )