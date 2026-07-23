"""Self-service password change business logic."""

from __future__ import annotations

from app.core.exceptions import (
    PasswordChangeRateLimitError,
    PasswordOldIncorrectError,
    PasswordPolicyError,
    PasswordSameAsOldError,
    PasswordWeakError,
    UserProtectedAccountError,
)
from app.core.protected_account import is_protected_username
from app.core.password_validation import (
    collect_password_policy_violations,
    password_policy_error_message,
    validate_new_password,
)
from app.core.security import hash_password, verify_password
from app.repositories.password_change_repository import PasswordChangeRepository
from app.repositories.user_repository import UserRecord, UserRepository
from app.schemas.admin_password import ChangePasswordData
from app.services.effective_settings_service import EffectiveSettingsService


class PasswordChangeService:
    FAIL_LIMIT = 5
    FAIL_WINDOW_MINUTES = 15
    SUCCESS_LIMIT = 3
    SUCCESS_WINDOW_HOURS = 24

    def __init__(
        self,
        user_repo: UserRepository,
        attempt_repo: PasswordChangeRepository,
        effective_settings: EffectiveSettingsService | None = None,
    ) -> None:
        self._users = user_repo
        self._attempts = attempt_repo
        self._effective = effective_settings

    def change_password(
        self,
        user: UserRecord,
        *,
        old_password: str,
        new_password: str,
    ) -> ChangePasswordData:
        if is_protected_username(user.username):
            raise UserProtectedAccountError()

        if (
            self._attempts.count_recent_failures(
                user.id,
                minutes=self.FAIL_WINDOW_MINUTES,
            )
            >= self.FAIL_LIMIT
        ):
            raise PasswordChangeRateLimitError()

        if (
            self._attempts.count_recent_successes(
                user.id,
                hours=self.SUCCESS_WINDOW_HOURS,
            )
            >= self.SUCCESS_LIMIT
        ):
            raise PasswordChangeRateLimitError()

        if not verify_password(old_password, user.password_hash):
            self._attempts.insert_attempt(user_id=user.id, success=False)
            raise PasswordOldIncorrectError()

        policy = self._effective.get_password_policy() if self._effective is not None else None
        violations = (
            collect_password_policy_violations(new_password, policy, old_password=old_password)
            if policy is not None
            else []
        )
        validation = (
            "same_as_old"
            if "same_as_old" in violations
            else "weak"
            if "weak" in violations
            else "policy"
            if violations
            else None
        )
        if policy is None:
            validation = validate_new_password(new_password, old_password=old_password)
        if validation == "same_as_old":
            raise PasswordSameAsOldError()
        if validation == "weak":
            raise PasswordWeakError()
        if validation == "policy":
            raise PasswordPolicyError(
                password_policy_error_message(violations, policy)
                if policy is not None
                else "新密码不符合安全策略",
                violations=violations or None,
                policy={
                    "min_length": policy.min_length,
                    "max_length": policy.max_length,
                    "require_letter": True,
                    "require_digit": True,
                }
                if policy is not None
                else None,
            )

        updated = self._users.change_password(user.id, hash_password(new_password))
        if updated is None:
            raise PasswordOldIncorrectError()

        self._attempts.insert_attempt(user_id=user.id, success=True)
        return ChangePasswordData(success=True)
