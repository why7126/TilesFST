"""User and login log ORM models."""

from __future__ import annotations

from sqlalchemy import CheckConstraint, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint("role IN ('admin', 'employee', 'store_owner')", name="ck_users_role"),
        CheckConstraint("status IN ('active', 'disabled', 'deleted')", name="ck_users_status"),
        CheckConstraint(
            "theme_mode IN ('system', 'dark_flagship', 'comfort_dark', 'light')",
            name="ck_users_theme_mode",
        ),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    phone: Mapped[str | None] = mapped_column(String, nullable=True)
    email: Mapped[str | None] = mapped_column(String, nullable=True)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    display_name: Mapped[str | None] = mapped_column(String, nullable=True)
    role: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False, default="active")
    avatar_object_key: Mapped[str | None] = mapped_column(String, nullable=True)
    remark: Mapped[str | None] = mapped_column(Text, nullable=True)
    token_version: Mapped[int] = mapped_column(nullable=False, default=0)
    theme_mode: Mapped[str] = mapped_column(String, nullable=False, default="system")
    last_login_at: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[str] = mapped_column(String, nullable=False)
    updated_at: Mapped[str] = mapped_column(String, nullable=False)

    login_logs: Mapped[list[LoginLog]] = relationship(back_populates="user")


class LoginLog(Base):
    __tablename__ = "login_logs"
    __table_args__ = (
        CheckConstraint("result IN ('success', 'failed')", name="ck_login_logs_result"),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True)
    user_id: Mapped[str | None] = mapped_column(String, ForeignKey("users.id"), nullable=True)
    login_identifier: Mapped[str] = mapped_column(String, nullable=False)
    result: Mapped[str] = mapped_column(String, nullable=False)
    failure_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    ip: Mapped[str | None] = mapped_column(String, nullable=True)
    user_agent: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[str] = mapped_column(String, nullable=False)

    user: Mapped[User | None] = relationship(back_populates="login_logs")


class ProfileActivityLog(Base):
    __tablename__ = "profile_activity_logs"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=False)
    action_type: Mapped[str] = mapped_column(String, nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    metadata_json: Mapped[str | None] = mapped_column("metadata", Text, nullable=True)
    created_at: Mapped[str] = mapped_column(String, nullable=False)


class PasswordChangeAttempt(Base):
    __tablename__ = "password_change_attempts"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=False)
    success: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[str] = mapped_column(String, nullable=False)
