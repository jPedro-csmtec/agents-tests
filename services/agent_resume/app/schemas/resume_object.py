from pydantic import BaseModel, Field

class ResumeData(BaseModel):
    result: str
    
class RequestResume(BaseModel):
    text_resume: str = Field(..., description="Texto contém informação do sintomas diversos")