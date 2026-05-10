from typing import List, Optional
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload
from app.dtos.paginated_response import PaginatedResponseDto
from app.dtos.service_orders import OutputServiceOrderDto
from app.entities.service_order import (
    ServiceOrder,
    ServiceOrderStatusHistoryProps,
    WorkSessionHistoryProps,
    WorkSessionProps,
)
from app.enums.service_order_status import ServiceOrderStatus
from app.mappers.employee_mapper import EmployeeMapper
from app.mappers.position_mapper import PositionMapper
from app.mappers.service_order_mapper import ServiceOrderMapper
from app.mappers.service_type_mapper import ServiceTypeMapper
from math import ceil
from sqlalchemy import func
from datetime import datetime

from app.models.employee import EmployeeModel
from app.models.service_order import (
    ServiceOrderModel,
    ServiceOrderStatusHistoryModel,
    WorkSessionHistoryModel,
    WorkSessionModel,
)


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

    def find_by_id(self, id: UUID) -> ServiceOrder:
        service_order_model = (
            self.db.query(ServiceOrderModel)
            .options(
                joinedload(ServiceOrderModel.work_sessions).joinedload(
                    WorkSessionModel.histories
                ),
            )
            .filter(ServiceOrderModel.id == id, ServiceOrderModel.deleted_at.is_(None))
            .first()
        )

        if not service_order_model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service order not found",
            )

        return ServiceOrderMapper.model_to_entity(model=service_order_model)

    def delete(self, id: UUID) -> None:
        try:
            service_order_model = (
                self.db.query(ServiceOrderModel)
                .filter(ServiceOrderModel.id == id)
                .first()
            )
            if not service_order_model:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Service order not found",
                )
            service_order_model.deleted_at = datetime.now()
            self.db.commit()
        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Integrity error: {e}",
            )

    def report_progress(
        self,
        service_order_id: UUID,
        new_work_sessions: List[WorkSessionProps],
        new_histories: List[WorkSessionHistoryProps],
    ) -> None:
        try:
            now = datetime.now()

            exists = (
                self.db.query(ServiceOrderModel.id)
                .filter(
                    ServiceOrderModel.id == service_order_id,
                    ServiceOrderModel.deleted_at.is_(None),
                )
                .scalar()
            )
            if not exists:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Service order not found",
                )

            if new_histories:
                ws_ids = list({h.work_session_id for h in new_histories})
                count = (
                    self.db.query(func.count(WorkSessionModel.id))
                    .filter(WorkSessionModel.id.in_(ws_ids))
                    .scalar()
                )
                if count != len(ws_ids):
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="One or more work sessions not found",
                    )
                self.db.query(WorkSessionModel).filter(
                    WorkSessionModel.id.in_(ws_ids)
                ).update({"updated_at": now}, synchronize_session=False)

            self.db.query(ServiceOrderModel).filter(
                ServiceOrderModel.id == service_order_id
            ).update({"updated_at": now}, synchronize_session=False)

            if new_work_sessions:
                self.db.add_all(
                    [
                        WorkSessionModel(
                            id=ws.id,
                            service_order_id=ws.service_order_id,
                            employee_id=ws.employee_id,
                            created_at=ws.created_at,
                        )
                        for ws in new_work_sessions
                    ]
                )
                self.db.flush()
                self.db.add_all(
                    [
                        WorkSessionHistoryModel(
                            id=h.id,
                            work_session_id=h.work_session_id,
                            status=h.status,
                            observations=h.observations,
                            occurred_at=h.occurred_at,
                            created_at=h.created_at,
                        )
                        for ws in new_work_sessions
                        for h in ws.histories
                    ]
                )

            if new_histories:
                self.db.add_all(
                    [
                        WorkSessionHistoryModel(
                            id=h.id,
                            work_session_id=h.work_session_id,
                            status=h.status,
                            observations=h.observations,
                            occurred_at=h.occurred_at,
                            created_at=h.created_at,
                        )
                        for h in new_histories
                    ]
                )

            self.db.commit()
        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Integrity error: {e}",
            )

    def change_service_order_status(
        self,
        service_order_status: ServiceOrderStatus,
        status_history: ServiceOrderStatusHistoryProps,
    ):
        try:
            service_order_model = (
                self.db.query(ServiceOrderModel)
                .filter(
                    ServiceOrderModel.id == status_history.service_order_id,
                    ServiceOrderModel.deleted_at.is_(None),
                )
                .first()
            )

            if not service_order_model:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Service order not found",
                )

            service_order_model.updated_at = datetime.now()
            service_order_model.status = service_order_status

            status_history_model = ServiceOrderStatusHistoryModel(
                id=status_history.id,
                reason=status_history.reason,
                status=status_history.status,
                created_at=status_history.created_at,
                service_order_id=status_history.service_order_id,
            )

            self.db.add(status_history_model)
            self.db.commit()

        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Integrity error: {e}",
            )
