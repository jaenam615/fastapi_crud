import random

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.core.db import read_engines, write_engine


class DBRoutingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        method = request.method.upper()

        if method == "GET":
            request.state.db_engine = random.choice(read_engines)

        else:
            request.state.db_engine = write_engine

        response = await call_next(request)
        return response
