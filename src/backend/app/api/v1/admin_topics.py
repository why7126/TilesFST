"""Admin topics read-only API routes."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.core.deps import get_topic_repository, require_admin_user
from app.repositories.topic_repository import TopicRepository
from app.schemas.banner_admin import TopicAdminListData
from app.schemas.common import ApiResponse
from app.services.topic_admin_service import TopicAdminService

router = APIRouter(dependencies=[Depends(require_admin_user)])


def get_topic_admin_service(
    repo: Annotated[TopicRepository, Depends(get_topic_repository)],
) -> TopicAdminService:
    return TopicAdminService(repo)


@router.get(
    "", response_model=ApiResponse[TopicAdminListData], summary="专题列表（只读）"
)
def list_topics(
    service: Annotated[TopicAdminService, Depends(get_topic_admin_service)],
    keyword: str | None = Query(None),
    status: str | None = Query("ENABLED"),
) -> ApiResponse[TopicAdminListData]:
    return ApiResponse(data=service.list_topics(keyword=keyword, status=status))
