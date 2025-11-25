import traceback
import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from libs.errors.exceptions import APIError
from gateway.app.schemas.errors import ResultErrorSchema
from libs.errors.models import StandardResponse

logger = logging.getLogger("uvicorn.error")


async def api_exception_handler(request: Request, exc: Exception):
    
    if isinstance(exc, StarletteHTTPException):
        
        body = ResultErrorSchema(
            code=1,
            code_alias="GENERIC_ERROR",
            system_code="ROUTE_ERROR",
            description=str(exc.detail),
            about_link=None,
            details=None
        )
        
        payload =  StandardResponse[None](
            success = False,
            data= None,
            error = body
        )
        
        return JSONResponse(status_code=exc.status_code, content=payload.model_dump(exclude_none=True))

    if isinstance(exc, APIError):
        
        logger.warning(
            f"[APIError] code={exc.code.value} system_code={exc.system_code} "
            f"description={exc.description} details={exc.details}"
        )
        body = ResultErrorSchema(
            code=exc.code.value,
            code_alias=exc.code_alias,
            system_code=exc.system_code,
            description=exc.description,
            about_link=exc.about_link,
            details=exc.details
        )
        
        payload = StandardResponse[None](
            success = False,
            data    = None,
            error   = body
        )
        return JSONResponse(status_code=exc.status_code, content=payload.model_dump(exclude_none=True))

    
    tb = traceback.format_exc()
    logger.error(f"[Unhandled Exception] {tb}")

    body = ResultErrorSchema(
        code=1,
        code_alias="GENERIC_ERROR",
        system_code="INTERNAL_SERVER_ERROR",
        description="Ocorreu um erro interno. Tente novamente mais tarde.",
        about_link=None,
        details=None
    )
    
    payload = StandardResponse[None](
        success = False,
        data    = None,
        error   = body
    )
    return JSONResponse(status_code=500, content=payload.model_dump(exclude_none=True))
