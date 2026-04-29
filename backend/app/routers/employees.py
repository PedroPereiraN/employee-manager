from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dtos.paginated_response import PaginatedResponseDto

from app.middleware.get_token import get_token
from app.middleware.get_db import get_db
from app.dtos.employees import (
    CreateEmployeeInputDto,
    CreateEmployeeOutputDto,
    DeleteEmployeeInputDto,
    ListEmployeeInputDto,
    ListPaginatedEmployeesInputDto,
    OutputEmployeeDto,
    UpdateEmployeeInputDto,
    UpdateEmployeeOutputDto,
)
from app.repositories.employee_repository import EmployeeRepository
from app.repositories.position_repository import PositionRepository
from app.usecases.employees.create_employee_usecase import CreateEmployeeUsecase
from app.usecases.employees.list_employee_usecase import ListEmployeeUsecase
from app.usecases.employees.list_paginated_employees_usecase import (
    ListPaginatedEmployeesUsecase,
)
from app.usecases.employees.update_employee_usecase import UpdateEmployeeUsecase
from app.usecases.employees.delete_employee_usecase import DeleteEmployeeUsecase

employee_router = APIRouter(prefix="/employee", tags=["employees"])


@employee_router.post("/", status_code=200, response_model=CreateEmployeeOutputDto)
async def create_employee(
    body: CreateEmployeeInputDto,
    db: Session = Depends(get_db),
    _: str = Depends(get_token),
):
    employee_repository = EmployeeRepository(db=db)
    position_repository = PositionRepository(db=db)

    return CreateEmployeeUsecase(
        employee_repository=employee_repository, position_repository=position_repository
    ).execute(body)


@employee_router.get(
    "/", status_code=200, response_model=PaginatedResponseDto[OutputEmployeeDto]
)
async def list_paginated_employees(
    page: int = 1,
    size: int = 10,
    filter: Optional[str] = None,
    db: Session = Depends(get_db),
    _: str = Depends(get_token),
):
    employee_repository = EmployeeRepository(db=db)

    input = ListPaginatedEmployeesInputDto(page=page, size=size, filter=filter)

    return ListPaginatedEmployeesUsecase(
        employee_repository=employee_repository
    ).execute(input)


@employee_router.get("/{id}", status_code=200, response_model=OutputEmployeeDto)
async def list_employee(
    id: UUID,
    db: Session = Depends(get_db),
    _: str = Depends(get_token),
):
    employee_repository = EmployeeRepository(db=db)
    position_repository = PositionRepository(db=db)

    input = ListEmployeeInputDto(id=id)

    return ListEmployeeUsecase(
        employee_repository=employee_repository, position_repository=position_repository
    ).execute(input)


@employee_router.put("/", status_code=200, response_model=UpdateEmployeeOutputDto)
async def update_employee(
    body: UpdateEmployeeInputDto,
    db: Session = Depends(get_db),
    _: str = Depends(get_token),
):
    employee_repository = EmployeeRepository(db=db)
    position_repository = PositionRepository(db=db)

    return UpdateEmployeeUsecase(
        employee_repository=employee_repository, position_repository=position_repository
    ).execute(body)


@employee_router.delete("/", status_code=204, response_model=None)
async def delete_employee(
    id: UUID,
    db: Session = Depends(get_db),
    _: str = Depends(get_token),
):
    employee_repository = EmployeeRepository(db=db)

    return DeleteEmployeeUsecase(employee_repository=employee_repository).execute(
        DeleteEmployeeInputDto(id=id)
    )
