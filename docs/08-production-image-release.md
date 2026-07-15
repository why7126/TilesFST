---
title: 生产镜像包构建与云服务器部署手册
purpose: 记录 tilesfst-release-v0.0.1 的 x86_64 镜像包构建、交付和云服务器部署流程
created_at: 2026-06-30 21:52:26
updated_at: 2026-07-15 23:57:27
owner: 项目团队
status: draft
---

# 生产镜像包构建与云服务器部署手册

本文记录 `tilesfst-release-v0.0.1` 的离线镜像包构建与云服务器部署流程。当前流程已验证：后端镜像构建、Web 镜像构建、镜像导出、云服务器 Docker Compose 启动、登录、头像上传、外部 MinIO 读写、用户资料更新。云服务器宿主机 Nginx 域名反代尚未完成验证。

## 1. 部署目标

生产部署采用：

```text
云服务器宿主机 Nginx（80/443，域名与 HTTPS）
  → TilesFST Web 容器（Nginx，宿主机 127.0.0.1:3000 或临时 0.0.0.0:3000）
  → TilesFST Backend 容器（FastAPI，容器内 8000）
  → 外部 MySQL 8.0+
  → 外部 MinIO / S3 兼容对象存储
```

交付包名称固定为：

```text
tilesfst-release-v0.0.1
```

镜像目标架构固定为：

```text
linux/amd64
```

## 2. 交付包目录

发布产物建议放在项目目录外，避免大镜像包进入 Git 工作区。例如：

```bash
export RELEASE_DIR="$HOME/CodeSpaces/Projects/ProjectTilesFST/releases/v0.0.1"
mkdir -p "$RELEASE_DIR/images"
```

当前已验证的本地发布产物目录为：

```text
~/CodeSpaces/Projects/ProjectTilesFST/releases/v0.0.1/
```

对外交付时可将该目录整体打包或重命名为：

```text
tilesfst-release-v0.0.1/
```

推荐交付结构如下：

```text
tilesfst-release-v0.0.1/
├── images/
│   ├── tilesfst-v0.0.1-linux-amd64.tar.gz
│   └── tilesfst-v0.0.1-linux-amd64.tar.gz.sha256
├── docker-compose.yml
├── .env.example
└── README-deploy.md
```

说明：

- `images/*.tar.gz` 为离线镜像包，包含业务运行依赖。
- `images/*.sha256` 为镜像包校验文件。
- `docker-compose.yml` 为交付版编排文件，使用 `image:`，不使用 `build:`。
- `.env.example` 只能包含示例值；真实 `.env` 只在服务器上创建，不提交 Git。
- `README-deploy.md` 可从本文摘取服务器操作步骤生成。

## 3. 构建前置条件

本地构建机需要：

```text
Docker / OrbStack / Docker Desktop
docker buildx
可访问基础镜像源与依赖包源
```

检查 buildx：

```bash
docker buildx version
```

创建或启用 builder：

```bash
docker buildx create --name tilesfst-builder --driver docker-container --use
docker buildx inspect --bootstrap
```

若 `docker buildx inspect --bootstrap` 卡在 `context deadline exceeded`，通常是 Docker / OrbStack 后端状态异常。可重启 Docker / OrbStack 后执行：

```bash
docker buildx ls
docker ps -a | grep buildx
docker buildx inspect tilesfst-builder
docker context ls
docker info
docker buildx ls
docker buildx rm tilesfst-builder
docker buildx create --name tilesfst-builder --driver docker-container --use
docker buildx inspect --bootstrap
```

本次实际构建中，先创建 `tilesfst-builder`，遇到 BuildKit 状态查询超时后，通过 `docker buildx rm tilesfst-builder` 清理并重新创建 builder 后继续构建。

## 4. 脚本化构建镜像包

推荐使用 `scripts/build-images.sh` + env 文件完成后端镜像、Web 镜像、基础验证、离线包导出和 sha256 校验文件生成。

准备构建配置：

```bash
cp scripts/build-images.env.example scripts/build-images.env
```

编辑 `scripts/build-images.env`：

```env
IMAGE_BUILD_TAG=v0.0.1
IMAGE_BUILD_PLATFORM=linux/amd64
IMAGE_BUILD_BACKEND_IMAGE=tilesfst-backend
IMAGE_BUILD_WEB_IMAGE=tilesfst-web
IMAGE_BUILD_RELEASE_DIR=../releases/v0.0.1
IMAGE_BUILD_TAR_NAME=tilesfst-v0.0.1-linux-amd64.tar.gz
IMAGE_BUILD_EXPORT_TAR=true
```

执行构建：

```bash
./scripts/build-images.sh
```

如需使用临时配置文件，可传入 env 路径：

```bash
./scripts/build-images.sh /path/to/build-images.env
```

脚本会依次执行：

1. 检查 Docker 与 buildx。
2. 按 env 配置创建或复用 `IMAGE_BUILD_BUILDER`。
3. 构建 `IMAGE_BUILD_BACKEND_IMAGE:IMAGE_BUILD_TAG` 与 `IMAGE_BUILD_WEB_IMAGE:IMAGE_BUILD_TAG`。
4. 验证镜像平台、后端依赖导入与 Web Nginx 配置。
5. 当 `IMAGE_BUILD_EXPORT_TAR=true` 时，导出 gzip 离线镜像包并生成 `.sha256`。

输出示例：

```text
../releases/v0.0.1/images/tilesfst-v0.0.1-linux-amd64.tar.gz
../releases/v0.0.1/images/tilesfst-v0.0.1-linux-amd64.tar.gz.sha256
```

`scripts/build-images.env` 为本地构建配置，禁止提交；可提交的示例文件是 `scripts/build-images.env.example`。

## 5. 手工参考：构建后端镜像

在项目根目录执行：

```bash
docker buildx build \
  --platform linux/amd64 \
  -t tilesfst-backend:v0.0.1 \
  -f src/backend/Dockerfile \
  --load \
  src/backend
```

后端镜像构建时会执行 `uv sync --locked --no-dev --no-install-project`，Python 运行依赖会进入镜像。云服务器部署时不需要再安装 Python 包。

验证后端镜像架构：

```bash
docker image inspect tilesfst-backend:v0.0.1 --format '{{.Os}}/{{.Architecture}}'
```

期望输出：

```text
linux/amd64
```

验证后端依赖：

```bash
docker run --rm tilesfst-backend:v0.0.1 \
  uv run --no-sync python -c "import fastapi, sqlalchemy, pymysql, minio; print('backend deps ok')"
```

## 6. 手工参考：构建 Web 镜像

在项目根目录执行：

```bash
docker buildx build \
  --platform linux/amd64 \
  -t tilesfst-web:v0.0.1 \
  -f src/web/Dockerfile \
  --load \
  .
```

Web 镜像为多阶段构建：

- builder 阶段安装 Node 依赖并执行 `npm run build`。
- runtime 阶段只包含 Nginx 与 `dist` 静态资源。

因此生产 Web 镜像不需要携带完整 `node_modules`，云服务器部署时也不需要安装 Node 依赖。

验证 Web 镜像架构：

```bash
docker image inspect tilesfst-web:v0.0.1 --format '{{.Os}}/{{.Architecture}}'
```

期望输出：

```text
linux/amd64
```

验证 Web Nginx 配置：

```bash
docker run --rm tilesfst-web:v0.0.1 nginx -t
```

## 7. 手工参考：导出离线镜像包

创建交付目录：

```bash
export RELEASE_DIR="$HOME/CodeSpaces/Projects/ProjectTilesFST/releases/v0.0.1"
mkdir -p "$RELEASE_DIR/images"
```

导出并压缩镜像：

```bash
docker save \
  tilesfst-backend:v0.0.1 \
  tilesfst-web:v0.0.1 \
  | gzip > "$RELEASE_DIR/images/tilesfst-v0.0.1-linux-amd64.tar.gz"
```

生成校验文件：

```bash
cd "$RELEASE_DIR/images"
shasum -a 256 tilesfst-v0.0.1-linux-amd64.tar.gz \
  > tilesfst-v0.0.1-linux-amd64.tar.gz.sha256
```

本次实际执行的产物目录命令为：

```bash
mkdir -p ~/CodeSpaces/Projects/ProjectTilesFST/releases/v0.0.1/images
docker save tilesfst-backend:v0.0.1 tilesfst-web:v0.0.1 | gzip > ~/CodeSpaces/Projects/ProjectTilesFST/releases/v0.0.1/images/tilesfst-v0.0.1-linux-amd64.tar.gz
cd ~/CodeSpaces/Projects/ProjectTilesFST/releases/v0.0.1/images
shasum -a 256 tilesfst-v0.0.1-linux-amd64.tar.gz > tilesfst-v0.0.1-linux-amd64.tar.gz.sha256
```

说明：`docker load` 支持直接加载 gzip 压缩的镜像包，服务器无需手动解压。

### 7.1 本次已验证的端到端构建命令

以下命令为本次 `tilesfst-release-v0.0.1` 构建验证使用的完整流水，已将 shell 历史中的换行转义整理为可直接复制执行的格式：

```bash
docker buildx version

docker buildx create --name tilesfst-builder --use
docker buildx inspect --bootstrap

docker buildx ls
docker ps -a | grep buildx
docker buildx inspect tilesfst-builder
docker context ls
docker info
docker buildx ls

docker buildx rm tilesfst-builder
docker buildx create --name tilesfst-builder --driver docker-container --use
docker buildx inspect --bootstrap

docker buildx build \
  --platform linux/amd64 \
  -t tilesfst-backend:v0.0.1 \
  -f src/backend/Dockerfile \
  --load \
  src/backend

docker buildx build \
  --platform linux/amd64 \
  -t tilesfst-web:v0.0.1 \
  -f src/web/Dockerfile \
  --load \
  .

docker image ls
docker image inspect tilesfst-backend:v0.0.1 --format '{{.Os}}/{{.Architecture}}'
docker image inspect tilesfst-web:v0.0.1 --format '{{.Os}}/{{.Architecture}}'

mkdir -p ~/CodeSpaces/Projects/ProjectTilesFST/releases/v0.0.1/images
docker save tilesfst-backend:v0.0.1 tilesfst-web:v0.0.1 | gzip > ~/CodeSpaces/Projects/ProjectTilesFST/releases/v0.0.1/images/tilesfst-v0.0.1-linux-amd64.tar.gz

cd ~/CodeSpaces/Projects/ProjectTilesFST/releases/v0.0.1/images
ls
shasum -a 256 tilesfst-v0.0.1-linux-amd64.tar.gz > tilesfst-v0.0.1-linux-amd64.tar.gz.sha256
```

## 8. 交付版 docker-compose.yml

交付版 `docker-compose.yml` 使用 `image:`，不使用 `build:`：

```yaml
services:
  # FastAPI 后端服务
  # 生产环境只连接外部 MySQL 和外部 MinIO，不在本 compose 内启动数据库/对象存储
  backend:
    image: tilesfst-backend:v0.0.1
    container_name: tilesfst-backend-prod

    # 后端生产环境变量
    # 敏感信息从同目录 .env 注入，不要直接写死在 compose 中
    environment:
      APP_ENV: production
      APP_DEBUG: "false"

      # 应用密钥：生产必须替换为强随机值
      APP_SECRET_KEY: ${APP_SECRET_KEY:?Set APP_SECRET_KEY}

      # 外部 MySQL 8.0+ 连接串
      # 示例：mysql+pymysql://user:password@mysql-host:3306/tilesfst?charset=utf8mb4
      DATABASE_URL: ${DATABASE_URL:?Set MySQL DATABASE_URL}

      # 后端容器内部监听地址和端口，一般不要修改
      BACKEND_HOST: 0.0.0.0
      BACKEND_PORT: 8000

      # 默认管理员账号，仅首次初始化空库时使用
      ADMIN_USERNAME: ${ADMIN_USERNAME:-admin}
      ADMIN_INITIAL_PASSWORD: ${ADMIN_INITIAL_PASSWORD:?Set ADMIN_INITIAL_PASSWORD}
      ADMIN_RESET_PASSWORD_ON_STARTUP: ${ADMIN_RESET_PASSWORD_ON_STARTUP:-false}

      # 外部 MinIO / S3 兼容对象存储配置
      # MINIO_ENDPOINT 示例：minio.example.com:9000；不要包含 http:// 或 https://
      MINIO_ENDPOINT: ${MINIO_ENDPOINT:?Set external MinIO endpoint}
      MINIO_ACCESS_KEY: ${MINIO_ACCESS_KEY:?Set external MinIO access key}
      MINIO_SECRET_KEY: ${MINIO_SECRET_KEY:?Set external MinIO secret key}
      MINIO_SECURE: ${MINIO_SECURE:-true}
      MINIO_BUCKET: ${MINIO_BUCKET:?Set existing bucket}

      # 对象存储前缀：一个 Bucket 内按前缀区分资源类型
      MINIO_PREFIX_IMAGES: ${MINIO_PREFIX_IMAGES:-images/}
      MINIO_PREFIX_FILES: ${MINIO_PREFIX_FILES:-files/}
      MINIO_PREFIX_THUMBNAILS: ${MINIO_PREFIX_THUMBNAILS:-thumbnails/}
      MINIO_PREFIX_PROCESSED: ${MINIO_PREFIX_PROCESSED:-processed/}
      MINIO_PREFIX_TEMP: ${MINIO_PREFIX_TEMP:-tmp/}
      MINIO_PREFIX_VIDEO: ${MINIO_PREFIX_VIDEO:-videos/}
      MINIO_PREFIX_VIDEO_COVER: ${MINIO_PREFIX_VIDEO_COVER:-videos/covers/}
      MINIO_PREFIX_VIDEO_TRANSCODED: ${MINIO_PREFIX_VIDEO_TRANSCODED:-videos/transcoded/}

      # 上传限制；需与 Web 容器 Nginx client_max_body_size 保持兼容
      MAX_IMAGE_SIZE_MB: ${MAX_IMAGE_SIZE_MB:-20}
      MAX_VIDEO_SIZE_MB: ${MAX_VIDEO_SIZE_MB:-500}
      ALLOWED_IMAGE_TYPES: ${ALLOWED_IMAGE_TYPES:-image/jpeg,image/jpg,image/png,image/webp,image/gif,image/svg+xml,image/bmp,image/tiff,image/heic}
      ALLOWED_VIDEO_TYPES: ${ALLOWED_VIDEO_TYPES:-video/mp4,video/quicktime,video/x-msvideo,video/webm,video/x-matroska,video/mpeg,video/3gpp}

    # 后端本地临时处理目录
    # 业务媒体文件正式存储在外部 MinIO，不写入这些目录
    volumes:
      - ./data/processed:/app/data/processed
      - ./data/tmp:/app/data/tmp

    networks:
      - tilesfst

  # Web 前端服务
  # Nginx 托管 React 静态资源，并反向代理 /api/ 和 /media/ 到 backend
  web:
    image: tilesfst-web:v0.0.1
    container_name: tilesfst-web-prod

    # 宿主机端口映射
    # 正式生产推荐 HOST_PORT_WEB=127.0.0.1:3000，由宿主机 Nginx 反代访问
    # 临时公网测试可用 HOST_PORT_WEB=3000，并在安全组放行 TCP 3000
    ports:
      - "${HOST_PORT_WEB:-127.0.0.1:3000}:80"

    depends_on:
      - backend

    networks:
      - tilesfst

networks:
  tilesfst:
    driver: bridge
```

## 9. 服务器 .env 示例

在云服务器交付目录中创建 `.env`，不要提交真实 `.env`：

```env
APP_ENV=production
APP_DEBUG=false
APP_SECRET_KEY=replace-with-strong-random-secret

DATABASE_URL=mysql+pymysql://tiles_user:replace-with-secret@mysql.example.com:3306/tilesfst?charset=utf8mb4

ADMIN_USERNAME=admin
ADMIN_INITIAL_PASSWORD=replace-with-first-login-password
ADMIN_RESET_PASSWORD_ON_STARTUP=false

MINIO_ENDPOINT=minio.example.com:9000
MINIO_ACCESS_KEY=replace-with-external-access-key
MINIO_SECRET_KEY=replace-with-external-secret-key
MINIO_SECURE=true
MINIO_BUCKET=tile-info-platform

MINIO_PREFIX_IMAGES=images/
MINIO_PREFIX_FILES=files/
MINIO_PREFIX_THUMBNAILS=thumbnails/
MINIO_PREFIX_PROCESSED=processed/
MINIO_PREFIX_TEMP=tmp/
MINIO_PREFIX_VIDEO=videos/
MINIO_PREFIX_VIDEO_COVER=videos/covers/
MINIO_PREFIX_VIDEO_TRANSCODED=videos/transcoded/

MAX_IMAGE_SIZE_MB=20
MAX_VIDEO_SIZE_MB=500
ALLOWED_IMAGE_TYPES=image/jpeg,image/jpg,image/png,image/webp,image/gif,image/svg+xml,image/bmp,image/tiff,image/heic
ALLOWED_VIDEO_TYPES=video/mp4,video/quicktime,video/x-msvideo,video/webm,video/x-matroska,video/mpeg,video/3gpp

# 正式生产推荐仅绑定本机，由宿主机 Nginx 暴露 80/443
HOST_PORT_WEB=127.0.0.1:3000
```

注意：

- `DATABASE_URL` 必须是 MySQL 8.0+，生产不得使用 SQLite。
- `MINIO_ENDPOINT` 不要写 `http://` 或 `https://`。
- `MINIO_SECURE=true` 表示 HTTPS；HTTP 内网对象存储使用 `false`。
- 外部 MinIO 必须提前创建 `MINIO_BUCKET`，并授予当前 AccessKey 读写权限。

## 10. 云服务器部署步骤

上传交付包到服务器，例如：

```text
/root/workspace/TilesFST/tilesfst-release-v0.0.1/
```

进入目录：

```bash
cd /root/workspace/TilesFST/tilesfst-release-v0.0.1
```

校验镜像包：

```bash
cd images
shasum -a 256 -c tilesfst-v0.0.1-linux-amd64.tar.gz.sha256
cd ..
```

加载镜像：

```bash
docker load -i images/tilesfst-v0.0.1-linux-amd64.tar.gz
```

确认镜像：

```bash
docker images | grep tilesfst
```

生成并编辑 `.env`：

```bash
cp .env.example .env
```

检查 Compose：

```bash
docker compose config
```

启动：

```bash
docker compose up -d
```

查看状态：

```bash
docker compose ps
docker compose logs web --tail=100
docker compose logs backend --tail=100
```

## 11. 冒烟验证

验证 Web 容器：

```bash
curl -I http://127.0.0.1:3000
```

期望：

```text
HTTP/1.1 200 OK
```

验证后端健康：

```bash
docker compose exec backend uv run --no-sync python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8000/health').read().decode())"
```

验证后端读取到的 MinIO 配置：

```bash
docker compose exec backend uv run --no-sync python -c "from app.core.config import settings; print('endpoint=', settings.minio_endpoint); print('secure=', settings.minio_secure); print('bucket=', settings.minio_bucket); print('access_key=', settings.minio_access_key)"
```

注意：若输出仍为 `endpoint= minio:9000`、`access_key= minioadmin`，说明 `.env` 未正确配置为外部 MinIO，上传会返回 `502 对象存储不可用`。

验证外部 MinIO bucket：

```bash
docker compose exec backend uv run --no-sync python -c "from app.core.config import settings; from minio import Minio; c=Minio(settings.minio_endpoint, access_key=settings.minio_access_key, secret_key=settings.minio_secret_key, secure=settings.minio_secure); print('bucket_exists=', c.bucket_exists(settings.minio_bucket))"
```

验证对象写入权限：

```bash
docker compose exec backend uv run --no-sync python -c "from io import BytesIO; from app.core.config import settings; from minio import Minio; c=Minio(settings.minio_endpoint, access_key=settings.minio_access_key, secret_key=settings.minio_secret_key, secure=settings.minio_secure); c.put_object(settings.minio_bucket, 'tmp/healthcheck.txt', BytesIO(b'ok'), length=2, content_type='text/plain'); print('put ok')"
```

通过浏览器验证：

1. 打开 Web 页面。
2. 使用管理员账号登录。
3. 打开用户管理。
4. 上传头像，确认上传接口返回 200。
5. 确认头像 URL `/media/images/...` 可显示。
6. 创建或编辑用户，确认用户列表刷新正常。

## 12. 宿主机 Nginx 接入

当前容器部署流程已验证，宿主机 Nginx 反代尚未完成验证。若云服务器已有其他项目占用 80/443，推荐使用独立子域名，例如：

```text
tiles.example.com
```

在宿主机 Nginx 新增独立站点配置，反代到本机 Web 容器端口：

```nginx
server {
    listen 80;
    server_name tiles.example.com;

    client_max_body_size 512m;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

若配置 HTTPS，则在 `443 ssl` 的 `server` 中使用同样的 `location /` 反代规则，并配置证书路径。

检查并重载：

```bash
nginx -t
systemctl reload nginx
```

生产建议只在安全组开放 80/443，不长期开放 3000。

## 13. 常见问题

### 12.1 公网 IP:3000 访问不了

若 `.env` 使用：

```env
HOST_PORT_WEB=127.0.0.1:3000
```

则公网 `IP:3000` 无法访问，这是预期行为。服务器本机执行：

```bash
curl -I http://127.0.0.1:3000
```

若返回 200，说明容器正常。正式生产应通过宿主机 Nginx 域名访问。

临时公网测试可改为：

```env
HOST_PORT_WEB=3000
```

然后：

```bash
docker compose down
docker compose up -d
```

同时在云厂商安全组放行 TCP 3000。

### 12.2 上传文件返回 502 对象存储不可用

先查看后端实际配置：

```bash
docker compose exec backend uv run --no-sync python -c "from app.core.config import settings; print(settings.minio_endpoint, settings.minio_secure, settings.minio_bucket, settings.minio_access_key)"
```

若仍是 `minio:9000` 或 `minioadmin`，说明 `.env` 未替换为外部 MinIO 配置。

再检查 bucket：

```bash
docker compose exec backend uv run --no-sync python -c "from app.core.config import settings; from minio import Minio; c=Minio(settings.minio_endpoint, access_key=settings.minio_access_key, secret_key=settings.minio_secret_key, secure=settings.minio_secure); print(c.bucket_exists(settings.minio_bucket))"
```

常见原因：

- `MINIO_ENDPOINT` 写了 `http://` 或 `https://`。
- `MINIO_SECURE` 与外部 MinIO 协议不一致。
- `MINIO_BUCKET` 不存在。
- AccessKey / SecretKey 错误。
- AccessKey 没有 `GetObject` / `PutObject` / `ListBucket` 权限。
- 云服务器到 MinIO endpoint 的安全组或防火墙未放行。

### 12.3 创建用户返回 422

`422 Unprocessable Entity` 表示请求体校验失败。创建用户请求必须包含：

```json
{
  "username": "testuser01",
  "display_name": "测试用户",
  "role": "employee",
  "avatar_object_key": null
}
```

规则：

- `username` 长度 4-32。
- 用户名建议小写字母开头，例如 `testuser01`。
- `display_name` 最长 32。
- `role` 必须为 `admin`、`employee` 或 `store_owner`。

浏览器开发者工具中查看 `POST /api/v1/admin/users` 的 Response，可看到具体字段错误。

## 14. 已验证与待验证

已验证：

- `linux/amd64` 后端镜像构建。
- `linux/amd64` Web 镜像构建。
- 镜像导出为 `tilesfst-v0.0.1-linux-amd64.tar.gz` 并生成 `.sha256`。
- 镜像包在云服务器加载。
- `docker compose up -d` 启动 backend 与 web。
- 服务器本机 `curl -I http://127.0.0.1:3000` 返回 200。
- 管理端登录、用户列表、头像上传、媒体读取、用户资料更新。
- 外部 MinIO 配置修正后，上传与读取 `/media/...` 正常。

待验证：

- 宿主机 Nginx 使用生产域名反代到 `127.0.0.1:3000`。
- HTTPS 证书配置与 80 → 443 跳转。
- 腾讯云安全组仅开放 80/443 的生产访问路径。
