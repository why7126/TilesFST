"""Authentication business logic."""

from __future__ import annotations

from app.core.exceptions import AuthInvalidCredentialsError, AuthUserDisabledError
from app.core.security import create_access_token, verify_password
from app.repositories.user_repository import UserRecord, UserRepository
from app.schemas.auth import LoginData, UserProfile


class AuthService:
    def __init__(self, repo: UserRepository) -> None:
        self._repo = repo

    @staticmethod
    def to_profile(user: UserRecord) -> UserProfile:
        return UserProfile(
            id=user.id,
            username=user.username,
            display_name=user.display_name or user.username,
            role=user.role,
            status=user.status,
        )

    def login(self, *, username: str, password: str, remember_me: bool) -> LoginData:
        user = self._repo.get_by_username(username.strip())
        if user is None or not verify_password(password, user.password_hash):
            raise AuthInvalidCredentialsError()
        if user.status != "active":
            raise AuthUserDisabledError()

        token, expires_in = create_access_token(
            user_id=user.id,
            role=user.role,
            remember_me=remember_me,
        )
        self._repo.update_last_login_at(user.id)
        return LoginData(
            access_token=token,
            expires_in=expires_in,
            user=self.to_profile(user),
        )

    def get_current_profile(self, user: UserRecord) -> UserProfile:
        return self.to_profile(user)
