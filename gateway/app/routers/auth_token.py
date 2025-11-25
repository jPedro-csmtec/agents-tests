from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
import jwt
from jose import JWTError
from configurations.config import Config
from gateway.app.schemas.auth import LoginRequest, TokenCall
from logs.logger import log_function_call

router = APIRouter(prefix="")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

@log_function_call
def authenticate_user(username: str, password: str) -> bool:
    return username == Config.USERNAME and password == Config.PASSWORD

@log_function_call
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        #payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM], verify=False,)
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

@router.post("/token", response_model=TokenCall)
@log_function_call
async def login_for_access_token(body: LoginRequest = Body(...)):
    if not authenticate_user(body.username, body.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    expire = datetime.utcnow() + timedelta(minutes=int(Config.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode = {"sub": body.username, "exp": expire}
    #to_encode = {"sub": body.username}
    token = jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}