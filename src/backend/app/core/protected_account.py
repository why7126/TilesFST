"""Protected system account helpers."""

from __future__ import annotations

from app.core.config import settings

DEFAULT_PROTECTED_ADMIN_USERNAME = "admin"
PROTECTED_ACCOUNT_REASON = "系统保底管理员账号不允许执行该操作"


def _normalized_username(username: str) -> str:
    return username.strip().lower()


def protected_admin_username() -> str:
    configured = (settings.admin_username or DEFAULT_PROTECTED_ADMIN_USERNAME).strip()
    return _normalized_username(configured or DEFAULT_PROTECTED_ADMIN_USERNAME)


def is_protected_username(username: str | None) -> bool:
    if not username:
        return False
    return _normalized_username(username) == protected_admin_username()
