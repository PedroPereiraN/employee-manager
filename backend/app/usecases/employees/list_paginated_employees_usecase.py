from app.dtos.employees import ListPaginatedEmployeesInputDto, OutputEmployeeDto
from app.dtos.paginated_response import PaginatedResponseDto
from app.protocols.usecase import UseCase
from app.repositories.employee_repository import EmployeeRepository


class ListPaginatedEmployeesUsecase(
    UseCase[ListPaginatedEmployeesInputDto, PaginatedResponseDto[OutputEmployeeDto]]
):
    def __init__(self, employee_repository: EmployeeRepository) -> None:
        self.employee_repository = employee_repository

    def execute(
        self, input: ListPaginatedEmployeesInputDto
    ) -> PaginatedResponseDto[OutputEmployeeDto]:

        output = self.employee_repository.list_paginated(
            page=input.page,
            size=input.size,
            filter=input.filter,
        )

        return output
