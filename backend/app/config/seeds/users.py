from typing import List
from app.models.user import UserModel
from datetime import date
import uuid6
from app.services.hash_service import HashService

users: List[UserModel] = [
    UserModel(
        id=uuid6.uuid7(),
        name="default admin",
        email="admin@email.com",
        password=HashService.hash("admin@123"),
        role="admin",
        created_at=date.today(),
        updated_at=None,
        deleted_at=None,
    )
]
