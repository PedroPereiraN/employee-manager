from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dtos.paginated_response import PaginatedResponse
from app.dtos.user import (
    CreateUserInput,
    CreateUserOutput,
    DeleteUserInput,
    ListPaginatedUsersInput,
    ListUserInput,
    OutputUserDto,
    UpdateUserInput,
    UpdateUserPasswordInput,
)
from app.enums.user_role import UserRole
from app.middleware.get_token import get_token
from app.middleware.get_db import get_db
from app.repositories.user_repository import UserRepository
from app.usecases.users.create_user_usecase import CreateUserUsecase
from app.usecases.users.delete_user_usecase import DeleteUserUsecase
from app.usecases.users.list_paginated_users_usecase import ListPaginatedUsersUsecase
from app.usecases.users.list_user_usecase import ListUserUsecase
from app.usecases.users.update_user_password_usecase import UpdateUserPasswordUsecase
from app.usecases.users.update_user_usecase import UpdateUserUsecase

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post("/", status_code=200, response_model=CreateUserOutput)
async def create_user(
    body: CreateUserInput,
    db: Session = Depends(get_db),
    _: str = Depends(get_token),
):
    user_repository = UserRepository(db=db)

    return CreateUserUsecase(user_repository=user_repository).execute(body)


@user_router.get("/", status_code=200, response_model=PaginatedResponse[OutputUserDto])
async def list_paginated_users(
    page: int = 1,
    size: int = 10,
    filter: Optional[str] = None,
    filter_role: Optional[UserRole] = None,
    db: Session = Depends(get_db),
    _: str = Depends(get_token),
):
    user_repository = UserRepository(db=db)

    input = ListPaginatedUsersInput(
        page=page, size=size, filter=filter, filter_role=filter_role
    )

    return ListPaginatedUsersUsecase(user_repository=user_repository).execute(input)


@user_router.get("/{id}", status_code=200, response_model=OutputUserDto)
async def list_user(
    id: UUID,
    db: Session = Depends(get_db),
    _: str = Depends(get_token),
):
    user_repository = UserRepository(db=db)

    input = ListUserInput(id=id)

    return ListUserUsecase(user_repository=user_repository).execute(input)


@user_router.put("/", status_code=200, response_model=CreateUserOutput)
async def update_user(
    body: UpdateUserInput,
    db: Session = Depends(get_db),
    _: str = Depends(get_token),
):
    user_repository = UserRepository(db=db)

    return UpdateUserUsecase(user_repository=user_repository).execute(body)


@user_router.delete("/", status_code=204, response_model=None)
async def delete_user(
    id: UUID,
    db: Session = Depends(get_db),
    _: str = Depends(get_token),
):
    user_repository = UserRepository(db=db)

    return DeleteUserUsecase(user_repository=user_repository).execute(
        DeleteUserInput(id=id)
    )


@user_router.patch("/update-password", status_code=204, response_model=None)
async def update_user_password(
    body: UpdateUserPasswordInput,
    db: Session = Depends(get_db),
    _: str = Depends(get_token),
):
    user_repository = UserRepository(db=db)

    return UpdateUserPasswordUsecase(user_repository=user_repository).execute(body)
