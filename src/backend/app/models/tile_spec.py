"""Tile spec ORM model (reference; repository uses raw SQL)."""

from __future__ import annotations

from sqlalchemy import CheckConstraint, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class TileSpec(Base):
    __tablename__ = "tile_specs"
    __table_args__ = (
        CheckConstraint("status IN ('ENABLED', 'DISABLED')", name="ck_tile_specs_status"),
        CheckConstraint("sku_count >= 0", name="ck_tile_specs_sku_count"),
        CheckConstraint("width_mm BETWEEN 1 AND 9999", name="ck_tile_specs_width"),
        CheckConstraint("length_mm BETWEEN 1 AND 9999", name="ck_tile_specs_length"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    width_mm: Mapped[int] = mapped_column(Integer, nullable=False)
    length_mm: Mapped[int] = mapped_column(Integer, nullable=False)
    thickness_mm: Mapped[float | None] = mapped_column(Float, nullable=True)
    unit: Mapped[str] = mapped_column(String, nullable=False, default="mm")
    display_name: Mapped[str] = mapped_column(String, nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=100)
    status: Mapped[str] = mapped_column(String, nullable=False, default="ENABLED")
    sku_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    remark: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[str] = mapped_column(String, nullable=False)
    updated_at: Mapped[str] = mapped_column(String, nullable=False)
