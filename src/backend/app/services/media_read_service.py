"""Bounded authorization and metadata probing, with no object-byte downloads."""

from datetime import UTC, datetime, timedelta
from pathlib import PurePosixPath
from urllib.parse import unquote, urlsplit

from app.core.config import settings
from app.core.error_codes import STORAGE_UNAVAILABLE
from app.core.exceptions import AppError
from app.modules.media.key_migration import map_legacy_object_key
from app.modules.media.read_tickets import make_ticket
from app.modules.media.storage import MEDIA_NOT_FOUND, get_media_storage_client, media_variant_object_key, resolve_media_path
from app.repositories.media_read_repository import MediaReadRepository
from app.repositories.user_repository import UserRecord
from app.schemas.media_read import MediaReadData, MediaReadDescriptor, MediaReadError, MediaReadItem, MediaReadRequest

READ_TTL_SECONDS = 300


def owned_object_key(reference: str) -> str | None:
    """Normalize configured storage URLs only; no domain inferred from request input."""
    parsed = urlsplit(reference)
    if not parsed.scheme and not parsed.netloc:
        return str(resolve_media_path(reference.removeprefix("/media/")))
    endpoint = settings.effective_object_storage_endpoint()
    configured = urlsplit(endpoint if "://" in endpoint else f"https://{endpoint}")
    bucket = settings.effective_object_storage_bucket()
    if parsed.scheme not in {"http", "https"} or parsed.username or parsed.password:
        return None
    path = unquote(parsed.path).lstrip("/")
    if parsed.netloc == configured.netloc and path.startswith(f"{bucket}/"):
        return str(resolve_media_path(path[len(bucket) + 1:]))
    if parsed.netloc == f"{bucket}.{configured.netloc}":
        return str(resolve_media_path(path))
    return None


def media_candidates(key: str, variant: str, is_image: bool) -> list[tuple[str, str]]:
    """Keep variants tied to one stored original; only known legacy mappings are tried."""
    key = str(resolve_media_path(key.removeprefix("/media/")))
    variants = {"thumbnail": ["thumbnail", "display", "original"], "display": ["display", "original"], "original": ["original"]}[variant]
    if not is_image and variant != "original":
        return []
    originals = list(dict.fromkeys([map_legacy_object_key(key) or key, key]))
    candidates: list[tuple[str, str]] = []
    for selected in variants:
        for original in originals:
            candidate = (media_variant_object_key(original, selected), selected)
            if candidate not in candidates:
                candidates.append(candidate)
        if selected == "thumbnail":
            # Deterministic old derivatives of this exact original, never sibling originals.
            path = PurePosixPath(key)
            historical = [str(path.with_name(f"{path.stem}.thumb{path.suffix}")), f"thumbnails/{key}"]
            for old in historical:
                if (old, selected) not in candidates:
                    candidates.append((old, selected))
    return candidates[:8]


class MediaReadService:
    def __init__(self, repository: MediaReadRepository) -> None:
        self.repository = repository

    def authorize(self, request: MediaReadRequest, actor: UserRecord | None = None, client_type: str = "unknown") -> MediaReadData:
        results = []
        # Request-local cache only. Each item still checks current business visibility.
        metadata = {}
        original_fallbacks = 0
        for ref in request.items:
            try:
                owned = self.repository.resolve(ref, actor)
                if not owned or not owned.reference:
                    raise AppError(status_code=404, code=MEDIA_NOT_FOUND, message="媒体不可用")
                media_ref = f"{ref.resource_type}:{ref.resource_id}:{ref.media_id or 'main'}"
                parsed = urlsplit(owned.reference)
                original_key = owned_object_key(owned.reference)
                if original_key is None:
                    # Existing HTTPS external references may be displayed, never fetched or re-signed.
                    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
                        raise AppError(status_code=404, code=MEDIA_NOT_FOUND, message="媒体不可用")
                    degraded = ref.variant != "original"
                    if degraded and (not owned.is_image or original_fallbacks >= 2):
                        raise AppError(status_code=404, code=MEDIA_NOT_FOUND, message="媒体不可用")
                    original_fallbacks += int(degraded)
                    descriptor = MediaReadDescriptor(media_ref=media_ref, variant="original", url=owned.reference, read_mode="external", degraded=degraded)
                else:
                    storage = get_media_storage_client()
                    resolved = None
                    candidates = [(original_key, owned.exact_variant)] if owned.exact_variant else media_candidates(original_key, ref.variant, owned.is_image)
                    for key, variant in candidates:
                        if variant == "original" and ref.variant != "original" and original_fallbacks >= 2:
                            break
                        if key not in metadata:
                            try:
                                metadata[key] = storage.get_object_info(key)
                            except AppError as exc:
                                if exc.code != MEDIA_NOT_FOUND:
                                    raise
                                metadata[key] = None
                        if metadata[key] is not None:
                            resolved = (key, variant, metadata[key])
                            break
                    if resolved is None:
                        raise AppError(status_code=404, code=MEDIA_NOT_FOUND, message="媒体不可用")
                    key, variant, info = resolved
                    if variant == "original" and ref.variant != "original":
                        original_fallbacks += 1
                    issued_at = datetime.now(UTC)
                    direct = settings.object_storage_direct_read_enabled and client_type in settings.media_read_clients.split(",") and ref.resource_type in settings.media_read_kinds.split(",")
                    if request.mode == "proxy":
                        if not settings.media_read_proxy_fallback_enabled:
                            raise AppError(status_code=403, code=MEDIA_NOT_FOUND, message="媒体不可用")
                        direct = False
                    url = storage.build_direct_read_url(key, READ_TTL_SECONDS) if direct else "/api/v1/media/read?ticket=" + make_ticket(ref, key, "GET", actor)
                    head_url = storage.build_direct_head_url(key, READ_TTL_SECONDS) if direct else "/api/v1/media/read?ticket=" + make_ticket(ref, key, "HEAD", actor)
                    descriptor = MediaReadDescriptor(
                        media_ref=media_ref, variant=variant,
                        url=url,
                        head_url=head_url,
                        expires_at=issued_at + timedelta(seconds=READ_TTL_SECONDS),
                        read_mode="direct" if direct else "proxy", degraded=variant != ref.variant,
                        content_type=info.content_type, size_bytes=info.total_size,
                    )
                results.append(MediaReadItem(reference=ref, status="ready", descriptor=descriptor))
            except ValueError:
                results.append(MediaReadItem(reference=ref, status="unavailable", error=MediaReadError(code=MEDIA_NOT_FOUND, message="媒体不可用")))
            except AppError as exc:
                unavailable = exc.status_code in {400, 403, 404}
                results.append(MediaReadItem(
                    reference=ref, status="unavailable" if unavailable else "failed",
                    error=MediaReadError(code=MEDIA_NOT_FOUND if unavailable else STORAGE_UNAVAILABLE,
                                         message="媒体不可用" if unavailable else "媒体服务暂不可用"),
                ))
        return MediaReadData(server_time=datetime.now(UTC), items=results)
