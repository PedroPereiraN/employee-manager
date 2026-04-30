from app.dtos.service_types import CreateServiceTypeInputDto, CreateServiceTypeOutputDto
from app.entities.service_type import CreateServiceTypeProps, ServiceType
from app.protocols.usecase import UseCase
from app.repositories.service_type_repository import ServiceTypeRepository


class CreateServiceTypeUsecase(
    UseCase[CreateServiceTypeInputDto, CreateServiceTypeOutputDto]
):
    def __init__(self, service_type_repository: ServiceTypeRepository) -> None:
        self.service_type_repository = service_type_repository

    def execute(self, input: CreateServiceTypeInputDto) -> CreateServiceTypeOutputDto:
        service_type = ServiceType.create(
            props=CreateServiceTypeProps(name=input.name, description=input.description)
        )

        self.service_type_repository.create(entity=service_type)

        return CreateServiceTypeOutputDto(
            id=service_type.id,
            name=service_type.name,
            description=service_type.description,
            created_at=service_type.created_at,
        )
