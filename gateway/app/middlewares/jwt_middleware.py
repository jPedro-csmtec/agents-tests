from fastapi.responses import JSONResponse
from jose import JWTError
import jwt
from fastapi import Request
from configurations.config import Config
from gateway.app.main import app

PUBLIC_PATHS = {
    "/swagger",
    "/swagger/",
    "/docs",
    "/docs/",
    "/docs/oauth2-redirect",
    "/redoc",
    "/redoc/",
    "/openapi.json",
    "/debug/openapi",
    "/api/v1/auth/token"
}

@app.middleware("http")
async def jwt_middleware(request: Request, call_next):
    path = request.url.path
    if path.startswith("/auth") or path in PUBLIC_PATHS:
        return await call_next(request)

    auth = request.headers.get("Authorization")
    if not auth:
        return JSONResponse(status_code=401, content={"detail": "Token ausente"})

    parts = auth.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return JSONResponse(status_code=401, content={"detail": "Formato do token inválido"})

    token = parts[1]

    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        request.state.user = payload.get("sub")
    except JWTError:
        return JSONResponse(status_code=401, content={"detail": "Token inválido ou expirado"})

    return await call_next(request)



