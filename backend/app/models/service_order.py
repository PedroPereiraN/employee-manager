from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.employee import EmployeeModel
    from app.models.service_type import ServiceTypeModel

from app.enums.service_order_status import ServiceOrderStatus
from app.enums.work_session_status import WorkSessionStatus

from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey, String, Enum as SAEnum, DateTime, Float
from uuid import UUID as PyUUID
from datetime import datetime
from app.config.base import Base
import uuid6


class ServiceOrderModel(Base):
    __tablename__ = "service_orders"

    id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid6.uuid7
    )
    order_number: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[ServiceOrderStatus] = mapped_column(
        SAEnum(ServiceOrderStatus), nullable=False
    )
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    total_hours: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    service_type_id: Mapped[Optional[PyUUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("service_types.id"), nullable=True
    )

    service_type: Mapped[ServiceTypeModel] = relationship(
        "ServiceTypeModel", back_populates="service_orders"
    )
    work_sessions: Mapped[list[WorkSessionModel]] = relationship(
        "WorkSessionModel", back_populates="service_order"
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class WorkSessionModel(Base):
    __tablename__ = "work_sessions"

    id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid6.uuid7
    )
    service_order_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("service_orders.id"), nullable=False
    )
    service_order: Mapped[ServiceOrderModel] = relationship(
        "ServiceOrderModel", back_populates="work_sessions"
    )
    employee_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("employees.id"), nullable=False
    )

    employee: Mapped[EmployeeModel] = relationship(
        "EmployeeModel", back_populates="work_sessions"
    )

    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    histories: Mapped[list[WorkSessionHistoryModel]] = relationship(
        "WorkSessionHistoryModel", back_populates="work_session"
    )


class WorkSessionHistoryModel(Base):
    __tablename__ = "work_session_histories"

    id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid6.uuid7
    )
    work_session_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("work_sessions.id"), nullable=False
    )
    status: Mapped[WorkSessionStatus] = mapped_column(
        SAEnum(WorkSessionStatus), nullable=False
    )
    occurred_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    work_session: Mapped[WorkSessionModel] = relationship(
        "WorkSessionModel", back_populates="histories"
    )
