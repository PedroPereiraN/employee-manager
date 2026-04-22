from app.protocols.usecase import UseCase
from app.dtos.user import UpdateUserPasswordInputDto
from app.repositories.user_repository import UserRepository
from app.services.hash_service import HashService


class UpdateUserPasswordUsecase(UseCase[UpdateUserPasswordInputDto, None]):
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def execute(self, input: UpdateUserPasswordInputDto) -> None:
        hashed_password = HashService.hash(password=input.new_password)

        self.user_repository.update_password(id=input.id, new_password=hashed_password)
