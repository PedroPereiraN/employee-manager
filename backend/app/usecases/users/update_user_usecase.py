from datetime import date
from fastapi import HTTPException, status
from app.entities.user import User, UserProps
from app.protocols.usecase import UseCase
from app.dtos.user import UpdateUserInput, UpdateUserOutput
from app.repositories.user_repository import UserRepository


class UpdateUserUsecase(UseCase[UpdateUserInput, UpdateUserOutput]):
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def execute(self, input: UpdateUserInput) -> UpdateUserOutput:
        find_user = self.user_repository.find_by_id(id=input.id)

        user = User.restore(
            props=UserProps(
                id=input.id,
                name=input.name if input.name else find_user.name,
                email=input.email if input.email else find_user.email,
                password="",
                role=input.role if input.role else find_user.role,
                created_at=find_user.created_at,
                updated_at=date.today(),
                deleted_at=None,
            )
        )

        self.user_repository.update(entity=user)

        return UpdateUserOutput(
            id=user.id, name=user.name, email=user.email, role=user.role
        )
