from typing import Optional
from pydantic import BaseModel, Field

class SummaryData(BaseModel):
    result: str
    
class RequestSummary(BaseModel):
    text_summary: str = Field(..., description="Texto contém informação necessária para criação do resumo")
    agent_resume: Optional[bool] = Field(True, description="Seleção do agente utilizado")