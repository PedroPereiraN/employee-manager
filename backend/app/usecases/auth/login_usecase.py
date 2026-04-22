from fastapi import HTTPException, status
from pydantic import BaseModel
from app.dtos.auth import LoginInputDto, LoginOutputDto
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.hash_service import HashService


class LoginUsecase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, input: LoginInputDto) -> LoginOutputDto:
        user = self.user_repository.find_by_email(email=input.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )
        if not HashService.verify(input.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )
        token = AuthService.generate_token(
            user_id=str(user.id),
            role=user.role.value,
        )
        return LoginOutputDto(access_token=token)
