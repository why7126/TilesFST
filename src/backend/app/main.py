from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.v1.router import api_router
from app.core.exceptions import AppError
from app.db.seed import seed_admin_user
from app.db.session import get_session_factory, init_database

app = FastAPI(title="TilesFST API", version="0.1.0")
app.include_router(api_router, prefix="/api/v1")


@app.exception_handler(AppError)
async def app_error_handler(_: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.code, "message": exc.message, "data": None},
    )


@app.on_event("startup")
def on_startup() -> None:
    init_database()
    session = get_session_factory()()
    try:
        seed_admin_user(session)
    finally:
        session.close()


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
