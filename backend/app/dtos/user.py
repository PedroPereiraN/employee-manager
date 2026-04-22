from datetime import date
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel
from app.enums.user_role import UserRole


class CreateUserInput(BaseModel):
    name: str
    password: str
    email: str
    role: UserRole


class CreateUserOutput(BaseModel):
    id: UUID
    name: str
    email: str
    role: str


class ListPaginatedUsersInput(BaseModel):
    page: int
    size: int
    filter: Optional[str] = None
    filter_role: Optional[UserRole] = None


class OutputUserDto(BaseModel):
    id: UUID
    name: str
    email: str
    role: UserRole
    created_at: date
    updated_at: Optional[date] = None
    deleted_at: Optional[date] = None


class ListUserInput(BaseModel):
    id: UUID


class UpdateUserInput(BaseModel):
    id: UUID
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[UserRole] = None


class UpdateUserOutput(BaseModel):
    id: UUID
    name: str
    email: str
    role: str


class DeleteUserInput(BaseModel):
    id: UUID
