from datetime import datetime
from typing import Optional, Any
from uuid import UUID

from pydantic import BaseModel, Field
from pydantic import ConfigDict


class AtdSessionBioimpedance(BaseModel):
    id: UUID = Field(..., alias="Id")
    device: UUID = Field(..., alias="Device")
    session: UUID = Field(..., alias="Session")

    percent_body_fat: Optional[float] = Field(None, alias="PercentBodyFat")
    fat_mass_kg: Optional[float] = Field(None, alias="FatMassKg")
    resting_energy_expenditure_kcal: Optional[float] = Field(None, alias="RestingEnergyExpenditureKcal")
    body_water_percent: Optional[float] = Field(None, alias="BodyWaterPercent")
    eval_body_water_rate: Optional[float] = Field(None, alias="EvalBodyWaterRate")
    skeletal_muscle_percent: Optional[float] = Field(None, alias="SkeletalMusclePercent")
    eval_skeletal_muscle: Optional[float] = Field(None, alias="EvalSkeletalMuscle")
    visceral_fat_index: Optional[float] = Field(None, alias="VisceralFatIndex")
    eval_visceral_fat: Optional[float] = Field(None, alias="EvalVisceralFat")
    bone_mineral_content_kg: Optional[float] = Field(None, alias="BoneMineralContentKg")
    eval_bone_mineral: Optional[float] = Field(None, alias="EvalBoneMineral")
    extracellular_fluid_kg: Optional[float] = Field(None, alias="ExtracellularFluidKg")
    intracellular_fluid_kg: Optional[float] = Field(None, alias="IntracellularFluidKg")
    total_body_water_kg: Optional[float] = Field(None, alias="TotalBodyWaterKg")
    protein_mass_kg: Optional[float] = Field(None, alias="ProteinMassKg")
    inorganic_salt_kg: Optional[float] = Field(None, alias="InorganicSaltKg")
    body_age_years: Optional[float] = Field(None, alias="BodyAgeYears")
    overall_rating: Optional[float] = Field(None, alias="OverallRating")

    error: Optional[Any] = Field(None, alias="Error")
    collected: datetime = Field(..., alias="Collected")
    updated: Optional[datetime] = Field(None, alias="Updated")
    created: datetime = Field(default_factory=datetime.now(), alias="Created")

    # permite popular tanto por alias (C#/JSON) quanto por nome python
    model_config = ConfigDict(populate_by_name=True)
