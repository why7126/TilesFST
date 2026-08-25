from pydantic import BaseModel

class UploadResult(BaseModel):
    object_key: str
    url: str
    thumbnail_key: str | None = None
    thumbnail_url: str | None = None
    display_key: str | None = None
    display_url: str | None = None
    original_url: str | None = None
    task_trace_id: str | None = None
    task_type: str | None = None
    file_key: str | None = None
    file_url: str | None = None
    file_name: str | None = None
    mime_type: str | None = None
    size: int | None = None
