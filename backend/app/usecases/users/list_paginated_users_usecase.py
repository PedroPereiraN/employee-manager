from app.dtos.paginated_response import PaginatedResponseDto
from app.protocols.usecase import UseCase
from app.dtos.user import ListPaginatedUsersInputDto, OutputUserDto
from app.repositories.user_repository import UserRepository


class ListPaginatedUsersUsecase(
    UseCase[ListPaginatedUsersInputDto, PaginatedResponseDto[OutputUserDto]]
):
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def execute(
        self, input: ListPaginatedUsersInputDto
    ) -> PaginatedResponseDto[OutputUserDto]:

        output = self.user_repository.list_paginated(
            page=input.page,
            size=input.size,
            filter=input.filter,
            filter_role=input.filter_role,
        )

        return output
