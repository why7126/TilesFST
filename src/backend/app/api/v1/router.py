from fastapi import APIRouter
from app.api.v1 import tiles, admin_tiles, uploads

api_router = APIRouter()
api_router.include_router(tiles.router, prefix="/tiles", tags=["tiles"])
api_router.include_router(admin_tiles.router, prefix="/admin/tiles", tags=["admin-tiles"])
api_router.include_router(uploads.router, prefix="/admin/uploads", tags=["uploads"])
