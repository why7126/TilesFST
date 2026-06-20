from fastapi import APIRouter
from app.api.v1 import (
    admin_brands,
    admin_tile_categories,
    admin_tile_skus,
    admin_tiles,
    admin_users,
    auth,
    tiles,
    uploads,
)

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(tiles.router, prefix="/tiles", tags=["tiles"])
api_router.include_router(admin_tiles.router, prefix="/admin/tiles", tags=["admin-tiles"])
api_router.include_router(admin_users.router, prefix="/admin/users", tags=["admin-users"])
api_router.include_router(admin_brands.router, prefix="/admin/brands", tags=["admin-brands"])
api_router.include_router(
    admin_tile_categories.router,
    prefix="/admin/tile-categories",
    tags=["admin-tile-categories"],
)
api_router.include_router(
    admin_tile_skus.router,
    prefix="/admin/tile-skus",
    tags=["admin-tile-skus"],
)
api_router.include_router(uploads.router, prefix="/admin/uploads", tags=["uploads"])
