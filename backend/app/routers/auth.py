from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.dtos.auth import LoginInputDto, LoginOutputDto
from app.middleware.get_db import get_db
from app.repositories.user_repository import UserRepository
from app.usecases.auth.login_usecase import LoginUsecase

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/login", status_code=200, response_model=LoginOutputDto)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user_repository = UserRepository(db=db)

    body = LoginInputDto(email=form_data.username, password=form_data.password)

    return LoginUsecase(user_repository=user_repository).execute(body)
