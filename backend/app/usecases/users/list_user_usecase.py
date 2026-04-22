from fastapi import HTTPException, status
from app.protocols.usecase import UseCase
from app.dtos.user import ListUserInput, OutputUserDto
from app.repositories.user_repository import UserRepository


class ListUserUsecase(UseCase[ListUserInput, OutputUserDto]):
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def execute(self, input: ListUserInput) -> OutputUserDto:

        output = self.user_repository.find_by_id(id=input.id)

        if output:
            return output

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
