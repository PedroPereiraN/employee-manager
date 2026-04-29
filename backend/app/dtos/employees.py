from datetime import date
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

from app.enums.employee_status import EmployeeStatus
from app.enums.employee_type import EmployeeType
from app.enums.payment_method import PaymentMethod
from app.dtos.positions import OutputPositionDto


class OutputEmployeeDto(BaseModel):
    id: UUID
    name: str
    birthday: Optional[date] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    admission_date: Optional[date] = None
    status: EmployeeStatus
    type: EmployeeType
    payment_method: PaymentMethod
    payment_value: float
    hourly_rate: Optional[float] = None
    hourly_bonus: Optional[float] = None
    observations: Optional[str] = None
    position: OutputPositionDto
    created_at: date
    updated_at: Optional[date] = None
    deleted_at: Optional[date] = None


class CreateEmployeeInputDto(BaseModel):
    name: str
    birthday: Optional[date] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    admission_date: Optional[date] = None
    status: EmployeeStatus
    type: EmployeeType
    payment_method: PaymentMethod
    payment_value: float
    hourly_rate: Optional[float] = None
    hourly_bonus: Optional[float] = None
    observations: Optional[str] = None
    position_id: UUID


class CreateEmployeeOutputDto(BaseModel):
    id: UUID
    name: str
    birthday: Optional[date] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    admission_date: Optional[date] = None
    status: EmployeeStatus
    type: EmployeeType
    payment_method: PaymentMethod
    payment_value: float
    hourly_rate: Optional[float] = None
    hourly_bonus: Optional[float] = None
    observations: Optional[str] = None
    position_id: UUID
    created_at: date


class DeleteEmployeeInputDto(BaseModel):
    id: UUID


class ListPaginatedEmployeesInputDto(BaseModel):
    page: int
    size: int
    filter: Optional[str] = None


class ListEmployeeInputDto(BaseModel):
    id: UUID


class UpdateEmployeeInputDto(BaseModel):
    id: UUID
    name: Optional[str] = None
    birthday: Optional[date] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    admission_date: Optional[date] = None
    status: Optional[EmployeeStatus] = None
    type: Optional[EmployeeType] = None
    payment_method: Optional[PaymentMethod] = None
    payment_value: Optional[float] = None
    hourly_rate: Optional[float] = None
    hourly_bonus: Optional[float] = None
    observations: Optional[str] = None
    position_id: Optional[UUID] = None


class UpdateEmployeeOutputDto(BaseModel):
    id: UUID
    name: str
    birthday: Optional[date] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    admission_date: Optional[date] = None
    status: EmployeeStatus
    type: EmployeeType
    payment_method: PaymentMethod
    payment_value: float
    hourly_rate: Optional[float] = None
    hourly_bonus: Optional[float] = None
    observations: Optional[str] = None
    position_id: UUID
    created_at: date
    updated_at: date
