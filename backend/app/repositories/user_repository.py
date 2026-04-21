from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.entities.user import User
from app.mappers.user_mapper import UserMapper


class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, entity: User) -> None:
        user_model = UserMapper().to_model(entity=entity)
        self.db.add(user_model)

        try:
            self.db.commit()
        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro de integridade: {e}",
            )
