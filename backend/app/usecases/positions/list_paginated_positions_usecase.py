from app.dtos.paginated_response import PaginatedResponseDto
from app.dtos.positions import ListPaginatedPositionsInputDto, OutputPositionDto
from app.protocols.usecase import UseCase
from app.repositories.position_repository import PositionRepository


class ListPaginatedPositionsUsecase(
    UseCase[ListPaginatedPositionsInputDto, PaginatedResponseDto[OutputPositionDto]]
):
    def __init__(self, position_repository: PositionRepository) -> None:
        self.position_repository = position_repository

    def execute(
        self, input: ListPaginatedPositionsInputDto
    ) -> PaginatedResponseDto[OutputPositionDto]:

        output = self.position_repository.list_paginated(
            page=input.page,
            size=input.size,
            filter=input.filter,
        )

        return output
