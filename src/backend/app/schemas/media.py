from pydantic import BaseModel

class UploadResult(BaseModel):
    object_key: str
    url: str
    file_key: str | None = None
    file_url: str | None = None
    file_name: str | None = None
    mime_type: str | None = None
    size: int | None = None
