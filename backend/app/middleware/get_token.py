from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.services.auth_service import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_token(token: str = Depends(oauth2_scheme)) -> dict:
    return AuthService.validate_token(token)
