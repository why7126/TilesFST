"""Admin topic read-only service."""

from __future__ import annotations

from app.repositories.topic_repository import TopicRecord, TopicRepository
from app.schemas.banner_admin import TopicAdminItem, TopicAdminListData


def _cover_url(object_key: str | None) -> str | None:
    if not object_key:
        return None
    return f"/media/{object_key}"


class TopicAdminService:
    def __init__(self, repo: TopicRepository) -> None:
        self._repo = repo

    @staticmethod
    def to_item(topic: TopicRecord) -> TopicAdminItem:
        return TopicAdminItem(
            id=topic.id,
            code=topic.code,
            title=topic.title,
            status=topic.status,
            cover_object_key=topic.cover_object_key,
            cover_url=_cover_url(topic.cover_object_key),
        )

    def list_topics(
        self,
        *,
        keyword: str | None,
        status: str | None = "ENABLED",
    ) -> TopicAdminListData:
        if status and status not in {"ENABLED", "DISABLED"}:
            status = "ENABLED"
        items = self._repo.list_topics(
            keyword=keyword.strip() if keyword else None,
            status=status,
        )
        mapped = [self.to_item(t) for t in items]
        return TopicAdminListData(items=mapped, total=len(mapped))
