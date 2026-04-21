from sqlalchemy import DATE, String

from sqlalchemy import Column, String, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from app.config.base import Base
from app.enums.user_role import UserRole
import uuid6


class UserModel(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid6.uuid7)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(SAEnum(UserRole), nullable=False)
    created_at = Column(
        DATE,
        nullable=False,
    )
    updated_at = Column(
        DATE,
        nullable=True,
    )
    deleted_at = Column(
        DATE,
        nullable=True,
    )
