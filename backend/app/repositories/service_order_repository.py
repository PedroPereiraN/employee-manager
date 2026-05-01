from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload
from app.dtos.paginated_response import PaginatedResponseDto
from app.dtos.service_orders import OutputServiceOrderDto
from app.entities.service_order import ServiceOrder
from app.mappers.employee_mapper import EmployeeMapper
from app.mappers.position_mapper import PositionMapper
from app.mappers.service_order_mapper import ServiceOrderMapper
from app.mappers.service_type_mapper import ServiceTypeMapper
from math import ceil
from sqlalchemy import func

from app.models.employee import EmployeeModel
from app.models.service_order import ServiceOrderModel, WorkSessionModel


class ServiceOrderRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def generate_order_number(self) -> str:
        last = (
            self.db.query(ServiceOrderModel.order_number)
            .order_by(ServiceOrderModel.created_at.desc())
            .first()
        )
        if last is None:
            next_number = 1
        else:
            current = int(last[0].replace("OS", ""))
            next_number = current + 1
        return f"{next_number:04d}OS"

    def create(self, entity: ServiceOrder) -> None:
        service_order_model = ServiceOrderMapper.to_model(entity=entity)
        self.db.add(service_order_model)
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
    ) -> PaginatedResponseDto[OutputServiceOrderDto]:
        query = (
            self.db.query(ServiceOrderModel)
            .options(
                joinedload(ServiceOrderModel.service_type),
                joinedload(ServiceOrderModel.work_sessions).joinedload(
                    WorkSessionModel.histories
                ),
            )
            .filter(ServiceOrderModel.deleted_at.is_(None))
        )
        if filter:
            query = query.filter(
                ServiceOrderModel.order_number.ilike(f"%{filter}%"),
            )
        total = (
            self.db.query(func.count(ServiceOrderModel.id))
            .filter(ServiceOrderModel.deleted_at.is_(None))
            .scalar()
        )
        query = query.order_by(ServiceOrderModel.created_at.asc())
        items = query.offset((page - 1) * size).limit(size).all()

        employee_ids = {ws.employee_id for item in items for ws in item.work_sessions}
        employees = (
            (
                self.db.query(EmployeeModel)
                .options(joinedload(EmployeeModel.position))
                .filter(EmployeeModel.id.in_(employee_ids))
                .all()
            )
            if employee_ids
            else []
        )
        employees_map = {
            e.id: EmployeeMapper.model_to_output(
                model=e,
                position_output=PositionMapper.model_to_output(model=e.position),
            )
            for e in employees
        }

        items_output = [
            ServiceOrderMapper.model_to_output(
                model=item,
                employees_output=employees_map,
                service_type_output=(
                    ServiceTypeMapper.model_to_output(model=item.service_type)
                    if item.service_type
                    else None
                ),
            )
            for item in items
        ]
        pages = ceil(total / size) if total > 0 else 1
        return PaginatedResponseDto(
            total=total, page=page, size=size, pages=pages, items=items_output
        )
