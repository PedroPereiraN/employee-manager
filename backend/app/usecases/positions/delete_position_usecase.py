from app.dtos.positions import DeletePositionInputDto
from app.protocols.usecase import UseCase
from app.repositories.position_repository import PositionRepository


class DeletePositionUsecase(UseCase[DeletePositionInputDto, None]):
    def __init__(self, position_repository: PositionRepository) -> None:
        self.position_repository = position_repository

    def execute(self, input: DeletePositionInputDto) -> None:
        self.position_repository.delete(id=input.id)
