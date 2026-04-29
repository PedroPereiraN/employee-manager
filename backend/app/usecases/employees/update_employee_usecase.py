from datetime import date
from app.dtos.employees import UpdateEmployeeInputDto, UpdateEmployeeOutputDto
from app.entities.employee import Employee, EmployeeProps
from app.protocols.usecase import UseCase
from app.repositories.employee_repository import EmployeeRepository
from app.repositories.position_repository import PositionRepository


class UpdateEmployeeUsecase(UseCase[UpdateEmployeeInputDto, UpdateEmployeeOutputDto]):
    def __init__(
        self,
        employee_repository: EmployeeRepository,
        position_repository: PositionRepository,
    ) -> None:
        self.employee_repository = employee_repository
        self.position_repository = position_repository

    def execute(self, input: UpdateEmployeeInputDto) -> UpdateEmployeeOutputDto:
        find_employee = self.employee_repository.find_by_id(id=input.id)

        if input.position_id:
            self.position_repository.find_by_id(id=input.position_id)

        employee = Employee.restore(
            props=EmployeeProps(
                id=input.id,
                name=input.name if input.name else find_employee.name,
                birthday=input.birthday if input.birthday else find_employee.birthday,
                phone=input.phone if input.phone else find_employee.phone,
                email=input.email if input.email else find_employee.email,
                admission_date=(
                    input.admission_date
                    if input.admission_date
                    else find_employee.admission_date
                ),
                status=input.status if input.status else find_employee.status,
                type=input.type if input.type else find_employee.type,
                payment_method=(
                    input.payment_method
                    if input.payment_method
                    else find_employee.payment_method
                ),
                payment_value=(
                    input.payment_value
                    if input.payment_value
                    else find_employee.payment_value
                ),
                hourly_rate=(
                    input.hourly_rate
                    if input.hourly_rate
                    else find_employee.hourly_rate
                ),
                hourly_bonus=(
                    input.hourly_bonus
                    if input.hourly_bonus
                    else find_employee.hourly_bonus
                ),
                observations=(
                    input.observations
                    if input.observations
                    else find_employee.observations
                ),
                position_id=(
                    input.position_id
                    if input.position_id
                    else find_employee.position_id
                ),
                created_at=find_employee.created_at,
                updated_at=date.today(),
                deleted_at=None,
            )
        )

        self.employee_repository.update(entity=employee)

        return UpdateEmployeeOutputDto(
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
            position_id=employee.position_id,
            created_at=employee.created_at,
            updated_at=employee.updated_at if employee.updated_at else date.today(),
        )
