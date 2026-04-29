from datetime import date
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class CreatePositionInputDto(BaseModel):
    name: str
    description: Optional[str] = None


class CreatePositionOutputDto(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    created_at: date


class DeletePositionInputDto(BaseModel):
    id: UUID


class ListPaginatedPositionsInputDto(BaseModel):
    filter: Optional[str] = None
    page: int
    size: int


class ListPositionInputDto(BaseModel):
    id: UUID


class UpdatePositionInputDto(BaseModel):
    id: UUID
    name: Optional[str] = None
    description: Optional[str] = None


class UpdatePositionOutputDto(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    created_at: date
    updated_at: date


class OutputPositionDto(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    created_at: date
    updated_at: Optional[date] = None
    deleted_at: Optional[date] = None
