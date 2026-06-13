from fastapi import APIRouter
from app.api import auth, products, categories, brands, files, employees, statistics

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(products.router)
api_router.include_router(categories.router)
api_router.include_router(brands.router)
api_router.include_router(files.router)
api_router.include_router(employees.router)
api_router.include_router(statistics.router)