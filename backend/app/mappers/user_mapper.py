from app.entities.user import User
from app.models.user import UserModel


class UserMapper:
    @staticmethod
    def to_model(entity: User) -> UserModel:
        return UserModel(
            id=entity.id,
            name=entity.name,
            password=entity.password,
            email=entity.email,
            role=entity.role,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            deleted_at=entity.deleted_at,
        )
