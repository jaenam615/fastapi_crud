from fastapi import FastAPI
from app.core.db import Base, engine
from app.routers import auth_router, post_router, comment_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Boilerplate")

app.include_router(auth_router.router)
app.include_router(post_router.router)
app.include_router(comment_router.router)