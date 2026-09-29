"""Durable upload coordination. Callers own transactions and storage side effects."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from sqlalchemy import (
    BigInteger, CheckConstraint, Column, Index, Integer, MetaData, String, Table,
    Text, UniqueConstraint, select, update,
)
from sqlalchemy.engine import Connection
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy.dialects.mysql import insert as mysql_insert, VARCHAR
from sqlalchemy.orm import Session

metadata = MetaData()
upload_sessions = Table(
    "media_upload_sessions", metadata,
    Column("id", String(36), primary_key=True),
    Column("owner_id", String(64).with_variant(VARCHAR(64, collation="utf8mb4_bin"), "mysql"), nullable=False),
    Column("idempotency_key", String(128).with_variant(VARCHAR(128, collation="utf8mb4_bin"), "mysql"), nullable=False),
    Column("request_hash", String(64), nullable=False),
    Column("media_kind", String(32), nullable=False),
    Column("business_id", BigInteger),
    Column("expected_size", BigInteger, nullable=False),
    Column("mime_type", String(128), nullable=False),
    Column("part_size", Integer, nullable=False),
    Column("mode", String(16), nullable=False),
    Column("state", String(20), nullable=False),
    Column("version", Integer, nullable=False, server_default="0"),
    Column("temporary_key", String(512), nullable=False),
    Column("stable_key", String(512), nullable=False),
    Column("upload_id", String(512)),
    Column("source_version_id", String(256)),
    Column("stable_version_id", String(256)),
    Column("source_etag", String(128)),
    Column("actual_size", BigInteger),
    Column("actual_mime_type", String(128)),
    Column("integrity_hash", String(128)),
    Column("variants_json", Text),
    Column("object_versions_json", Text),
    Column("task_trace_id", String(64)),
    Column("error_code", String(64)),
    Column("bound_business_id", String(64)),
    Column("lease_token", String(36)),
    Column("lease_expires_at", String(32)),
    Column("expires_at", String(32), nullable=False),
    Column("created_at", String(32), nullable=False),
    Column("updated_at", String(32), nullable=False),
    UniqueConstraint("owner_id", "idempotency_key", name="uq_media_upload_owner_idem"),
    CheckConstraint("expected_size > 0 AND part_size > 0", name="ck_media_upload_sizes"),
    CheckConstraint("version >= 0", name="ck_media_upload_version"),
    CheckConstraint("state IN ('created','uploading','verifying','processing','ready','binding','bound','failed','cancelled','expired','cleaning','cleaned')", name="ck_media_upload_state"),
    Index("ix_media_upload_expiry", "state", "expires_at"),
    Index("ix_media_upload_business", "media_kind", "business_id"),
    Index("ix_media_upload_task", "task_trace_id"),
    mysql_engine="InnoDB", mysql_charset="utf8mb4", mysql_collate="utf8mb4_unicode_ci",
)


def ensure_upload_sessions(connection: Connection) -> None:
    """Additive, idempotent SQLite/MySQL migration; never touches business rows."""
    metadata.create_all(connection)


def utc_timestamp(now: datetime) -> str:
    if now.tzinfo is None:
        raise ValueError("Timezone-aware timestamp required")
    return now.astimezone(timezone.utc).isoformat(timespec="milliseconds")


class UploadSessionConflict(ValueError):
    pass


class UploadSessionNotFound(LookupError):
    pass


# Leased transitions must use claim/finish, never a blind status update.
LEASED_STATES = {"verifying", "processing", "binding", "cleaning"}
TRANSITIONS = {
    "created": {"uploading", "cancelled", "expired"},
    "uploading": {"verifying", "cancelled", "expired"},
    "verifying": {"ready", "processing", "failed", "cancelled"},
    "processing": {"ready", "failed", "cancelled"},
    "ready": {"binding", "cancelled", "cleaning"},
    "binding": {"bound", "ready", "failed"},
    "failed": {"verifying", "processing", "cancelled", "cleaning"},
    "cancelled": {"cleaning"}, "expired": {"cleaning"},
    "cleaning": {"cleaned"}, "bound": set(), "cleaned": set(),
}
RESULT_FIELDS = {
    "upload_id", "source_version_id", "stable_version_id", "source_etag",
    "actual_size", "actual_mime_type", "integrity_hash", "variants_json",
    "object_versions_json", "error_code", "bound_business_id", "task_trace_id", "stable_key",
}


class UploadSessionRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_idempotent(self, owner_id: str, idempotency_key: str) -> dict | None:
        row = self.db.execute(select(upload_sessions).where(
            upload_sessions.c.owner_id == owner_id,
            upload_sessions.c.idempotency_key == idempotency_key,
        )).mappings().one_or_none()
        return dict(row) if row is not None else None

    def get(self, session_id: str, owner_id: str) -> dict:
        row = self.db.execute(select(upload_sessions).where(
            upload_sessions.c.id == session_id, upload_sessions.c.owner_id == owner_id,
        )).mappings().one_or_none()
        if row is None:
            raise UploadSessionNotFound("Upload session not found")
        return dict(row)

    def create(self, *, owner_id: str, idempotency_key: str, media_kind: str,
               business_id: int | None, expected_size: int, mime_type: str,
               part_size: int, mode: str, temporary_key: str, stable_key: str,
               now: datetime, lifetime_seconds: int = 86400) -> dict:
        if expected_size <= 0 or part_size <= 0 or lifetime_seconds <= 0:
            raise ValueError("Invalid upload size or lifetime")
        if temporary_key == stable_key:
            raise ValueError("Temporary and stable objects must be isolated")
        fingerprint = hashlib.sha256(json.dumps(
            [media_kind, business_id, expected_size, mime_type], separators=(",", ":"),
        ).encode()).hexdigest()
        values = dict(id=str(uuid4()), owner_id=owner_id, idempotency_key=idempotency_key,
                      request_hash=fingerprint, media_kind=media_kind, business_id=business_id,
                      expected_size=expected_size, mime_type=mime_type, part_size=part_size,
                      mode=mode, state="created", version=0, task_trace_id="task_upload_" + uuid4().hex, temporary_key=temporary_key,
                      stable_key=stable_key, created_at=utc_timestamp(now),
                      updated_at=utc_timestamp(now), expires_at=utc_timestamp(now + timedelta(seconds=lifetime_seconds)))
        dialect = self.db.get_bind().dialect.name
        if dialect == "sqlite":
            statement = sqlite_insert(upload_sessions).values(**values).on_conflict_do_nothing(
                index_elements=["owner_id", "idempotency_key"],
            )
        elif dialect == "mysql":
            statement = mysql_insert(upload_sessions).values(**values).on_duplicate_key_update(
                id=upload_sessions.c.id,
            )
        else:
            raise ValueError("Unsupported upload session database")
        # A plain INSERT starts a real SQLite transaction. An outermost SAVEPOINT
        # in sqlite3 legacy transaction mode could otherwise commit before caller rollback.
        self.db.execute(statement)
        row = self.db.execute(select(upload_sessions).where(
            upload_sessions.c.owner_id == owner_id,
            upload_sessions.c.idempotency_key == idempotency_key,
        )).mappings().one()
        if row["request_hash"] != fingerprint:
            raise UploadSessionConflict("Idempotency key has different input")
        return dict(row)

    def move(self, row: dict, target: str, *, now: datetime) -> dict:
        if target in LEASED_STATES or row["state"] in LEASED_STATES:
            raise UploadSessionConflict("Leased operation requires claim or finish")
        return self._write(row, target, now=now)

    def claim(self, row: dict, target: str, *, now: datetime, lease_seconds: int = 120) -> dict:
        if target not in LEASED_STATES or lease_seconds <= 0:
            raise ValueError("Invalid lease")
        if row["state"] in LEASED_STATES and row["state"] != target:
            raise UploadSessionConflict("Cannot steal a different operation")
        if row["state"] == target:
            if not row["lease_expires_at"] or row["lease_expires_at"] > utc_timestamp(now):
                raise UploadSessionConflict("Operation lease is still active")
        return self._write(row, target, now=now, reclaim=row["state"] == target,
                           changes={"lease_token": str(uuid4()), "lease_expires_at": utc_timestamp(now + timedelta(seconds=lease_seconds))})

    def finish(self, row: dict, target: str, *, now: datetime, **changes) -> dict:
        if row["state"] not in LEASED_STATES or not row["lease_token"]:
            raise UploadSessionConflict("No operation lease")
        if row["lease_expires_at"] <= utc_timestamp(now):
            raise UploadSessionConflict("Operation lease expired")
        if target in LEASED_STATES:
            raise UploadSessionConflict("Finish before claiming the next operation")
        if "stable_key" in changes and (row["state"] != "binding" or target != "bound"):
            raise UploadSessionConflict("Only binding may formalize a stable key")
        if set(changes) - RESULT_FIELDS:
            raise ValueError("Invalid result fields")
        return self._write(row, target, now=now, changes={**changes, "lease_token": None, "lease_expires_at": None}, require_lease=True)

    def queue_processing(self, row: dict, *, now: datetime, metadata: dict, delay_seconds: int = 0) -> dict:
        """Release verification/processing into a durable queue without a live lease."""
        if row["state"] not in {"verifying", "processing", "failed"}:
            raise UploadSessionConflict("Upload cannot enter processing")
        if not row["stable_version_id"] or row["mime_type"] not in {"image/jpeg", "image/png", "image/webp"}:
            raise UploadSessionConflict("Verified image required")
        if delay_seconds < 0:
            raise ValueError("Invalid processing delay")
        return self._write(row, "processing", now=now, reclaim=row["state"] == "processing",
            require_lease=row["state"] in {"verifying", "processing"}, changes={
                "variants_json": json.dumps(metadata, separators=(",", ":")), "error_code": None,
                "lease_token": None,
                "lease_expires_at": utc_timestamp(now + timedelta(seconds=delay_seconds)),
            })

    def heartbeat(self, row: dict, *, now: datetime, lease_seconds: int = 120) -> dict:
        if row["state"] not in LEASED_STATES or not row["lease_token"] or lease_seconds <= 0:
            raise UploadSessionConflict("No valid lease")
        if row["lease_expires_at"] <= utc_timestamp(now):
            raise UploadSessionConflict("Operation lease expired")
        return self._write(row, row["state"], now=now, reclaim=True, require_lease=True,
                           changes={"lease_expires_at": utc_timestamp(now + timedelta(seconds=lease_seconds))})

    def reserve_initialization(self, row: dict, *, now: datetime) -> dict:
        """Fence multipart initiation without holding a DB lock across COS calls."""
        if row["state"] != "created" or row["expires_at"] <= utc_timestamp(now):
            raise UploadSessionConflict("Upload cannot be initialized")
        if row["lease_expires_at"] and row["lease_expires_at"] > utc_timestamp(now):
            raise UploadSessionConflict("Initialization is already running")
        return self._write(row, "created", now=now, reclaim=True, changes={
            "lease_token": str(uuid4()),
            "lease_expires_at": utc_timestamp(now + timedelta(seconds=120)),
        })

    def activate(self, row: dict, *, upload_id: str | None, now: datetime) -> dict:
        if row["state"] != "created" or not row["lease_token"]:
            raise UploadSessionConflict("Initialization lease required")
        return self._write(row, "uploading", now=now, require_lease=True, changes={
            "upload_id": upload_id, "lease_token": None, "lease_expires_at": None, "error_code": None,
        })

    def release_initialization(self, row: dict, *, now: datetime) -> dict:
        if row["state"] != "created" or not row["lease_token"]:
            raise UploadSessionConflict("Initialization lease required")
        return self._write(row, "created", now=now, reclaim=True, require_lease=True, changes={
            "lease_token": None, "lease_expires_at": None, "error_code": "50001",
        })

    def checkpoint(self, row: dict, *, now: datetime, **changes) -> dict:
        """Persist external-operation results before the next side effect."""
        if row["state"] not in LEASED_STATES or not row["lease_token"]:
            raise UploadSessionConflict("Operation lease required")
        if not changes or set(changes) - (RESULT_FIELDS - {"stable_key"}):
            raise ValueError("Invalid checkpoint fields")
        return self._write(row, row["state"], now=now, reclaim=True,
                           require_lease=True, changes=changes)

    def cancel(self, row: dict, *, now: datetime) -> dict:
        if row["state"] == "cancelled":
            return row
        # Cancellation invalidates verification/initialization workers, but never
        # interrupts a business binding or a cleaner that owns deletion rights.
        if row["state"] not in {"created", "uploading", "verifying", "processing", "ready", "failed"}:
            raise UploadSessionConflict("Upload can no longer be cancelled")
        return self._write(row, "cancelled", now=now, changes={
            "lease_token": None, "lease_expires_at": None,
        })

    def reserve_cleanup(self, row: dict, *, now: datetime) -> dict:
        """Only expired, unleased sessions are eligible; caller checks references."""
        if row["state"] == "bound" or row["expires_at"] > utc_timestamp(now):
            raise UploadSessionConflict("Upload remains protected")
        if row["lease_expires_at"] and row["lease_expires_at"] > utc_timestamp(now):
            raise UploadSessionConflict("Upload operation is still active")
        return self._write(row, "cleaning", now=now, reclaim=True, changes={
            "lease_token": str(uuid4()),
            "lease_expires_at": utc_timestamp(now + timedelta(seconds=120)),
        })

    def _write(self, row: dict, target: str, *, now: datetime, changes=None,
               reclaim=False, require_lease=False) -> dict:
        if not reclaim and target not in TRANSITIONS[row["state"]]:
            raise UploadSessionConflict("Invalid upload transition")
        stamp = utc_timestamp(now)
        if target in {"uploading", "verifying", "processing", "binding", "ready"} and row["expires_at"] <= stamp:
            raise UploadSessionConflict("Upload session expired")
        if target == "cleaning" and row["expires_at"] > stamp:
            raise UploadSessionConflict("Retention period has not elapsed")
        condition = [upload_sessions.c.id == row["id"], upload_sessions.c.owner_id == row["owner_id"],
                     upload_sessions.c.version == row["version"], upload_sessions.c.state == row["state"]]
        if require_lease:
            condition.extend([upload_sessions.c.lease_token == row["lease_token"], upload_sessions.c.lease_expires_at > stamp])
        result = self.db.execute(update(upload_sessions).where(*condition).values(
            state=target, version=row["version"] + 1, updated_at=stamp, **(changes or {}),
        ))
        if result.rowcount != 1:
            raise UploadSessionConflict("Upload session changed concurrently")
        return self.get(row["id"], row["owner_id"])
