"""Seed default admin user when configured."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import hash_password

DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_DISPLAY_NAME = "系统管理员"


def seed_admin_user(db: Session) -> bool:
    """Create default admin if missing. Returns True when a user was created."""
    password = settings.admin_initial_password
    if not password:
        return False

    existing = db.execute(
        text("SELECT id FROM users WHERE username = :username"),
        {"username": DEFAULT_ADMIN_USERNAME},
    ).first()
    if existing:
        return False

    now = datetime.now(UTC).isoformat()
    db.execute(
        text(
            """
            INSERT INTO users (
                id, username, phone, email, password_hash, display_name,
                role, status, last_login_at, created_at, updated_at
            ) VALUES (
                :id, :username, NULL, NULL, :password_hash, :display_name,
                'admin', 'active', NULL, :created_at, :updated_at
            )
            """
        ),
        {
            "id": str(uuid4()),
            "username": DEFAULT_ADMIN_USERNAME,
            "password_hash": hash_password(password),
            "display_name": DEFAULT_ADMIN_DISPLAY_NAME,
            "created_at": now,
            "updated_at": now,
        },
    )
    db.commit()
    return True
