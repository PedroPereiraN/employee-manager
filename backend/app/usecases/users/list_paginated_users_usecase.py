from app.dtos.paginated_response import PaginatedResponse
from app.protocols.usecase import UseCase
from app.dtos.user import ListPaginatedUsersInput, OutputUserDto
from app.repositories.user_repository import UserRepository


class ListPaginatedUsersUsecase(
    UseCase[ListPaginatedUsersInput, PaginatedResponse[OutputUserDto]]
):
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def execute(
        self, input: ListPaginatedUsersInput
    ) -> PaginatedResponse[OutputUserDto]:

        output = self.user_repository.list_paginated(
            page=input.page,
            size=input.size,
            filter=input.filter,
            filter_role=input.filter_role,
        )

        return output
