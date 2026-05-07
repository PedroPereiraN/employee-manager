from app.dtos.service_orders import (
    ReportServiceOrderProgressInputDto,
    ReportServiceOrderProgressOutputDto,
)
from app.protocols.usecase import UseCase
from app.repositories.service_order_repository import ServiceOrderRepository
from fastapi import HTTPException, status


class ReportServiceOrderProgressUsecasae(
    UseCase[ReportServiceOrderProgressInputDto, ReportServiceOrderProgressOutputDto]
):
    def __init__(self, service_order_repository: ServiceOrderRepository) -> None:
        self.service_order_repository = service_order_repository

    def execute(
        self, input: ReportServiceOrderProgressInputDto
    ) -> ReportServiceOrderProgressOutputDto:
        service_order = self.service_order_repository.find_by_id(
            id=input.service_order_id
        )
