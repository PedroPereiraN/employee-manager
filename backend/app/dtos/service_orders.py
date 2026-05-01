from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel

from app.dtos.employees import OutputEmployeeDto
from app.enums.service_order_status import ServiceOrderStatus
from app.dtos.service_types import OutputServiceTypeDto
from app.enums.work_session_status import WorkSessionStatus


class OutputWorkSessionHistoryDto(BaseModel):
    id: UUID
    work_session_id: UUID
    status: WorkSessionStatus
    occurred_at: datetime
    created_at: datetime


class OutputWorkSessionDto(BaseModel):
    id: UUID
    service_order_id: UUID
    employee: OutputEmployeeDto
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    histories: List[OutputWorkSessionHistoryDto]


class OutputServiceOrderDto(BaseModel):
    id: UUID
    order_number: str
    status: ServiceOrderStatus
    description: Optional[str] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    total_hours: Optional[float] = None
    service_type: Optional[OutputServiceTypeDto] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    work_sessions: List[OutputWorkSessionDto]


class CreateWorkSessionHistoryInputDto(BaseModel):
    status: WorkSessionStatus
    occurred_at: datetime


class CreateWorkSessionInputDto(BaseModel):
    employee_id: UUID
    histories: List[CreateWorkSessionHistoryInputDto]


class CreateServiceOrderInputDto(BaseModel):
    status: ServiceOrderStatus
    description: Optional[str] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    total_hours: Optional[float] = None
    service_type_id: Optional[UUID] = None
    work_sessions: List[CreateWorkSessionInputDto]


class CreateWorkSessionHistoryOutputDto(BaseModel):
    id: UUID
    work_session_id: UUID
    status: WorkSessionStatus
    occurred_at: datetime
    created_at: datetime


class CreateWorkSessionOutputDto(BaseModel):
    id: UUID
    service_order_id: UUID
    employee_id: UUID
    created_at: datetime
    histories: List[CreateWorkSessionHistoryOutputDto]


class CreateServiceOrderOutputDto(BaseModel):
    id: UUID
    order_number: str
    status: ServiceOrderStatus
    description: Optional[str] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    total_hours: Optional[float] = None
    service_type_id: Optional[UUID] = None
    created_at: datetime
    work_sessions: List[CreateWorkSessionOutputDto]


class ListPaginatedServiceOrdersInputDto(BaseModel):
    filter: Optional[str] = None
    page: int
    size: int
