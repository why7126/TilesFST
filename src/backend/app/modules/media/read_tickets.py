"""Media-only capabilities and bounded proxy capacity; access tokens cannot be reused."""
from contextlib import contextmanager
from datetime import UTC, datetime, timedelta
import hashlib

from jose import JWTError, jwt

from app.core.config import settings
from app.core.exceptions import AppError
from app.core.error_codes import MEDIA_READ_RATE_LIMIT
from app.modules.media.storage import MEDIA_NOT_FOUND

MEDIA_READ_LIMIT = MEDIA_READ_RATE_LIMIT
PROXY_MAX_BYTES = 64 * 1024 * 1024
PROXY_RANGE_BYTES = 4 * 1024 * 1024


def unavailable():
    return AppError(status_code=404, code=MEDIA_NOT_FOUND, message="媒体不可用")


def key_hash(key):
    return hashlib.sha256(key.encode()).hexdigest()


def make_ticket(reference, key, method, actor=None):
    now = datetime.now(UTC)
    payload = {"aud": "media-proxy", "purpose": "media-read", "method": method,
               "reference": reference.model_dump(), "key_hash": key_hash(key),
               "iat": now, "exp": now + timedelta(seconds=300)}
    if actor:
        payload.update(actor_id=actor.id, token_version=actor.token_version)
    return jwt.encode(payload, settings.app_secret_key, algorithm=settings.jwt_algorithm)


def decode_ticket(token, method):
    try:
        claims = jwt.decode(token, settings.app_secret_key, algorithms=[settings.jwt_algorithm], audience="media-proxy",
                            options={"require_exp": True, "require_iat": True, "require_aud": True})
        if claims.get("purpose") != "media-read" or claims.get("method") != method:
            raise unavailable()
        if claims["exp"] - claims["iat"] > 300:
            raise unavailable()
        return claims
    except (JWTError, ValueError, TypeError, KeyError):
        raise unavailable() from None


class SharedProxyBudget:
    """Two flock slots plus a durable byte ledger shared by same-host replicas.

    Never delete/replace these files while workers run: locks refer to their inodes.
    Container replicas must mount the same local filesystem; cross-host NFS is unsupported.
    """
    @contextmanager
    def claim(self, size):
        import fcntl
        import json
        import os
        from pathlib import Path
        from time import time
        limit = lambda: AppError(status_code=429, code=MEDIA_READ_LIMIT, message="媒体读取繁忙，请稍后重试")
        if size < 0 or size > PROXY_MAX_BYTES:
            raise limit()
        slot = None
        try:
            directory = Path(settings.media_read_proxy_budget_dir)
            directory.mkdir(parents=True, exist_ok=True)
            for index in range(2):
                candidate = open(directory / f"slot-{index}.lock", "a+b")
                try:
                    fcntl.flock(candidate, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    slot = candidate
                    break
                except BlockingIOError:
                    candidate.close()
            if slot is None:
                raise limit()
            existed = (directory / "bytes.json").exists()
            with open(directory / "bytes.json", "a+b") as ledger:
                fcntl.flock(ledger, fcntl.LOCK_EX | fcntl.LOCK_NB)
                ledger.seek(0)
                raw = ledger.read(1024)
                if not raw and existed:
                    raise ValueError("Incomplete budget ledger")
                state = json.loads(raw) if raw else {"started": time(), "bytes": 0}
                if not isinstance(state.get("bytes"), int) or state["bytes"] < 0:
                    raise ValueError("Invalid budget ledger")
                if time() - state["started"] >= 60:
                    state = {"started": time(), "bytes": 0}
                if state["bytes"] + size > 128 * 1024 * 1024:
                    raise limit()
                state["bytes"] += size
                ledger.seek(0); ledger.truncate()
                ledger.write(json.dumps(state).encode()); ledger.flush(); os.fsync(ledger.fileno())
        except (OSError, ValueError, TypeError, KeyError):
            if slot is not None:
                slot.close()
            raise limit() from None
        except Exception:
            if slot is not None:
                slot.close()
            raise
        try:
            yield
        finally:
            slot.close()


proxy_budget = SharedProxyBudget()
