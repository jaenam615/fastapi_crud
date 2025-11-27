from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import create_access_token
from app.dependencies import get_user_service
from app.schemas.user import UserCreate
from app.services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup")
async def signup(
    data: UserCreate,
    user_service: UserService = Depends(get_user_service),
):
    await user_service.create_user(data=data)
    return {"message": "ok"}


@router.post("/login")
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(get_user_service),
):
    user = await user_service.authenticate(
        username=form.username, password=form.password
    )
    if not user:
        raise HTTPException(400, "Wrong credentials")

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}
