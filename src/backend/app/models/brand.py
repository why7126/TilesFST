"""Brand ORM model (reference; repository uses raw SQL)."""

from __future__ import annotations

from sqlalchemy import CheckConstraint, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Brand(Base):
    __tablename__ = "brands"
    __table_args__ = (
        CheckConstraint("status IN ('ENABLED', 'DISABLED')", name="ck_brands_status"),
        CheckConstraint("sku_count >= 0", name="ck_brands_sku_count"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False)
    short_name: Mapped[str | None] = mapped_column(String(30), nullable=True)
    english_name: Mapped[str | None] = mapped_column(String(80), nullable=True)
    logo_object_key: Mapped[str | None] = mapped_column(String, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=False, default="ENABLED")
    sku_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[str] = mapped_column(String, nullable=False)
    updated_at: Mapped[str] = mapped_column(String, nullable=False)
