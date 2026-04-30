from datetime import date
from app.dtos.service_types import UpdateServiceTypeInputDto, UpdateServiceTypeOutputDto
from app.entities.service_type import ServiceType, ServiceTypeProps
from app.protocols.usecase import UseCase
from app.repositories.service_type_repository import ServiceTypeRepository


class UpdateServiceTypeUsecase(
    UseCase[UpdateServiceTypeInputDto, UpdateServiceTypeOutputDto]
):
    def __init__(self, service_type_repository: ServiceTypeRepository) -> None:
        self.service_type_repository = service_type_repository

    def execute(self, input: UpdateServiceTypeInputDto) -> UpdateServiceTypeOutputDto:
        find_service_type = self.service_type_repository.find_by_id(id=input.id)

        service_type = ServiceType.restore(
            props=ServiceTypeProps(
                id=input.id,
                name=input.name if input.name else find_service_type.name,
                description=(
                    input.description
                    if input.description
                    else find_service_type.description
                ),
                created_at=find_service_type.created_at,
                updated_at=date.today(),
                deleted_at=None,
            )
        )

        self.service_type_repository.update(entity=service_type)

        return UpdateServiceTypeOutputDto(
            id=service_type.id,
            name=service_type.name,
            description=service_type.description,
            created_at=service_type.created_at,
            updated_at=(
                service_type.updated_at if service_type.updated_at else date.today()
            ),
        )
