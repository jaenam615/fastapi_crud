from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.core.db import get_db
from app.core.security import create_access_token
from app.services.user_service import user_service

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup")
def signup(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_service.create_user(db, data)
    return {"message": "ok"}

@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = user_service.authenticate(db, form.username, form.password)
    if not user:
        raise HTTPException(400, "Wrong credentials")

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}
