"""Tile domain ORM models."""

from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, String, Text
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
    model: Mapped[str] = mapped_column(String, nullable=False)
    category_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("tile_categories.id"))
    color: Mapped[str | None] = mapped_column(String, nullable=True)
    size: Mapped[str | None] = mapped_column(String, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=False, default="draft")
    created_at: Mapped[str | None] = mapped_column(String, nullable=True)
    updated_at: Mapped[str | None] = mapped_column(String, nullable=True)

    category: Mapped[TileCategory | None] = relationship(back_populates="tiles")
    images: Mapped[list[TileImage]] = relationship(back_populates="tile")


class TileImage(Base):
    __tablename__ = "tile_images"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tile_id: Mapped[int] = mapped_column(Integer, ForeignKey("tiles.id"), nullable=False)
    object_key: Mapped[str] = mapped_column(String, nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)
    is_main: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    tile: Mapped[Tile] = relationship(back_populates="images")
