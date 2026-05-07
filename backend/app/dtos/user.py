from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from app.enums.user_role import UserRole


class CreateUserInputDto(BaseModel):
    name: str
    password: str
    email: str
    role: UserRole


class CreateUserOutputDto(BaseModel):
    id: UUID
    name: str
    email: str
    role: str
    created_at: datetime


class ListPaginatedUsersInputDto(BaseModel):
    page: int
    size: int
    filter: Optional[str] = None
    filter_role: Optional[UserRole] = None


class OutputUserDto(BaseModel):
    id: UUID
    name: str
    email: str
    role: UserRole
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None


class ListUserInputDto(BaseModel):
    id: UUID


class UpdateUserInputDto(BaseModel):
    id: UUID
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[UserRole] = None


class UpdateUserOutputDto(BaseModel):
    id: UUID
    name: str
    email: str
    role: str
    created_at: datetime
    updated_at: datetime


class DeleteUserInputDto(BaseModel):
    id: UUID


class UpdateUserPasswordInputDto(BaseModel):
    id: UUID
    new_password: str
