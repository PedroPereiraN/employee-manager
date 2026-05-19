from datetime import datetime
from typing import Optional
from app.dtos.service_orders import ReportServiceOrderProgressInputDto
from app.entities.service_order import ServiceOrderStatusHistoryProps, WorkSessionHistoryProps, WorkSessionProps
from app.enums.service_order_status import ServiceOrderStatus
from app.protocols.usecase import UseCase
from app.repositories.service_order_repository import ServiceOrderRepository
import uuid6

TERMINAL_STATUSES = {ServiceOrderStatus.completed, ServiceOrderStatus.cancelled, ServiceOrderStatus.suspended}


class ReportServiceOrderProgressUsecase(
    UseCase[ReportServiceOrderProgressInputDto, None]
):
    def __init__(self, service_order_repository: ServiceOrderRepository) -> None:
        self.service_order_repository = service_order_repository

    def execute(self, input: ReportServiceOrderProgressInputDto) -> None:
        now = datetime.now()

        existing = self.service_order_repository.find_by_id(input.service_order_id)

        started_at: Optional[datetime] = existing.started_at
        finished_at: Optional[datetime] = None
        total_hours: Optional[float] = None

        if input.status == ServiceOrderStatus.in_progress and existing.started_at is None:
            started_at = now
        elif input.status in TERMINAL_STATUSES:
            finished_at = now
            if started_at:
                total_hours = (finished_at - started_at).total_seconds() / 3600

        status_history = ServiceOrderStatusHistoryProps(
            id=uuid6.uuid7(),
            service_order_id=input.service_order_id,
            status=input.status,
            reason=input.status_reason,
            created_at=now,
        )

        new_work_sessions = []
        if input.work_sessions:
            for ws in input.work_sessions:
                ws_id = uuid6.uuid7()
                new_work_sessions.append(
                    WorkSessionProps(
                        id=ws_id,
                        service_order_id=input.service_order_id,
                        employee_id=ws.employee_id,
                        created_at=now,
                        histories=[
                            WorkSessionHistoryProps(
                                id=uuid6.uuid7(),
                                work_session_id=ws_id,
                                status=history.status,
                                observations=history.observations,
                                occurred_at=history.occurred_at,
                                created_at=now,
                            )
                            for history in ws.histories
                        ],
                    )
                )

        new_histories = [
            WorkSessionHistoryProps(
                id=uuid6.uuid7(),
                work_session_id=h.work_session_id,
                status=h.status,
                observations=h.observations,
                occurred_at=h.occurred_at,
                created_at=now,
            )
            for h in (input.new_histories or [])
        ]

        self.service_order_repository.report_progress(
            service_order_id=input.service_order_id,
            new_status=input.status,
            status_history=status_history,
            new_work_sessions=new_work_sessions,
            new_histories=new_histories,
            started_at=started_at,
            finished_at=finished_at,
            total_hours=total_hours,
        )
