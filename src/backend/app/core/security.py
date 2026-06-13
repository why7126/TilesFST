"""Password hashing and JWT helpers."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

import bcrypt
from jose import JWTError, jwt

from app.core.config import settings


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), password_hash.encode("utf-8"))


def create_access_token(*, user_id: str, role: str, remember_me: bool = False) -> tuple[str, int]:
    if remember_me:
        expires_delta = timedelta(days=settings.jwt_remember_me_expire_days)
    else:
        expires_delta = timedelta(minutes=settings.jwt_access_token_expire_minutes)
    expires_at = datetime.now(UTC) + expires_delta
    payload = {
        "sub": user_id,
        "role": role,
        "exp": expires_at,
    }
    token = jwt.encode(payload, settings.app_secret_key, algorithm=settings.jwt_algorithm)
    return token, int(expires_delta.total_seconds())


def decode_access_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, settings.app_secret_key, algorithms=[settings.jwt_algorithm])


def is_token_valid(token: str) -> bool:
    try:
        decode_access_token(token)
        return True
    except JWTError:
        return False
