"""Seed default admin user when configured."""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import hash_password

DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_DISPLAY_NAME = "系统管理员"
logger = logging.getLogger(__name__)


def seed_admin_user(db: Session) -> bool:
    """Create or explicitly recover the configured default admin user."""
    password = settings.admin_initial_password
    if not password:
        if settings.admin_reset_password_on_startup:
            logger.warning(
                "Default admin password recovery was requested but ADMIN_INITIAL_PASSWORD is not set."
            )
        return False

    username = settings.admin_username.strip() or DEFAULT_ADMIN_USERNAME
    existing = db.execute(
        text("SELECT id FROM users WHERE username = :username"),
        {"username": username},
    ).mappings().first()
    if existing:
        if settings.admin_reset_password_on_startup:
            now = datetime.now(UTC).isoformat()
            db.execute(
                text(
                    """
                    UPDATE users
                    SET password_hash = :password_hash, updated_at = :updated_at
                    WHERE id = :id
                    """
                ),
                {
                    "id": existing["id"],
                    "password_hash": hash_password(password),
                    "updated_at": now,
                },
            )
            db.commit()
            logger.warning(
                "Default admin password recovery applied for configured admin username."
            )
            return True
        logger.info(
            "Default admin user already exists; startup seed did not update the password."
        )
        return False

    now = datetime.now(UTC).isoformat()
    db.execute(
        text(
            """
            INSERT INTO users (
                id, username, phone, email, password_hash, display_name,
                role, status, theme_mode, last_login_at, created_at, updated_at
            ) VALUES (
                :id, :username, NULL, NULL, :password_hash, :display_name,
                'admin', 'active', 'system', NULL, :created_at, :updated_at
            )
            """
        ),
        {
            "id": str(uuid4()),
            "username": username,
            "password_hash": hash_password(password),
            "display_name": DEFAULT_ADMIN_DISPLAY_NAME,
            "created_at": now,
            "updated_at": now,
        },
    )
    db.commit()
    logger.info("Default admin user created from configured initial password.")
    return True
