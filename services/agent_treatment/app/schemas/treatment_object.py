from pydantic import BaseModel, Field

class TreatmentData(BaseModel):
    result: str
    
class RequestTreatment(BaseModel):
    text_treatment: str = Field(..., description="Texto contém informação do sintomas diversos")