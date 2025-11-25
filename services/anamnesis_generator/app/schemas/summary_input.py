from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict

from services.anamnesis_generator.app.schemas.anamnesis_object import Anamnesis
from services.anamnesis_generator.app.schemas.atd_session_bioimpedance import AtdSessionBioimpedance
from services.anamnesis_generator.app.schemas.attendance_history import AttendanceHistory
from services.anamnesis_generator.app.schemas.file_object import FileAnamnesis
from services.anamnesis_generator.app.schemas.patient_object import Patient


class SummaryInputData(BaseModel):
    patient_entity: Patient = Field(..., alias="PatientEntity")
    historico_atendimento_entity: Optional[List[AttendanceHistory]] = Field(
        None, alias="HistoricoAtendimentoEntity"
    )
    anamnesis_entity: Anamnesis = Field(..., alias="AnamnesisEntity")
    bioimpedance_entity: Optional[AtdSessionBioimpedance] = Field(
        None, alias="BioimpedanceEntity"
    )
    interview: Optional[str] = Field(..., alias="Interview")
    files: Optional[List[FileAnamnesis]] = Field(..., alias="Files")

    model_config = ConfigDict(populate_by_name=True)
