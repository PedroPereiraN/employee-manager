from app.dtos.employees import CreateEmployeeInputDto, CreateEmployeeOutputDto
from app.entities.employee import CreateEmployeeProps, Employee
from app.protocols.usecase import UseCase
from app.repositories.employee_repository import EmployeeRepository
from app.repositories.position_repository import PositionRepository


class CreateEmployeeUsecase(UseCase[CreateEmployeeInputDto, CreateEmployeeOutputDto]):
    def __init__(
        self,
        employee_repository: EmployeeRepository,
        position_repository: PositionRepository,
    ) -> None:
        self.employee_repository = employee_repository
        self.position_repository = position_repository

    def execute(self, input: CreateEmployeeInputDto) -> CreateEmployeeOutputDto:
        self.position_repository.find_by_id(id=input.position_id)

        employee = Employee.create(
            props=CreateEmployeeProps(
                name=input.name,
                birthday=input.birthday,
                phone=input.phone,
                email=input.email,
                admission_date=input.admission_date,
                status=input.status,
                type=input.type,
                payment_method=input.payment_method,
                payment_value=input.payment_value,
                hourly_rate=input.hourly_rate,
                hourly_bonus=input.hourly_bonus,
                observations=input.observations,
                position_id=input.position_id,
            )
        )

        self.employee_repository.create(entity=employee)

        return CreateEmployeeOutputDto(
            id=employee.id,
            name=employee.name,
            birthday=employee.birthday,
            phone=employee.phone,
            email=employee.email,
            admission_date=employee.admission_date,
            status=employee.status,
            type=employee.type,
            payment_method=employee.payment_method,
            payment_value=employee.payment_value,
            hourly_rate=employee.hourly_rate,
            hourly_bonus=employee.hourly_bonus,
            observations=employee.observations,
            created_at=employee.created_at,
            position_id=employee.position_id,
        )
