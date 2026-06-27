"""Admin user management API schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class UserAdminSummary(BaseModel):
    total: int
    filtered: int
    active_count: int
    disabled_count: int


class UserAdminItem(BaseModel):
    id: str
    username: str
    display_name: str | None
    role: str
    status: str
    avatar_object_key: str | None = None
    avatar_url: str | None = None
    email: str | None = None
    phone: str | None = None
    last_login_at: str | None = None
    created_at: str


class UserAdminListData(BaseModel):
    items: list[UserAdminItem]
    page: int
    page_size: int
    total: int
    summary: UserAdminSummary


class UserCreateRequest(BaseModel):
    username: str = Field(min_length=4, max_length=32)
    display_name: str | None = Field(default=None, max_length=32)
    role: str
    avatar_object_key: str | None = None


class UserUpdateRequest(BaseModel):
    display_name: str | None = Field(default=None, max_length=32)
    role: str | None = None
    avatar_object_key: str | None = None


class UserStatusUpdateRequest(BaseModel):
    status: str


class UserCreateData(BaseModel):
    user: UserAdminItem
    initial_password: str


class ResetPasswordData(BaseModel):
    password: str
