import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.db import Base, write_engine
from app.core.middleware import DBRoutingMiddleware
from app.core.monitoring import setup_metrics
from app.routers import auth_router, comment_router, post_router

RUN_DB_INIT = os.getenv("RUN_DB_INIT", "false").lower() == "true"


@asynccontextmanager
async def lifespan(app: FastAPI):
    if RUN_DB_INIT:
        async with write_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="FastAPI CRUD", lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(DBRoutingMiddleware)

app.include_router(auth_router.router)
app.include_router(post_router.router)
app.include_router(comment_router.router)


setup_metrics(app)
