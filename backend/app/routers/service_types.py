from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dtos.paginated_response import PaginatedResponseDto
from app.dtos.service_types import (
    CreateServiceTypeInputDto,
    CreateServiceTypeOutputDto,
    DeleteServiceTypeInputDto,
    ListPaginatedServiceTypesInputDto,
    ListServiceTypeInputDto,
    OutputServiceTypeDto,
    UpdateServiceTypeInputDto,
    UpdateServiceTypeOutputDto,
)
from app.usecases.service_types.create_service_type_usecase import (
    CreateServiceTypeUsecase,
)

from app.middleware.get_token import get_token
from app.middleware.get_db import get_db
from app.repositories.service_type_repository import ServiceTypeRepository
from app.usecases.service_types.delete_service_type_usecase import (
    DeleteServiceTypeUsecase,
)
from app.usecases.service_types.list_paginated_service_types_usecase import (
    ListPaginatedServiceTypesUsecase,
)
from app.usecases.service_types.list_service_type_usecase import ListServiceTypeUsecase
from app.usecases.service_types.update_service_type_usecase import (
    UpdateServiceTypeUsecase,
)
from app.usecases.service_types.delete_service_type_usecase import (
    DeleteServiceTypeUsecase,
)

service_type_router = APIRouter(prefix="/service_types", tags=["service_types"])


@service_type_router.post(
    "/", status_code=200, response_model=CreateServiceTypeOutputDto
)
async def create_service_type(
    body: CreateServiceTypeInputDto,
    db: Session = Depends(get_db),
    _: str = Depends(get_token),
):
    service_type_repository = ServiceTypeRepository(db=db)

    return CreateServiceTypeUsecase(
        service_type_repository=service_type_repository
    ).execute(body)


@service_type_router.get(
    "/", status_code=200, response_model=PaginatedResponseDto[OutputServiceTypeDto]
)
async def list_paginated_service_types(
    page: int = 1,
    size: int = 10,
    filter: Optional[str] = None,
    db: Session = Depends(get_db),
    _: str = Depends(get_token),
):
    service_type_repository = ServiceTypeRepository(db=db)

    input = ListPaginatedServiceTypesInputDto(page=page, size=size, filter=filter)

    return ListPaginatedServiceTypesUsecase(
        service_type_repository=service_type_repository
    ).execute(input)


@service_type_router.get("/{id}", status_code=200, response_model=OutputServiceTypeDto)
async def list_service_type(
    id: UUID,
    db: Session = Depends(get_db),
    _: str = Depends(get_token),
):
    service_type_repository = ServiceTypeRepository(db=db)

    input = ListServiceTypeInputDto(id=id)

    return ListServiceTypeUsecase(
        service_type_repository=service_type_repository
    ).execute(input)


@service_type_router.put(
    "/", status_code=200, response_model=UpdateServiceTypeOutputDto
)
async def update_service_type(
    body: UpdateServiceTypeInputDto,
    db: Session = Depends(get_db),
    _: str = Depends(get_token),
):
    service_type_repository = ServiceTypeRepository(db=db)

    return UpdateServiceTypeUsecase(
        service_type_repository=service_type_repository
    ).execute(body)


@service_type_router.delete("/", status_code=204, response_model=None)
async def delete_service_type(
    id: UUID,
    db: Session = Depends(get_db),
    _: str = Depends(get_token),
):
    service_type_repository = ServiceTypeRepository(db=db)

    return DeleteServiceTypeUsecase(
        service_type_repository=service_type_repository
    ).execute(DeleteServiceTypeInputDto(id=id))
