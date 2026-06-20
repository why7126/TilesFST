"""Tile domain ORM models."""

from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, Real, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class TileCategory(Base):
    __tablename__ = "tile_categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    tiles: Mapped[list[Tile]] = relationship(back_populates="category")


class Tile(Base):
    __tablename__ = "tiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    sku_code: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    brand_id: Mapped[int] = mapped_column(Integer, ForeignKey("brands.id"), nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("tile_categories.id"), nullable=False)
    size: Mapped[str] = mapped_column(String, nullable=False)
    surface_finish: Mapped[str] = mapped_column(String, nullable=False)
    color_family: Mapped[str | None] = mapped_column(String, nullable=True)
    reference_price: Mapped[float | None] = mapped_column(Real, nullable=True)
    remark: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=False, default="DRAFT")
    created_at: Mapped[str | None] = mapped_column(String, nullable=True)
    updated_at: Mapped[str | None] = mapped_column(String, nullable=True)

    category: Mapped[TileCategory | None] = relationship(back_populates="tiles")
    images: Mapped[list[TileImage]] = relationship(back_populates="tile")
    videos: Mapped[list[TileVideo]] = relationship(back_populates="tile")


class TileImage(Base):
    __tablename__ = "tile_images"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tile_id: Mapped[int] = mapped_column(Integer, ForeignKey("tiles.id"), nullable=False)
    object_key: Mapped[str] = mapped_column(String, nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)
    is_main: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    tile: Mapped[Tile] = relationship(back_populates="images")


class TileVideo(Base):
    __tablename__ = "tile_videos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tile_id: Mapped[int] = mapped_column(Integer, ForeignKey("tiles.id"), nullable=False)
    object_key: Mapped[str] = mapped_column(String, nullable=False)
    file_name: Mapped[str] = mapped_column(String, nullable=False)
    file_size_bytes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    duration_seconds: Mapped[float | None] = mapped_column(Real, nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[str] = mapped_column(String, nullable=False)

    tile: Mapped[Tile] = relationship(back_populates="videos")
