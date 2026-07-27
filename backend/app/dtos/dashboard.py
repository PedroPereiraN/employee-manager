from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel


class EmployeeHoursRankingInputDto(BaseModel):
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None
    limit: Optional[int] = 10


class EmployeeHoursRankingItemDto(BaseModel):
    employee_id: UUID
    name: str
    total_hours: float
    session_count: int


class EmployeeHoursRankingOutputDto(BaseModel):
    total: int
    items: List[EmployeeHoursRankingItemDto]
