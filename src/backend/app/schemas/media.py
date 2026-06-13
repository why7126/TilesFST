from pydantic import BaseModel

class UploadResult(BaseModel):
    object_key: str
    url: str
