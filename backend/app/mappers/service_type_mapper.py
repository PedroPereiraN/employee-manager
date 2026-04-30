from app.dtos.service_types import OutputServiceTypeDto
from app.entities.service_type import ServiceType, ServiceTypeProps
from app.models.service_type import ServiceTypeModel


class ServiceTypeMapper:
    @staticmethod
    def to_model(entity: ServiceType) -> ServiceTypeModel:
        return ServiceTypeModel(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            deleted_at=entity.deleted_at,
        )

    @staticmethod
    def model_to_entity(model: ServiceTypeModel) -> ServiceType:
        return ServiceType(
            props=ServiceTypeProps(
                id=model.id,
                name=model.name,
                description=model.description,
                created_at=model.created_at,
                updated_at=model.updated_at,
                deleted_at=model.deleted_at,
            )
        )

    @staticmethod
    def model_to_output(model: ServiceTypeModel) -> OutputServiceTypeDto:
        return OutputServiceTypeDto(
            id=model.id,
            name=model.name,
            description=model.description,
            created_at=model.created_at,
            updated_at=model.updated_at,
            deleted_at=model.deleted_at,
        )

    @staticmethod
    def entity_to_output(entity: ServiceType) -> OutputServiceTypeDto:
        return OutputServiceTypeDto(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            deleted_at=entity.deleted_at,
        )
