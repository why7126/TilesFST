"""Run isolated, destructive-to-synthetic-data-only MCP acceptance with real services."""

from __future__ import annotations

import argparse
import base64
from concurrent.futures import ThreadPoolExecutor
import io
import json
import os
from pathlib import Path
import re
import secrets
import sqlite3
import subprocess
import sys
import time
from urllib.request import Request, urlopen


BASE = "http://backend:8000"
CHECKS: list[str] = []
REQUESTS: list[dict] = []


def check(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    CHECKS.append(name)


def http(path: str, payload: dict | None = None, token: str | None = None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    body = json.dumps(payload).encode() if payload is not None else None
    with urlopen(Request(BASE + path, data=body, headers=headers), timeout=60) as response:
        return json.load(response)


def mcp(name: str, args: dict, *, token: str | None = None, scopes: str | None = None) -> dict:
    env = os.environ.copy()
    # The evidence driver needs these; the MCP process must only receive an API token.
    for key in ("ADMIN_INITIAL_PASSWORD", "OBJECT_STORAGE_SECRET_KEY"):
        env.pop(key, None)
    if token is not None:
        env["TILESFST_CONNECTOR_TOKEN"] = token
    if scopes is not None:
        env["TILESFST_CONNECTOR_WRITE_SCOPES"] = scopes
    messages = [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
            "protocolVersion": "2024-11-05", "capabilities": {},
            "clientInfo": {"name": "isolated-acceptance", "version": "1"},
        }},
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
        {"jsonrpc": "2.0", "id": 3, "method": "tools/list"},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/call",
         "params": {"name": name, "arguments": args}},
    ]
    process = subprocess.run(
        [sys.executable, "-m", "src.mcp.workbuddy.server"], env=env,
        input="\n".join(json.dumps(item) for item in messages) + "\n",
        capture_output=True, text=True, timeout=120,
    )
    if process.returncode:
        kinds = re.findall(r"^([A-Za-z]+Error):", process.stderr, re.MULTILINE)
        frames = re.findall(r'File "([^"]+)", line (\d+)', process.stderr)
        location = ",".join(f"{Path(path).name}:{line}" for path, line in frames)
        raise AssertionError(f"stdio_exit:{process.returncode}:{name}:{','.join(kinds)}:{location}")
    check("stdio_exit", True)
    responses = [json.loads(line) for line in process.stdout.splitlines()]
    listed = next(item["result"]["tools"] for item in responses if item.get("id") == 3)
    check("tool_discovery", name in {item["name"] for item in listed})
    result = next(item["result"] for item in responses if item.get("id") == 2)
    value = json.loads(result["content"][0]["text"])
    check("mcp_error_flag", result["isError"] == (value.get("ok") is False))
    for forbidden in (env["TILESFST_CONNECTOR_TOKEN"], os.environ["ADMIN_INITIAL_PASSWORD"],
                      os.environ["OBJECT_STORAGE_SECRET_KEY"], "PRIVATE-PAYLOAD-MARKER"):
        check("audit_secret_absent", forbidden not in process.stderr)
    if value.get("client_request_id"):
        REQUESTS.append({"tool": name, "client_request_id": value["client_request_id"],
                         "authenticated": token is None,
                         "trace": (value.get("data") or {}).get("task_trace_id")})
    return value


def write(name: str, **kwargs) -> dict:
    result = mcp(name, {"confirmed": True, "idempotency_key": secrets.token_hex(16), **kwargs})
    check(name + ":success:" + str(result.get("error", "")), result.get("ok") is True)
    return result["data"]


def db():
    connection = sqlite3.connect("file:/evidence/acceptance.db?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    return connection


def verify_request_links():
    # Middleware commits after the response; allow a bounded persistence delay.
    deadline = time.monotonic() + 10
    while True:
        with db() as connection:
            rows = {row["client_request_id"]: dict(row) for row in connection.execute(
                "SELECT * FROM request_logs WHERE client_type = 'workbuddy_connector'"
            )}
        if all(item["client_request_id"] in rows for item in REQUESTS):
            break
        if time.monotonic() > deadline:
            raise AssertionError("request_logs_persisted")
        time.sleep(.1)
    with db() as connection:
        for item in REQUESTS:
            row = rows[item["client_request_id"]]
            if item["authenticated"]:
                check("request_identity", row["actor_user_id"] is not None)
            else:
                check("unauthenticated_request_denied", row["status_code"] == 401)
            if item["trace"]:
                trace = connection.execute(
                    "SELECT * FROM task_traces WHERE task_trace_id = ?", (item["trace"],)
                ).fetchone()
                check("trace_request_link", trace is not None and
                      trace["parent_request_id"] == row["request_id"])
                count = connection.execute(
                    "SELECT count(*) FROM task_trace_spans WHERE task_trace_id = ?",
                    (item["trace"],),
                ).fetchone()[0]
                check("trace_spans_persisted", count > 0)
            if row["method"] in {"POST", "PUT"} and row["path"].startswith("/api/v1/admin/"):
                trace = connection.execute(
                    "SELECT task_trace_id FROM task_traces WHERE parent_request_id = ?",
                    (row["request_id"],),
                ).fetchone()
                check("every_write_has_trace", trace is not None)
                count = connection.execute(
                    "SELECT count(*) FROM task_trace_spans WHERE task_trace_id = ?",
                    (trace["task_trace_id"],),
                ).fetchone()[0]
                check("every_write_has_spans", count > 0)
        for table in ("request_logs", "task_traces", "task_trace_spans"):
            records = json.dumps([dict(row) for row in connection.execute(f"SELECT * FROM {table}")])
            for secret in (os.environ["TILESFST_CONNECTOR_TOKEN"],
                           os.environ["ADMIN_INITIAL_PASSWORD"], "PRIVATE-PAYLOAD-MARKER"):
                check("persisted_logs_redacted", secret not in records)
        check("no_fabricated_usage", connection.execute(
            "SELECT count(*) FROM usage_events WHERE client_type = 'workbuddy_connector'"
        ).fetchone()[0] == 0)


def verify_object(data: dict):
    from minio import Minio
    # The backend-issued media URL is authoritative; never invent a business object path.
    path = data["url"]
    check("backend_media_url", path.startswith("/media/"))
    key = path.removeprefix("/media/")
    storage = Minio("storage:9000", access_key="acceptance",
                    secret_key=os.environ["OBJECT_STORAGE_SECRET_KEY"], secure=False)
    info = storage.stat_object("acceptance", key)
    with urlopen(BASE + path, timeout=30) as response:
        content = response.read()
        check("object_url_bytes", len(content) == info.size)
    return {"object_key": key, "url": path, "is_main": True, "sort_order": 1}


def worker(resume: bool):
    check("isolated_backend_only", os.environ.get("TILESFST_API_BASE_URL") == BASE)
    deadline = time.monotonic() + 90
    while True:
        try:
            http("/health")
            break
        except Exception:
            if time.monotonic() > deadline:
                raise AssertionError("isolated_backend_health") from None
            time.sleep(1)
    token = http("/api/v1/auth/login", {
        "username": "acceptance-admin", "password": os.environ["ADMIN_INITIAL_PASSWORD"]
    })["data"]["access_token"]
    os.environ["TILESFST_CONNECTOR_TOKEN"] = token
    memo = Path("/journal/acceptance.json")
    if resume:
        state = json.loads(memo.read_text())
        check("duplicate_after_container_restart", mcp("create_tile_sku", state["args"])
              .get("error") == "duplicate_operation")
        detail = mcp("get_tile_sku_detail", {"sku_id": state["sku_id"]})
        check("database_survives_restart", detail.get("ok") is True)
        verify_object(state["media"])
        verify_request_links()
        return

    from PIL import Image
    image = io.BytesIO()
    Image.new("RGB", (64, 64), (20, 120, 80)).save(image, format="PNG")
    png = image.getvalue()
    spec = http("/api/v1/admin/tile-specs", {
        "width_mm": 600, "length_mm": 600, "sort_order": 1,
    }, token)["data"]
    ids = {}
    for tool, id_key, name in (("manage_brand", "brand_id", "Acceptance Brand"),
                               ("manage_category", "category_id", "Acceptance")):
        created = write(tool, operation="create", payload={"name": name, "sort_order": 1})
        ids[id_key] = created["id"]
        write(tool, operation="update", **{id_key: created["id"]},
              payload={"name": name + "2", "sort_order": 2})
        disabled = write(tool, operation="disable", **{id_key: created["id"]})
        check(tool + ":disabled", disabled["status"] == "DISABLED")
        enabled = write(tool, operation="enable", **{id_key: created["id"]})
        check(tool + ":enabled", enabled["status"] == "ENABLED")

    payload = {"name": "Acceptance SKU", "save_mode": "draft", **ids,
               "spec_id": spec["id"], "surface_finish": "POLISHED"}
    args = {"payload": payload, "confirmed": True, "idempotency_key": secrets.token_hex(16)}
    check("missing_scope_rejected", mcp("create_tile_sku", args, scopes="catalog:read")
          .get("error") == "missing_scope")
    check("invalid_identity_rejected", mcp("search_tile_skus", {}, token="invalid-synthetic-token")
          .get("ok") is False)
    preview = mcp("preview_create_tile_sku", {"payload": payload})
    check("draft_preview", preview.get("side_effects") is False)
    for bad in ({**args, "confirmed": False}, {**args, "payload": {}},
                {**args, "unexpected": True}):
        check("invalid_write_rejected", mcp("create_tile_sku", bad).get("ok") is False)
    with db() as connection:
        check("preview_invalid_no_sku", connection.execute("SELECT count(*) FROM tiles").fetchone()[0] == 0)
    results = []
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(lambda _: mcp("create_tile_sku", args), range(4)))
    check("concurrent_single_write", sum(item.get("ok") is True for item in results) == 1)
    sku = next(item["data"] for item in results if item.get("ok"))
    check("duplicate_new_process", mcp("create_tile_sku", args).get("error") == "duplicate_operation")
    check("conflicting_key", mcp("create_tile_sku", {
        **args, "payload": {**payload, "name": "Conflict"}
    }).get("error") == "idempotency_conflict")
    with db() as connection:
        check("one_database_effect", connection.execute("SELECT count(*) FROM tiles").fetchone()[0] == 1)

    media = {}
    # Video is a synthetic transport fixture, not evidence of browser playback or transcoding.
    video = b"\x00\x00\x00\x18ftypmp42\x00\x00\x00\x00mp42isom"
    for target, mime, content in (("tile_image", "image/png", png),
                                  ("brand_logo", "image/png", png),
                                  ("brand_certificate", "image/png", png),
                                  ("tile_video", "video/mp4", video)):
        data = write("upload_tile_media", target=target, content_type=mime,
                     file_name="synthetic.png" if mime == "image/png" else "synthetic.mp4",
                     tile_id=sku["id"], base64_content=base64.b64encode(content).decode())
        verify_object(data)
        media[target] = data
    image_input = verify_object(media["tile_image"])
    write("update_tile_sku", sku_id=sku["id"], payload={
        "name": "Acceptance Edited", "images": [image_input], "remark": "PRIVATE-PAYLOAD-MARKER",
    })
    published = write("set_tile_sku_status", sku_id=sku["id"], target_status="PUBLISHED")
    check("sku_published", published["status"] == "PUBLISHED")
    disabled = write("set_tile_sku_status", sku_id=sku["id"], target_status="DISABLED")
    check("sku_unpublished", disabled["status"] == "DISABLED")
    for name, params in (
        ("search_tile_skus", {"page_size": 5}), ("get_tile_sku_detail", {"sku_id": sku["id"]}),
        ("list_tile_brands", {}), ("list_tile_categories", {}), ("summarize_catalog", {"sample_size": 5}),
    ):
        check(name + ":read_success", mcp(name, params).get("ok") is True)

    def business_snapshot():
        from minio import Minio
        storage = Minio("storage:9000", access_key="acceptance",
                        secret_key=os.environ["OBJECT_STORAGE_SECRET_KEY"], secure=False)
        with db() as connection:
            counts = tuple(connection.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
                           for table in ("tiles", "brands", "tile_categories"))
        return counts, sorted(obj.object_name for obj in storage.list_objects("acceptance", recursive=True))

    before = business_snapshot()
    for name, params in (
        ("preview_create_tile_sku", {"payload": {}}),
        ("preview_update_tile_sku", {"sku_id": sku["id"], "payload": {"name": "Preview only"}}),
        ("preview_publish_tile_sku", {"sku_id": sku["id"], "target_status": "DISABLED"}),
        ("preview_manage_brand", {"operation": "create", "payload": {}}),
        ("preview_manage_category", {"operation": "create", "payload": {}}),
        ("preview_media_upload", {"target": "tile_image", "file_name": "preview.png",
                                  "content_type": "image/png", "file_size_bytes": len(png)}),
    ):
        check(name + ":dry_run", mcp(name, params).get("side_effects") is False)
    check("all_previews_no_business_or_storage_effect", before == business_snapshot())
    detail = mcp("get_tile_sku_detail", {"sku_id": sku["id"]})["data"]
    check("previews_no_status_or_field_change", detail["status"] == "DISABLED" and detail["name"] == "Acceptance Edited")

    for target, mime, seed in (("tile_image", "image/png", png),
                               ("brand_logo", "image/png", png),
                               ("brand_certificate", "image/png", png),
                               ("tile_video", "video/mp4", video)):
        boundary = seed + b"\0" * (1024 * 1024 - len(seed))
        upload_args = {"target": target, "content_type": mime,
                       "file_name": "boundary.png" if mime == "image/png" else "boundary.mp4",
                       "tile_id": sku["id"], "confirmed": True}
        exact = write("upload_tile_media", **{k: v for k, v in upload_args.items() if k != "confirmed"},
                      base64_content=base64.b64encode(boundary).decode())
        verify_object(exact)
        for suffix, body, content_type in (("over_limit", boundary + b"x", mime),
                                           ("invalid_mime", b"synthetic", "application/x-test")):
            bad = mcp("upload_tile_media", {**upload_args, "content_type": content_type,
                "base64_content": base64.b64encode(body).decode(), "idempotency_key": secrets.token_hex(16)})
            check(target + ":" + suffix, bad.get("ok") is False)
            if suffix == "over_limit":
                # A known backend failure must not automatically retry an ambiguous reservation.
                repeat_args = {**upload_args, "base64_content": base64.b64encode(body).decode(),
                               "idempotency_key": secrets.token_hex(16)}
                check("backend_size_failure", mcp("upload_tile_media", repeat_args).get("ok") is False)
                check("failed_attempt_no_retry", mcp("upload_tile_media", repeat_args)
                      .get("error") == "operation_uncertain")
    for patch in ({"file_name": "missing-extension"}, {"file_name": "mismatch.exe"},
                  {"file_name": "../image.png"}, {"base64_content": ""}, {"base64_content": "!invalid!"}):
        before = len(REQUESTS)
        rejected = mcp("upload_tile_media", {
            "target": "tile_image", "content_type": "image/png", "file_name": "fixture.png",
            "base64_content": base64.b64encode(png).decode(), "confirmed": True,
            "idempotency_key": secrets.token_hex(16), **patch,
        })
        check("invalid_media_no_backend", rejected.get("error") == "invalid_media" and len(REQUESTS) == before)
    verify_request_links()
    # Only synthetic replay inputs and backend-issued media references persist here.
    memo.write_text(json.dumps({"args": args, "sku_id": sku["id"], "media": media["tile_image"]}))
    os.chmod(memo, 0o600)


def orchestrate():
    root = Path(__file__).resolve().parents[2]
    project = "wb-req0132-" + secrets.token_hex(4)
    env = {key: value for key, value in os.environ.items()
           if not key.startswith(("COMPOSE_", "TILESFST_", "OBJECT_STORAGE_"))}
    env.update(APP_SECRET_KEY=secrets.token_urlsafe(40),
               ADMIN_INITIAL_PASSWORD=secrets.token_urlsafe(24),
               OBJECT_STORAGE_SECRET_KEY=secrets.token_urlsafe(32))
    command = ["docker", "compose", "--env-file", os.devnull, "-p", project,
               "-f", str(root / "deploy/local/compose.workbuddy-acceptance.yml")]
    print(json.dumps({"project": project, "scope": "isolated-local-stdio-real-backend-minio"}), flush=True)

    def run(*args, report=False):
        result = subprocess.run([*command, *args], env=env, capture_output=True, text=True, timeout=300)
        # Never print raw Compose output, environment, HTTP payloads or tracebacks.
        if report:
            for line in result.stdout.splitlines():
                try:
                    value = json.loads(line)
                except ValueError:
                    continue
                if "checks" in value or "failed_check" in value:
                    print(json.dumps(value), flush=True)
        if result.returncode:
            raise RuntimeError("acceptance stage failed: " + args[0])

    try:
        run("up", "-d", "backend", "storage")
        run("run", "--rm", "acceptance", report=True)
        run("restart", "backend", "storage")
        run("run", "--rm", "acceptance", "--resume", report=True)
        print(json.dumps({"result": "passed", "persistent_volumes_retained": True}), flush=True)
    finally:
        run("down")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--resume", action="store_true", help=argparse.SUPPRESS)
    options = parser.parse_args()
    try:
        if options.worker:
            worker(options.resume)
            print(json.dumps({"phase": "restart" if options.resume else "writes", "checks": len(CHECKS),
                              "assertions": sorted(set(CHECKS)), "requests": len(REQUESTS)}))
        else:
            orchestrate()
    except Exception as exc:
        # Assertion names are controlled constants, never exception/response bodies.
        safe = str(exc) if isinstance(exc, AssertionError) else type(exc).__name__
        print(json.dumps({"failed_check": safe, "checks": len(CHECKS)}), flush=True)
        sys.exit(1)
