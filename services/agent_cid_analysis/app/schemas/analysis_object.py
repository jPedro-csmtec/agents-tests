from pydantic import BaseModel, Field
class ExtractData(BaseModel):
    result: str
    cid: str
class RequestAnalysis(BaseModel):
    text_analysis: str = Field(..., description="Texto contém informação do sintomas diversos")
    
class OutputCid(BaseModel):
    cid: str
    result: str
    
class ExtractDataCid(BaseModel):
    result: OutputCid