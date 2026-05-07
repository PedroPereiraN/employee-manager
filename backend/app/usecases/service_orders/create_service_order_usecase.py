from app.dtos.service_orders import (
    CreateServiceOrderInputDto,
    CreateServiceOrderOutputDto,
    CreateServiceOrderStatusHistoryOutputDto,
    CreateWorkSessionHistoryOutputDto,
    CreateWorkSessionOutputDto,
)
from app.entities.service_order import (
    CreateServiceOrderProps,
    CreateServiceOrderStatusHistoryProps,
    CreateWorkSessionHistoryProps,
    CreateWorkSessionProps,
    ServiceOrder,
)
from app.protocols.usecase import UseCase
from app.repositories.service_order_repository import ServiceOrderRepository


class CreateServiceOrderUsecase(
    UseCase[CreateServiceOrderInputDto, CreateServiceOrderOutputDto]
):
    def __init__(self, service_order_repository: ServiceOrderRepository) -> None:
        self.service_order_repository = service_order_repository

    def execute(self, input: CreateServiceOrderInputDto) -> CreateServiceOrderOutputDto:
        order_number = self.service_order_repository.generate_order_number()

        service_order = ServiceOrder.create(
            props=CreateServiceOrderProps(
                order_number=order_number,
                status=input.status,
                description=input.description,
                started_at=input.started_at,
                finished_at=input.finished_at,
                total_hours=input.total_hours,
                service_type_id=input.service_type_id,
                status_history=CreateServiceOrderStatusHistoryProps(
                    status=input.status_history.status,
                    reason=input.status_history.reason,
                ),
                work_sessions=[
                    CreateWorkSessionProps(
                        employee_id=ws.employee_id,
                        histories=[
                            CreateWorkSessionHistoryProps(
                                status=h.status,
                                occurred_at=h.occurred_at,
                            )
                            for h in ws.histories
                        ],
                    )
                    for ws in input.work_sessions
                ],
            )
        )
        self.service_order_repository.create(entity=service_order)
        return CreateServiceOrderOutputDto(
            id=service_order.id,
            order_number=service_order.order_number,
            status=service_order.status,
            description=service_order.description,
            started_at=service_order.started_at,
            finished_at=service_order.finished_at,
            total_hours=service_order.total_hours,
            service_type_id=service_order.service_type_id,
            created_at=service_order.created_at,
            status_histories=[
                CreateServiceOrderStatusHistoryOutputDto(
                    id=sh.id,
                    service_order_id=sh.service_order_id,
                    reason=sh.reason,
                    status=sh.status,
                    created_at=sh.created_at,
                )
                for sh in service_order.status_histories
            ],
            work_sessions=[
                CreateWorkSessionOutputDto(
                    id=ws.id,
                    service_order_id=ws.service_order_id,
                    employee_id=ws.employee_id,
                    created_at=ws.created_at,
                    histories=[
                        CreateWorkSessionHistoryOutputDto(
                            id=h.id,
                            work_session_id=h.work_session_id,
                            status=h.status,
                            occurred_at=h.occurred_at,
                            created_at=h.created_at,
                        )
                        for h in ws.histories
                    ],
                )
                for ws in service_order.work_sessions
            ],
        )
