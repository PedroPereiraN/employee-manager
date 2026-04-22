from datetime import date
from typing import Optional
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy import func, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from math import ceil
from app.dtos.paginated_response import PaginatedResponse
from app.dtos.user import OutputUserDto
from app.entities.user import User
from app.enums.user_role import UserRole
from app.mappers.user_mapper import UserMapper
from app.models.user import UserModel


class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, entity: User) -> None:
        user_model = UserMapper.to_model(entity=entity)
        self.db.add(user_model)

        try:
            self.db.commit()
        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Integrity error: {e}",
            )

    def list_paginated(
        self,
        page: int = 1,
        size: int = 10,
        filter: Optional[str] = None,
        filter_role: Optional[UserRole] = None,
    ) -> PaginatedResponse[OutputUserDto]:
        query = self.db.query(UserModel).filter(UserModel.deleted_at.is_(None))

        if filter:
            query = query.filter(
                or_(
                    UserModel.name.ilike(f"%{filter}%"),
                    UserModel.email.ilike(f"%{filter}%"),
                )
            )

        if filter_role:
            query = query.filter(UserModel.role == filter_role)

        total = query.with_entities(func.count(UserModel.id)).scalar()

        query = query.order_by(UserModel.created_at.asc())

        items = query.offset((page - 1) * size).limit(size).all()

        items_output = [UserMapper.model_to_output(item) for item in items]

        pages = ceil(total / size) if total > 0 else 1

        return PaginatedResponse(
            total=total, page=page, size=size, pages=pages, items=items_output
        )

    def find_by_id(self, id: UUID) -> OutputUserDto:
        user_model = (
            self.db.query(UserModel)
            .filter(UserModel.id == id, UserModel.deleted_at.is_(None))
            .first()
        )

        if not user_model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return UserMapper.model_to_output(model=user_model)

    def find_by_email(self, email: str) -> User:
        user_model = (
            self.db.query(UserModel)
            .filter(UserModel.email == email, UserModel.deleted_at.is_(None))
            .first()
        )

        if not user_model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return UserMapper.model_to_entity(model=user_model)

    def update(self, entity: User) -> None:
        user_model = UserMapper.to_model(entity=entity)
        try:
            self.db.merge(user_model)
            self.db.commit()
        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Integrity error: {e}",
            )

    def delete(self, id: UUID) -> None:
        try:
            user_model = self.db.query(UserModel).filter(UserModel.id == id).first()
            if not user_model:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found",
                )
            user_model.deleted_at = date.today()
            self.db.commit()
        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Integrity error: {e}",
            )

    def update_password(self, id: UUID, new_password: str) -> None:
        try:
            user_model = (
                self.db.query(UserModel)
                .filter(UserModel.id == id, UserModel.deleted_at.is_(None))
                .first()
            )
            if not user_model:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found",
                )

            user_model.password = new_password
            user_model.updated_at = date.today()

            self.db.commit()
        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Integrity error: {e}",
            )
