from app.dtos.service_orders import DeleteServiceOrderInputDto
from app.protocols.usecase import UseCase
from app.repositories.service_order_repository import ServiceOrderRepository
from fastapi import HTTPException, status


class DeleteServiceOrderUsecase(UseCase[DeleteServiceOrderInputDto, None]):
    def __init__(self, service_order_repository: ServiceOrderRepository) -> None:
        self.service_order_repository = service_order_repository

    def execute(self, input: DeleteServiceOrderInputDto) -> None:
        service_order = self.service_order_repository.find_by_id(id=input.id)

        if service_order.status != "not_started":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Deletion is only allowed for orders with 'Not Started' status.",
            )

        self.service_order_repository.delete(id=input.id)
