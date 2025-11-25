from pydantic import BaseModel, Field

class IntervationPlannerData(BaseModel):
    result: str
    
class RequestIntervationPlanner(BaseModel):
    text_info: str = Field(..., description="Texto contém informação do sintomas diversos")