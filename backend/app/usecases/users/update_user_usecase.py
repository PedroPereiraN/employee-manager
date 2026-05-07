from datetime import datetime

from fastapi import HTTPException, status
from app.entities.user import User, UserProps
from app.protocols.usecase import UseCase
from app.dtos.user import UpdateUserInputDto, UpdateUserOutputDto
from app.repositories.user_repository import UserRepository


class UpdateUserUsecase(UseCase[UpdateUserInputDto, UpdateUserOutputDto]):
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def execute(self, input: UpdateUserInputDto) -> UpdateUserOutputDto:
        find_user = self.user_repository.find_by_id(id=input.id)

        user = User.restore(
            props=UserProps(
                id=input.id,
                name=input.name if input.name else find_user.name,
                email=input.email if input.email else find_user.email,
                password=find_user.password,
                role=input.role if input.role else find_user.role,
                created_at=find_user.created_at,
                updated_at=datetime.now(),
                deleted_at=None,
            )
        )

        self.user_repository.update(entity=user)

        if not user.updated_at:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Update error",
            )

        return UpdateUserOutputDto(
            id=user.id,
            name=user.name,
            email=user.email,
            role=user.role,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
