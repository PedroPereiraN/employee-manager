from app.dtos.employees import OutputEmployeeDto
from app.dtos.positions import OutputPositionDto
from app.entities.employee import Employee, EmployeeProps
from app.models.employee import EmployeeModel


class EmployeeMapper:
    @staticmethod
    def to_model(entity: Employee) -> EmployeeModel:
        return EmployeeModel(
            id=entity.id,
            name=entity.name,
            birthday=entity.birthday,
            phone=entity.phone,
            email=entity.email,
            admission_date=entity.admission_date,
            status=entity.status,
            type=entity.type,
            payment_method=entity.payment_method,
            payment_value=entity.payment_value,
            hourly_rate=entity.hourly_rate,
            hourly_bonus=entity.hourly_bonus,
            observations=entity.observations,
            position_id=entity.position_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            deleted_at=entity.deleted_at,
        )

    @staticmethod
    def model_to_entity(model: EmployeeModel) -> Employee:
        return Employee(
            props=EmployeeProps(
                id=model.id,
                name=model.name,
                birthday=model.birthday,
                phone=model.phone,
                email=model.email,
                admission_date=model.admission_date,
                status=model.status,
                type=model.type,
                payment_method=model.payment_method,
                payment_value=model.payment_value,
                hourly_rate=model.hourly_rate,
                hourly_bonus=model.hourly_bonus,
                observations=model.observations,
                position_id=model.position_id,
                created_at=model.created_at,
                updated_at=model.updated_at,
                deleted_at=model.deleted_at,
            )
        )

    @staticmethod
    def model_to_output(
        model: EmployeeModel, position_output: OutputPositionDto
    ) -> OutputEmployeeDto:
        return OutputEmployeeDto(
            id=model.id,
            name=model.name,
            birthday=model.birthday,
            phone=model.phone,
            email=model.email,
            admission_date=model.admission_date,
            status=model.status,
            type=model.type,
            payment_method=model.payment_method,
            payment_value=model.payment_value,
            hourly_rate=model.hourly_rate,
            hourly_bonus=model.hourly_bonus,
            observations=model.observations,
            position=position_output,
            created_at=model.created_at,
            updated_at=model.updated_at,
            deleted_at=model.deleted_at,
        )

    @staticmethod
    def entity_to_output(
        entity: Employee, position_output: OutputPositionDto
    ) -> OutputEmployeeDto:
        return OutputEmployeeDto(
            id=entity.id,
            name=entity.name,
            birthday=entity.birthday,
            phone=entity.phone,
            email=entity.email,
            admission_date=entity.admission_date,
            status=entity.status,
            type=entity.type,
            payment_method=entity.payment_method,
            payment_value=entity.payment_value,
            hourly_rate=entity.hourly_rate,
            hourly_bonus=entity.hourly_bonus,
            observations=entity.observations,
            position=position_output,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            deleted_at=entity.deleted_at,
        )
