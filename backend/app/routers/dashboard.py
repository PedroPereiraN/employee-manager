from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.middleware.get_token import get_token
from app.middleware.get_db import get_db
from app.dtos.dashboard import EmployeeHoursRankingInputDto, EmployeeHoursRankingOutputDto
from app.repositories.service_order_repository import ServiceOrderRepository
from app.usecases.dashboard.get_employee_hours_ranking_usecase import GetEmployeeHoursRankingUsecase

dashboard_router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@dashboard_router.get(
    "/employee_hours_ranking",
    status_code=200,
    response_model=EmployeeHoursRankingOutputDto,
)
async def get_employee_hours_ranking(
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    limit: Optional[int] = 10,
    db: Session = Depends(get_db),
    _: str = Depends(get_token),
):
    return GetEmployeeHoursRankingUsecase(
        service_order_repository=ServiceOrderRepository(db=db)
    ).execute(EmployeeHoursRankingInputDto(from_date=from_date, to_date=to_date, limit=limit))
