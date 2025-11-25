from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Patient(BaseModel):
    cpf: Optional[str] = None
    patient_name: Optional[str] = None
    mother_name: Optional[str] = None
    birth_date: Optional[datetime] = None
    birth_date_rd_conversas: Optional[str] = None
    home_phone: Optional[str] = None
    ddd_home_phone: Optional[str] = None
    genre: Optional[str] = None
    address: Optional[str] = None
    number: Optional[str] = None
    complement: Optional[str] = None
    neighborhood: Optional[str] = None
    neighborhood_type: int = 0
    state_address: Optional[str] = None
    zip_code: Optional[str] = None
    city: Optional[str] = None
    name_breed_color: Optional[str] = None
    nationalities: Optional[str] = None
    identity: Optional[str] = None
    identity_issuing_company: Optional[str] = None
    identity_uf: Optional[str] = None
    identity_issuance_date: Optional[datetime] = None
