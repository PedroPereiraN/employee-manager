from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dtos.paginated_response import PaginatedResponseDto
from app.dtos.positions import (
    CreatePositionInputDto,
    CreatePositionOutputDto,
    DeletePositionInputDto,
    ListPaginatedPositionsInputDto,
    ListPositionInputDto,
    OutputPositionDto,
    UpdatePositionInputDto,
    UpdatePositionOutputDto,
)
from app.usecases.positions.create_position_usecase import CreatePositionUsecase

from app.middleware.get_token import get_token
from app.middleware.get_db import get_db
from app.repositories.position_repository import PositionRepository
from app.usecases.positions.delete_position_usecase import DeletePositionUsecase
from app.usecases.positions.list_paginated_positions_usecase import (
    ListPaginatedPositionsUsecase,
)
from app.usecases.positions.list_position_usecase import ListPositionUsecase
from app.usecases.positions.update_position_usecase import UpdatePositionUsecase
from app.usecases.positions.delete_position_usecase import DeletePositionUsecase

position_router = APIRouter(prefix="/positions", tags=["positions"])


@position_router.post("/", status_code=200, response_model=CreatePositionOutputDto)
async def create_position(
    body: CreatePositionInputDto,
    db: Session = Depends(get_db),
    _: str = Depends(get_token),
):
    position_repository = PositionRepository(db=db)

    return CreatePositionUsecase(position_repository=position_repository).execute(body)


@position_router.get(
    "/", status_code=200, response_model=PaginatedResponseDto[OutputPositionDto]
)
async def list_paginated_positions(
    page: int = 1,
    size: int = 10,
    filter: Optional[str] = None,
    db: Session = Depends(get_db),
    _: str = Depends(get_token),
):
    position_repository = PositionRepository(db=db)

    input = ListPaginatedPositionsInputDto(page=page, size=size, filter=filter)

    return ListPaginatedPositionsUsecase(
        position_repository=position_repository
    ).execute(input)


@position_router.get("/{id}", status_code=200, response_model=OutputPositionDto)
async def list_position(
    id: UUID,
    db: Session = Depends(get_db),
    _: str = Depends(get_token),
):
    position_repository = PositionRepository(db=db)

    input = ListPositionInputDto(id=id)

    return ListPositionUsecase(position_repository=position_repository).execute(input)


@position_router.put("/", status_code=200, response_model=UpdatePositionOutputDto)
async def update_position(
    body: UpdatePositionInputDto,
    db: Session = Depends(get_db),
    _: str = Depends(get_token),
):
    position_repository = PositionRepository(db=db)

    return UpdatePositionUsecase(position_repository=position_repository).execute(body)


@position_router.delete("/", status_code=204, response_model=None)
async def delete_position(
    id: UUID,
    db: Session = Depends(get_db),
    _: str = Depends(get_token),
):
    position_repository = PositionRepository(db=db)

    return DeletePositionUsecase(position_repository=position_repository).execute(
        DeletePositionInputDto(id=id)
    )
