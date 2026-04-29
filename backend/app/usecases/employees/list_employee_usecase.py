from app.dtos.employees import ListEmployeeInputDto, OutputEmployeeDto
from app.mappers.employee_mapper import EmployeeMapper
from app.mappers.position_mapper import PositionMapper
from app.protocols.usecase import UseCase
from app.repositories.employee_repository import EmployeeRepository
from app.repositories.position_repository import PositionRepository


class ListEmployeeUsecase(UseCase[ListEmployeeInputDto, OutputEmployeeDto]):
    def __init__(
        self,
        employee_repository: EmployeeRepository,
        position_repository: PositionRepository,
    ) -> None:
        self.employee_repository = employee_repository
        self.position_repository = position_repository

    def execute(self, input: ListEmployeeInputDto) -> OutputEmployeeDto:

        output = self.employee_repository.find_by_id(id=input.id)

        position_entity = self.position_repository.find_by_id(id=output.position_id)

        position_output = PositionMapper.entity_to_output(entity=position_entity)

        return EmployeeMapper.entity_to_output(
            entity=output, position_output=position_output
        )
