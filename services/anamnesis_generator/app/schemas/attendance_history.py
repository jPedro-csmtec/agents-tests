from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from pydantic import ConfigDict


class AttendanceHistory(BaseModel):
    patient_name: Optional[str] = Field(None, alias="NOMEPACIENTE")
    medical_record: Optional[str] = Field(None, alias="PRONTUARIO")
    attendance_entry_date: Optional[datetime] = Field(None, alias="DATAENTRADA")
    attendance_exit_date: Optional[datetime] = Field(None, alias="DATASAIDA")
    attendance_entry_hour: Optional[str] = Field(None, alias="HORAENTRADA")
    attendance_exit_hours: Optional[str] = Field(None, alias="HORASAIDA")
    practitioner_name: Optional[str] = Field(None, alias="NOMEMEDICO")
    practitioner_specialty: Optional[str] = Field(None, alias="ESPECIALIDADE")
    status: Optional[str] = Field(None, alias="STATUS")

    model_config = ConfigDict(populate_by_name=True)
