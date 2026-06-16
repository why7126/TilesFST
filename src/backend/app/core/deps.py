"""FastAPI dependencies for authentication."""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.exceptions import AuthForbiddenError, AuthUnauthorizedError, AuthUserDisabledError
from app.core.security import decode_access_token
from app.db.session import get_db
from app.repositories.user_repository import UserRecord, UserRepository

bearer_scheme = HTTPBearer(auto_error=False)

ADMIN_ROLES = {"admin", "employee"}


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
    repo: Annotated[UserRepository, Depends(get_user_repository)],
) -> UserRecord:
    if credentials is None or not credentials.credentials:
        raise AuthUnauthorizedError()

    try:
        payload = decode_access_token(credentials.credentials)
        user_id = payload.get("sub")
    except JWTError as exc:
        raise AuthUnauthorizedError() from exc

    if not user_id:
        raise AuthUnauthorizedError()

    user = repo.get_by_id(str(user_id))
    if user is None:
        raise AuthUnauthorizedError()
    if user.status != "active":
        raise AuthUserDisabledError()
    return user


def require_admin_access(
    current_user: Annotated[UserRecord, Depends(get_current_user)],
) -> UserRecord:
    if current_user.role not in ADMIN_ROLES:
        raise AuthForbiddenError()
    return current_user


def require_system_admin(
    current_user: Annotated[UserRecord, Depends(get_current_user)],
) -> UserRecord:
    if current_user.role != "admin":
        raise AuthForbiddenError()
    return current_user
