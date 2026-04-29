from datetime import date
from typing import Optional
from pydantic import BaseModel
import uuid6
from uuid import UUID

from app.enums.employee_status import EmployeeStatus
from app.enums.employee_type import EmployeeType
from app.enums.payment_method import PaymentMethod


class CreateEmployeeProps(BaseModel):
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


class EmployeeProps(BaseModel):
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
    updated_at: Optional[date] = None
    deleted_at: Optional[date] = None


class Employee:
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
    updated_at: Optional[date] = None
    deleted_at: Optional[date] = None

    def __init__(self, props: EmployeeProps):
        self.id = props.id
        self.name = props.name
        self.email = props.email
        self.birthday = props.birthday
        self.phone = props.phone
        self.admission_date = props.admission_date
        self.status = props.status
        self.type = props.type
        self.payment_method = props.payment_method
        self.payment_value = props.payment_value
        self.hourly_rate = props.hourly_rate
        self.hourly_bonus = props.hourly_bonus
        self.observations = props.observations
        self.position_id = props.position_id
        self.created_at = props.created_at
        self.updated_at = props.updated_at
        self.deleted_at = props.deleted_at

    @staticmethod
    def create(props: CreateEmployeeProps):
        return Employee(
            EmployeeProps(
                id=uuid6.uuid7(),
                name=props.name,
                email=props.email,
                birthday=props.birthday,
                phone=props.phone,
                admission_date=props.admission_date,
                status=props.status,
                type=props.type,
                payment_method=props.payment_method,
                payment_value=props.payment_value,
                hourly_rate=props.hourly_rate,
                hourly_bonus=props.hourly_bonus,
                observations=props.observations,
                position_id=props.position_id,
                created_at=date.today(),
            )
        )

    @staticmethod
    def restore(props: EmployeeProps):
        return Employee(
            EmployeeProps(
                id=props.id,
                name=props.name,
                email=props.email,
                birthday=props.birthday,
                phone=props.phone,
                admission_date=props.admission_date,
                status=props.status,
                type=props.type,
                payment_method=props.payment_method,
                payment_value=props.payment_value,
                hourly_rate=props.hourly_rate,
                hourly_bonus=props.hourly_bonus,
                observations=props.observations,
                position_id=props.position_id,
                created_at=props.created_at,
                updated_at=props.updated_at,
                deleted_at=props.deleted_at,
            )
        )
