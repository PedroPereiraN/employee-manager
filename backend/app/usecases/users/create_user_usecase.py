from app.entities.user import CreateUserProps, User
from app.protocols.usecase import UseCase
from app.dtos.user import CreateUserInput, CreateUserOutput
from app.repositories.user_repository import UserRepository


class CreateUserUsecase(UseCase[CreateUserInput, CreateUserOutput]):
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def execute(self, input: CreateUserInput) -> CreateUserOutput:
        user = User.create(
            props=CreateUserProps(
                name=input.name,
                email=input.email,
                password=input.password,
                role=input.role,
            )
        )

        self.user_repository.create(entity=user)

        return CreateUserOutput(
            id=user.id, name=user.name, email=user.email, role=user.role
        )
