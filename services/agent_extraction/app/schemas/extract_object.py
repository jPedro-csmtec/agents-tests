from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class ExtractData(BaseModel):
    result: str
    
class Source(BaseModel):
    type: str = Field("s3 ou http ou base64", description="Tipo de fonte")
    url: str = Field(..., description="Url de acesso aos dados")
    data: Optional[str] = Field(None, description="Dados em base64")
    name: str = Field(..., description="Nome do arquivo ou objeto")
    extension: str = Field(..., description="Extensão do arquivo ou objeto")
    
class ModelOptions(BaseModel):
    type_model: str = Field("OCR ou DOCUMENT_UNDERSTANDING", description="Tipo de analise")
    prompt: Optional[str] = Field("Apenas para a opção DOCUMENT_UNDERSTANDING", description="Prompt para o modelo")
    model_name: Optional[str] = Field("mistral-ocr-2505", description="Modelo de resposta do modelo")

class Options(BaseModel):
    model: str = Field("model", description="Model selecionado para extração da informação")
    modelOptions: Optional[ModelOptions] = Field(None, description="Opções adicionais para a extração")

class Output(BaseModel):
    type_format: Literal["json", "csv", "text"] = Field("json", description="Formato de saída dos dados extraídos")

class ExtractObject(BaseModel):
    id: str = Field(..., description="Identificador único do objeto extraído")
    source: Source = Field(..., description="Fonte dos dados")
    options: Options = Field(..., description="Opções para a extração")
    #output: Output = Field(..., description="Formato de saída dos dados extraídos")

class ErrorResponse(BaseModel):
    code: str = Field(..., description="Código de erro")
    description: str = Field(..., description="Descrição do erro")

class ExtractResponse(BaseModel):
    id : str = Field(..., description="Identificador único do objeto extraído")
    result: str = Field(..., description="Resultado da extração")
    success: bool = Field(..., description="Indica se a extração foi bem sucedida")
    error: Optional[ErrorResponse] = Field(None, description="Detalhes do erro caso a extração não tenha sido bem sucedida")