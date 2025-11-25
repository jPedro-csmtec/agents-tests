

from typing import List
from pydantic import BaseModel, Field

class SummaryReport(BaseModel):
    cid: str = Field(..., description="Código do CID-10")
    cidDescription: str = Field(..., description="Descrição do código")
    activeIngredients: str = Field(..., description="Lista de principios ativos de medicamentos")
    causes: str = Field(..., description="Lista de principais causas da alergia")
    xmlResponse: str = Field(
        ...,
        description="Estrutura os dados recebidos em xml"
    )
    dataRawResponse: str = Field(
        ...,
        description="Estrutura de dados recebidos em texto."
    )
    resultSummary: str = Field(..., description="Estrutura final doi ssumario criado.")
    
    
class ExtractDataSummary(BaseModel):
    summaryReport: SummaryReport