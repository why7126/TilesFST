"""Legacy URLs are public business references, never unrestricted storage keys."""
from pathlib import PurePosixPath

from sqlalchemy import bindparam, text
from app.core.exceptions import AppError

from app.modules.media.read_tickets import unavailable
from app.modules.media.storage import MEDIA_NOT_FOUND, resolve_media_path
from app.repositories.media_read_repository import MediaReadRepository
from app.schemas.media_read import MediaReadReference
from app.services.media_proxy_service import read_exact_proxy
from app.services.media_read_service import media_candidates, owned_object_key


# Identifiers are fixed here, never interpolated from request input.
LOOKUPS = (
    ("system_settings", "value", "'store'", "NULL", "store_logo"),
    ("tile_images", "object_key", "tile_id", "id", "sku_image"),
    ("tile_videos", "object_key", "tile_id", "id", "sku_video"),
    ("brands", "logo_object_key", "id", "NULL", "brand_logo"),
    ("banners", "image_object_key", "id", "NULL", "banner_image"),
    ("brand_certificates", "file_key", "id", "NULL", "certificate"),
    ("brand_certificate_images", "file_key", "certificate_id", "id", "certificate"),
)


def read_legacy_media(db, object_key: str, method: str, range_header: str | None = None):
    key = str(resolve_media_path(object_key))
    originals = {key}
    if key.startswith("thumbnails/"):
        originals.add(key.removeprefix("thumbnails/"))
    path = PurePosixPath(key)
    if path.stem.endswith((".thumb", ".display")):
        stem = path.stem.rsplit(".", 1)[0]
        originals.update(str(path.with_name(stem + suffix)) for suffix in {path.suffix, ".jpg", ".jpeg", ".png", ".webp"})
    values = sorted(originals | {"/media/" + value for value in originals})
    repository = MediaReadRepository(db)
    for table, column, owner, media, kind in LOOKUPS:
        query = text(f"SELECT {owner} AS owner_id, {media} AS media_id FROM {table} WHERE {column} IN :keys LIMIT 51").bindparams(bindparam("keys", expanding=True))
        if table == "system_settings":
            query = text("SELECT 'store' AS owner_id, NULL AS media_id FROM system_settings WHERE `key`='miniapp.logo_url' AND value IN :keys LIMIT 1").bindparams(bindparam("keys", expanding=True))
        rows = db.execute(query, {"keys": values}).mappings().all()
        # Ambiguous fan-out is rejected rather than performing unbounded permission work.
        if len(rows) > 50:
            raise unavailable()
        for row in rows:
            ref = MediaReadReference(resource_type=kind, resource_id=str(row["owner_id"]), media_id=row["media_id"], variant="original")
            owned = repository.resolve(ref, None)
            original = owned_object_key(owned.reference) if owned else None
            if original is None:
                continue
            candidates = media_candidates(original, "thumbnail" if owned.is_image else "original", owned.is_image)
            selected = next((variant for candidate, variant in candidates if candidate == key), None)
            if selected is not None:
                for candidate, _ in media_candidates(original, selected, owned.is_image):
                    try:
                        return read_exact_proxy(candidate, method, range_header)
                    except AppError as error:
                        if error.code != MEDIA_NOT_FOUND:
                            raise
                raise unavailable()
    raise unavailable()
