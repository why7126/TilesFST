"""Authentication business logic."""

from __future__ import annotations

from app.core.exceptions import AuthInvalidCredentialsError, AuthUserDisabledError
from app.core.security import create_access_token, verify_password
from app.repositories.profile_activity_repository import ProfileActivityRepository
from app.repositories.user_repository import UserRecord, UserRepository
from app.schemas.auth import LoginData, UserProfile


from app.services.effective_settings_service import EffectiveSettingsService


class AuthService:
    def __init__(
        self,
        repo: UserRepository,
        activity_repo: ProfileActivityRepository | None = None,
        effective_settings: EffectiveSettingsService | None = None,
    ) -> None:
        self._repo = repo
        self._activity_repo = activity_repo
        self._effective = effective_settings

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

        expire_minutes = (
            self._effective.get_jwt_access_expire_minutes() if self._effective else None
        )
        token, expires_in = create_access_token(
            user_id=user.id,
            role=user.role,
            token_version=user.token_version,
            remember_me=remember_me,
            access_expire_minutes=expire_minutes,
        )
        self._repo.update_last_login_at(user.id)
        if self._activity_repo is not None and user.role in {"admin", "employee"}:
            self._activity_repo.insert(
                user_id=user.id,
                action_type="login",
                summary="安全登录成功",
            )
        return LoginData(
            access_token=token,
            expires_in=expires_in,
            user=self.to_profile(user),
        )

    def get_current_profile(self, user: UserRecord) -> UserProfile:
        return self.to_profile(user)
