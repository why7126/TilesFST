"""Isolated image job entrypoint. No database access or cloud processing service."""
from __future__ import annotations

import hashlib
import json
import logging
import subprocess
import sys
import time
from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image

from app.core.exceptions import AppError
from app.modules.media.storage import generate_image_thumbnail

SUPPORTED = {'image/jpeg': 'JPEG', 'image/png': 'PNG', 'image/webp': 'WEBP'}


class ImageProcessingFailure(ValueError):
    pass


def render_variant(content: bytes, mime: str, variant: str, target_kib: int = 0) -> tuple[bytes, dict]:
    if mime not in SUPPORTED or variant not in {'thumbnail', 'display'}:
        raise ImageProcessingFailure('unsupported_format')
    with Image.open(BytesIO(content)) as image:
        if image.format != SUPPORTED[mime]:
            raise ImageProcessingFailure('mime_mismatch')
        image.verify()
    started = time.monotonic()
    bound, quality = (480, 82) if variant == 'thumbnail' else (1600, 86)
    result = generate_image_thumbnail(content, mime, max_width=bound, max_height=bound,
                                     webp_quality=quality, target_max_size_kb=target_kib)
    return result.content, {'width': result.width, 'height': result.height, 'size': result.size,
        'mime_type': result.content_type, 'quality_start': quality, 'target_kib': target_kib,
        'warning': bool(target_kib and result.size > target_kib * 1024),
        'duration_ms': round((time.monotonic() - started) * 1000, 2)}


def render_isolated(content: bytes, mime: str, variant: str, target_kib: int):
    # A process deadline also interrupts C-library decode/encode calls, unlike a Python signal handler.
    with TemporaryDirectory(prefix="image-derive-") as directory:
        source = Path(directory) / "source"
        output = Path(directory) / "output.webp"
        source.write_bytes(content)
        request = {"source": str(source), "output": str(output), "mime": mime,
                   "variant": variant, "target_kib": target_kib}
        try:
            completed = subprocess.run([sys.executable, "-m", "app.modules.media.image_processing", "--render"],
                input=json.dumps(request), capture_output=True, text=True,
                timeout=18 if variant == "thumbnail" else 90)
        except subprocess.TimeoutExpired:
            raise ImageProcessingFailure(variant + "_timeout") from None
        if completed.returncode != 0:
            raise ImageProcessingFailure("decode_encode_or_resource_failure")
        return output.read_bytes(), json.loads(completed.stdout)


def execute(job: dict, gateway) -> dict:
    """Run in a killable dedicated process; the supervisor enforces the total deadline."""
    source = gateway.inspect(job['stable_key'], version_id=job['stable_version_id'], expected_size=job['expected_size'])
    if source.content_type != job['mime_type']:
        raise ImageProcessingFailure('mime_mismatch')
    started = time.monotonic()
    response = gateway._call('get_object', Key=source.key, VersionId=source.version_id)
    stream = response['Body'].get_raw_stream()
    # Source limits are fixed when the authorized session is created.
    try:
        content = stream.read(source.size + 1)
    finally:
        stream.close()
    if len(content) != source.size:
        raise ImageProcessingFailure('size_mismatch')
    download_ms = round((time.monotonic() - started) * 1000, 2)
    outputs = {}
    for variant, target in [('thumbnail', job['thumbnail_target_kib']), ('display', job['display_target_kib'])]:
        raw, info = render_isolated(content, job['mime_type'], variant, target)
        key = job['output_keys'][variant]
        started = time.monotonic()
        response = gateway._call('put_object', Key=key, Body=raw, ContentType='image/webp')
        version = response.get('x-cos-version-id') or response.get('VersionId')
        if not version or version == 'null':
            raise ImageProcessingFailure('missing_version')
        gateway.inspect(key, version_id=version, expected_size=len(raw))
        outputs[variant] = {**info, 'key': key, 'version_id': version,
                           'sha256': hashlib.sha256(raw).hexdigest(),
                           'put_ms': round((time.monotonic() - started) * 1000, 2)}
    return {'outputs': outputs, 'download_ms': download_ms}


def main():
    # SDK diagnostics may contain URLs. Only our fixed result envelope reaches stdout.
    logging.disable(logging.CRITICAL)
    if "--render" in sys.argv:
        try:
            request = json.loads(sys.stdin.read())
            raw, metadata = render_variant(Path(request['source']).read_bytes(), request['mime'],
                                           request['variant'], request['target_kib'])
            Path(request['output']).write_bytes(raw)
            print(json.dumps(metadata))
        except Exception:
            sys.exit(2)
        return
    from app.services.upload_session_service import get_upload_gateway
    try:
        job = json.loads(sys.stdin.read())
        result = {'ok': True, **execute(job, get_upload_gateway())}
    except AppError:
        result = {'ok': False, 'reason': 'storage_unavailable', 'retryable': True}
    except ImageProcessingFailure as exc:
        result = {'ok': False, 'reason': str(exc), 'retryable': False}
    except MemoryError:
        result = {'ok': False, 'reason': 'memory_limit', 'retryable': False}
    except Exception:
        result = {'ok': False, 'reason': 'decode_or_encode_failed', 'retryable': False}
    print(json.dumps(result))


if __name__ == '__main__':
    main()
