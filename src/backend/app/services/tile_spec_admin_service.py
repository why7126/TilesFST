"""Admin tile spec management business logic."""

from __future__ import annotations

from app.core.exceptions import (
    AuthInvalidRequestError,
    TileSpecDeleteForbiddenError,
    TileSpecDuplicatedError,
    TileSpecInvalidSortOrderError,
    TileSpecNotFoundError,
)
from app.repositories.tile_spec_repository import TileSpecRecord, TileSpecRepository
from app.schemas.tile_spec_admin import (
    TileSpecAdminItem,
    TileSpecAdminListData,
    TileSpecAdminSummary,
    TileSpecCreateRequest,
    TileSpecUpdateRequest,
)

VALID_PAGE_SIZES = frozenset({20, 50, 100})


class TileSpecAdminService:
    def __init__(self, repo: TileSpecRepository) -> None:
        self._repo = repo

    @staticmethod
    def to_item(spec: TileSpecRecord) -> TileSpecAdminItem:
        return TileSpecAdminItem(
            id=spec.id,
            width_mm=spec.width_mm,
            length_mm=spec.length_mm,
            thickness_mm=spec.thickness_mm,
            unit=spec.unit,
            display_name=spec.display_name,
            sort_order=spec.sort_order,
            status=spec.status,
            sku_count=spec.sku_count,
            remark=spec.remark,
            created_at=spec.created_at,
            updated_at=spec.updated_at,
        )

    @staticmethod
    def _validate_sort_order(sort_order: int) -> None:
        if sort_order < 1:
            raise TileSpecInvalidSortOrderError()

    @staticmethod
    def _normalize_remark(value: str | None) -> str | None:
        if value is None:
            return None
        trimmed = value.strip()
        if not trimmed:
            return None
        return trimmed[:200]

    def list_specs(
        self,
        *,
        page: int,
        page_size: int,
        keyword: str | None,
        status: str | None,
    ) -> TileSpecAdminListData:
        if page_size not in VALID_PAGE_SIZES:
            page_size = 20
        if page < 1:
            page = 1
        if status and status not in {"ENABLED", "DISABLED"}:
            status = None

        result = self._repo.list_specs(
            page=page,
            page_size=page_size,
            keyword=keyword.strip() if keyword else None,
            status=status,
        )
        summary = result.summary
        return TileSpecAdminListData(
            items=[self.to_item(spec) for spec in result.items],
            page=page,
            page_size=page_size,
            total=result.total,
            summary=TileSpecAdminSummary(
                total=summary["total"],
                enabled_count=summary["enabled_count"],
                disabled_count=summary["disabled_count"],
                unlinked_sku_count=summary["unlinked_sku_count"],
            ),
        )

    def get_spec(self, spec_id: int) -> TileSpecAdminItem:
        spec = self._repo.get_by_id(spec_id)
        if spec is None:
            raise TileSpecNotFoundError()
        return self.to_item(spec)

    def create_spec(self, payload: TileSpecCreateRequest) -> TileSpecAdminItem:
        self._validate_sort_order(payload.sort_order)
        if self._repo.get_by_dimensions(
            width_mm=payload.width_mm,
            length_mm=payload.length_mm,
        ):
            raise TileSpecDuplicatedError()
        spec = self._repo.create(
            width_mm=payload.width_mm,
            length_mm=payload.length_mm,
            thickness_mm=payload.thickness_mm,
            sort_order=payload.sort_order,
            remark=self._normalize_remark(payload.remark),
        )
        return self.to_item(spec)

    def update_spec(self, spec_id: int, payload: TileSpecUpdateRequest) -> TileSpecAdminItem:
        spec = self._repo.get_by_id(spec_id)
        if spec is None:
            raise TileSpecNotFoundError()
        self._validate_sort_order(payload.sort_order)
        existing = self._repo.get_by_dimensions(
            width_mm=payload.width_mm,
            length_mm=payload.length_mm,
            exclude_id=spec_id,
        )
        if existing:
            raise TileSpecDuplicatedError()
        updated = self._repo.update(
            spec_id,
            width_mm=payload.width_mm,
            length_mm=payload.length_mm,
            thickness_mm=payload.thickness_mm,
            sort_order=payload.sort_order,
            remark=self._normalize_remark(payload.remark),
        )
        assert updated is not None
        return self.to_item(updated)

    def enable_spec(self, spec_id: int) -> TileSpecAdminItem:
        spec = self._repo.get_by_id(spec_id)
        if spec is None:
            raise TileSpecNotFoundError()
        updated = self._repo.update_status(spec_id, "ENABLED")
        assert updated is not None
        return self.to_item(updated)

    def disable_spec(self, spec_id: int) -> TileSpecAdminItem:
        spec = self._repo.get_by_id(spec_id)
        if spec is None:
            raise TileSpecNotFoundError()
        updated = self._repo.update_status(spec_id, "DISABLED")
        assert updated is not None
        return self.to_item(updated)

    def delete_spec(self, spec_id: int) -> None:
        spec = self._repo.get_by_id(spec_id)
        if spec is None:
            raise TileSpecNotFoundError()
        if spec.sku_count != 0 or spec.status != "DISABLED":
            raise TileSpecDeleteForbiddenError()
        self._repo.delete(spec_id)

    def validate_spec_for_sku(
        self,
        spec_id: int,
        *,
        allow_disabled: bool = False,
    ) -> TileSpecRecord:
        spec = self._repo.get_by_id(spec_id)
        if spec is None:
            raise AuthInvalidRequestError("所选规格不存在")
        if spec.status != "ENABLED" and not allow_disabled:
            from app.core.exceptions import TileSpecDisabledError

            raise TileSpecDisabledError()
        return spec
