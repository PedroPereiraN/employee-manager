from typing import Optional
from uuid import UUID
from app.dtos.employees import OutputEmployeeDto
from app.dtos.service_orders import (
    OutputServiceOrderDto,
    OutputWorkSessionDto,
    OutputWorkSessionHistoryDto,
)
from app.dtos.service_types import OutputServiceTypeDto
from app.entities.service_order import (
    ServiceOrder,
    ServiceOrderProps,
    WorkSessionProps,
    WorkSessionHistoryProps,
)
from app.models.service_order import (
    ServiceOrderModel,
    WorkSessionModel,
    WorkSessionHistoryModel,
)


class ServiceOrderMapper:
    @staticmethod
    def to_model(entity: ServiceOrder) -> ServiceOrderModel:
        return ServiceOrderModel(
            id=entity.id,
            order_number=entity.order_number,
            status=entity.status,
            description=entity.description,
            started_at=entity.started_at,
            finished_at=entity.finished_at,
            total_hours=entity.total_hours,
            service_type_id=entity.service_type_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            deleted_at=entity.deleted_at,
            work_sessions=[
                WorkSessionModel(
                    id=ws.id,
                    service_order_id=ws.service_order_id,
                    employee_id=ws.employee_id,
                    created_at=ws.created_at,
                    updated_at=ws.updated_at,
                    deleted_at=ws.deleted_at,
                    histories=[
                        WorkSessionHistoryModel(
                            id=h.id,
                            work_session_id=h.work_session_id,
                            status=h.status,
                            occurred_at=h.occurred_at,
                            created_at=h.created_at,
                        )
                        for h in ws.histories
                    ],
                )
                for ws in entity.work_sessions
            ],
        )

    @staticmethod
    def model_to_entity(model: ServiceOrderModel) -> ServiceOrder:
        return ServiceOrder(
            props=ServiceOrderProps(
                id=model.id,
                order_number=model.order_number,
                status=model.status,
                description=model.description,
                started_at=model.started_at,
                finished_at=model.finished_at,
                total_hours=model.total_hours,
                service_type_id=model.service_type_id,
                created_at=model.created_at,
                updated_at=model.updated_at,
                deleted_at=model.deleted_at,
                work_sessions=[
                    WorkSessionProps(
                        id=ws.id,
                        service_order_id=ws.service_order_id,
                        employee_id=ws.employee_id,
                        created_at=ws.created_at,
                        updated_at=ws.updated_at,
                        deleted_at=ws.deleted_at,
                        histories=[
                            WorkSessionHistoryProps(
                                id=h.id,
                                work_session_id=h.work_session_id,
                                status=h.status,
                                occurred_at=h.occurred_at,
                                created_at=h.created_at,
                            )
                            for h in ws.histories
                        ],
                    )
                    for ws in model.work_sessions
                ],
            )
        )

    @staticmethod
    def model_to_output(
        model: ServiceOrderModel,
        employees_output: dict[UUID, OutputEmployeeDto],
        service_type_output: Optional[OutputServiceTypeDto] = None,
    ) -> OutputServiceOrderDto:
        return OutputServiceOrderDto(
            id=model.id,
            order_number=model.order_number,
            status=model.status,
            description=model.description,
            started_at=model.started_at,
            finished_at=model.finished_at,
            total_hours=model.total_hours,
            service_type=service_type_output,
            created_at=model.created_at,
            updated_at=model.updated_at,
            deleted_at=model.deleted_at,
            work_sessions=[
                OutputWorkSessionDto(
                    id=ws.id,
                    service_order_id=ws.service_order_id,
                    employee=employees_output[ws.employee_id],
                    created_at=ws.created_at,
                    updated_at=ws.updated_at,
                    deleted_at=ws.deleted_at,
                    histories=[
                        OutputWorkSessionHistoryDto(
                            id=h.id,
                            work_session_id=h.work_session_id,
                            status=h.status,
                            occurred_at=h.occurred_at,
                            created_at=h.created_at,
                        )
                        for h in ws.histories
                    ],
                )
                for ws in model.work_sessions
            ],
        )

    @staticmethod
    def entity_to_output(
        entity: ServiceOrder,
        employees_output: dict[UUID, OutputEmployeeDto],
        service_type_output: Optional[OutputServiceTypeDto] = None,
    ) -> OutputServiceOrderDto:
        return OutputServiceOrderDto(
            id=entity.id,
            order_number=entity.order_number,
            status=entity.status,
            description=entity.description,
            started_at=entity.started_at,
            finished_at=entity.finished_at,
            total_hours=entity.total_hours,
            service_type=service_type_output,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            deleted_at=entity.deleted_at,
            work_sessions=[
                OutputWorkSessionDto(
                    id=ws.id,
                    service_order_id=ws.service_order_id,
                    employee=employees_output[ws.employee_id],
                    created_at=ws.created_at,
                    updated_at=ws.updated_at,
                    deleted_at=ws.deleted_at,
                    histories=[
                        OutputWorkSessionHistoryDto(
                            id=h.id,
                            work_session_id=h.work_session_id,
                            status=h.status,
                            occurred_at=h.occurred_at,
                            created_at=h.created_at,
                        )
                        for h in ws.histories
                    ],
                )
                for ws in entity.work_sessions
            ],
        )
