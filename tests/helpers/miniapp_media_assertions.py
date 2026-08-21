from __future__ import annotations

import re


_SENSITIVE_PATTERNS = (
    "authorization:",
    "cookie:",
    "access_key",
    "secret_key",
    "secretkey",
    "database_url",
    ".env",
    "/users/",
    "c:\\",
)


def assert_controlled_media_url(url: str) -> None:
    assert url.startswith("/media/"), f"media URL must use controlled /media path: {url}"
    lowered = url.lower()
    assert "://" not in url, f"media URL must not be absolute: {url}"
    assert "minio" not in lowered, f"media URL must not expose object storage host: {url}"
    assert ".." not in url, f"media URL must not contain path traversal: {url}"


def assert_no_sensitive_media_evidence(text: str) -> None:
    lowered = text.lower()
    for pattern in _SENSITIVE_PATTERNS:
        assert pattern not in lowered, f"media evidence leaks sensitive marker: {pattern}"


def assert_image_media_binding(
    wxml: str,
    *,
    src_expr: str,
    preview_expr: str | None = None,
    fallback_expr: str | None = None,
    lazy_load_expr: str | None = None,
) -> None:
    assert f'src="{{{{{src_expr}}}}}"' in wxml
    if preview_expr is not None:
        assert f'data-url="{{{{{preview_expr}}}}}"' in wxml
    if fallback_expr is not None:
        assert fallback_expr in src_expr
    if lazy_load_expr is not None:
        assert f'lazy-load="{{{{{lazy_load_expr}}}}}"' in wxml


def assert_video_media_binding(
    wxml: str,
    *,
    src_expr: str,
    poster_expr: str,
    play_handler: str,
    error_handler: str,
) -> None:
    assert "<video" in wxml
    assert f'src="{{{{{src_expr}}}}}"' in wxml
    assert f'poster="{{{{{poster_expr}}}}}"' in wxml
    assert f'bindplay="{play_handler}"' in wxml
    assert f'binderror="{error_handler}"' in wxml


def assert_wxml_uses_safe_media_bindings(wxml: str) -> None:
    assert not re.search(r'src="{{[^"}]*https?://', wxml)
    assert not re.search(r'(access[_-]?key|secret[_-]?key|authorization|cookie)', wxml, re.I)
