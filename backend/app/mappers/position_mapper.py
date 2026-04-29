from app.dtos.positions import OutputPositionDto
from app.dtos.user import OutputUserDto
from app.entities.position import Position, PositionProps
from app.models.position import PositionModel


class PositionMapper:
    @staticmethod
    def to_model(entity: Position) -> PositionModel:
        return PositionModel(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            deleted_at=entity.deleted_at,
        )

    @staticmethod
    def model_to_entity(model: PositionModel) -> Position:
        return Position(
            props=PositionProps(
                id=model.id,
                name=model.name,
                description=model.description,
                created_at=model.created_at,
                updated_at=model.updated_at,
                deleted_at=model.deleted_at,
            )
        )

    @staticmethod
    def model_to_output(model: PositionModel) -> OutputPositionDto:
        return OutputPositionDto(
            id=model.id,
            name=model.name,
            description=model.description,
            created_at=model.created_at,
            updated_at=model.updated_at,
            deleted_at=model.deleted_at,
        )

    @staticmethod
    def entity_to_output(entity: Position) -> OutputPositionDto:
        return OutputPositionDto(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            deleted_at=entity.deleted_at,
        )
