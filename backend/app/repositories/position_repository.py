from datetime import date
from typing import Optional
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from math import ceil
from app.dtos.paginated_response import PaginatedResponseDto
from app.dtos.positions import OutputPositionDto
from app.entities.position import Position
from app.mappers.position_mapper import PositionMapper
from app.models.position import PositionModel


class PositionRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, entity: Position) -> None:
        position_model = PositionMapper.to_model(entity=entity)
        self.db.add(position_model)

        try:
            self.db.commit()
        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Integrity error: {e}",
            )

    def list_paginated(
        self,
        page: int = 1,
        size: int = 10,
        filter: Optional[str] = None,
    ) -> PaginatedResponseDto[OutputPositionDto]:
        query = self.db.query(PositionModel).filter(PositionModel.deleted_at.is_(None))

        if filter:
            query = query.filter(
                PositionModel.name.ilike(f"%{filter}%"),
            )

        total = query.with_entities(func.count(PositionModel.id)).scalar()

        query = query.order_by(PositionModel.created_at.asc())

        items = query.offset((page - 1) * size).limit(size).all()

        items_output = [PositionMapper.model_to_output(item) for item in items]

        pages = ceil(total / size) if total > 0 else 1

        return PaginatedResponseDto(
            total=total, page=page, size=size, pages=pages, items=items_output
        )

    def find_by_id(self, id: UUID) -> Position:
        position_model = (
            self.db.query(PositionModel)
            .filter(PositionModel.id == id, PositionModel.deleted_at.is_(None))
            .first()
        )

        if not position_model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Position not found",
            )

        return PositionMapper.model_to_entity(model=position_model)

    def update(self, entity: Position) -> None:
        position_model = PositionMapper.to_model(entity=entity)
        try:
            self.db.merge(position_model)
            self.db.commit()
        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Integrity error: {e}",
            )

    def delete(self, id: UUID) -> None:
        try:
            position_model = (
                self.db.query(PositionModel).filter(PositionModel.id == id).first()
            )
            if not position_model:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Position not found",
                )
            position_model.deleted_at = date.today()
            self.db.commit()
        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Integrity error: {e}",
            )
