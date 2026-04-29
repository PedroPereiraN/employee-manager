from app.dtos.positions import CreatePositionInputDto, CreatePositionOutputDto
from app.entities.position import CreatePositionProps, Position
from app.protocols.usecase import UseCase
from app.repositories.position_repository import PositionRepository


class CreatePositionUsecase(UseCase[CreatePositionInputDto, CreatePositionOutputDto]):
    def __init__(self, position_repository: PositionRepository) -> None:
        self.position_repository = position_repository

    def execute(self, input: CreatePositionInputDto) -> CreatePositionOutputDto:
        position = Position.create(
            props=CreatePositionProps(
                name=input.name,
            )
        )

        self.position_repository.create(entity=position)

        return CreatePositionOutputDto(
            id=position.id, name=position.name, created_at=position.created_at
        )
