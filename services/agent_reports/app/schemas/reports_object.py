from typing import Any, List, Optional
from pydantic import BaseModel, Field

class ReporttData(BaseModel):
    result: str

class RequestReport(BaseModel):
    text_report: str = Field(..., description="Texto contém informação do sintomas diversos")

class Message(BaseModel):
    content: str
    role: str
    tool_calls: Optional[Any] = None
    function_call: Optional[Any] = None

class Choice(BaseModel):
    finish_reason: str
    index: int
    message: Message

class PromptTokensDetails(BaseModel):
    audio_tokens: Optional[Any] = None
    cached_tokens: int

class Usage(BaseModel):
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int
    completion_tokens_details: Optional[Any] = None
    prompt_tokens_details: PromptTokensDetails
    cache_creation_input_tokens: int
    cache_read_input_tokens: int

class ChatCompletion(BaseModel):
    id: str
    created: int
    model: str
    object: str = Field(..., alias="object")
    system_fingerprint: Optional[Any] = None
    choices: List[Choice]
    usage: Usage