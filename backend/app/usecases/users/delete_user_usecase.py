from app.protocols.usecase import UseCase
from app.dtos.user import DeleteUserInput
from app.repositories.user_repository import UserRepository


class DeleteUserUsecase(UseCase[DeleteUserInput, None]):
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def execute(self, input: DeleteUserInput) -> None:
        self.user_repository.delete(id=input.id)
