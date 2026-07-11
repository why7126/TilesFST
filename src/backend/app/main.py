from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.error_codes import INVALID_PARAMETER
from app.core.exceptions import AppError
from app.core.request_logging import RequestLoggingMiddleware
from app.db.seed import seed_admin_user
from app.db.session import get_session_factory, init_database
from app.modules.media.storage import get_media_file_response

app = FastAPI(
    title="TilesFST API",
    version="0.1.0",
    swagger_ui_parameters={"tryItOutEnabled": settings.allow_swagger_try_it_out()},
)
app.add_middleware(RequestLoggingMiddleware)
app.include_router(api_router, prefix="/api/v1")


@app.exception_handler(AppError)
async def app_error_handler(_: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.code, "message": exc.message, "data": exc.data},
    )


def _validation_field(location: list[str]) -> str:
    if not location:
        return "request"
    source = location[0]
    rest = location[1:]
    if source in {"body", "form"} and rest:
        return ".".join(rest)
    if rest:
        return ".".join([source, *rest])
    return source


def _normalize_validation_errors(exc: RequestValidationError) -> list[dict[str, object]]:
    errors: list[dict[str, object]] = []
    for item in exc.errors():
        location = [str(part) for part in item.get("loc", [])]
        errors.append(
            {
                "field": _validation_field(location),
                "message": str(item.get("msg") or "字段校验失败"),
                "type": str(item.get("type") or "validation_error"),
                "location": location,
            }
        )
    return errors


@app.exception_handler(RequestValidationError)
async def request_validation_error_handler(
    _: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "code": INVALID_PARAMETER,
            "message": "请求参数无效",
            "data": {"errors": _normalize_validation_errors(exc)},
        },
    )


@app.on_event("startup")
def on_startup() -> None:
    init_database()
    session = get_session_factory()()
    try:
        seed_admin_user(session)
    finally:
        session.close()


@app.get("/health", summary="健康检查", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/media/{object_key:path}", include_in_schema=False)
def read_media_file(object_key: str):
    return get_media_file_response(object_key)
