---
purpose: 部署文档
content: 部署组件、环境变量和运行方式
source: AI自动生成初稿，项目团队确认
update_method: 项目初始化后由人工确认；后续由AI辅助更新并经人工Review
created_at: 2026-06-13 00:00:00
updated_at: 2026-07-01 09:01:07
note: 适用于瓷砖信息管理平台项目模板
---

# 部署说明


## 部署组件

- FastAPI 应用服务
- SQLite 数据库文件（本地开发 / demo）
- 外部 MySQL 8.0+（生产）
- MinIO 对象存储
- Web 静态资源

## 环境变量

参考 `.env.example`。

## 生产镜像包交付

`tilesfst-release-v0.0.1` 的 `linux/amd64` 镜像构建、离线交付包、外部 MySQL / 外部 MinIO 云服务器部署与冒烟验证流程，见 [08-production-image-release.md](08-production-image-release.md)。

## Docker Compose 部署方案

本项目默认支持 Docker Compose 本地开发与演示部署。

### 服务组成

| 服务 | 容器名 | 端口 | 说明 |
|---|---|---|---|
| backend | tile-info-platform-backend | 8000 | FastAPI 后端服务 |
| web | tile-info-platform-web | 3000 | React Web 展示端与管理端 |
| minio | tile-info-platform-minio | 9000 / 9001 | 对象存储与控制台 |

### 启动命令

```bash
./scripts/docker-up.sh
```

### 停止命令

```bash
./scripts/docker-down.sh
```

### 数据持久化

- SQLite 数据文件挂载到 `./data/sqlite/`。
- MinIO 数据映射到 `./data/minio/`，为本地 Docker 下对象存储持久化卷；桶内对象增长属预期行为。
- 业务媒体上传正式写入 MinIO `MINIO_BUCKET`，**不**写入 `data/uploads/`。
- `data/processed/`、`data/tmp/` 仍挂载供处理后产物与临时文件使用。

### Legacy uploads 清理

若曾在对象存储迁移（BUG-0006）前使用本地上传，宿主机 `data/uploads/` 可能残留无数据库引用的孤儿文件。清理方式：

```bash
python scripts/clean_legacy_uploads.py
python scripts/clean_legacy_uploads.py --apply
```

说明见 `data/README.md` 与 `docs/07-object-storage-strategy.md` §3。

### 默认管理员与密码恢复

Docker Compose 通过根目录 `.env` 向后端注入默认管理员相关变量：

```env
ADMIN_USERNAME=admin
ADMIN_INITIAL_PASSWORD=change-me-on-first-run
ADMIN_RESET_PASSWORD_ON_STARTUP=false
```

- 空数据库首次启动时，如果 `ADMIN_INITIAL_PASSWORD` 已配置，系统会创建 `ADMIN_USERNAME` 对应的 `admin` 角色账号，密码以 bcrypt 哈希写入 `users.password_hash`。
- `./data/sqlite/` 是持久化目录。数据库中已存在默认管理员时，普通服务重启不会自动覆盖该账号密码，也不会因为修改 `.env` 中的 `ADMIN_INITIAL_PASSWORD` 而静默重置密码。
- 若本地开发、演示或受控运维场景需要恢复默认管理员密码，可临时设置 `ADMIN_RESET_PASSWORD_ON_STARTUP=true` 并重启后端。恢复完成后应立即改回 `false`，避免后续重启再次覆盖管理员密码。
- 恢复流程不会在日志、接口响应或文档中输出明文密码；生产环境应使用安全的运维流程和密钥管理系统注入真实密码。

### 配置文件

| 文件 | 作用 |
|---|---|
| `docker-compose.yml` | 服务编排 |
| `docker-compose.prod.yml` | VPS 生产编排（外部 MySQL + 自建 MinIO） |
| `docker-compose.prod.external.yml` | VPS 生产编排（外部 MySQL + 外部 MinIO） |
| `src/backend/Dockerfile` | 后端镜像构建 |
| `src/backend/.env.docker` | 后端Docker环境变量 |
| `src/web/Dockerfile` | Web镜像构建 |
| `src/web/nginx.conf` | Web静态资源与API代理配置 |

### 配置注释维护规范

- `docker-compose*.yml`、`src/backend/Dockerfile`、`src/web/Dockerfile`、`.env`、`.env.example`、`src/backend/.env.example`、`src/backend/.env.docker` 必须保留解释性注释。
- 后续新增或修改 service、environment、ports、volumes、networks、构建阶段、启动命令或环境变量时，必须同步更新邻近注释。
- 注释用于说明用途、默认值含义、生产安全边界、持久化影响和端口映射关系，不得写入真实密钥、真实客户数据或敏感生产地址。

### 注意事项

- 本地默认 MinIO 账号密码仅用于开发环境。
- 生产环境必须更换密钥，并使用安全的配置管理方式。
- 本地开发与演示默认 SQLite；生产环境必须使用外部 MySQL `DATABASE_URL`。
- **大文件上传（图片/视频）**：后端通过 `MAX_IMAGE_SIZE_MB`、`MAX_VIDEO_SIZE_MB` 与 `ALLOWED_*_TYPES` 限制（见根目录 `.env.example`）。Web 容器 Nginx 在 `src/web/nginx.conf` 中配置 `client_max_body_size`，须 ≥ `max(MAX_IMAGE_SIZE_MB, MAX_VIDEO_SIZE_MB)`（默认 `512m`）。修改 `nginx.conf` 后 MUST **重建并重启 Web 镜像**（`docker compose build web && docker compose up -d web`），仅重启 backend 不会更新 Nginx body 限制。详见 `docs/standards/file-upload.md`。

## VPS 生产部署（外部 MySQL + 自建 MinIO）

生产部署使用 `docker-compose.prod.yml`，仅启动 `backend`、`web`、`minio`、`minio-init`，不内嵌 MySQL 服务。客户需提前提供 MySQL 8.0+ 实例。

### MySQL 前置检查

| 检查项 | 要求 |
|---|---|
| 版本 | MySQL 8.0+ |
| 字符集 | `utf8mb4` |
| Collation | 推荐 `utf8mb4_unicode_ci` |
| 账号权限 | 目标库具备 DDL + DML 权限，可执行 `CREATE TABLE`、`CREATE INDEX`、`INSERT`、`UPDATE`、`SELECT` |
| 网络 | VPS 可访问 MySQL 主机与端口，安全组 / 白名单已放行 |
| 密钥 | `APP_SECRET_KEY`、MySQL 密码、MinIO 密钥、管理员初始密码不得使用 `.env.example` 示例值 |

### 生产环境变量

```env
APP_ENV=production
APP_DEBUG=false
APP_SECRET_KEY=replace-with-secret
DATABASE_URL=mysql+pymysql://tiles_user:replace-with-secret@mysql.example.com:3306/tilesfst?charset=utf8mb4
ADMIN_USERNAME=admin
ADMIN_INITIAL_PASSWORD=replace-with-first-login-password
ADMIN_RESET_PASSWORD_ON_STARTUP=false
MINIO_ACCESS_KEY=replace-with-non-default-access-key
MINIO_SECRET_KEY=replace-with-non-default-secret-key
MINIO_BUCKET=tile-info-platform
HOST_PORT_BACKEND=8000
HOST_PORT_WEB=3000
```

- `APP_ENV=production` 时，后端必须使用 MySQL `DATABASE_URL`；缺失、SQLite URL 或非法 URL 会在启动时快速失败。
- `SQLITE_DATABASE_URL` 只用于非生产；生产 Compose 不挂载 `./data/sqlite`。
- `DATABASE_URL` 日志输出会隐藏密码，不应在文档、Issue、日志截图中暴露真实连接串。

### 启动与校验

```bash
cp .env.example .env
# 编辑 .env，替换所有生产密钥与 DATABASE_URL
docker compose -f docker-compose.prod.yml config
docker compose -f docker-compose.prod.yml up -d --build
```

生产冒烟：

1. 打开 `http://<host>:<HOST_PORT_WEB>`，确认 Web 可访问。
2. 打开 `http://<host>:<HOST_PORT_BACKEND>/health`，确认后端健康。
3. 使用 `ADMIN_USERNAME` / `ADMIN_INITIAL_PASSWORD` 登录管理端。
4. 完成一次品牌 Logo 或 SKU 图片上传，确认返回 `/media/{object_key}`，并可通过 Web 反代读取。
5. 重启 `backend`、`web`、`minio` 后再次访问同一 `/media/{object_key}`，确认 MinIO 持久化有效。

### MinIO 生产策略

- 生产 MinIO 使用 Docker named volume `minio-data` 持久化。
- `minio-init` 只创建一个 `MINIO_BUCKET`，并设置 anonymous `none`。
- 桶内继续使用 `images/`、`videos/`、`videos/covers/`、`processed/` 等前缀；禁止为不同业务随意新增 Bucket。

## VPS 生产部署（外部 MySQL + 外部 MinIO）

若客户同时提供 MySQL 8.0+ 与外部 MinIO/S3 兼容对象存储，使用 `docker-compose.prod.external.yml`。该文件只启动 `backend` 与 `web`，不会启动 `mysql`、`minio`、`minio-init`。

### 外部 MinIO 前置检查

| 检查项 | 要求 |
|---|---|
| Endpoint | `MINIO_ENDPOINT` 可从 VPS backend 容器访问，例如 `minio.example.com:9000` |
| TLS | HTTPS 场景设置 `MINIO_SECURE=true`；仅内网明文测试可设为 `false` |
| Bucket | `MINIO_BUCKET` 已提前创建，继续采用一个项目一个 Bucket |
| 权限 | `MINIO_ACCESS_KEY` / `MINIO_SECRET_KEY` 对该 Bucket 具备最小读写权限 |
| 前缀 | 继续使用 `images/`、`videos/`、`videos/covers/`、`processed/` 等对象前缀 |
| 网络 | VPS 到外部 MinIO endpoint 的端口、安全组、白名单已放行 |

### 外部服务型生产环境变量

```env
APP_ENV=production
APP_DEBUG=false
APP_SECRET_KEY=replace-with-secret
DATABASE_URL=mysql+pymysql://tiles_user:replace-with-secret@mysql.example.com:3306/tilesfst?charset=utf8mb4
ADMIN_USERNAME=admin
ADMIN_INITIAL_PASSWORD=replace-with-first-login-password
ADMIN_RESET_PASSWORD_ON_STARTUP=false
MINIO_ENDPOINT=minio.example.com:9000
MINIO_ACCESS_KEY=replace-with-external-access-key
MINIO_SECRET_KEY=replace-with-external-secret-key
MINIO_SECURE=true
MINIO_BUCKET=tile-info-platform
HOST_PORT_BACKEND=8000
HOST_PORT_WEB=3000
```

### 启动与校验

```bash
cp .env.example .env
# 编辑 .env，替换 DATABASE_URL 与外部 MinIO 连接信息
docker compose -f docker-compose.prod.external.yml config
docker compose -f docker-compose.prod.external.yml up -d --build
```

外部服务型生产冒烟：

1. `docker compose -f docker-compose.prod.external.yml config --services` 仅应输出 `backend`、`web`。
2. 打开 `http://<host>:<HOST_PORT_BACKEND>/health`，确认后端健康。
3. 使用默认管理员登录管理端。
4. 完成一次品牌 Logo 或 SKU 图片上传，确认对象写入外部 `MINIO_BUCKET`。
5. 访问上传响应中的 `/media/{object_key}`，确认由 backend 受控读取对象。

说明：

- 外部 MinIO 场景不会自动创建 Bucket；Bucket 与权限由运维前置准备。
- Web 仍通过 `/media/` 反代 backend，前端不直连对象存储写入。
- 该部署同样不挂载 `./data/sqlite`，生产结构化数据全部写入外部 MySQL。

## V4 环境变量与数据目录

初始化本地环境：

```bash
cp .env.example .env
./scripts/docker-up.sh
```

Docker Compose 会使用：

```text
.env.example
src/backend/.env.docker
data/sqlite/
data/minio/          # MinIO 持久化卷（正式业务媒体落盘）
data/uploads/        # 历史兼容目录；迁移后不应新增业务文件
data/processed/
data/tmp/
```

生产环境不得直接使用示例密钥，必须通过部署平台注入真实环境变量。

## Docker Compose 端口策略

默认开发端口：

```text
Backend: 8000
Web: 3000
MinIO API: 9000
MinIO Console: 9001
```

采用：

```text
容器内部端口固定
宿主机端口通过 .env 配置
```

示例：

```env
HOST_PORT_BACKEND=18080
HOST_PORT_WEB=13000
```

## MinIO 单桶策略

使用一个项目一个 Bucket：

```env
MINIO_BUCKET=tile-info-platform
```

并在桶内通过前缀区分：

```text
original/
thumbnails/
processed/
videos/
videos/covers/
videos/transcoded/
```
