from datetime import date
from typing import Optional
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from math import ceil
from app.dtos.employees import OutputEmployeeDto
from app.dtos.paginated_response import PaginatedResponseDto
from app.entities.employee import Employee
from app.mappers.employee_mapper import EmployeeMapper
from app.models.employee import EmployeeModel
from sqlalchemy.orm import joinedload
from app.mappers.position_mapper import PositionMapper


class EmployeeRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, entity: Employee) -> None:
        employee_model = EmployeeMapper.to_model(entity=entity)
        self.db.add(employee_model)

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
    ) -> PaginatedResponseDto[OutputEmployeeDto]:
        query = (
            self.db.query(EmployeeModel)
            .options(joinedload(EmployeeModel.position))
            .filter(EmployeeModel.deleted_at.is_(None))
        )
        if filter:
            query = query.filter(
                EmployeeModel.name.ilike(f"%{filter}%"),
            )
        total = query.with_entities(func.count(EmployeeModel.id)).scalar()

        query = query.order_by(EmployeeModel.created_at.asc())

        items = query.offset((page - 1) * size).limit(size).all()

        items_output = [
            EmployeeMapper.model_to_output(
                model=item,
                position_output=PositionMapper.model_to_output(model=item.position),
            )
            for item in items
        ]

        pages = ceil(total / size) if total > 0 else 1
        return PaginatedResponseDto(
            total=total, page=page, size=size, pages=pages, items=items_output
        )

    def find_by_id(self, id: UUID) -> Employee:
        employee_model = (
            self.db.query(EmployeeModel)
            .filter(EmployeeModel.id == id, EmployeeModel.deleted_at.is_(None))
            .first()
        )

        if not employee_model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found",
            )

        return EmployeeMapper.model_to_entity(model=employee_model)

    def update(self, entity: Employee) -> None:
        employee_model = EmployeeMapper.to_model(entity=entity)
        try:
            self.db.merge(employee_model)
            self.db.commit()
        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Integrity error: {e}",
            )

    def delete(self, id: UUID) -> None:
        try:
            employee_model = (
                self.db.query(EmployeeModel).filter(EmployeeModel.id == id).first()
            )
            if not employee_model:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Employee not found",
                )
            employee_model.deleted_at = date.today()
            self.db.commit()
        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Integrity error: {e}",
            )
