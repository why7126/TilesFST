"""Admin dashboard summary API routes."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import require_admin_user
from app.db.session import get_db
from app.repositories.user_repository import UserRecord
from app.schemas.admin_dashboard import AdminDashboardSummary
from app.schemas.common import ApiResponse
from app.services.admin_dashboard_service import AdminDashboardService

router = APIRouter(dependencies=[Depends(require_admin_user)])


def get_admin_dashboard_service(
    db: Annotated[Session, Depends(get_db)],
) -> AdminDashboardService:
    return AdminDashboardService(db)


@router.get(
    "/summary",
    response_model=ApiResponse[AdminDashboardSummary],
    summary="管理端 Dashboard 数据概览",
)
def get_admin_dashboard_summary(
    service: Annotated[AdminDashboardService, Depends(get_admin_dashboard_service)],
    current_user: Annotated[UserRecord, Depends(require_admin_user)],
) -> ApiResponse[AdminDashboardSummary]:
    return ApiResponse(data=service.get_summary(current_user))
