"""Authentication request and response schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field

from app.schemas.common import ApiResponse


class LoginRequest(BaseModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)
    remember_me: bool = False


class UserProfile(BaseModel):
    id: str
    username: str
    display_name: str
    role: str
    status: str


class LoginData(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    expires_in: int
    user: UserProfile


class LogoutData(BaseModel):
    success: bool = True


LoginResponse = ApiResponse[LoginData]
UserProfileResponse = ApiResponse[UserProfile]
LogoutResponse = ApiResponse[LogoutData]
