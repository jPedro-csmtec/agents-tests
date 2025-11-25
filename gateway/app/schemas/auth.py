from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str
    
class TokenCall(BaseModel):
    access_token: str
    token_type: str
