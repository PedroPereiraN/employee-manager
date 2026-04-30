from datetime import date
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class CreateServiceTypeInputDto(BaseModel):
    name: str
    description: Optional[str] = None


class CreateServiceTypeOutputDto(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    created_at: date


class DeleteServiceTypeInputDto(BaseModel):
    id: UUID


class ListPaginatedServiceTypesInputDto(BaseModel):
    filter: Optional[str] = None
    page: int
    size: int


class ListServiceTypeInputDto(BaseModel):
    id: UUID


class UpdateServiceTypeInputDto(BaseModel):
    id: UUID
    name: Optional[str] = None
    description: Optional[str] = None


class UpdateServiceTypeOutputDto(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    created_at: date
    updated_at: date


class OutputServiceTypeDto(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    created_at: date
    updated_at: Optional[date] = None
    deleted_at: Optional[date] = None
