from typing import Generic, List, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PaginatedResponseDto(BaseModel, Generic[T]):
    total: int
    page: int
    size: int
    pages: int
    items: List[T]
