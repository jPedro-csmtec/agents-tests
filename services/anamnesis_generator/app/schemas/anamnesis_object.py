from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class VitalSigns(BaseModel):
    cardio_frequency: Optional[float] = Field(None, alias="cardioFrequency")
    respiratory_frequency: Optional[float] = Field(None, alias="respiratoryFrequency")
    transesophageal_temp: Optional[float] = Field(None, alias="transesophagealTemp")
    body_temperature: Optional[float] = Field(None, alias="bodyTemperature")
    weight: Optional[float] = Field(None, alias="weight")
    height: Optional[float] = Field(None, alias="height")
    pas: Optional[float] = Field(None, alias="pas")
    pad: Optional[float] = Field(None, alias="pad")
    pam: Optional[float] = Field(None, alias="pam")

    model_config = ConfigDict(populate_by_name=True)


class LastAnamnesis(BaseModel):
    vital_signs: Optional[VitalSigns] = Field(None, alias="vitalSigns")
    complaint: Optional[str] = Field(None, alias="complaint")
    saturation: Optional[float] = Field(None, alias="saturation")
    diagnostic_hypothesis: Optional[str] = Field(None, alias="diagnosticHypothesis")
    cid_version: Optional[int] = Field(None, alias="cidVersion")
    cid_code: Optional[str] = Field(None, alias="cidCode")
    cid_description: Optional[str] = Field(None, alias="cidDescription")
    sign_process_cod: Optional[int] = Field(None, alias="signProcessCod")
    status: Optional[str] = Field(None, alias="status")

    model_config = ConfigDict(populate_by_name=True)


class Anamnesis(BaseModel):
    care_unit_description: Optional[str] = Field(None, alias="careUnitDescription")
    professional_name: Optional[str] = Field(None, alias="professionalName")
    modified_date_time: datetime = Field(..., alias="modifiedDateTime")
    last_anamnesis: LastAnamnesis = Field(
        default_factory=LastAnamnesis,
        alias="lastAnamnesis",
    )
    sign_process_cod: Optional[int] = Field(None, alias="signProcessCod")
    historico_clinico_pep2: Optional[bool] = Field(None, alias="historicoClinicoPep2")
    has_record_restriction: Optional[bool] = Field(None, alias="hasRecordRestriction")
    status: Optional[str] = Field(None, alias="status")
    ia_anamnesis_entity: Optional[str] = Field(None, alias="ia_anamnesis_entity")

    model_config = ConfigDict(populate_by_name=True)
