from app.protocols.usecase import UseCase
from app.dtos.user import DeleteUserInputDto
from app.repositories.user_repository import UserRepository


class DeleteUserUsecase(UseCase[DeleteUserInputDto, None]):
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def execute(self, input: DeleteUserInputDto) -> None:
        self.user_repository.delete(id=input.id)
