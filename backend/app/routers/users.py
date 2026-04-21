from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dtos.user import CreateUserInput, CreateUserOutput
from app.middleware.get_db import get_db
from app.repositories.user_repository import UserRepository
from app.usecases.users.create_user_usecase import CreateUserUsecase

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post("/", status_code=200, response_model=CreateUserOutput)
async def create_user(body: CreateUserInput, db: Session = Depends(get_db)):
    user_repository = UserRepository(db=db)

    return CreateUserUsecase(user_repository=user_repository).execute(body)
