from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dtos.auth import LoginInputDto, LoginOutputDto
from app.middleware.get_db import get_db
from app.repositories.user_repository import UserRepository
from app.usecases.auth.login_usecase import LoginUsecase

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/", status_code=200, response_model=LoginOutputDto)
async def create_user(body: LoginInputDto, db: Session = Depends(get_db)):
    user_repository = UserRepository(db=db)

    return LoginUsecase(user_repository=user_repository).execute(body)
