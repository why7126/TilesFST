from app.core.config import Settings


def test_upload_settings_parse_allowed_types() -> None:
    settings = Settings(
        ALLOWED_IMAGE_TYPES="image/png, image/jpeg",
        ALLOWED_VIDEO_TYPES="video/mp4,video/webm",
    )
    assert settings.allowed_image_type_set() == frozenset({"image/png", "image/jpeg"})
    assert settings.allowed_video_type_set() == frozenset({"video/mp4", "video/webm"})


def test_upload_settings_max_proxy_body_size() -> None:
    settings = Settings(MAX_IMAGE_SIZE_MB=20, MAX_VIDEO_SIZE_MB=500)
    assert settings.max_proxy_body_size_mb() == 500
