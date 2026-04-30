from app.dtos.service_types import ListServiceTypeInputDto, OutputServiceTypeDto
from app.mappers.service_type_mapper import ServiceTypeMapper
from app.protocols.usecase import UseCase
from app.repositories.service_type_repository import ServiceTypeRepository


class ListServiceTypeUsecase(UseCase[ListServiceTypeInputDto, OutputServiceTypeDto]):
    def __init__(self, service_type_repository: ServiceTypeRepository) -> None:
        self.service_type_repository = service_type_repository

    def execute(self, input: ListServiceTypeInputDto) -> OutputServiceTypeDto:

        output = self.service_type_repository.find_by_id(id=input.id)

        service_type = ServiceTypeMapper.entity_to_output(entity=output)

        return service_type
