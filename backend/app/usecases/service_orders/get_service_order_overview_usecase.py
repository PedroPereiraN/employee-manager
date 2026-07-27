from app.dtos.service_orders import ServiceOrderOverviewInputDto, ServiceOrderOverviewOutputDto
from app.protocols.usecase import UseCase
from app.repositories.service_order_repository import ServiceOrderRepository


class GetServiceOrderOverviewUsecase(
    UseCase[ServiceOrderOverviewInputDto, ServiceOrderOverviewOutputDto]
):
    def __init__(self, service_order_repository: ServiceOrderRepository) -> None:
        self.service_order_repository = service_order_repository

    def execute(self, input: ServiceOrderOverviewInputDto) -> ServiceOrderOverviewOutputDto:
        data = self.service_order_repository.get_overview(
            from_date=input.from_date,
            to_date=input.to_date,
        )
        return ServiceOrderOverviewOutputDto(**data)
