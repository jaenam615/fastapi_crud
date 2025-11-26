from fastapi import FastAPI
from app.core.db import Base, engine
from app.routers import auth_router, post_router, comment_router
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI CRUD")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(post_router.router)
app.include_router(comment_router.router)