from app.dtos.positions import ListPositionInputDto, OutputPositionDto
from app.mappers.position_mapper import PositionMapper
from app.protocols.usecase import UseCase
from app.repositories.position_repository import PositionRepository


class ListPositionUsecase(UseCase[ListPositionInputDto, OutputPositionDto]):
    def __init__(self, position_repository: PositionRepository) -> None:
        self.position_repository = position_repository

    def execute(self, input: ListPositionInputDto) -> OutputPositionDto:

        output = self.position_repository.find_by_id(id=input.id)

        position = PositionMapper.entity_to_output(entity=output)

        return position
