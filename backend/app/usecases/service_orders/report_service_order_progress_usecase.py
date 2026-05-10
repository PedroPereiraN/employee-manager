from datetime import datetime
from app.dtos.service_orders import (
    ReportServiceOrderProgressInputDto,
)
from app.entities.service_order import WorkSessionHistoryProps, WorkSessionProps
from app.protocols.usecase import UseCase
from app.repositories.service_order_repository import ServiceOrderRepository
import uuid6


class ReportServiceOrderProgressUsecase(
    UseCase[ReportServiceOrderProgressInputDto, None]
):
    def __init__(self, service_order_repository: ServiceOrderRepository) -> None:
        self.service_order_repository = service_order_repository

    def execute(self, input: ReportServiceOrderProgressInputDto) -> None:
        now = datetime.now()

        new_histories = [
            WorkSessionHistoryProps(
                id=uuid6.uuid7(),
                work_session_id=history.work_session_id,
                status=history.status,
                observations=history.observations,
                occurred_at=history.occurred_at,
                created_at=now,
            )
            for history in input.new_histories
        ]

        new_work_sessions = []
        for ws in input.new_work_sessions:
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

        self.service_order_repository.report_progress(
            service_order_id=input.service_order_id,
            new_work_sessions=new_work_sessions,
            new_histories=new_histories,
        )
