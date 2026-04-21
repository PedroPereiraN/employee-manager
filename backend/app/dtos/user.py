from uuid import UUID
from pydantic import BaseModel

from app.enums.user_role import UserRole


class CreateUserInput(BaseModel):
    name: str
    password: str
    email: str
    role: UserRole


class CreateUserOutput(BaseModel):
    id: UUID
    name: str
    email: str
    role: str
