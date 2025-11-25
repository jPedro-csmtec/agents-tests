from pydantic import BaseModel, Field
from typing import Optional

from services.agent_extraction.app.schemas.extract_object import Options, Source

class ExtractDocument(BaseModel):
    id: str = Field(..., description="Identificador único do objeto extraído")
    type: Optional[str] = Field("default", description="Identificador único do objeto extraído")
    source: Source = Field(..., description="Fonte dos dados")
    options: Options = Field(..., description="Opções para a extração")

class Address(BaseModel):
    line: str = Field(..., description="Linha")
    number: str = Field(..., description="Numero")
    complement: str = Field(..., description="Complemento")
    neighborhood: str = Field(..., description="Bairro")
    state: str = Field(..., description="Estado")
    zipCode: str = Field(..., description="Codigo Zip")
    city: str = Field(..., description="Cidade")
    
class MobilePhone(BaseModel):
    phone: str = Field(..., description="Telefone")
    ddd: str = Field(..., description="DDD")
    type: str = Field(..., description="Tipo")

class BrazilDocument(BaseModel):
    name: str = Field(..., description="Nome")
    email: str = Field(..., description="Email")
    genre: str = Field(..., description="Genero")
    cpf: str = Field(..., description="CPF")
    rg: str = Field(..., description="RG")
    address: Address = Field(..., description="Endereço")
    mobilePhone: MobilePhone = Field(..., description="Telefone")
    motherName: str = Field(..., description="Nome da mãe")
    birthDate: str = Field(..., description="Data de nascimento")
