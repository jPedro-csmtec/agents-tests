from typing import Generic, Optional, TypeVar
from pydantic import BaseModel
from gateway.app.schemas.errors import ResultErrorSchema

T = TypeVar("T")

class StandardResponse(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    error: Optional[ResultErrorSchema] = None
    
    class Config:
        json_encoders = {}
        ignored_types = (BaseModel,)
        from_attributes = True
