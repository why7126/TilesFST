from fastapi import APIRouter
from app.api.v1 import (
    admin_banners,
    admin_brands,
    admin_profile,
    admin_tile_categories,
    admin_tile_skus,
    admin_tile_specs,
    admin_tiles,
    admin_topics,
    admin_users,
    admin_system_settings,
    admin_api_docs,
    auth,
    profile,
    tiles,
    uploads,
)

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(profile.router, prefix="/profile", tags=["profile"])
api_router.include_router(admin_profile.router, prefix="/admin/profile", tags=["admin-profile"])
api_router.include_router(tiles.router, prefix="/tiles", tags=["tiles"])
api_router.include_router(admin_tiles.router, prefix="/admin/tiles", tags=["admin-tiles"])
api_router.include_router(admin_users.router, prefix="/admin/users", tags=["admin-users"])
api_router.include_router(
    admin_system_settings.router,
    prefix="/admin/system-settings",
    tags=["admin-system-settings"],
)
api_router.include_router(admin_api_docs.router, prefix="/admin/api-docs")
api_router.include_router(admin_brands.router, prefix="/admin/brands", tags=["admin-brands"])
api_router.include_router(admin_banners.router, prefix="/admin/banners", tags=["admin-banners"])
api_router.include_router(admin_topics.router, prefix="/admin/topics", tags=["admin-topics"])
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
api_router.include_router(
    admin_tile_specs.router,
    prefix="/admin/tile-specs",
    tags=["admin-tile-specs"],
)
api_router.include_router(uploads.router, prefix="/admin/uploads", tags=["uploads"])
