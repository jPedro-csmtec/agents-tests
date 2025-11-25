import traceback
import logging
from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware
from libs.errors.exceptions import APIError
from libs.errors.models import StandardResponse
from gateway.app.schemas.errors import ResultErrorSchema
from libs.utils.custom_route import CustomRoute
from logs.logger import log_function_call
from .routers.v1 import router as v1_router
from gateway.app.routers.auth_token import get_current_user, router as auth_router 
from fastapi_mcp import FastApiMCP
from fastapi.openapi.utils import get_openapi

logger = logging.getLogger("uvicorn.error")

app = FastAPI(
    title="Gateway Service",
    version="1.0.0",
    docs_url="/swagger",
    redoc_url="/redoc",
    route_class=CustomRoute,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

@app.exception_handler(StarletteHTTPException)
@log_function_call
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    err = ResultErrorSchema(
        code=1,
        code_alias="GENERIC_ERROR",
        system_code="ROUTE_ERROR",
        description=str(exc.detail),
        about_link=None,
        details=None
    )
    code=500
    try:
        if exc.status_code == 401:
            err = ResultErrorSchema(
                code=4,
                code_alias="UNAUTHORIZED",
                system_code="AUTH_ERROR",
                description=str(exc.detail),
                about_link=None,
                details=None
            )
            code=401
    except Exception as e:
        pass
    
    envelope = StandardResponse[None](
        success=False,
        error=err
    )
    return JSONResponse(
        status_code=code,
        content=envelope.model_dump(exclude_none=True)
    )

@app.exception_handler(APIError)
@log_function_call
async def api_error_handler(request: Request, exc: APIError):
    logger.warning(
        f"[APIError] code={int(exc.code)} alias={exc.code_alias} "
        f"system_code={exc.system_code} desc={exc.description}"
    )
    err = ResultErrorSchema(
        code=int(exc.code),
        code_alias=exc.code_alias,
        system_code=exc.system_code,
        description=exc.description,
        about_link=exc.about_link,
        details=exc.details
    )
    
    envelope = StandardResponse[None](
        success=False,
        error=err
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=envelope.model_dump(exclude_none=True)
    )

@app.exception_handler(Exception)
@log_function_call
async def all_exception_handler(request: Request, exc: Exception):
    tb = traceback.format_exc()
    logger.error(f"[Unhandled Exception]\n{tb}")
    err = ResultErrorSchema(
        code=1,
        code_alias="GENERIC_ERROR",
        system_code="INTERNAL_SERVER_ERROR",
        description="Ocorreu um erro interno. Tente novamente mais tarde.",
        about_link=None,
        details=None
    )
    code = 500
    try:
        if exc.status_code == 401:
            err = ResultErrorSchema(
                code=4,
                code_alias="UNAUTHORIZED",
                system_code="AUTH_ERROR",
                description=str(exc.detail),
                about_link=None,
                details=None
            )
            code = 401
    except Exception as e:
        print(f"Erro: {exc.args}")
        pass
        
    envelope = StandardResponse[None](
        success=False,
        error=err
    )
    return JSONResponse(
        status_code=code,
        content=envelope.model_dump(exclude_none=True)
    )

app.include_router(auth_router, tags=["auth"], prefix="/api/v1/auth")

app.include_router(
    v1_router,
    prefix="/api/v1",
    dependencies=[Depends(get_current_user),],
    include_in_schema=True
)


mcp = FastApiMCP(
    app,
    name="GatewayServiceMCP",
    description="API stateless via MCP",
    describe_full_response_schema=True,
    describe_all_responses=True,
)

mcp.mount_http(mount_path="/mcp/api")

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Gateway Service",
        version="1.0.0",
        description="Autenticação Bearer Token",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi