from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from typing import List
from app.storage.minio_storage import minio_client
from app.services.auth_service import get_current_user
from app.schemas.schemas import FileUploadResponse

router = APIRouter(prefix="/files", tags=["files"])

ALLOWED_IMAGE_TYPES = {"jpg", "jpeg", "png", "webp"}
ALLOWED_VIDEO_TYPES = {"mp4", "mov", "avi"}
MAX_IMAGE_SIZE = 10 * 1024 * 1024
MAX_VIDEO_SIZE = 100 * 1024 * 1024


@router.post("/upload/image", response_model=FileUploadResponse)
async def upload_image(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    ext = file.filename.split(".")[-1].lower()
    if ext not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Allowed image types: {', '.join(ALLOWED_IMAGE_TYPES)}"
        )
    
    content = await file.read()
    if len(content) > MAX_IMAGE_SIZE:
        raise HTTPException(status_code=400, detail="Image size exceeds 10MB limit")
    
    object_key = minio_client.upload_file(content, ext, "images")
    if not object_key:
        raise HTTPException(status_code=500, detail="Upload failed")
    
    url = minio_client.get_presigned_url(object_key) or f"/files/{object_key}"
    return FileUploadResponse(object_key=object_key, url=url)


@router.post("/upload/video", response_model=FileUploadResponse)
async def upload_video(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    ext = file.filename.split(".")[-1].lower()
    if ext not in ALLOWED_VIDEO_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Allowed video types: {', '.join(ALLOWED_VIDEO_TYPES)}"
        )
    
    content = await file.read()
    if len(content) > MAX_VIDEO_SIZE:
        raise HTTPException(status_code=400, detail="Video size exceeds 100MB limit")
    
    object_key = minio_client.upload_file(content, ext, "videos")
    if not object_key:
        raise HTTPException(status_code=500, detail="Upload failed")
    
    url = minio_client.get_presigned_url(object_key) or f"/files/{object_key}"
    return FileUploadResponse(object_key=object_key, url=url)


@router.post("/upload/batch")
async def upload_batch(
    files: List[UploadFile] = File(...),
    current_user: dict = Depends(get_current_user)
):
    results = []
    for file in files:
        ext = file.filename.split(".")[-1].lower()
        content = await file.read()
        
        file_type = "images" if ext in ALLOWED_IMAGE_TYPES else "videos"
        max_size = MAX_IMAGE_SIZE if ext in ALLOWED_IMAGE_TYPES else MAX_VIDEO_SIZE
        
        if len(content) > max_size:
            results.append({"filename": file.filename, "status": "failed", "error": "Size exceeds limit"})
            continue
        
        object_key = minio_client.upload_file(content, ext, file_type)
        if object_key:
            results.append({"filename": file.filename, "status": "success", "object_key": object_key})
        else:
            results.append({"filename": file.filename, "status": "failed", "error": "Upload failed"})
    
    return {"results": results}


@router.delete("/{object_key}")
async def delete_file(
    object_key: str,
    current_user: dict = Depends(get_current_user)
):
    success = minio_client.delete_file(object_key)
    if not success:
        raise HTTPException(status_code=500, detail="Delete failed")
    return {"message": "File deleted successfully"}