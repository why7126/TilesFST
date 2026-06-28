"""Profile self-service API schemas."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ProfileMe(BaseModel):
    id: str
    username: str
    display_name: str
    role: str
    status: str
    email: str | None = None
    phone: str | None = None
    remark: str | None = None
    avatar_object_key: str | None = None
    avatar_url: str | None = None
    last_login_at: str | None = None
    updated_at: str


class ProfilePatchRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    display_name: str | None = Field(default=None, min_length=2, max_length=32)
    email: str | None = Field(default=None, max_length=128)
    phone: str | None = Field(default=None, max_length=32)
    remark: str | None = Field(default=None, max_length=200)
    avatar_object_key: str | None = Field(default=None, max_length=512)


class ProfileActivityItem(BaseModel):
    id: str
    action_type: str
    summary: str
    created_at: str
