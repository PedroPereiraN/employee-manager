from datetime import date
from app.dtos.positions import UpdatePositionInputDto, UpdatePositionOutputDto
from app.entities.position import Position, PositionProps
from app.protocols.usecase import UseCase
from app.repositories.position_repository import PositionRepository


class UpdatePositionUsecase(UseCase[UpdatePositionInputDto, UpdatePositionOutputDto]):
    def __init__(self, position_repository: PositionRepository) -> None:
        self.position_repository = position_repository

    def execute(self, input: UpdatePositionInputDto) -> UpdatePositionOutputDto:
        find_position = self.position_repository.find_by_id(id=input.id)

        position = Position.restore(
            props=PositionProps(
                id=input.id,
                name=input.name if input.name else find_position.name,
                created_at=find_position.created_at,
                updated_at=date.today(),
                deleted_at=None,
            )
        )

        self.position_repository.update(entity=position)

        return UpdatePositionOutputDto(id=position.id, name=position.name)
