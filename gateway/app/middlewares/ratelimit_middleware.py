from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from configurations.config import Config
import time

REQUESTS = {}

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        now = time.time()
        window_start = now - int(Config.WINDOW)

        timestamps = [ts for ts in REQUESTS.get(client_ip, []) if ts > window_start]
        REQUESTS[client_ip] = timestamps

        if len(timestamps) >= int(Config.RATE_LIMIT):
            raise HTTPException(429, "Muitas requisições, tente mais tarde")

        REQUESTS[client_ip].append(now)
        return await call_next(request)
