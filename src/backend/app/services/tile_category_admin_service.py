"""Admin tile category management business logic."""

from __future__ import annotations

from app.core.exceptions import (
    AuthInvalidRequestError,
    CategoryCodeDuplicatedError,
    CategoryDeleteForbiddenError,
    CategoryInvalidSortOrderError,
    CategoryMaxDepthExceededError,
    CategoryNotFoundError,
)
from app.repositories.tile_category_repository import TileCategoryRecord, TileCategoryRepository
from app.schemas.tile_category_admin import (
    TileCategoryAdminItem,
    TileCategoryAdminListData,
    TileCategoryAdminSummary,
    TileCategoryCreateRequest,
    TileCategoryTreeNode,
    TileCategoryUpdateRequest,
)

VALID_PAGE_SIZES = frozenset({10, 20, 50})
VALID_STATUSES = frozenset({"ENABLED", "DISABLED"})
MAX_CATEGORY_LEVEL = 2


class TileCategoryAdminService:
    def __init__(self, repo: TileCategoryRepository) -> None:
        self._repo = repo

    @staticmethod
    def to_item(category: TileCategoryRecord) -> TileCategoryAdminItem:
        return TileCategoryAdminItem(
            id=category.id,
            parent_id=category.parent_id,
            name=category.name,
            code=category.code,
            sort_order=category.sort_order,
            level=category.level,
            description=category.description,
            status=category.status,
            sku_count=category.sku_count,
            path=category.path,
            created_at=category.created_at,
            updated_at=category.updated_at,
        )

    @staticmethod
    def _validate_sort_order(sort_order: int) -> None:
        if sort_order < 1:
            raise CategoryInvalidSortOrderError()

    @staticmethod
    def _validate_name(name: str) -> str:
        trimmed = name.strip()
        if not trimmed:
            raise AuthInvalidRequestError("类目名称不能为空")
        if len(trimmed) > 30:
            raise AuthInvalidRequestError("类目名称不能超过 30 个字符")
        return trimmed

    @staticmethod
    def _validate_code(code: str) -> str:
        trimmed = code.strip().upper()
        if not trimmed:
            raise AuthInvalidRequestError("类目编码不能为空")
        if len(trimmed) > 32:
            raise AuthInvalidRequestError("类目编码不能超过 32 个字符")
        return trimmed

    def _compute_path(self, name: str, parent: TileCategoryRecord | None) -> tuple[int, str]:
        if parent is None:
            return 1, name
        if parent.level >= MAX_CATEGORY_LEVEL:
            raise CategoryMaxDepthExceededError()
        return parent.level + 1, f"{parent.path} / {name}"

    def _rebuild_path_for_subtree(self, category_id: int, new_path: str) -> None:
        record = self._repo.get_by_id(category_id)
        if record is None:
            return
        children = [
            item for item in self._repo.list_all() if item.parent_id == category_id
        ]
        for child in children:
            child_path = f"{new_path} / {child.name}"
            self._repo.update(
                child.id,
                name=child.name,
                sort_order=child.sort_order,
                description=child.description,
                path=child_path,
            )
            self._rebuild_path_for_subtree(child.id, child_path)

    def list_categories(
        self,
        *,
        page: int,
        page_size: int,
        keyword: str | None,
        status: str | None,
        level: int | None,
        parent_id: int | None,
    ) -> TileCategoryAdminListData:
        if page_size not in VALID_PAGE_SIZES:
            page_size = 10
        if page < 1:
            page = 1
        if status and status not in VALID_STATUSES:
            status = None
        if level is not None and level not in {1, 2}:
            raise CategoryMaxDepthExceededError()

        result = self._repo.list_categories(
            page=page,
            page_size=page_size,
            keyword=keyword.strip() if keyword else None,
            status=status,
            level=level,
            parent_id=parent_id,
        )
        summary = result.summary
        return TileCategoryAdminListData(
            items=[self.to_item(item) for item in result.items],
            page=page,
            page_size=page_size,
            total=result.total,
            summary=TileCategoryAdminSummary(
                total=summary["total"],
                enabled_count=summary["enabled_count"],
                bound_sku_total=summary["bound_sku_total"],
                max_level=MAX_CATEGORY_LEVEL,
            ),
        )

    def get_category_tree(self) -> list[TileCategoryTreeNode]:
        records = self._repo.list_all()
        by_parent: dict[int | None, list[TileCategoryRecord]] = {}
        for record in records:
            by_parent.setdefault(record.parent_id, []).append(record)

        def aggregate_sku(record: TileCategoryRecord) -> int:
            total = record.sku_count
            for child in by_parent.get(record.id, []):
                total += aggregate_sku(child)
            return total

        def build_node(record: TileCategoryRecord) -> TileCategoryTreeNode:
            children = sorted(by_parent.get(record.id, []), key=lambda r: (r.sort_order, r.id))
            return TileCategoryTreeNode(
                id=record.id,
                name=record.name,
                code=record.code,
                level=record.level,
                status=record.status,
                sku_count=aggregate_sku(record),
                children=[build_node(child) for child in children],
            )

        roots = sorted(by_parent.get(None, []), key=lambda r: (r.sort_order, r.id))
        return [build_node(root) for root in roots]

    def get_category(self, category_id: int) -> TileCategoryAdminItem:
        category = self._repo.get_by_id(category_id)
        if category is None:
            raise CategoryNotFoundError()
        return self.to_item(category)

    def create_category(self, payload: TileCategoryCreateRequest) -> TileCategoryAdminItem:
        name = self._validate_name(payload.name)
        code = self._validate_code(payload.code)
        self._validate_sort_order(payload.sort_order)
        if payload.status not in VALID_STATUSES:
            raise AuthInvalidRequestError("无效的状态")
        if self._repo.get_by_code(code):
            raise CategoryCodeDuplicatedError()

        parent = None
        if payload.parent_id is not None:
            parent = self._repo.get_by_id(payload.parent_id)
            if parent is None:
                raise CategoryNotFoundError("上级类目不存在")

        level, path = self._compute_path(name, parent)
        category = self._repo.create(
            parent_id=payload.parent_id,
            name=name,
            code=code,
            sort_order=payload.sort_order,
            level=level,
            description=(payload.description or "").strip() or None,
            status=payload.status,
            path=path,
        )
        return self.to_item(category)

    def update_category(
        self, category_id: int, payload: TileCategoryUpdateRequest
    ) -> TileCategoryAdminItem:
        category = self._repo.get_by_id(category_id)
        if category is None:
            raise CategoryNotFoundError()

        name = self._validate_name(payload.name)
        self._validate_sort_order(payload.sort_order)

        parent = (
            self._repo.get_by_id(category.parent_id) if category.parent_id is not None else None
        )
        _, path = self._compute_path(name, parent)

        updated = self._repo.update(
            category_id,
            name=name,
            sort_order=payload.sort_order,
            description=(payload.description or "").strip() or None,
            path=path,
        )
        assert updated is not None
        if name != category.name:
            self._rebuild_path_for_subtree(category_id, path)
            updated = self._repo.get_by_id(category_id)
            assert updated is not None
        return self.to_item(updated)

    def enable_category(self, category_id: int) -> TileCategoryAdminItem:
        category = self._repo.get_by_id(category_id)
        if category is None:
            raise CategoryNotFoundError()
        updated = self._repo.update_status(category_id, "ENABLED")
        assert updated is not None
        return self.to_item(updated)

    def disable_category(self, category_id: int) -> TileCategoryAdminItem:
        category = self._repo.get_by_id(category_id)
        if category is None:
            raise CategoryNotFoundError()
        updated = self._repo.update_status(category_id, "DISABLED")
        assert updated is not None
        return self.to_item(updated)

    def delete_category(self, category_id: int) -> None:
        category = self._repo.get_by_id(category_id)
        if category is None:
            raise CategoryNotFoundError()
        if category.sku_count != 0 or category.status != "DISABLED":
            raise CategoryDeleteForbiddenError()
        if self._repo.has_children(category_id):
            raise CategoryDeleteForbiddenError("存在子类目，无法删除")
        self._repo.delete(category_id)
