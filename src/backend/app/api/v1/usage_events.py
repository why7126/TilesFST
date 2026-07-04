"""Product usage event ingestion API."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPAuthorizationCredentials
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.deps import bearer_scheme
from app.core.security import decode_access_token
from app.db.session import get_db
from app.repositories.log_repository import LogRepository
from app.repositories.user_repository import UserRecord, UserRepository
from app.schemas.common import ApiResponse
from app.schemas.logs import UsageEventCreate, UsageEventData
from app.services.log_service import LogService

router = APIRouter()


def _optional_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
    db: Session = Depends(get_db),
) -> UserRecord | None:
    if credentials is None or not credentials.credentials:
        return None
    try:
        payload = decode_access_token(credentials.credentials)
    except JWTError:
        return None
    user_id = payload.get("sub")
    if not user_id:
        return None
    user = UserRepository(db).get_by_id(str(user_id))
    if user is None or user.status != "active":
        return None
    return user


@router.post(
    "",
    response_model=ApiResponse[UsageEventData],
    tags=["usage-events"],
    summary="上报产品使用行为事件",
    description="按事件字典上报产品使用行为；后端校验事件和属性并补充可信上下文。",
)
def create_usage_event(
    payload: UsageEventCreate,
    request: Request,
    current_user: Annotated[UserRecord | None, Depends(_optional_user)],
    db: Session = Depends(get_db),
) -> ApiResponse[UsageEventData]:
    service = LogService(LogRepository(db))
    request_id = getattr(request.state, "request_id", None)
    data = service.create_usage_event(
        payload,
        request_id=request_id,
        current_user=current_user,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    return ApiResponse(data=data)
