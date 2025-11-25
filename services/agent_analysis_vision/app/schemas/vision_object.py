from pydantic import BaseModel, Field

class ModelVisionData(BaseModel):
    result: str = Field("", description="Retorno da analise")
    explanation: str = Field("", description="Explicação do resultado")
    
class RequestVision(BaseModel):
    url : str = Field(..., description="Url para analise da imagem")
    text_vision: str = Field(..., description="Texto contém informação do sintomas diversos")