from typing import Callable
from fastapi import Request
from fastapi.routing import APIRoute
from fastapi.responses import JSONResponse
from libs.errors.models import StandardResponse

class CustomRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original = super().get_route_handler()
        async def wrapped(request: Request):
            response = await original(request)

            if request.url.path.endswith("/token"):
                return response

            status = response.status_code
            content = await response.json() if hasattr(response, "json") else response

            if status < 400:
                content = response.json() if hasattr(response, "json") else response
                envelope = StandardResponse(
                    success=True,
                    data=content
                )
                return JSONResponse(
                    status_code=status,
                    content=envelope.model_dump(exclude_none=True)
                )

            content = response.json() if hasattr(response, "json") else response
            envelope = StandardResponse(
                success=False,
                error=content
            )
            return JSONResponse(
                status_code=status,
                content=envelope.model_dump(exclude_none=True)
            )

        return wrapped
