"""Tile category ORM model (reference; repository uses raw SQL)."""

from __future__ import annotations

from sqlalchemy import CheckConstraint, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class TileCategory(Base):
    __tablename__ = "tile_categories"
    __table_args__ = (
        CheckConstraint("level BETWEEN 1 AND 3", name="ck_tile_categories_level"),
        CheckConstraint("status IN ('ENABLED', 'DISABLED')", name="ck_tile_categories_status"),
        CheckConstraint("sku_count >= 0", name="ck_tile_categories_sku_count"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    parent_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("tile_categories.id"), nullable=True
    )
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    code: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=False, default="ENABLED")
    sku_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    path: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[str] = mapped_column(String, nullable=False)
    updated_at: Mapped[str] = mapped_column(String, nullable=False)
