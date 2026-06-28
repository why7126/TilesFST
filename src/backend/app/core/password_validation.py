"""Password policy and weak-password checks for self-service change."""

from __future__ import annotations

import re

from app.services.effective_settings_service import PasswordPolicy

_HAS_LETTER = re.compile(r"[A-Za-z]")
_HAS_DIGIT = re.compile(r"\d")
_HAS_UPPER = re.compile(r"[A-Z]")
_HAS_LOWER = re.compile(r"[a-z]")
_HAS_SPECIAL = re.compile(r"[!@#$%^&*\-_=+]")

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
    return password.lower() in {item.lower() for item in WEAK_PASSWORDS} or password in WEAK_PASSWORDS


def validate_password_policy(
    password: str,
    policy: PasswordPolicy,
    *,
    old_password: str | None = None,
) -> str | None:
    if len(password) < policy.min_length or len(password) > policy.max_length:
        return "policy"
    if policy.require_uppercase and not _HAS_UPPER.search(password):
        return "policy"
    if policy.require_lowercase and not _HAS_LOWER.search(password):
        return "policy"
    if policy.require_digit and not _HAS_DIGIT.search(password):
        return "policy"
    if policy.require_special and not _HAS_SPECIAL.search(password):
        return "policy"
    if old_password is not None and password == old_password:
        return "same_as_old"
    if is_weak_password(password):
        return "weak"
    return None


def validate_new_password(new_password: str, *, old_password: str | None = None) -> str | None:
    """Legacy default-policy validation (8–32, letter+digit)."""
    if len(new_password) < 8 or len(new_password) > 32:
        return "policy"
    if not _HAS_LETTER.search(new_password) or not _HAS_DIGIT.search(new_password):
        return "policy"
    if old_password is not None and new_password == old_password:
        return "same_as_old"
    if is_weak_password(new_password):
        return "weak"
    return None
