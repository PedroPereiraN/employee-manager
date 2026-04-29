from app.dtos.employees import DeleteEmployeeInputDto
from app.protocols.usecase import UseCase
from app.repositories.employee_repository import EmployeeRepository


class DeleteEmployeeUsecase(UseCase[DeleteEmployeeInputDto, None]):
    def __init__(self, employee_repository: EmployeeRepository) -> None:
        self.employee_repository = employee_repository

    def execute(self, input: DeleteEmployeeInputDto) -> None:
        self.employee_repository.delete(id=input.id)
