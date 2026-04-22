from datetime import date
from fastapi import HTTPException, status
from app.entities.user import User, UserProps
from app.protocols.usecase import UseCase
from app.dtos.user import UpdateUserOutput, UpdateUserPasswordInput
from app.repositories.user_repository import UserRepository
from app.services.hash_service import HashService


class UpdateUserPasswordUsecase(UseCase[UpdateUserPasswordInput, None]):
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def execute(self, input: UpdateUserPasswordInput) -> None:
        hashed_password = HashService.hash(password=input.new_password)

        self.user_repository.update_password(id=input.id, new_password=hashed_password)
