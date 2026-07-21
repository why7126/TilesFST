"""Banner ORM model (reference; repository uses raw SQL)."""

from __future__ import annotations

from sqlalchemy import CheckConstraint, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Banner(Base):
    __tablename__ = "banners"
    __table_args__ = (
        UniqueConstraint("display_client", "position", "title", name="uq_banners_client_position_title"),
        CheckConstraint(
            "status IN ('DRAFT', 'ONLINE', 'OFFLINE', 'EXPIRED')",
            name="ck_banners_status",
        ),
        CheckConstraint(
            "display_client = 'MINIAPP_HOME'",
            name="ck_banners_display_client",
        ),
        CheckConstraint(
            "position IN ('MINIAPP_HOME_CAROUSEL', 'MINIAPP_BRAND_LIST_CAROUSEL')",
            name="ck_banners_position",
        ),
        CheckConstraint(
            "jump_type IN ('SKU_DETAIL', 'BRAND_DETAIL', 'EXTERNAL_LINK', 'TOPIC_PAGE', 'NO_JUMP')",
            name="ck_banners_jump_type",
        ),
        CheckConstraint(
            "image_source IN ('sku_main_image', 'sku_gallery_image', 'custom_upload', 'topic_cover', 'brand_logo')",
            name="ck_banners_image_source",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    display_client: Mapped[str] = mapped_column(String, nullable=False)
    position: Mapped[str] = mapped_column(String, nullable=False)
    image_object_key: Mapped[str] = mapped_column(String, nullable=False)
    image_source: Mapped[str] = mapped_column(String, nullable=False)
    sku_gallery_asset_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("tile_images.id"), nullable=True
    )
    jump_type: Mapped[str] = mapped_column(String, nullable=False)
    sku_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("tiles.id"), nullable=True)
    external_url: Mapped[str | None] = mapped_column(String, nullable=True)
    topic_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("topics.id"), nullable=True)
    brand_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("brands.id"), nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=100)
    valid_from: Mapped[str | None] = mapped_column(String, nullable=True)
    valid_to: Mapped[str | None] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=False, default="DRAFT")
    remark: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[str] = mapped_column(String, nullable=False)
    updated_at: Mapped[str] = mapped_column(String, nullable=False)
