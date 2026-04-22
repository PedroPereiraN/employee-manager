from pydantic import BaseModel


class LoginInputDto(BaseModel):
    email: str
    password: str


class LoginOutputDto(BaseModel):
    access_token: str
    token_type: str = "bearer"
