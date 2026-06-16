from fastapi import APIRouter
from app.api.v1 import admin_tiles, admin_users, auth, tiles, uploads

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(tiles.router, prefix="/tiles", tags=["tiles"])
api_router.include_router(admin_tiles.router, prefix="/admin/tiles", tags=["admin-tiles"])
api_router.include_router(admin_users.router, prefix="/admin/users", tags=["admin-users"])
api_router.include_router(uploads.router, prefix="/admin/uploads", tags=["uploads"])
