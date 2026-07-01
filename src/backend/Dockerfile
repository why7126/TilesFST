# 文档用途：后端 Docker 镜像构建
# 文档内容：Python 3.12 + uv + FastAPI 运行环境
# 内容来源：AI自动生成，项目团队确认
# 更新方式：后端依赖、启动命令、运行目录或端口变化时必须同步更新注释
# 备注：用于 docker-compose 本地部署、演示环境与生产镜像构建

# 官方基础镜像备用写法；当前启用国内镜像源以提升本地构建稳定性。
# FROM python:3.12-slim
# Python 3.12 slim 运行时，满足项目后端技术栈约束。
FROM m.daocloud.io/docker.io/python:3.12-slim

# pip / uv 国内索引备用写法；仅在网络环境需要时取消注释。
# ENV PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
# ENV UV_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple

# 容器内应用根目录；后续 COPY、RUN、CMD 均以此为工作目录。
WORKDIR /app

# Python 与 uv 运行参数：避免 pyc 写入、开启无缓冲日志并优化 uv 安装产物。
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# 安装 uv，用于按 uv.lock 还原后端依赖。
RUN pip install --no-cache-dir uv

# 先复制依赖声明文件，以便 Docker 构建缓存复用依赖安装层。
COPY pyproject.toml uv.lock ./
# 安装锁定的生产依赖，不安装项目自身与 dev 依赖。
RUN uv sync --locked --no-dev --no-install-project

# 复制 FastAPI 应用代码。
COPY app ./app

# 创建容器内数据根目录；具体持久化路径由 docker-compose volumes 挂载。
RUN mkdir -p /app/data

# 声明 FastAPI 容器内监听端口；宿主机映射由 docker-compose 控制。
EXPOSE 8000

# 启动 FastAPI 应用；host/port 与 docker-compose 容器内端口保持一致。
CMD ["uv", "run", "--no-sync", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
