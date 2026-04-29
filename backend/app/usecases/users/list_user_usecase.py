from app.mappers.user_mapper import UserMapper
from app.protocols.usecase import UseCase
from app.dtos.user import ListUserInputDto, OutputUserDto
from app.repositories.user_repository import UserRepository


class ListUserUsecase(UseCase[ListUserInputDto, OutputUserDto]):
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def execute(self, input: ListUserInputDto) -> OutputUserDto:

        output = self.user_repository.find_by_id(id=input.id)

        return UserMapper.entity_to_output(entity=output)
