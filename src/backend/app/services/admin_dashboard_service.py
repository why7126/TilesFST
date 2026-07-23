"""Admin dashboard summary service."""

from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.repositories.banner_repository import VALID_BANNER_SCOPE_SQL
from app.repositories.user_repository import UserRecord
from app.schemas.admin_dashboard import AdminDashboardMetric, AdminDashboardSummary


class AdminDashboardService:
    def __init__(self, db: Session) -> None:
        self._db = db

    def get_summary(self, current_user: UserRecord) -> AdminDashboardSummary:
        user_metric = self._user_total_metric(current_user)
        return AdminDashboardSummary(
            sku_total=AdminDashboardMetric(
                value=self._count("tiles"),
                description="全部商品主数据",
            ),
            brand_total=AdminDashboardMetric(
                value=self._count("brands"),
                description="品牌资料库",
            ),
            banner_total=AdminDashboardMetric(
                value=self._count("banners", where_sql=VALID_BANNER_SCOPE_SQL),
                description="展示位素材",
            ),
            user_total=user_metric,
        )

    def _count(self, table: str, *, where_sql: str | None = None) -> int:
        clause = f" WHERE {where_sql}" if where_sql else ""
        value = self._db.execute(text(f"SELECT COUNT(*) FROM {table}{clause}")).scalar_one()
        return int(value or 0)

    def _user_total_metric(self, current_user: UserRecord) -> AdminDashboardMetric:
        if current_user.role != "admin":
            return AdminDashboardMetric(
                value=0,
                description="仅系统管理员可见",
                visible=False,
            )
        return AdminDashboardMetric(
            value=self._count("users"),
            description="后台授权账号",
        )
