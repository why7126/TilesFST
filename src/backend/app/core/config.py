"""Application configuration.

V5:
- Use one object storage bucket per project.
- Use object prefixes to separate resource categories.
- Keep internal ports stable, allow host port override in docker-compose.
"""

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = Field(default="tilesfst", alias="APP_NAME")
    app_env: str = Field(default="development", alias="APP_ENV")
    app_debug: bool = Field(default=True, alias="APP_DEBUG")
    app_secret_key: str = Field(default="change-me-in-local-env", alias="APP_SECRET_KEY")

    backend_host: str = Field(default="0.0.0.0", alias="BACKEND_HOST")
    backend_port: int = Field(default=8000, alias="BACKEND_PORT")

    database_url: str | None = Field(default="sqlite:////app/data/sqlite/tilesfst.db", alias="DATABASE_URL")

    max_image_size_mb: int = Field(default=20, alias="MAX_IMAGE_SIZE_MB")
    max_video_size_mb: int = Field(default=500, alias="MAX_VIDEO_SIZE_MB")
    max_file_size_mb: int = Field(default=25, alias="MAX_FILE_SIZE_MB")
    allowed_image_types: str = Field(
        default="image/jpeg,image/jpg,image/png,image/webp,image/gif,image/svg+xml,image/bmp,image/tiff,image/heic",
        alias="ALLOWED_IMAGE_TYPES",
    )
    allowed_video_types: str = Field(
        default="video/mp4,video/quicktime,video/x-msvideo,video/webm,video/x-matroska,video/mpeg,video/3gpp",
        alias="ALLOWED_VIDEO_TYPES",
    )

    object_storage_provider: str = Field(default="minio", alias="OBJECT_STORAGE_PROVIDER")
    object_storage_endpoint: str = Field(default="minio:9000", alias="OBJECT_STORAGE_ENDPOINT")
    object_storage_access_key: str = Field(default="minioadmin", alias="OBJECT_STORAGE_ACCESS_KEY")
    object_storage_secret_key: str = Field(default="minioadmin", alias="OBJECT_STORAGE_SECRET_KEY")
    object_storage_secure: bool = Field(default=False, alias="OBJECT_STORAGE_SECURE")
    object_storage_bucket: str = Field(default="tilesfst", alias="OBJECT_STORAGE_BUCKET")
    object_storage_region: str | None = Field(default=None, alias="OBJECT_STORAGE_REGION")
    object_storage_path_style: bool | None = Field(default=None, alias="OBJECT_STORAGE_PATH_STYLE")
    object_storage_auto_create_bucket: bool | None = Field(default=None, alias="OBJECT_STORAGE_AUTO_CREATE_BUCKET")

    object_storage_prefix_images: str = Field(default="images/", alias="OBJECT_STORAGE_PREFIX_IMAGES")
    object_storage_prefix_original: str = Field(
        default="original/",
        alias="OBJECT_STORAGE_PREFIX_ORIGINAL",
        description="Deprecated: legacy image prefix; new uploads MUST use OBJECT_STORAGE_PREFIX_IMAGES.",
    )
    object_storage_prefix_files: str = Field(default="files/", alias="OBJECT_STORAGE_PREFIX_FILES")
    object_storage_prefix_audios: str = Field(default="audios/", alias="OBJECT_STORAGE_PREFIX_AUDIOS")
    object_storage_prefix_thumbnails: str = Field(default="thumbnails/", alias="OBJECT_STORAGE_PREFIX_THUMBNAILS")
    object_storage_prefix_processed: str = Field(default="processed/", alias="OBJECT_STORAGE_PREFIX_PROCESSED")
    object_storage_prefix_temp: str = Field(default="tmp/", alias="OBJECT_STORAGE_PREFIX_TEMP")
    object_storage_prefix_import: str = Field(default="imports/", alias="OBJECT_STORAGE_PREFIX_IMPORT")
    object_storage_prefix_export: str = Field(default="exports/", alias="OBJECT_STORAGE_PREFIX_EXPORT")
    object_storage_prefix_video: str = Field(default="videos/", alias="OBJECT_STORAGE_PREFIX_VIDEO")
    object_storage_prefix_video_cover: str = Field(default="videos/covers/", alias="OBJECT_STORAGE_PREFIX_VIDEO_COVER")
    object_storage_prefix_video_transcoded: str = Field(
        default="videos/transcoded/",
        alias="OBJECT_STORAGE_PREFIX_VIDEO_TRANSCODED",
    )

    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    jwt_access_token_expire_minutes: int = Field(default=120, alias="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")
    jwt_remember_me_expire_days: int = Field(default=7, alias="JWT_REMEMBER_ME_EXPIRE_DAYS")
    admin_username: str = Field(default="admin", alias="ADMIN_USERNAME")
    admin_initial_password: str | None = Field(default=None, alias="ADMIN_INITIAL_PASSWORD")
    admin_reset_password_on_startup: bool = Field(
        default=False,
        alias="ADMIN_RESET_PASSWORD_ON_STARTUP",
    )

    class Config:
        env_file = ".env"
        extra = "ignore"

    def allowed_image_type_set(self) -> frozenset[str]:
        return frozenset(
            part.strip() for part in self.allowed_image_types.split(",") if part.strip()
        )

    def allowed_video_type_set(self) -> frozenset[str]:
        return frozenset(
            part.strip() for part in self.allowed_video_types.split(",") if part.strip()
        )

    def max_proxy_body_size_mb(self) -> int:
        return max(self.max_image_size_mb, self.max_video_size_mb, self.max_file_size_mb)

    def allow_swagger_try_it_out(self) -> bool:
        return self.app_env.strip().lower() in {"local", "development", "dev", "demo", "test"}

    def effective_object_storage_provider(self) -> str:
        provider = self.object_storage_provider.strip().lower()
        return provider or "minio"

    def effective_object_storage_endpoint(self) -> str:
        return self.object_storage_endpoint.strip()

    def effective_object_storage_access_key(self) -> str:
        return self.object_storage_access_key.strip()

    def effective_object_storage_secret_key(self) -> str:
        return self.object_storage_secret_key

    def effective_object_storage_secure(self) -> bool:
        return self.object_storage_secure

    def effective_object_storage_bucket(self) -> str:
        return self.object_storage_bucket.strip()

    def effective_object_storage_region(self) -> str | None:
        value = (self.object_storage_region or "").strip()
        return value or None

    def effective_object_storage_path_style(self) -> bool:
        if self.object_storage_path_style is not None:
            return self.object_storage_path_style
        return self.effective_object_storage_provider() in {"minio", "self-hosted-minio"}

    def effective_object_storage_auto_create_bucket(self) -> bool:
        if self.object_storage_auto_create_bucket is not None:
            return self.object_storage_auto_create_bucket
        return self.effective_object_storage_provider() in {"minio", "self-hosted-minio"}

    def object_storage_public_summary(self) -> dict[str, str | bool | None]:
        return {
            "provider": self.effective_object_storage_provider(),
            "endpoint": self.effective_object_storage_endpoint(),
            "bucket": self.effective_object_storage_bucket(),
            "secure": self.effective_object_storage_secure(),
            "region": self.effective_object_storage_region(),
            "path_style": self.effective_object_storage_path_style(),
            "auto_create_bucket": self.effective_object_storage_auto_create_bucket(),
        }


settings = Settings()
