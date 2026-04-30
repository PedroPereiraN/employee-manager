from app.dtos.paginated_response import PaginatedResponseDto
from app.dtos.service_types import (
    ListPaginatedServiceTypesInputDto,
    OutputServiceTypeDto,
)
from app.protocols.usecase import UseCase
from app.repositories.service_type_repository import ServiceTypeRepository


class ListPaginatedServiceTypesUsecase(
    UseCase[
        ListPaginatedServiceTypesInputDto, PaginatedResponseDto[OutputServiceTypeDto]
    ]
):
    def __init__(self, service_type_repository: ServiceTypeRepository) -> None:
        self.service_type_repository = service_type_repository

    def execute(
        self, input: ListPaginatedServiceTypesInputDto
    ) -> PaginatedResponseDto[OutputServiceTypeDto]:

        output = self.service_type_repository.list_paginated(
            page=input.page,
            size=input.size,
            filter=input.filter,
        )

        return output
