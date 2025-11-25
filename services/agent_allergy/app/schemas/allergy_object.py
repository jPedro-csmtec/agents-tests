from pydantic import BaseModel, Field

    
class RequestAllergy(BaseModel):
    text_allergy: str = Field(..., description="Texto contém informações")
    model: str = Field(..., description="Model usado para analise")
    
class Medicines(BaseModel):
    active_ingredients: str = Field(
        ...,
        description="Princípios ativos separados por vírgula; use string vazia se nenhum."
    )
    reason_return: str = Field(
        ...,
        description="Explicação baseada apenas nos dados fornecidos."
    )

class Alerts(BaseModel):
    causes: str = Field(
        ...,
        description="Possíveis causas não medicamentosas separadas por vírgula; use string vazia se nenhuma."
    )
    reason_return: str = Field(
        ...,
        description="Explicação baseada apenas nos dados fornecidos."
    )

class Allergies(BaseModel):
    medicines: Medicines
    alerts: Alerts
    
class AllergyReport(BaseModel):
    allergies: Allergies
        
class ExtractData(BaseModel):
    allergies: Allergies