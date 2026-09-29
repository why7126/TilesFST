"""Audit and redaction helpers for connector calls."""

from __future__ import annotations

import hashlib
from uuid import uuid4

CLIENT_TYPE = "workbuddy_connector"
CLIENT_REQUEST_ID_PREFIX = "wb"
SENSITIVE_KEYS = {
    "authorization",
    "cookie",
    "password",
    "secret",
    "token",
    "access_token",
    "refresh_token",
    "object_key",
    "raw_object_key",
    "file_name",
    "filename",
    "internal_path",
}


def new_client_request_id() -> str:
    return f"{CLIENT_REQUEST_ID_PREFIX}_{uuid4().hex[:24]}"


def fingerprint(value: str | None) -> str | None:
    if not value:
        return None
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:12]


def redact_payload(value: object) -> object:
    if isinstance(value, dict):
        redacted: dict[str, object] = {}
        for key, item in value.items():
            if key.lower() in SENSITIVE_KEYS:
                redacted[key] = "[redacted]"
            else:
                redacted[key] = redact_payload(item)
        return redacted
    if isinstance(value, list):
        return [redact_payload(item) for item in value]
    return value
