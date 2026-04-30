from __future__ import annotations
from typing import TYPE_CHECKING

from app.enums.service_order_status import ServiceOrderStatus

if TYPE_CHECKING:
    from app.models.employee import EmployeeModel

from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Date, Enum as SAEnum, DateTime, Float
from uuid import UUID as PyUUID
from datetime import date, datetime
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
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
