from datetime import datetime
from typing import Optional
from pydantic import BaseModel
import uuid6
from uuid import UUID


class CreateServiceTypeProps(BaseModel):
    name: str
    description: Optional[str] = None


class ServiceTypeProps(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None


class ServiceType:
    id: UUID
    name: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    def __init__(self, props: ServiceTypeProps):
        self.id = props.id
        self.name = props.name
        self.description = props.description
        self.created_at = props.created_at
        self.updated_at = props.updated_at
        self.deleted_at = props.deleted_at

    @staticmethod
    def create(props: CreateServiceTypeProps):
        return ServiceType(
            ServiceTypeProps(
                id=uuid6.uuid7(),
                name=props.name,
                description=props.description,
                created_at=datetime.now(),
            )
        )

    @staticmethod
    def restore(props: ServiceTypeProps):
        return ServiceType(
            ServiceTypeProps(
                id=props.id,
                name=props.name,
                description=props.description,
                created_at=props.created_at,
                updated_at=props.updated_at,
                deleted_at=props.deleted_at,
            )
        )
