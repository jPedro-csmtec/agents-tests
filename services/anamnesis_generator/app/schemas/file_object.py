from typing import Optional
from pydantic import BaseModel


class FileAnamnesis(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    
class ExtractionFileInfo(BaseModel):
    id: str = None
    url: str = None
    name: str = None
    extension: str = None