"""Remote credentials are server-managed and bound to backend-verified identities."""

import hashlib
import json
from dataclasses import replace
from pathlib import Path

from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict, Field, SecretStr

from src.mcp.workbuddy.adapters.api_client import BackendApiError, TilesFSTApiClient
from src.mcp.workbuddy.config import WorkBuddyConnectorConfig
from src.mcp.workbuddy.tools.registry import ToolRegistry


class Credential(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    backend_token: SecretStr
    scopes: list[str] = Field(default_factory=list)


def authenticate(config: WorkBuddyConnectorConfig, authorization: str | None) -> ToolRegistry:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "Connector credential required")
    if not config.remote_credentials_file:
        raise HTTPException(503, "Remote authentication is not configured")
    digest = hashlib.sha256(authorization[7:].encode()).hexdigest()
    try:
        document = json.loads(Path(config.remote_credentials_file).read_text())
        raw = document.get(digest)
        if raw is None:
            raise HTTPException(401, "Invalid connector credential")
        credential = Credential.model_validate(raw)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(503, "Remote authentication configuration unavailable") from None
    per_user = replace(
        config, api_token=credential.backend_token.get_secret_value(),
        write_scopes=config.write_scopes.intersection(credential.scopes),
    )
    client = TilesFSTApiClient(per_user)
    try:
        profile = client.get("/api/v1/auth/me").get("data", {})
    except BackendApiError as exc:
        status = 401 if exc.status_code in {401, 403} else 503
        raise HTTPException(status, "Backend identity verification failed") from None
    if not profile.get("id") or profile.get("role") not in {"admin", "employee"} or profile.get("status") != "active":
        raise HTTPException(403, "Backend management access required")
    if "catalog:read" not in credential.scopes:
        raise HTTPException(403, "Catalog read scope required")
    return ToolRegistry(client, per_user, principal=str(profile["id"]))
