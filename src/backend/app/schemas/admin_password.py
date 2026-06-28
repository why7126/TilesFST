"""Admin self-service password change schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ChangePasswordRequest(BaseModel):
    old_password: str = Field(min_length=1)
    new_password: str = Field(min_length=1)


class ChangePasswordData(BaseModel):
    success: bool = True
