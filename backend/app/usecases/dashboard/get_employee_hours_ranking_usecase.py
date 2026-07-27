from app.dtos.dashboard import EmployeeHoursRankingInputDto, EmployeeHoursRankingOutputDto
from app.protocols.usecase import UseCase
from app.repositories.service_order_repository import ServiceOrderRepository


class GetEmployeeHoursRankingUsecase(
    UseCase[EmployeeHoursRankingInputDto, EmployeeHoursRankingOutputDto]
):
    def __init__(self, service_order_repository: ServiceOrderRepository) -> None:
        self.service_order_repository = service_order_repository

    def execute(self, input: EmployeeHoursRankingInputDto) -> EmployeeHoursRankingOutputDto:
        data = self.service_order_repository.get_employee_hours_ranking(
            from_date=input.from_date,
            to_date=input.to_date,
            limit=input.limit,
        )
        return EmployeeHoursRankingOutputDto(**data)
