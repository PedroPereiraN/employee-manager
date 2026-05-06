from app.dtos.service_orders import ListServiceOrderInputDto, OutputServiceOrderDto
from app.mappers.employee_mapper import EmployeeMapper
from app.mappers.position_mapper import PositionMapper
from app.mappers.service_order_mapper import ServiceOrderMapper
from app.mappers.service_type_mapper import ServiceTypeMapper
from app.protocols.usecase import UseCase
from app.repositories.employee_repository import EmployeeRepository
from app.repositories.position_repository import PositionRepository
from app.repositories.service_order_repository import ServiceOrderRepository
from app.repositories.service_type_repository import ServiceTypeRepository


class ListServiceOrderUsecase(UseCase[ListServiceOrderInputDto, OutputServiceOrderDto]):
    def __init__(
        self,
        service_order_repository: ServiceOrderRepository,
        employee_repository: EmployeeRepository,
        position_repository: PositionRepository,
        service_type_repository: ServiceTypeRepository,
    ) -> None:
        self.service_order_repository = service_order_repository
        self.employee_repository = employee_repository
        self.position_repository = position_repository
        self.service_type_repository = service_type_repository

    def execute(self, input: ListServiceOrderInputDto) -> OutputServiceOrderDto:
        service_order = self.service_order_repository.find_by_id(id=input.id)

        employees_output = {}
        for ws in service_order.work_sessions:
            if ws.employee_id not in employees_output:
                employee = self.employee_repository.find_by_id(id=ws.employee_id)
                position = self.position_repository.find_by_id(id=employee.position_id)
                employees_output[ws.employee_id] = EmployeeMapper.entity_to_output(
                    entity=employee,
                    position_output=PositionMapper.entity_to_output(entity=position),
                )

        service_type_output = None
        if service_order.service_type_id:
            service_type = self.service_type_repository.find_by_id(
                id=service_order.service_type_id
            )
            service_type_output = ServiceTypeMapper.entity_to_output(
                entity=service_type
            )

        return ServiceOrderMapper.entity_to_output(
            entity=service_order,
            employees_output=employees_output,
            service_type_output=service_type_output,
        )
