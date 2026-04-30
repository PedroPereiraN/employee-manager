from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.service_order import ServiceOrderModel

from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Date
from uuid import UUID as PyUUID
from datetime import date
from app.config.base import Base
import uuid6


class ServiceTypeModel(Base):
    __tablename__ = "service_types"

    id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid6.uuid7
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    service_orders: Mapped[list[ServiceOrderModel]] = relationship(
        "ServiceOrderModel", back_populates="service_type"
    )
    created_at: Mapped[date] = mapped_column(Date, nullable=False)
    updated_at: Mapped[date | None] = mapped_column(Date, nullable=True)
    deleted_at: Mapped[date | None] = mapped_column(Date, nullable=True)
