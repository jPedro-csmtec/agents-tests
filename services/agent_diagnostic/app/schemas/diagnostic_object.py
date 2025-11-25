from typing import Optional
from pydantic import BaseModel, Field

class ExtractData(BaseModel):
    result: str
    
class RequestDiagnostic(BaseModel):
    text_diagnostic: str = Field(None, description="Texto contém informação do sintomas diversos")
    model: Optional[str] = Field(None, description="Modelos: gpt-4o-2024-08-06 ou o3-2025-04-16") 