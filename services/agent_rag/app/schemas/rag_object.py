from typing import Any, List, Literal, Optional
from pydantic import BaseModel, Field

class IDDescription(BaseModel):
    id: str = Field(..., description="Identificador para filtro RAG")
    group_id: str = Field(..., alias="groupId", description="Identificador do grupo")
    descricao: str = Field(..., alias="description", description="Descrição do grupo")

    class Config:
        populate_by_name = True

class Part(BaseModel):
    type: Literal["text", "file"] = Field(..., description="Tipo de parte: texto ou arquivo")
    text: Optional[str] = None
    mime: Optional[str] = None
    data: Optional[str] = None

class Content(BaseModel):
    role: str = Field(..., example="user", description="Quem enviou: 'user' ou 'model'")
    parts: List[Part] = Field(..., description="Lista de partes que compõem a mensagem")
    
class SafetySettingModel(BaseModel):
    harmCategory: str
    threshold: str
    method: Optional[str] = None

class GenerationConfigModel(BaseModel):
    maxTokens: Optional[int]
    temperature: Optional[float]

class PostRequest(BaseModel):
    id_descriptions: List[IDDescription]
    content: Content
    safety: Optional[List[SafetySettingModel]] = None
    config: Optional[GenerationConfigModel] = None

class PostQuery(BaseModel):
    id_descriptions: List[IDDescription]
    message: str
    
class PostResponse(BaseModel):
    result: str
    
class Query(BaseModel):
    result: str