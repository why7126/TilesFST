"""Validate current ownership again before serving one bounded, exact object."""
from fastapi.responses import Response

from app.modules.media.read_tickets import decode_ticket, key_hash, proxy_budget, PROXY_RANGE_BYTES, unavailable
from app.modules.media.storage import get_media_storage_client, _parse_byte_range
from app.repositories.media_read_repository import MediaReadRepository
from app.repositories.user_repository import UserRepository
from app.schemas.media_read import MediaReadReference
from app.services.media_read_service import media_candidates, owned_object_key


def read_proxy(db, ticket: str, method: str, range_header: str | None = None):
    claims = decode_ticket(ticket, method)
    actor = None
    if claims.get("actor_id"):
        actor = UserRepository(db).get_by_id(claims["actor_id"])
        if not actor or actor.status != "active" or actor.role not in {"admin", "employee"} or actor.token_version != claims.get("token_version"):
            raise unavailable()
    try:
        ref = MediaReadReference.model_validate(claims["reference"])
    except (KeyError, ValueError, TypeError):
        raise unavailable() from None
    owned = MediaReadRepository(db).resolve(ref, actor)
    if not owned:
        raise unavailable()
    original = owned_object_key(owned.reference)
    if original is None:
        raise unavailable()
    candidates = [(original, owned.exact_variant)] if owned.exact_variant else media_candidates(original, ref.variant, owned.is_image)
    key = next((key for key, _ in candidates if key_hash(key) == claims.get("key_hash")), None)
    if key is None:
        raise unavailable()
    return read_exact_proxy(key, method, range_header)


def read_exact_proxy(key, method, range_header):
    storage = get_media_storage_client()
    info = storage.get_object_info(key)
    headers = {"Cache-Control": "no-store", "Referrer-Policy": "no-referrer", "Accept-Ranges": "bytes", "X-Content-Type-Options": "nosniff"}
    if method == "HEAD":
        headers["Content-Length"] = str(info.total_size)
        return Response(headers=headers, media_type=info.content_type)
    if range_header:
        byte_range = _parse_byte_range(range_header, info.total_size)
        if byte_range is None:
            return Response(status_code=416, headers={**headers, "Content-Range": f"bytes */{info.total_size}"})
        start, end = byte_range
        end = min(end, start + PROXY_RANGE_BYTES - 1)
        length = end - start + 1
        with proxy_budget.claim(length):
            content = storage.get_object_range(key, start, length).content
        headers.update({"Content-Range": f"bytes {start}-{end}/{info.total_size}", "Content-Length": str(len(content))})
        return Response(content=content, status_code=206, headers=headers, media_type=info.content_type)
    with proxy_budget.claim(info.total_size):
        content = storage.get_object(key).content
    return Response(content=content, headers=headers, media_type=info.content_type)
