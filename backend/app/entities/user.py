from datetime import date
from typing import Optional
from pydantic import BaseModel
import uuid6
from uuid import UUID

from app.enums.user_role import UserRole
from app.services.hash_service import HashService


class CreateUserProps(BaseModel):
    name: str
    password: str
    email: str
    role: UserRole


class UserProps(BaseModel):
    id: UUID
    name: str
    email: str
    role: UserRole
    password: str
    created_at: date
    updated_at: Optional[date] = None
    deleted_at: Optional[date] = None


class User:
    id: UUID
    name: str
    email: str
    role: UserRole
    password: str
    created_at: date
    updated_at: Optional[date] = None
    deleted_at: Optional[date] = None

    def __init__(self, props: UserProps):
        self.id = props.id
        self.name = props.name
        self.email = props.email
        self.role = props.role
        self.password = props.password
        self.created_at = props.created_at
        self.updated_at = props.updated_at
        self.deleted_at = props.deleted_at

    @staticmethod
    def create(props: CreateUserProps):
        return User(
            UserProps(
                id=uuid6.uuid7(),
                name=props.name,
                email=props.email,
                role=props.role,
                password=HashService().hash(props.password),
                created_at=date.today(),
            )
        )

    @staticmethod
    def restore(props: UserProps):
        return User(
            UserProps(
                id=props.id,
                name=props.name,
                email=props.email,
                role=props.role,
                password=props.password,
                created_at=props.created_at,
                updated_at=props.updated_at,
                deleted_at=props.deleted_at,
            )
        )
