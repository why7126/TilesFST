"""Password policy and weak-password checks for self-service change."""

from __future__ import annotations

import re

from app.services.effective_settings_service import PasswordPolicy

_HAS_LETTER = re.compile(r"[A-Za-z]")
_HAS_DIGIT = re.compile(r"[0-9]")

PASSWORD_POLICY_MESSAGES: dict[str, str] = {
    "min_length": "新密码至少需要 {min_length} 位字符",
    "max_length": "新密码不能超过 {max_length} 位字符",
    "missing_letter": "新密码需要包含英文字符",
    "missing_digit": "新密码需要包含数字",
    "same_as_old": "新密码不能与原密码相同",
    "weak": "新密码过于常见，请更换",
}

WEAK_PASSWORDS = frozenset(
    {
        "12345678",
        "123456789",
        "1234567890",
        "password",
        "password1",
        "password123",
        "admin123",
        "admin1234",
        "adminpass",
        "qwerty123",
        "qwertyui",
        "letmein1",
        "welcome1",
        "welcome123",
        "changeme",
        "changeme1",
        "abc12345",
        "abc123456",
        "11111111",
        "00000000",
        "88888888",
        "66666666",
        "iloveyou",
        "sunshine",
        "princess",
        "football",
        "baseball",
        "monkey123",
        "dragon123",
        "master123",
        "trustno1",
        "passw0rd",
        "pass1234",
        "tile1234",
        "tiles123",
        "tilesfst",
        "adminpass123",
        "operator123",
        "test1234",
        "test12345",
        "user1234",
        "user12345",
        "P@ssw0rd",
        "Password1",
        "Password123",
        "Admin1234",
        "AdminPass123",
    }
)


def is_weak_password(password: str) -> bool:
    return (
        password.lower() in {item.lower() for item in WEAK_PASSWORDS} or password in WEAK_PASSWORDS
    )


def validate_password_policy(
    password: str,
    policy: PasswordPolicy,
    *,
    old_password: str | None = None,
) -> str | None:
    violations = collect_password_policy_violations(password, policy, old_password=old_password)
    if "same_as_old" in violations:
        return "same_as_old"
    if "weak" in violations:
        return "weak"
    if violations:
        return "policy"
    return None


def collect_password_policy_violations(
    password: str,
    policy: PasswordPolicy,
    *,
    old_password: str | None = None,
) -> list[str]:
    violations: list[str] = []
    if len(password) < policy.min_length:
        violations.append("min_length")
    if len(password) > policy.max_length:
        violations.append("max_length")
    if not _HAS_LETTER.search(password):
        violations.append("missing_letter")
    if not _HAS_DIGIT.search(password):
        violations.append("missing_digit")
    if old_password is not None and password == old_password:
        violations.append("same_as_old")
    if is_weak_password(password):
        violations.append("weak")
    return violations


def password_policy_message(violation: str, policy: PasswordPolicy) -> str:
    template = PASSWORD_POLICY_MESSAGES.get(violation, "新密码不符合安全策略")
    return template.format(min_length=policy.min_length, max_length=policy.max_length)


def password_policy_error_message(violations: list[str], policy: PasswordPolicy) -> str:
    policy_violations = [item for item in violations if item not in {"same_as_old", "weak"}]
    if not policy_violations:
        return "新密码不符合安全策略"
    return "；".join(password_policy_message(item, policy) for item in policy_violations)


def validate_new_password(new_password: str, *, old_password: str | None = None) -> str | None:
    """Default basic validation (5-32, ASCII letter + ASCII digit)."""
    policy = PasswordPolicy()
    violations = collect_password_policy_violations(
        new_password,
        policy,
        old_password=old_password,
    )
    if "same_as_old" in violations:
        return "same_as_old"
    if "weak" in violations:
        return "weak"
    if violations:
        return "policy"
    return None
