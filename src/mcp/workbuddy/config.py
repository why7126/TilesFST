"""Configuration for the WorkBuddy MCP connector."""

from __future__ import annotations

import os
from dataclasses import dataclass


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _env_float(name: str, default: float) -> float:
    value = os.getenv(name)
    if value is None or not value.strip():
        return default
    try:
        return float(value)
    except ValueError:
        return default


def _env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None or not value.strip():
        return default
    try:
        return int(value)
    except ValueError:
        return default


@dataclass(frozen=True)
class WorkBuddyConnectorConfig:
    """Runtime settings for both stdio and HTTP MCP entrypoints."""

    api_base_url: str
    api_token: str | None
    timeout_seconds: float = 10.0
    enable_write_tools: bool = False
    write_scopes: frozenset[str] = frozenset()
    transport: str = "stdio"
    http_bearer_token: str | None = None
    rate_limit_per_minute: int = 60
    idempotency_dir: str = "data/workbuddy/idempotency"
    remote_credentials_file: str | None = None
    max_request_bytes: int = 8 * 1024 * 1024

    @property
    def safe_summary(self) -> dict[str, object]:
        return {
            "api_base_url": self.api_base_url,
            "api_token_configured": bool(self.api_token),
            "timeout_seconds": self.timeout_seconds,
            "enable_write_tools": self.enable_write_tools,
            "write_scopes": sorted(self.write_scopes),
            "transport": self.transport,
            "http_bearer_token_configured": bool(self.http_bearer_token),
            "rate_limit_per_minute": self.rate_limit_per_minute,
        }


def load_config() -> WorkBuddyConnectorConfig:
    base_url = os.getenv("TILESFST_API_BASE_URL", "http://localhost:8000").strip()
    base_url = base_url.rstrip("/")
    token = (
        os.getenv("TILESFST_CONNECTOR_TOKEN")
        or os.getenv("TILESFST_API_TOKEN")
        or None
    )
    scopes = frozenset(
        scope.strip()
        for scope in os.getenv("TILESFST_CONNECTOR_WRITE_SCOPES", "").split(",")
        if scope.strip()
    )
    return WorkBuddyConnectorConfig(
        api_base_url=base_url,
        api_token=token,
        timeout_seconds=_env_float("TILESFST_CONNECTOR_TIMEOUT_SECONDS", 10.0),
        enable_write_tools=_env_bool("TILESFST_CONNECTOR_ENABLE_WRITE_TOOLS", False),
        write_scopes=scopes,
        transport=os.getenv("TILESFST_CONNECTOR_TRANSPORT", "stdio").strip() or "stdio",
        http_bearer_token=os.getenv("TILESFST_CONNECTOR_HTTP_BEARER_TOKEN") or None,
        rate_limit_per_minute=_env_int("TILESFST_CONNECTOR_RATE_LIMIT_PER_MINUTE", 60),
        idempotency_dir=os.getenv("TILESFST_CONNECTOR_IDEMPOTENCY_DIR", "data/workbuddy/idempotency"),
        remote_credentials_file=os.getenv("TILESFST_CONNECTOR_REMOTE_CREDENTIALS_FILE") or None,
        max_request_bytes=max(1024, _env_int("TILESFST_CONNECTOR_MAX_REQUEST_BYTES", 8 * 1024 * 1024)),
    )
