"""COS direct-upload primitives. Session service owns auth, leases and transactions."""
from __future__ import annotations

from dataclasses import dataclass
from math import ceil

from app.core.exceptions import AppError
from app.core.error_codes import STORAGE_UNAVAILABLE
from app.modules.media.storage import validate_object_key


class UploadObjectMismatch(ValueError):
    pass


@dataclass(frozen=True)
class ConfirmedObject:
    key: str
    version_id: str
    etag: str
    size: int
    content_type: str | None
    crc64: str | None = None


def part_length(total_size: int, part_size: int, number: int) -> int:
    if total_size <= 0 or part_size < 1024 * 1024:
        raise UploadObjectMismatch("Invalid upload size")
    count = ceil(total_size / part_size)
    if count > 10000 or number < 1 or number > count:
        raise UploadObjectMismatch("Invalid part number")
    return min(part_size, total_size - (number - 1) * part_size)


class TencentCOSUploadGateway:
    def __init__(self, client, *, bucket: str, region: str):
        self.client = client
        self.bucket = bucket
        self.region = region

    def _call(self, method: str, **kwargs):
        try:
            return getattr(self.client, method)(Bucket=self.bucket, **kwargs)
        except Exception as exc:
            # Never return SDK details: they may contain signed URLs or internal keys.
            raise AppError(status_code=502, code=STORAGE_UNAVAILABLE, message="对象存储不可用") from exc

    def require_versioning(self) -> None:
        if self._call("get_bucket_versioning").get("Status") != "Enabled":
            raise UploadObjectMismatch("Direct upload requires version protection")

    def initiate(self, key: str, mime_type: str) -> str:
        validate_object_key(key)
        self.require_versioning()
        return self._call("create_multipart_upload", Key=key, ContentType=mime_type)["UploadId"]

    def authorize(self, key: str, *, length: int, expires: int,
                  upload_id: str | None = None, part_number: int | None = None) -> str:
        validate_object_key(key)
        if length <= 0 or expires <= 0 or expires > 900:
            raise UploadObjectMismatch("Invalid upload authorization")
        if bool(upload_id) != (part_number is not None):
            raise UploadObjectMismatch("Multipart authorization must identify a part")
        if part_number is not None and not 1 <= part_number <= 10000:
            raise UploadObjectMismatch("Invalid part number")
        params = {"uploadId": upload_id, "partNumber": part_number} if upload_id else {}
        return self._call("get_presigned_url", Key=key, Method="PUT", Expired=expires,
                          Params=params, Headers={"Content-Length": str(length)})

    def complete(self, key: str, upload_id: str, *, expected_size: int, part_size: int) -> ConfirmedObject:
        try:
            return self._complete_parts(key, upload_id, expected_size=expected_size, part_size=part_size)
        except AppError as exc:
            if getattr(exc.__cause__, "get_error_code", lambda: None)() != "NoSuchUpload":
                raise
            # Only the backend can complete multipart uploads. A missing upload
            # plus an existing versioned object recovers a lost completion reply.
            # Missing/aborted objects still fail HEAD and cannot become ready.
            return self.inspect(key, expected_size=expected_size)

    def _complete_parts(self, key: str, upload_id: str, *, expected_size: int, part_size: int) -> ConfirmedObject:
        validate_object_key(key)
        count = ceil(expected_size / part_size) if part_size > 0 else 0
        part_length(expected_size, part_size, 1)
        parts = []; marker = 0
        while True:
            response = self._call("list_parts", Key=key, UploadId=upload_id,
                                  PartNumberMarker=marker, MaxParts=1000)
            for item in response.get("Part", []):
                number = int(item["PartNumber"])
                if number != len(parts) + 1 or int(item["Size"]) != part_length(expected_size, part_size, number):
                    raise UploadObjectMismatch("Multipart layout does not match authorization")
                if not item.get("ETag"):
                    raise UploadObjectMismatch("Missing part integrity marker")
                parts.append({"PartNumber": number, "ETag": item["ETag"]})
            if str(response.get("IsTruncated", "false")).lower() != "true":
                break
            next_marker = int(response["NextPartNumberMarker"])
            if next_marker <= marker or next_marker >= count:
                raise UploadObjectMismatch("Invalid multipart pagination")
            marker = next_marker
        if len(parts) != count:
            raise UploadObjectMismatch("Upload has missing parts")
        response = self._call("complete_multipart_upload", Key=key, UploadId=upload_id,
                              MultipartUpload={"Part": parts})
        version = response.get("x-cos-version-id") or response.get("VersionId")
        if not version or version == "null":
            raise UploadObjectMismatch("Upload completion did not identify a version")
        return self.inspect(key, version_id=version, expected_size=expected_size)

    def inspect(self, key: str, *, version_id: str | None = None,
                expected_size: int | None = None) -> ConfirmedObject:
        validate_object_key(key)
        response = self._call("head_object", Key=key, **({"VersionId": version_id} if version_id else {}))
        version = response.get("x-cos-version-id") or response.get("VersionId")
        size = int(response.get("Content-Length", -1))
        if not version or version == "null" or (version_id and version != version_id):
            raise UploadObjectMismatch("Immutable object version required")
        if size < 0 or (expected_size is not None and size != expected_size):
            raise UploadObjectMismatch("Object size differs from upload declaration")
        if not response.get("ETag"):
            raise UploadObjectMismatch("Object integrity marker missing")
        return ConfirmedObject(key, version, response["ETag"], size, response.get("Content-Type"),
                               response.get("x-cos-hash-crc64ecma"))

    def read_prefix(self, obj: ConfirmedObject, *, limit: int = 65536) -> bytes:
        if not 0 < limit <= 1048576:
            raise ValueError("Invalid bounded content inspection size")
        validate_object_key(obj.key)
        result = self._call("get_object", Key=obj.key, VersionId=obj.version_id,
                            Range=f"bytes=0-{min(obj.size, limit) - 1}")
        stream = result["Body"].get_raw_stream()
        try:
            return stream.read(limit)
        finally:
            stream.close()

    def copy_stable(self, source: ConfirmedObject, target: str) -> ConfirmedObject:
        validate_object_key(source.key); validate_object_key(target)
        if source.key == target:
            raise UploadObjectMismatch("Stable object must be isolated")
        response = self._call("copy_object", Key=target,
            CopySource={"Bucket": self.bucket, "Region": self.region,
                        "Key": source.key, "VersionId": source.version_id},
            CopySourceIfMatch=source.etag)
        version = response.get("x-cos-version-id") or response.get("VersionId")
        if not version or version == "null":
            raise UploadObjectMismatch("Stable copy version missing")
        copied = self.inspect(target, version_id=version, expected_size=source.size)
        if source.crc64 and copied.crc64 != source.crc64:
            raise UploadObjectMismatch("Stable copy integrity marker differs")
        return copied

    def abort(self, key: str, upload_id: str) -> None:
        validate_object_key(key)
        try:
            self.client.abort_multipart_upload(Bucket=self.bucket, Key=key, UploadId=upload_id)
        except Exception as exc:
            if getattr(exc, "get_error_code", lambda: None)() != "NoSuchUpload":
                raise AppError(status_code=502, code=STORAGE_UNAVAILABLE, message="对象存储不可用") from exc

    def delete_version(self, key: str, version_id: str) -> None:
        # Caller must hold cleaning lease and verify no business reference.
        validate_object_key(key)
        if not version_id or version_id == "null":
            raise UploadObjectMismatch("Exact version required for cleanup")
        self._call("delete_object", Key=key, VersionId=version_id)

    def versions(self, key: str):
        """Enumerate only this exact key, including crash-created duplicate versions."""
        validate_object_key(key)
        marker = {}; seen = set()
        while True:
            response = self._call("list_objects_versions", Prefix=key, MaxKeys=1000, **marker)
            for field in ("Version", "DeleteMarker"):
                for item in response.get(field, []):
                    if item["Key"] == key:
                        yield item["VersionId"]
            if str(response.get("IsTruncated", "false")).lower() != "true":
                return
            pair = (response.get("NextKeyMarker"), response.get("NextVersionIdMarker"))
            if not all(pair) or pair in seen:
                raise UploadObjectMismatch("Invalid version pagination")
            seen.add(pair)
            marker = {"KeyMarker": pair[0], "VersionIdMarker": pair[1]}

    def multipart_uploads(self, key: str):
        validate_object_key(key)
        marker = {}; seen = set()
        while True:
            response = self._call("list_multipart_uploads", Prefix=key, MaxUploads=1000, **marker)
            for item in response.get("Upload", []):
                if item["Key"] == key:
                    yield item["UploadId"]
            if str(response.get("IsTruncated", "false")).lower() != "true":
                return
            pair = (response.get("NextKeyMarker"), response.get("NextUploadIdMarker"))
            if not all(pair) or pair in seen:
                raise UploadObjectMismatch("Invalid upload pagination")
            seen.add(pair)
            marker = {"KeyMarker": pair[0], "UploadIdMarker": pair[1]}
