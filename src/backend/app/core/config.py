"""Application configuration.

V5:
- Use one MinIO bucket per project.
- Use object prefixes to separate resource categories.
- Keep internal ports stable, allow host port override in docker-compose.
"""

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = Field(default="tile-info-platform", alias="APP_NAME")
    app_env: str = Field(default="development", alias="APP_ENV")
    app_debug: bool = Field(default=True, alias="APP_DEBUG")
    app_secret_key: str = Field(default="change-me-in-local-env", alias="APP_SECRET_KEY")

    backend_host: str = Field(default="0.0.0.0", alias="BACKEND_HOST")
    backend_port: int = Field(default=8000, alias="BACKEND_PORT")

    database_url: str | None = Field(default=None, alias="DATABASE_URL")
    sqlite_database_url: str = Field(default="sqlite:////app/data/sqlite/tile-info-platform.db", alias="SQLITE_DATABASE_URL")

    max_image_size_mb: int = Field(default=20, alias="MAX_IMAGE_SIZE_MB")
    max_video_size_mb: int = Field(default=500, alias="MAX_VIDEO_SIZE_MB")
    allowed_image_types: str = Field(
        default="image/jpeg,image/jpg,image/png,image/webp,image/gif,image/svg+xml,image/bmp,image/tiff,image/heic",
        alias="ALLOWED_IMAGE_TYPES",
    )
    allowed_video_types: str = Field(
        default="video/mp4,video/quicktime,video/x-msvideo,video/webm,video/x-matroska,video/mpeg,video/3gpp",
        alias="ALLOWED_VIDEO_TYPES",
    )

    minio_endpoint: str = Field(default="minio:9000", alias="MINIO_ENDPOINT")
    minio_access_key: str = Field(default="minioadmin", alias="MINIO_ACCESS_KEY")
    minio_secret_key: str = Field(default="minioadmin", alias="MINIO_SECRET_KEY")
    minio_secure: bool = Field(default=False, alias="MINIO_SECURE")
    minio_bucket: str = Field(default="tile-info-platform", alias="MINIO_BUCKET")

    minio_prefix_images: str = Field(default="images/", alias="MINIO_PREFIX_IMAGES")
    minio_prefix_original: str = Field(
        default="original/",
        alias="MINIO_PREFIX_ORIGINAL",
        description="Deprecated: legacy image prefix; new uploads MUST use MINIO_PREFIX_IMAGES.",
    )
    minio_prefix_files: str = Field(default="files/", alias="MINIO_PREFIX_FILES")
    minio_prefix_audios: str = Field(default="audios/", alias="MINIO_PREFIX_AUDIOS")
    minio_prefix_thumbnails: str = Field(default="thumbnails/", alias="MINIO_PREFIX_THUMBNAILS")
    minio_prefix_processed: str = Field(default="processed/", alias="MINIO_PREFIX_PROCESSED")
    minio_prefix_temp: str = Field(default="tmp/", alias="MINIO_PREFIX_TEMP")
    minio_prefix_video: str = Field(default="videos/", alias="MINIO_PREFIX_VIDEO")
    minio_prefix_video_cover: str = Field(default="videos/covers/", alias="MINIO_PREFIX_VIDEO_COVER")
    minio_prefix_video_transcoded: str = Field(default="videos/transcoded/", alias="MINIO_PREFIX_VIDEO_TRANSCODED")

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
        return max(self.max_image_size_mb, self.max_video_size_mb)

    def allow_swagger_try_it_out(self) -> bool:
        return self.app_env.strip().lower() in {"local", "development", "dev", "demo", "test"}


settings = Settings()
