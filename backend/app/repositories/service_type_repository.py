from datetime import date
from typing import Optional
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from math import ceil
from app.dtos.paginated_response import PaginatedResponseDto
from app.dtos.service_types import OutputServiceTypeDto
from app.entities.service_type import ServiceType
from app.mappers.service_type_mapper import ServiceTypeMapper
from app.models.service_type import ServiceTypeModel


class ServiceTypeRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, entity: ServiceType) -> None:
        service_type_model = ServiceTypeMapper.to_model(entity=entity)
        self.db.add(service_type_model)

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
    ) -> PaginatedResponseDto[OutputServiceTypeDto]:
        query = self.db.query(ServiceTypeModel).filter(
            ServiceTypeModel.deleted_at.is_(None)
        )

        if filter:
            query = query.filter(
                ServiceTypeModel.name.ilike(f"%{filter}%"),
            )

        total = query.with_entities(func.count(ServiceTypeModel.id)).scalar()

        query = query.order_by(ServiceTypeModel.created_at.asc())

        items = query.offset((page - 1) * size).limit(size).all()

        items_output = [ServiceTypeMapper.model_to_output(item) for item in items]

        pages = ceil(total / size) if total > 0 else 1

        return PaginatedResponseDto(
            total=total, page=page, size=size, pages=pages, items=items_output
        )

    def find_by_id(self, id: UUID) -> ServiceType:
        service_type_model = (
            self.db.query(ServiceTypeModel)
            .filter(ServiceTypeModel.id == id, ServiceTypeModel.deleted_at.is_(None))
            .first()
        )

        if not service_type_model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service type not found",
            )

        return ServiceTypeMapper.model_to_entity(model=service_type_model)

    def update(self, entity: ServiceType) -> None:
        service_type_model = ServiceTypeMapper.to_model(entity=entity)
        try:
            self.db.merge(service_type_model)
            self.db.commit()
        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Integrity error: {e}",
            )

    def delete(self, id: UUID) -> None:
        try:
            service_type_model = (
                self.db.query(ServiceTypeModel)
                .filter(ServiceTypeModel.id == id)
                .first()
            )
            if not service_type_model:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Service type not found",
                )
            service_type_model.deleted_at = date.today()
            self.db.commit()
        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Integrity error: {e}",
            )
