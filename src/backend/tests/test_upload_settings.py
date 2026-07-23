from app.core.config import Settings


def test_upload_settings_parse_allowed_types() -> None:
    settings = Settings(
        ALLOWED_IMAGE_TYPES="image/png, image/jpeg",
        ALLOWED_VIDEO_TYPES="video/mp4,video/webm",
    )
    assert settings.allowed_image_type_set() == frozenset({"image/png", "image/jpeg"})
    assert settings.allowed_video_type_set() == frozenset({"video/mp4", "video/webm"})


def test_upload_settings_max_proxy_body_size() -> None:
    settings = Settings(MAX_IMAGE_SIZE_MB=20, MAX_VIDEO_SIZE_MB=500, MAX_FILE_SIZE_MB=25)
    assert settings.max_proxy_body_size_mb() == 500


def test_upload_settings_max_proxy_body_size_includes_file_limit() -> None:
    settings = Settings(MAX_IMAGE_SIZE_MB=20, MAX_VIDEO_SIZE_MB=100, MAX_FILE_SIZE_MB=200)
    assert settings.max_proxy_body_size_mb() == 200


def test_object_storage_settings_use_object_storage_variables() -> None:
    settings = Settings(
        OBJECT_STORAGE_PROVIDER="tencent-cos",
        OBJECT_STORAGE_ENDPOINT="cos.ap-guangzhou.example.com",
        OBJECT_STORAGE_ACCESS_KEY="cos-access",
        OBJECT_STORAGE_SECRET_KEY="cos-secret",
        OBJECT_STORAGE_BUCKET="tiles-cos",
        OBJECT_STORAGE_SECURE=True,
        OBJECT_STORAGE_REGION="ap-guangzhou",
        OBJECT_STORAGE_PATH_STYLE=False,
        OBJECT_STORAGE_AUTO_CREATE_BUCKET=False,
    )

    assert settings.effective_object_storage_provider() == "tencent-cos"
    assert settings.effective_object_storage_endpoint() == "cos.ap-guangzhou.example.com"
    assert settings.effective_object_storage_access_key() == "cos-access"
    assert settings.effective_object_storage_secret_key() == "cos-secret"
    assert settings.effective_object_storage_bucket() == "tiles-cos"
    assert settings.effective_object_storage_secure() is True
    assert settings.effective_object_storage_region() == "ap-guangzhou"
    assert settings.effective_object_storage_path_style() is False
    assert settings.effective_object_storage_auto_create_bucket() is False


def test_object_storage_settings_defaults_to_local_minio() -> None:
    settings = Settings(_env_file=None)

    assert settings.effective_object_storage_provider() == "minio"
    assert settings.effective_object_storage_endpoint() == "minio:9000"
    assert settings.effective_object_storage_access_key() == "minioadmin"
    assert settings.effective_object_storage_secret_key() == "minioadmin"
    assert settings.effective_object_storage_bucket() == "tilesfst"
    assert settings.effective_object_storage_secure() is False
    assert settings.effective_object_storage_path_style() is True
    assert settings.effective_object_storage_auto_create_bucket() is True


def test_object_storage_public_summary_excludes_secrets() -> None:
    settings = Settings(
        OBJECT_STORAGE_PROVIDER="volcengine-tos",
        OBJECT_STORAGE_ENDPOINT="tos-cn-beijing.example.com",
        OBJECT_STORAGE_ACCESS_KEY="tos-access",
        OBJECT_STORAGE_SECRET_KEY="tos-secret",
        OBJECT_STORAGE_BUCKET="tiles-tos",
        OBJECT_STORAGE_SECURE=True,
        OBJECT_STORAGE_REGION="cn-beijing",
        OBJECT_STORAGE_AUTO_CREATE_BUCKET=False,
    )

    summary = settings.object_storage_public_summary()

    assert summary == {
        "provider": "volcengine-tos",
        "endpoint": "tos-cn-beijing.example.com",
        "bucket": "tiles-tos",
        "secure": True,
        "region": "cn-beijing",
        "path_style": False,
        "auto_create_bucket": False,
    }
    assert "tos-secret" not in repr(summary)
    assert "tos-access" not in repr(summary)
