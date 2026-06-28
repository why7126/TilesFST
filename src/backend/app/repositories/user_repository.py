"""User persistence."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any
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
    display_name: str | None
    role: str
    status: str
    avatar_object_key: str | None
    last_login_at: str | None
    remark: str | None
    token_version: int
    created_at: str
    updated_at: str


@dataclass
class UserListResult:
    items: list[UserRecord]
    total: int
    summary: dict[str, int]


class UserRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def _to_record(self, row: dict[str, Any]) -> UserRecord:
        return UserRecord(
            id=row["id"],
            username=row["username"],
            phone=row.get("phone"),
            email=row.get("email"),
            password_hash=row["password_hash"],
            display_name=row.get("display_name"),
            role=row["role"],
            status=row["status"],
            avatar_object_key=row.get("avatar_object_key"),
            last_login_at=row.get("last_login_at"),
            remark=row.get("remark"),
            token_version=int(row.get("token_version") or 0),
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
        display_name: str | None,
        role: str,
        status: str = "active",
        avatar_object_key: str | None = None,
    ) -> UserRecord:
        now = datetime.now(UTC).isoformat()
        user_id = str(uuid4())
        self._db.execute(
            text(
                """
                INSERT INTO users (
                    id, username, phone, email, password_hash, display_name,
                    role, status, avatar_object_key, token_version, last_login_at,
                    created_at, updated_at
                ) VALUES (
                    :id, :username, NULL, NULL, :password_hash, :display_name,
                    :role, :status, :avatar_object_key, 0, NULL, :created_at, :updated_at
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
                "avatar_object_key": avatar_object_key,
                "created_at": now,
                "updated_at": now,
            },
        )
        self._db.commit()
        user = self.get_by_id(user_id)
        assert user is not None
        return user

    def _build_filters(
        self,
        *,
        keyword: str | None,
        role: str | None,
        status: str | None,
        login_filter: str | None,
    ) -> tuple[str, dict[str, Any]]:
        clauses: list[str] = []
        params: dict[str, Any] = {}

        if keyword:
            clauses.append(
                """
                (
                  username LIKE :keyword
                  OR IFNULL(display_name, '') LIKE :keyword
                )
                """
            )
            params["keyword"] = f"%{keyword.strip()}%"

        if role:
            clauses.append("role = :role")
            params["role"] = role

        if status:
            clauses.append("status = :status")
            params["status"] = status

        if login_filter == "never_logged":
            clauses.append("last_login_at IS NULL")
        elif login_filter == "recent_7_days":
            cutoff = (datetime.now(UTC) - timedelta(days=7)).isoformat()
            clauses.append("last_login_at IS NOT NULL AND last_login_at >= :recent_cutoff")
            params["recent_cutoff"] = cutoff
        elif login_filter == "inactive_30_days":
            cutoff = (datetime.now(UTC) - timedelta(days=30)).isoformat()
            clauses.append("last_login_at IS NOT NULL AND last_login_at < :inactive_cutoff")
            params["inactive_cutoff"] = cutoff

        where_sql = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        return where_sql, params

    def list_users(
        self,
        *,
        page: int = 1,
        page_size: int = 10,
        keyword: str | None = None,
        role: str | None = None,
        status: str | None = None,
        login_filter: str | None = None,
    ) -> UserListResult:
        where_sql, params = self._build_filters(
            keyword=keyword,
            role=role,
            status=status,
            login_filter=login_filter,
        )
        offset = (page - 1) * page_size

        total = self._db.execute(
            text(f"SELECT COUNT(*) AS cnt FROM users {where_sql}"),
            params,
        ).scalar_one()

        rows = (
            self._db.execute(
                text(
                    f"""
                    SELECT * FROM users
                    {where_sql}
                    ORDER BY created_at DESC
                    LIMIT :limit OFFSET :offset
                    """
                ),
                {**params, "limit": page_size, "offset": offset},
            )
            .mappings()
            .all()
        )

        summary_row = self._db.execute(
            text(
                f"""
                SELECT
                  COUNT(*) AS filtered,
                  SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) AS active_count,
                  SUM(CASE WHEN status = 'disabled' THEN 1 ELSE 0 END) AS disabled_count
                FROM users
                {where_sql}
                """
            ),
            params,
        ).mappings().one()

        total_all = self._db.execute(text("SELECT COUNT(*) FROM users")).scalar_one()

        return UserListResult(
            items=[self._to_record(dict(row)) for row in rows],
            total=int(total),
            summary={
                "total": int(total_all),
                "filtered": int(summary_row["filtered"] or 0),
                "active_count": int(summary_row["active_count"] or 0),
                "disabled_count": int(summary_row["disabled_count"] or 0),
            },
        )

    def update_user(
        self,
        user_id: str,
        *,
        display_name: str | None = None,
        role: str | None = None,
        avatar_object_key: str | None = None,
        update_avatar: bool = False,
    ) -> UserRecord | None:
        user = self.get_by_id(user_id)
        if user is None:
            return None

        now = datetime.now(UTC).isoformat()
        new_display = display_name if display_name is not None else user.display_name
        new_role = role if role is not None else user.role
        new_avatar = avatar_object_key if update_avatar else user.avatar_object_key

        self._db.execute(
            text(
                """
                UPDATE users
                SET display_name = :display_name,
                    role = :role,
                    avatar_object_key = :avatar_object_key,
                    updated_at = :updated_at
                WHERE id = :id
                """
            ),
            {
                "id": user_id,
                "display_name": new_display,
                "role": new_role,
                "avatar_object_key": new_avatar,
                "updated_at": now,
            },
        )
        self._db.commit()
        return self.get_by_id(user_id)

    def update_profile(
        self,
        user_id: str,
        *,
        display_name: str,
        email: str | None,
        phone: str | None,
        remark: str | None,
        avatar_object_key: str | None,
    ) -> UserRecord | None:
        user = self.get_by_id(user_id)
        if user is None:
            return None

        now = datetime.now(UTC).isoformat()
        self._db.execute(
            text(
                """
                UPDATE users
                SET display_name = :display_name,
                    email = :email,
                    phone = :phone,
                    remark = :remark,
                    avatar_object_key = :avatar_object_key,
                    updated_at = :updated_at
                WHERE id = :id
                """
            ),
            {
                "id": user_id,
                "display_name": display_name,
                "email": email,
                "phone": phone,
                "remark": remark,
                "avatar_object_key": avatar_object_key,
                "updated_at": now,
            },
        )
        self._db.commit()
        return self.get_by_id(user_id)

    def change_password(self, user_id: str, password_hash: str) -> UserRecord | None:
        user = self.get_by_id(user_id)
        if user is None:
            return None
        now = datetime.now(UTC).isoformat()
        new_version = user.token_version + 1
        self._db.execute(
            text(
                """
                UPDATE users
                SET password_hash = :password_hash,
                    token_version = :token_version,
                    updated_at = :updated_at
                WHERE id = :id
                """
            ),
            {
                "id": user_id,
                "password_hash": password_hash,
                "token_version": new_version,
                "updated_at": now,
            },
        )
        self._db.commit()
        return self.get_by_id(user_id)

    def update_password(self, user_id: str, password: str) -> UserRecord | None:
        user = self.get_by_id(user_id)
        if user is None:
            return None
        now = datetime.now(UTC).isoformat()
        self._db.execute(
            text(
                """
                UPDATE users
                SET password_hash = :password_hash, updated_at = :updated_at
                WHERE id = :id
                """
            ),
            {
                "id": user_id,
                "password_hash": hash_password(password),
                "updated_at": now,
            },
        )
        self._db.commit()
        return self.get_by_id(user_id)

    def update_status(self, user_id: str, status: str) -> UserRecord | None:
        user = self.get_by_id(user_id)
        if user is None:
            return None
        now = datetime.now(UTC).isoformat()
        self._db.execute(
            text(
                """
                UPDATE users SET status = :status, updated_at = :updated_at WHERE id = :id
                """
            ),
            {"id": user_id, "status": status, "updated_at": now},
        )
        self._db.commit()
        return self.get_by_id(user_id)
