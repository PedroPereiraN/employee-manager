from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dtos.paginated_response import PaginatedResponseDto
from app.dtos.service_orders import (
    CreateServiceOrderInputDto,
    CreateServiceOrderOutputDto,
    ListPaginatedServiceOrdersInputDto,
    OutputServiceOrderDto,
)
from app.usecases.service_orders.create_service_order_usecase import (
    CreateServiceOrderUsecase,
)

from app.middleware.get_token import get_token
from app.middleware.get_db import get_db
from app.repositories.service_order_repository import ServiceOrderRepository
from app.usecases.service_orders.list_paginated_service_orders_usecase import (
    ListPaginatedServiceOrdersUsecase,
)

service_order_router = APIRouter(prefix="/service_orders", tags=["service_orders"])


@service_order_router.post(
    "/", status_code=200, response_model=CreateServiceOrderOutputDto
)
async def create_service_order(
    body: CreateServiceOrderInputDto,
    db: Session = Depends(get_db),
    _: str = Depends(get_token),
):
    service_order_repository = ServiceOrderRepository(db=db)

    return CreateServiceOrderUsecase(
        service_order_repository=service_order_repository
    ).execute(body)


@service_order_router.get(
    "/", status_code=200, response_model=PaginatedResponseDto[OutputServiceOrderDto]
)
async def list_paginated_service_orders(
    page: int = 1,
    size: int = 10,
    filter: Optional[str] = None,
    db: Session = Depends(get_db),
    _: str = Depends(get_token),
):
    service_order_repository = ServiceOrderRepository(db=db)

    input = ListPaginatedServiceOrdersInputDto(page=page, size=size, filter=filter)

    return ListPaginatedServiceOrdersUsecase(
        service_order_repository=service_order_repository
    ).execute(input)
