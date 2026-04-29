from datetime import date
from typing import Optional
from pydantic import BaseModel
import uuid6
from uuid import UUID

from app.enums.user_role import UserRole
from app.services.hash_service import HashService


class CreatePositionProps(BaseModel):
    name: str
    description: Optional[str] = None


class PositionProps(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    created_at: date
    updated_at: Optional[date] = None
    deleted_at: Optional[date] = None


class Position:
    id: UUID
    name: str
    description: Optional[str] = None
    created_at: date
    updated_at: Optional[date] = None
    deleted_at: Optional[date] = None

    def __init__(self, props: PositionProps):
        self.id = props.id
        self.name = props.name
        self.description = props.description
        self.created_at = props.created_at
        self.updated_at = props.updated_at
        self.deleted_at = props.deleted_at

    @staticmethod
    def create(props: CreatePositionProps):
        return Position(
            PositionProps(
                id=uuid6.uuid7(),
                name=props.name,
                description=props.description,
                created_at=date.today(),
            )
        )

    @staticmethod
    def restore(props: PositionProps):
        return Position(
            PositionProps(
                id=props.id,
                name=props.name,
                description=props.description,
                created_at=props.created_at,
                updated_at=props.updated_at,
                deleted_at=props.deleted_at,
            )
        )
