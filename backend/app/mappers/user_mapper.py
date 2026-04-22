from app.dtos.user import OutputUserDto
from app.entities.user import User, UserProps
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

    @staticmethod
    def model_to_entity(model: UserModel) -> User:
        return User(
            props=UserProps(
                id=model.id,
                name=model.name,
                password=model.password,
                email=model.email,
                role=model.role,
                created_at=model.created_at,
                updated_at=model.updated_at,
                deleted_at=model.deleted_at,
            )
        )

    @staticmethod
    def model_to_output(model: UserModel) -> OutputUserDto:
        return OutputUserDto(
            id=model.id,
            name=model.name,
            email=model.email,
            role=model.role,
            created_at=model.created_at,
            updated_at=model.updated_at,
            deleted_at=model.deleted_at,
        )
