from enum import Enum


class UserRole(str, Enum):
    admin = "admin"
    supervisor = "supervisor"
    member = "member"
