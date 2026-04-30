from app.dtos.service_types import DeleteServiceTypeInputDto
from app.protocols.usecase import UseCase
from app.repositories.service_type_repository import ServiceTypeRepository


class DeleteServiceTypeUsecase(UseCase[DeleteServiceTypeInputDto, None]):
    def __init__(self, service_type_repository: ServiceTypeRepository) -> None:
        self.service_type_repository = service_type_repository

    def execute(self, input: DeleteServiceTypeInputDto) -> None:
        self.service_type_repository.delete(id=input.id)
