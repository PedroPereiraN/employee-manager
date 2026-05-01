from app.dtos.paginated_response import PaginatedResponseDto
from app.dtos.service_orders import (
    ListPaginatedServiceOrdersInputDto,
    OutputServiceOrderDto,
)
from app.protocols.usecase import UseCase
from app.repositories.service_order_repository import ServiceOrderRepository


class ListPaginatedServiceOrdersUsecase(
    UseCase[
        ListPaginatedServiceOrdersInputDto, PaginatedResponseDto[OutputServiceOrderDto]
    ]
):
    def __init__(self, service_order_repository: ServiceOrderRepository) -> None:
        self.service_order_repository = service_order_repository

    def execute(
        self, input: ListPaginatedServiceOrdersInputDto
    ) -> PaginatedResponseDto[OutputServiceOrderDto]:

        output = self.service_order_repository.list_paginated(
            page=input.page,
            size=input.size,
            filter=input.filter,
        )

        return output
