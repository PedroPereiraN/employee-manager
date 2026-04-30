from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.position import PositionModel
    from app.models.service_order import WorkSessionModel

from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey, String, Date, Enum as SAEnum, Float
from uuid import UUID as PyUUID
from datetime import date
from app.config.base import Base
import uuid6

from app.enums.employee_status import EmployeeStatus
from app.enums.employee_type import EmployeeType
from app.enums.payment_method import PaymentMethod


class EmployeeModel(Base):
    __tablename__ = "employees"

    id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid6.uuid7
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    birthday: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    admission_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    status: Mapped[EmployeeStatus] = mapped_column(
        SAEnum(EmployeeStatus), nullable=False
    )
    type: Mapped[EmployeeType] = mapped_column(SAEnum(EmployeeType), nullable=False)
    payment_method: Mapped[PaymentMethod] = mapped_column(
        SAEnum(PaymentMethod), nullable=False
    )
    payment_value: Mapped[float] = mapped_column(Float, nullable=False)
    hourly_rate: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    hourly_bonus: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    observations: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    position_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("positions.id"), nullable=False
    )
    position: Mapped[PositionModel] = relationship(
        "PositionModel", back_populates="employees"
    )
    work_sessions: Mapped[list[WorkSessionModel]] = relationship(
        "WorkSessionModel", back_populates="employee"
    )
    created_at: Mapped[date] = mapped_column(Date, nullable=False)
    updated_at: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    deleted_at: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
