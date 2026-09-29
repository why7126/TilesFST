"""Durable local write reservations; never store credentials or business payloads."""

import hashlib
import json
import os
from pathlib import Path
from typing import Callable


class WriteJournal:
    def __init__(self, directory: str):
        self.directory = Path(directory)

    def execute(self, principal: str, key: str, tool: str, arguments: dict, call: Callable) -> dict:
        digest = hashlib.sha256(json.dumps(
            {"tool": tool, "arguments": arguments}, sort_keys=True, separators=(",", ":"),
        ).encode()).hexdigest()
        identity = hashlib.sha256(f"{principal}\0{key}".encode()).hexdigest()
        self.directory.mkdir(parents=True, exist_ok=True, mode=0o700)
        reservation = self.directory / identity
        try:
            reservation.mkdir(mode=0o700)
        except FileExistsError:
            try:
                recorded = json.loads((reservation / "state.json").read_text())
            except (OSError, ValueError):
                return {"ok": False, "error": "operation_uncertain", "operation_ref": identity}
            if recorded["digest"] != digest:
                return {"ok": False, "error": "idempotency_conflict", "operation_ref": identity}
            return {
                "ok": False, "error": "duplicate_operation" if recorded["state"] == "completed" else "operation_uncertain",
                "operation_ref": identity, "state": recorded["state"],
                "message": "未重复执行。请查询业务对象或审计记录核对结果，不要自动更换幂等键。",
            }
        fd = os.open(self.directory, os.O_RDONLY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)
        self._persist(reservation, {"digest": digest, "state": "pending"})
        # Any crash or ambiguous backend outcome leaves a reservation that blocks retries.
        result = call()
        state = "completed" if result.get("ok") is True else "uncertain"
        self._persist(reservation, {"digest": digest, "state": state})
        return {**result, "operation_ref": identity}

    def _persist(self, directory: Path, record: dict) -> None:
        temporary = directory / "state.tmp"
        fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w") as stream:
            json.dump(record, stream)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, directory / "state.json")
        fd = os.open(directory, os.O_RDONLY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)
