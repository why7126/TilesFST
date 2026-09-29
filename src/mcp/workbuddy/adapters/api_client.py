"""Small HTTP adapter used by WorkBuddy MCP tools."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from src.mcp.workbuddy.adapters.audit import CLIENT_TYPE, new_client_request_id, redact_payload
from src.mcp.workbuddy.config import WorkBuddyConnectorConfig


class BackendApiError(RuntimeError):
    def __init__(
        self,
        *,
        status_code: int | None,
        message: str,
        error_code: str | None = None,
        client_request_id: str | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.error_code = error_code
        self.client_request_id = client_request_id

    def to_safe_dict(self) -> dict[str, object | None]:
        return {
            "status_code": self.status_code,
            "error_code": self.error_code,
            "message": str(self),
            "client_request_id": self.client_request_id,
        }


@dataclass
class TilesFSTApiClient:
    config: WorkBuddyConnectorConfig
    last_client_request_id: str | None = field(default=None, init=False)

    def get(self, path: str, query: dict[str, object | None] | None = None) -> dict[str, Any]:
        return self.request("GET", path, query=query)

    def post(
        self,
        path: str,
        *,
        json_body: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
        task_type: str | None = None,
    ) -> dict[str, Any]:
        return self.request(
            "POST",
            path,
            json_body=json_body,
            idempotency_key=idempotency_key,
            task_type=task_type,
        )

    def put(
        self,
        path: str,
        *,
        json_body: dict[str, Any],
        idempotency_key: str | None = None,
        task_type: str | None = None,
    ) -> dict[str, Any]:
        return self.request(
            "PUT",
            path,
            json_body=json_body,
            idempotency_key=idempotency_key,
            task_type=task_type,
        )

    def upload_file(
        self,
        path: str,
        *,
        file_bytes: bytes,
        file_name: str,
        content_type: str,
        query: dict[str, object | None] | None = None,
        idempotency_key: str | None = None,
        task_type: str | None = None,
    ) -> dict[str, Any]:
        boundary = f"tilesfst-workbuddy-{new_client_request_id()}"
        body = self._multipart_body(boundary, file_bytes, file_name, content_type)
        headers = {"content-type": f"multipart/form-data; boundary={boundary}"}
        return self.request(
            "POST",
            path,
            query=query,
            raw_body=body,
            extra_headers=headers,
            idempotency_key=idempotency_key,
            task_type=task_type,
        )

    def request(
        self,
        method: str,
        path: str,
        *,
        query: dict[str, object | None] | None = None,
        json_body: dict[str, Any] | None = None,
        raw_body: bytes | None = None,
        extra_headers: dict[str, str] | None = None,
        idempotency_key: str | None = None,
        task_type: str | None = None,
    ) -> dict[str, Any]:
        safe_path = self._safe_path(path)
        client_request_id = new_client_request_id()
        self.last_client_request_id = client_request_id
        url = f"{self.config.api_base_url}{safe_path}"
        query_string = self._query_string(query)
        if query_string:
            url = f"{url}?{query_string}"

        headers = {
            "accept": "application/json",
            "user-agent": "ProjectTilesFST-WorkBuddy-MCP/0.1",
            "x-client-type": CLIENT_TYPE,
            "x-client-request-id": client_request_id,
        }
        if self.config.api_token:
            headers["authorization"] = f"Bearer {self.config.api_token}"
        if idempotency_key:
            headers["x-idempotency-key"] = idempotency_key
        if task_type:
            headers["x-task-type"] = task_type
        if extra_headers:
            headers.update(extra_headers)

        body: bytes | None = raw_body
        if json_body is not None:
            body = json.dumps(json_body, ensure_ascii=False).encode("utf-8")
            headers["content-type"] = "application/json"

        req = Request(url, data=body, headers=headers, method=method.upper())
        try:
            with urlopen(req, timeout=self.config.timeout_seconds) as response:
                payload = response.read().decode("utf-8")
                return self._decode_response(payload, client_request_id)
        except HTTPError as exc:
            payload = exc.read().decode("utf-8", errors="replace")
            raise self._api_error(exc.code, payload, client_request_id) from exc
        except URLError as exc:
            raise BackendApiError(
                status_code=None,
                message="ProjectTilesFST API is not reachable",
                client_request_id=client_request_id,
            ) from exc

    def _safe_path(self, path: str) -> str:
        if "://" in path or ".." in path or not path.startswith(("/api/v1/", "/health")):
            raise ValueError("connector path must target a ProjectTilesFST API route")
        return path

    def _query_string(self, query: dict[str, object | None] | None) -> str:
        if not query:
            return ""
        normalized: dict[str, object] = {
            key: value for key, value in query.items() if value is not None and value != ""
        }
        return urlencode(normalized)

    def _decode_response(self, payload: str, client_request_id: str) -> dict[str, Any]:
        if not payload:
            return {"data": None, "client_request_id": client_request_id}
        decoded = json.loads(payload)
        if isinstance(decoded, dict):
            decoded.setdefault("client_request_id", client_request_id)
            return decoded
        return {"data": decoded, "client_request_id": client_request_id}

    def _api_error(
        self, status_code: int, payload: str, client_request_id: str
    ) -> BackendApiError:
        message = "ProjectTilesFST API request failed"
        error_code: str | None = None
        try:
            decoded = json.loads(payload)
        except json.JSONDecodeError:
            decoded = {}
        if isinstance(decoded, dict):
            error_code = str(decoded.get("code") or decoded.get("error_code") or "") or None
            message = "后端请求失败，请根据错误码和请求编号排查。"
        return BackendApiError(
            status_code=status_code,
            message=message,
            error_code=error_code,
            client_request_id=client_request_id,
        )

    def _multipart_body(
        self, boundary: str, file_bytes: bytes, file_name: str, content_type: str
    ) -> bytes:
        if any(character in file_name + content_type for character in '\r\n"'):
            raise ValueError("Invalid multipart metadata")
        safe_name = file_name.rsplit("/", 1)[-1].rsplit("\\", 1)[-1] or "upload.bin"
        parts = [
            f"--{boundary}\r\n".encode("utf-8"),
            (
                'Content-Disposition: form-data; name="file"; '
                f'filename="{safe_name}"\r\n'
            ).encode("utf-8"),
            f"Content-Type: {content_type}\r\n\r\n".encode("utf-8"),
            file_bytes,
            b"\r\n",
            f"--{boundary}--\r\n".encode("utf-8"),
        ]
        return b"".join(parts)


def unwrap_data(response: dict[str, Any]) -> Any:
    if "data" in response:
        return response["data"]
    return response


def safe_error_result(error: BackendApiError) -> dict[str, object | None]:
    safe = error.to_safe_dict()
    if safe["error_code"] is not None and not re.fullmatch(r"[0-9]{3,8}", str(safe["error_code"])):
        safe["error_code"] = "backend_error"
    safe["message"] = "后端请求失败，请根据错误码和请求编号排查。"
    return {"ok": False, "error": redact_payload(safe)}
