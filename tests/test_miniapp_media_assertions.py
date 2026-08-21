from __future__ import annotations

import pytest

from helpers.miniapp_media_assertions import (
    assert_controlled_media_url,
    assert_image_media_binding,
    assert_no_sensitive_media_evidence,
    assert_video_media_binding,
    assert_wxml_uses_safe_media_bindings,
)


def test_image_media_helper_covers_preview_fallback_and_lazy_load() -> None:
    wxml = """
    <image
      src="{{item.url || imageFallback}}"
      data-url="{{item.preview_url || item.url}}"
      lazy-load="{{index > 0}}"
    />
    """

    assert_image_media_binding(
        wxml,
        src_expr="item.url || imageFallback",
        preview_expr="item.preview_url || item.url",
        fallback_expr="imageFallback",
        lazy_load_expr="index > 0",
    )


def test_video_media_helper_covers_url_poster_play_and_error() -> None:
    wxml = """
    <video
      src="{{item.url}}"
      poster="{{item.cover_url || product.cover_image || imageFallback}}"
      bindplay="onVideoPlay"
      binderror="onMediaError"
    />
    """

    assert_video_media_binding(
        wxml,
        src_expr="item.url",
        poster_expr="item.cover_url || product.cover_image || imageFallback",
        play_handler="onVideoPlay",
        error_handler="onMediaError",
    )


def test_media_helpers_reject_missing_fallback_and_unsafe_urls() -> None:
    with pytest.raises(AssertionError):
        assert_image_media_binding(
            '<image src="{{item.url}}" data-url="{{item.preview_url}}" />',
            src_expr="item.url",
            preview_expr="item.preview_url",
            fallback_expr="imageFallback",
        )

    assert_controlled_media_url("/media/images/default/tiles/1/demo.jpg")
    with pytest.raises(AssertionError):
        assert_controlled_media_url("https://minio.local/tilesfst/demo.jpg")


def test_media_evidence_rejects_sensitive_markers() -> None:
    assert_no_sensitive_media_evidence("object_key_hash=abc123 request_domain=tilesfst.wjoyhappy.site")

    with pytest.raises(AssertionError):
        assert_no_sensitive_media_evidence("Authorization: Bearer test")

    with pytest.raises(AssertionError):
        assert_wxml_uses_safe_media_bindings('<image src="{{https://example.com/a.jpg}}" />')
