"""Common API response schemas."""

from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    code: int = 0
    message: str = "success"
    data: T | None = None


class ApiErrorResponse(BaseModel):
    code: int
    message: str
    data: None = Field(default=None)
