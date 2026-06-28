"""Username validation and password generation for user management."""

from __future__ import annotations

import re
import secrets
import string

from app.services.effective_settings_service import PasswordPolicy

USERNAME_PATTERN = re.compile(r"^[a-z][a-z0-9._-]{3,31}$")
CONSECUTIVE_SPECIAL = re.compile(r"(__|--|\.\.)")
RESERVED_USERNAMES = frozenset(
    {
        "admin",
        "administrator",
        "anonymous",
        "false",
        "login",
        "null",
        "root",
        "system",
        "test",
        "true",
        "user",
    }
)

_PASSWORD_ALPHABET = "".join(
    ch
    for ch in (string.ascii_letters + string.digits + "!@#$%^&*-_=+")
    if ch not in "O0Il"
)


def validate_username(username: str) -> str | None:
    """Return error message if invalid, else None."""
    value = username.strip()
    if len(value) < 4 or len(value) > 32:
        return "用户名长度须为 4–32 位"
    if not USERNAME_PATTERN.match(value):
        return "用户名须以小写字母开头，仅含小写字母、数字、_、-、."
    if CONSECUTIVE_SPECIAL.search(value):
        return "用户名不允许连续特殊符号"
    if value.lower() in RESERVED_USERNAMES:
        return "用户名为系统保留字"
    return None


def generate_random_password(
    length: int | None = None,
    policy: PasswordPolicy | None = None,
) -> str:
    """Generate a random password meeting effective complexity requirements."""
    active_policy = policy or PasswordPolicy()
    target_length = max(length or active_policy.min_length, active_policy.min_length, 12)

    while True:
        chars = [secrets.choice(_PASSWORD_ALPHABET) for _ in range(target_length)]
        password = "".join(chars)
        if _meets_policy(password, active_policy):
            return password


def _meets_policy(password: str, policy: PasswordPolicy) -> bool:
    if len(password) < policy.min_length:
        return False
    if policy.require_uppercase and not any(c.isupper() for c in password):
        return False
    if policy.require_lowercase and not any(c.islower() for c in password):
        return False
    if policy.require_digit and not any(c.isdigit() for c in password):
        return False
    if policy.require_special and not any(c in "!@#$%^&*-_=+" for c in password):
        return False
    return True
