from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from uuid import UUID
import uuid6
from app.enums.service_order_status import ServiceOrderStatus
from app.enums.work_session_status import WorkSessionStatus


class CreateWorkSessionHistoryProps(BaseModel):
    status: WorkSessionStatus
    occurred_at: datetime


class CreateWorkSessionProps(BaseModel):
    employee_id: UUID
    histories: List[CreateWorkSessionHistoryProps]


class CreateServiceOrderProps(BaseModel):
    order_number: str
    status: ServiceOrderStatus
    description: Optional[str] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    total_hours: Optional[float] = None
    service_type_id: Optional[UUID] = None
    work_sessions: List[CreateWorkSessionProps]


class WorkSessionHistoryProps(BaseModel):
    id: UUID
    work_session_id: UUID
    status: WorkSessionStatus
    occurred_at: datetime
    created_at: datetime


class WorkSessionProps(BaseModel):
    id: UUID
    service_order_id: UUID
    employee_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    histories: List[WorkSessionHistoryProps]


class ServiceOrderProps(BaseModel):
    id: UUID
    order_number: str
    status: ServiceOrderStatus
    description: Optional[str] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    total_hours: Optional[float] = None
    service_type_id: Optional[UUID] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    work_sessions: List[WorkSessionProps]


class ServiceOrder:
    id: UUID
    order_number: str
    status: ServiceOrderStatus
    description: Optional[str] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    total_hours: Optional[float] = None
    service_type_id: Optional[UUID] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    work_sessions: List[WorkSessionProps]

    def __init__(self, props: ServiceOrderProps):
        self.id = props.id
        self.order_number = props.order_number
        self.status = props.status
        self.description = props.description
        self.started_at = props.started_at
        self.finished_at = props.finished_at
        self.total_hours = props.total_hours
        self.service_type_id = props.service_type_id
        self.created_at = props.created_at
        self.updated_at = props.updated_at
        self.deleted_at = props.deleted_at
        self.work_sessions = props.work_sessions

    @staticmethod
    def create(props: CreateServiceOrderProps):
        now = datetime.now()
        order_id = uuid6.uuid7()

        work_sessions = []
        for ws in props.work_sessions:
            ws_id = uuid6.uuid7()
            work_sessions.append(
                WorkSessionProps(
                    id=ws_id,
                    service_order_id=order_id,
                    employee_id=ws.employee_id,
                    created_at=now,
                    histories=[
                        WorkSessionHistoryProps(
                            id=uuid6.uuid7(),
                            work_session_id=ws_id,
                            status=history.status,
                            occurred_at=history.occurred_at,
                            created_at=now,
                        )
                        for history in ws.histories
                    ],
                )
            )

        return ServiceOrder(
            ServiceOrderProps(
                id=order_id,
                order_number=props.order_number,
                status=props.status,
                description=props.description,
                started_at=props.started_at,
                finished_at=props.finished_at,
                total_hours=props.total_hours,
                service_type_id=props.service_type_id,
                created_at=now,
                work_sessions=work_sessions,
            )
        )

    @staticmethod
    def restore(props: ServiceOrderProps):
        return ServiceOrder(
            ServiceOrderProps(
                id=props.id,
                order_number=props.order_number,
                status=props.status,
                description=props.description,
                started_at=props.started_at,
                finished_at=props.finished_at,
                total_hours=props.total_hours,
                service_type_id=props.service_type_id,
                created_at=props.created_at,
                updated_at=props.updated_at,
                deleted_at=props.deleted_at,
                work_sessions=props.work_sessions,
            )
        )
