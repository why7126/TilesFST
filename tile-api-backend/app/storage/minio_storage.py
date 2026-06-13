from minio import Minio
from minio.error import S3Error
from app.core.config import settings
from app.core.logging import logger
from typing import Optional
import uuid


class MinIOClient:
    def __init__(self):
        self.client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            region=settings.MINIO_REGION,
            secure=settings.MINIO_SECURE
        )
        self.bucket = settings.MINIO_BUCKET

    def verify_connection(self) -> bool:
        try:
            if not self.client.bucket_exists(self.bucket):
                self.client.make_bucket(self.bucket)
            logger.info(f"MinIO connection verified, bucket: {self.bucket}")
            return True
        except S3Error as e:
            logger.error(f"MinIO connection failed: {e}")
            return False

    def upload_file(self, file_data: bytes, file_ext: str, prefix: str = "tiles") -> Optional[str]:
        try:
            object_key = f"{prefix}/{uuid.uuid4()}.{file_ext}"
            self.client.put_object(
                self.bucket,
                object_key,
                file_data,
                length=len(file_data)
            )
            logger.info(f"File uploaded: {object_key}")
            return object_key
        except S3Error as e:
            logger.error(f"File upload failed: {e}")
            return None

    def delete_file(self, object_key: str) -> bool:
        try:
            self.client.remove_object(self.bucket, object_key)
            logger.info(f"File deleted: {object_key}")
            return True
        except S3Error as e:
            logger.error(f"File deletion failed: {e}")
            return False

    def get_presigned_url(self, object_key: str, expires_hours: int = 1) -> Optional[str]:
        try:
            url = self.client.presigned_get_object(
                self.bucket,
                object_key,
                expires=expires_hours * 3600
            )
            return url
        except S3Error as e:
            logger.error(f"Presigned URL generation failed: {e}")
            return None


minio_client = MinIOClient()