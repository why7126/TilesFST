# 文档用途：后端Docker镜像构建
# 文档内容：Python3.12 + uv + FastAPI运行环境
# 内容来源：AI自动生成，项目团队确认
# 更新方式：后端依赖、启动命令变化时更新
# 备注：用于docker-compose本地部署与演示环境

FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

RUN pip install --no-cache-dir uv

COPY pyproject.toml ./
RUN uv sync --no-dev || uv pip install --system fastapi uvicorn pydantic minio python-multipart

COPY app ./app

RUN mkdir -p /app/data

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
