from datetime import date
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class CreatePositionInputDto(BaseModel):
    name: str


class CreatePositionOutputDto(BaseModel):
    id: UUID
    name: str


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
    name: str


class UpdatePositionOutputDto(BaseModel):
    id: UUID
    name: str


class OutputPositionDto(BaseModel):
    id: UUID
    name: str
    created_at: date
    updated_at: Optional[date] = None
    deleted_at: Optional[date] = None
