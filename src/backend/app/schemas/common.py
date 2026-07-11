"""Common API response schemas."""

from __future__ import annotations

from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    code: int = 0
    message: str = "success"
    data: T | None = None


class ApiErrorResponse(BaseModel):
    code: int
    message: str
    data: dict[str, Any] | None = Field(default=None)


class ValidationErrorItem(BaseModel):
    field: str
    message: str
    type: str
    location: list[str]


class ValidationErrorData(BaseModel):
    errors: list[ValidationErrorItem]


class ApiValidationErrorResponse(BaseModel):
    code: int = 40001
    message: str = "请求参数无效"
    data: ValidationErrorData


VALIDATION_ERROR_RESPONSE = {
    422: {
        "model": ApiValidationErrorResponse,
        "description": "请求参数校验失败，统一响应信封",
    }
}
