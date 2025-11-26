from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from schemas.user import UserCreate
from services.user_service import UserService, get_user_service
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup")
async def signup(
    data: UserCreate,
    db: AsyncSession = Depends(get_db),
    user_service: UserService = Depends(get_user_service),
):
    await user_service.create_user(db=db, data=data)
    return {"message": "ok"}


@router.post("/login")
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
    user_service: UserService = Depends(get_user_service),
):
    user = await user_service.authenticate(
        db=db, username=form.username, password=form.password
    )
    if not user:
        raise HTTPException(400, "Wrong credentials")

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}
