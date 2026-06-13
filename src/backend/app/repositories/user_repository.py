"""User persistence."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.security import hash_password


@dataclass
class UserRecord:
    id: str
    username: str
    phone: str | None
    email: str | None
    password_hash: str
    display_name: str
    role: str
    status: str
    last_login_at: str | None
    created_at: str
    updated_at: str


class UserRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def _to_record(self, row: dict) -> UserRecord:
        return UserRecord(
            id=row["id"],
            username=row["username"],
            phone=row["phone"],
            email=row["email"],
            password_hash=row["password_hash"],
            display_name=row["display_name"],
            role=row["role"],
            status=row["status"],
            last_login_at=row["last_login_at"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def get_by_username(self, username: str) -> UserRecord | None:
        row = (
            self._db.execute(
                text("SELECT * FROM users WHERE username = :username"),
                {"username": username},
            )
            .mappings()
            .first()
        )
        return self._to_record(dict(row)) if row else None

    def get_by_id(self, user_id: str) -> UserRecord | None:
        row = (
            self._db.execute(text("SELECT * FROM users WHERE id = :id"), {"id": user_id})
            .mappings()
            .first()
        )
        return self._to_record(dict(row)) if row else None

    def update_last_login_at(self, user_id: str) -> None:
        now = datetime.now(UTC).isoformat()
        self._db.execute(
            text("UPDATE users SET last_login_at = :now, updated_at = :now WHERE id = :id"),
            {"now": now, "id": user_id},
        )
        self._db.commit()

    def create_user(
        self,
        *,
        username: str,
        password: str,
        display_name: str,
        role: str,
        status: str = "active",
    ) -> UserRecord:
        now = datetime.now(UTC).isoformat()
        user_id = str(uuid4())
        self._db.execute(
            text(
                """
                INSERT INTO users (
                    id, username, phone, email, password_hash, display_name,
                    role, status, last_login_at, created_at, updated_at
                ) VALUES (
                    :id, :username, NULL, NULL, :password_hash, :display_name,
                    :role, :status, NULL, :created_at, :updated_at
                )
                """
            ),
            {
                "id": user_id,
                "username": username,
                "password_hash": hash_password(password),
                "display_name": display_name,
                "role": role,
                "status": status,
                "created_at": now,
                "updated_at": now,
            },
        )
        self._db.commit()
        user = self.get_by_id(user_id)
        assert user is not None
        return user
