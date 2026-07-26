---
purpose: 部署文档
content: 部署组件、环境变量和运行方式
source: AI自动生成初稿，项目团队确认
update_method: 项目初始化后由人工确认；后续由AI辅助更新并经人工Review
created_at: 2026-06-13 00:00:00
updated_at: 2026-07-26 15:19:59
note: 适用于瓷砖信息管理平台项目模板
---

# 部署说明


## 部署组件

- FastAPI 应用服务
- SQLite 数据库文件（本地开发 / demo）
- 外部 MySQL 8.0+（生产）
- MinIO / S3 兼容对象存储
- Web 静态资源

### Web 静态资源与产品 Logo

Web 镜像构建会将 `src/web/public/` 下的静态资源复制到前端站点根路径。产品自身 Logo 固定放在 `src/web/public/logos/`，当前使用 `64x64.png`、`128x128.png`、`256x256.png` 三个尺寸，分别服务于管理端品牌区、浏览器 favicon 与 Apple touch icon。

`src/web/public/logos/` 属于前端静态资源，不经过对象存储；门店品牌 Logo、SKU 图片、视频封面等业务媒体仍必须通过后端授权上传并写入 `OBJECT_STORAGE_BUCKET`。

## 环境变量

参考 `.env.example`。

## 生产镜像包交付

`tilesfst-release-v0.0.1` 的 `linux/amd64` 镜像构建、离线交付包、外部 MySQL / 外部对象存储云服务器部署与冒烟验证流程，见 [08-production-image-release.md](08-production-image-release.md)。

推荐使用脚本 + env 的方式构建生产镜像：

```bash
cp scripts/build-images.env.example scripts/build-images.env
# 编辑 scripts/build-images.env，设置 IMAGE_BUILD_TAG、IMAGE_BUILD_PLATFORM、基础镜像源、IMAGE_BUILD_RELEASE_DIR 等
./scripts/build-images.sh
```

也可传入自定义 env 文件：

```bash
./scripts/build-images.sh /path/to/build-images.env
```

`scripts/build-images.env` 属于本地构建配置，已加入 `.gitignore`；可提交的变量示例为 `scripts/build-images.env.example`。

## Docker Compose 部署方案

本项目默认支持 Docker Compose 本地开发与演示部署。

### 服务组成

| 服务 | 容器名 | 端口 | 说明 |
|---|---|---|---|
| backend | tilesfst-backend | 8000 | FastAPI 后端服务 |
| web | tilesfst-web | 3000 | React Web 展示端与管理端 |
| minio | tilesfst-minio | 9000 / 9001 | 本地自建对象存储与控制台，仅 `self-hosted-storage` profile 启动 |

### 启动命令

默认启动命令会读取根目录 `.env` 中的 `OBJECT_STORAGE_PROVIDER`：

```bash
./scripts/docker-up.sh
```

- 当 `OBJECT_STORAGE_PROVIDER=tencent-cos`、`volcengine-tos`、`s3-compatible` 等云上或外部对象存储时，只启动 `backend` 与 `web`，不会启动本地 `minio` / `minio-init`。
- 当 `OBJECT_STORAGE_PROVIDER=minio` 或 `self-hosted-minio` 时，脚本会启用 `self-hosted-storage` profile 并启动本地 MinIO。
- 若不使用脚本，本地云对象存储场景直接执行 `docker compose up -d --build`；本地自建 MinIO 场景执行 `docker compose --profile self-hosted-storage up -d --build`。

### Docker 基础镜像源

Compose 构建默认使用官方基础镜像：

- `BACKEND_PYTHON_BASE_IMAGE=python:3.12-slim`
- `WEB_NODE_BASE_IMAGE=node:22-alpine`
- `WEB_NGINX_BASE_IMAGE=nginx:1.27-alpine`

如本地网络访问 Docker Hub 较慢，可在 `.env` 中临时覆盖为可访问的镜像源，例如 `m.daocloud.io/docker.io/python:3.12-slim`、`m.daocloud.io/docker.io/node:22-alpine`、`m.daocloud.io/docker.io/nginx:1.27-alpine`。若使用 `scripts/build-images.sh` 构建离线镜像包，同名变量应写入 `scripts/build-images.env`；脚本会通过 `--build-arg` 传给 Dockerfile。若某个镜像源出现 `failed to fetch anonymous token`、DNS timeout 或 metadata 拉取超时，优先切换上述变量后重新执行 `./scripts/docker-up.sh` 或 `./scripts/build-images.sh`。

### 停止命令

```bash
./scripts/docker-down.sh
```

### 数据持久化

- SQLite 数据文件挂载到 `./data/sqlite/`。
- 当 `OBJECT_STORAGE_PROVIDER=minio` 或 `self-hosted-minio` 时，MinIO 数据映射到 `./data/minio/`，为本地 Docker 下对象存储持久化卷；桶内对象增长属预期行为。
- 当 `OBJECT_STORAGE_PROVIDER=tencent-cos`、`volcengine-tos` 或 `s3-compatible` 时，默认 `docker compose up` / `./scripts/docker-up.sh` 不启动本地 `minio` 和 `minio-init`。
- 业务媒体上传正式写入对象存储 `OBJECT_STORAGE_BUCKET`，**不**写入 `data/uploads/`。
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
| `docker-compose.prod.external.yml` | VPS 生产编排（外部 MySQL + 外部 MinIO/S3 兼容或云上对象存储） |
| `src/backend/Dockerfile` | 后端镜像构建 |
| `src/backend/.env.docker` | 后端Docker环境变量 |
| `src/web/Dockerfile` | Web镜像构建 |
| `src/web/nginx.conf.template` | Web容器运行时Nginx模板，支持上传反代超时环境变量 |
| `src/web/nginx.conf` | Web静态资源与API代理配置默认参考 |

### 配置注释维护规范

- `docker-compose*.yml`、`src/backend/Dockerfile`、`src/web/Dockerfile`、`.env`、`.env.example`、`src/backend/.env.example`、`src/backend/.env.docker` 必须保留解释性注释。
- 后续新增或修改 service、environment、ports、volumes、networks、构建阶段、启动命令或环境变量时，必须同步更新邻近注释。
- 注释用于说明用途、默认值含义、生产安全边界、持久化影响和端口映射关系，不得写入真实密钥、真实客户数据或敏感生产地址。

### 注意事项

- 本地自建 MinIO 的默认账号密码仅用于开发环境；云上对象存储场景不会启动本地 MinIO。
- `TILESFST_BACKEND_IMAGE` / `TILESFST_WEB_IMAGE` 用于生产 Compose 与离线交付 Compose 的镜像名；本地开发 `docker-compose.yml` 直接从源码 build，不依赖这两个变量。
- 生产环境必须更换密钥，并使用安全的配置管理方式。
- 本地开发与演示默认 SQLite；生产环境必须使用外部 MySQL `DATABASE_URL`。
- **大文件上传（图片/视频/文档）**：后端通过 `MAX_IMAGE_SIZE_MB`、`MAX_VIDEO_SIZE_MB`、`MAX_FILE_SIZE_MB` 与 `ALLOWED_*_TYPES` 限制（见根目录 `.env.example`）。Web 容器 Nginx 使用 `src/web/nginx.conf.template` 渲染运行时配置，并在 `/api/v1/admin/uploads/` 上单独设置 `UPLOAD_CLIENT_MAX_BODY_SIZE`（默认 `512m`）、`UPLOAD_PROXY_SEND_TIMEOUT_SECONDS` / `UPLOAD_PROXY_READ_TIMEOUT_SECONDS` / `UPLOAD_SEND_TIMEOUT_SECONDS`（默认 `600` 秒）和 `UPLOAD_PROXY_REQUEST_BUFFERING`（默认 `off`）。修改模板、默认配置或上传反代变量后 MUST **重建并重启 Web 镜像**（`docker compose build web && docker compose up -d web`），仅重启 backend 不会更新 Nginx 配置。详见 `docs/standards/file-upload.md`。

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
| 密钥 | `APP_SECRET_KEY`、MySQL 密码、对象存储密钥、管理员初始密码不得使用 `.env.example` 示例值 |

涉及 Banner 管理、生产 MySQL schema 或迁移的发布，必须在上线前执行目标库 drift 检查：

```bash
python scripts/check-mysql-schema-drift.py --database-url "$DATABASE_URL"
```

该检查只读取 `information_schema`，不得在发布记录中粘贴明文 `DATABASE_URL`。若 `banners` 缺失 `image_source`、`sku_gallery_asset_id`、`topic_id`、`brand_id`、`valid_from`、`valid_to`、`remark` 等字段，必须先部署并执行幂等兼容迁移，复查无阻塞缺列后才能继续发布。

### 生产环境变量

```env
TILESFST_BACKEND_IMAGE=tilesfst-backend:v0.0.4
TILESFST_WEB_IMAGE=tilesfst-web:v0.0.4
APP_ENV=production
APP_DEBUG=false
APP_SECRET_KEY=replace-with-secret
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=120
JWT_REMEMBER_ME_EXPIRE_DAYS=7
DATABASE_URL=mysql+pymysql://tiles_user:replace-with-secret@mysql.example.com:3306/tilesfst?charset=utf8mb4
ADMIN_USERNAME=admin
ADMIN_INITIAL_PASSWORD=replace-with-first-login-password
ADMIN_RESET_PASSWORD_ON_STARTUP=false
OBJECT_STORAGE_PROVIDER=self-hosted-minio
OBJECT_STORAGE_ENDPOINT=minio:9000
OBJECT_STORAGE_ACCESS_KEY=replace-with-non-default-access-key
OBJECT_STORAGE_SECRET_KEY=replace-with-non-default-secret-key
OBJECT_STORAGE_SECURE=false
OBJECT_STORAGE_BUCKET=tilesfst
OBJECT_STORAGE_PATH_STYLE=true
OBJECT_STORAGE_AUTO_CREATE_BUCKET=true
HOST_PORT_BACKEND=8000
HOST_PORT_WEB=3000
UPLOAD_CLIENT_MAX_BODY_SIZE=512m
UPLOAD_CLIENT_BODY_TIMEOUT_SECONDS=600
UPLOAD_PROXY_CONNECT_TIMEOUT_SECONDS=60
UPLOAD_PROXY_SEND_TIMEOUT_SECONDS=600
UPLOAD_PROXY_READ_TIMEOUT_SECONDS=600
UPLOAD_SEND_TIMEOUT_SECONDS=600
UPLOAD_PROXY_REQUEST_BUFFERING=off
```

- `APP_ENV=production` 时，后端必须使用 MySQL `DATABASE_URL`；缺失、SQLite URL 或非法 URL 会在启动时快速失败。
- 本地开发与 demo 直接使用 SQLite `DATABASE_URL`；生产 Compose 不挂载 `./data/sqlite`。
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
5. 若本次发布涉及 Banner 管理，创建一次品牌类型 Banner，确认 `POST /api/v1/admin/banners` 返回 200，响应回显 `brand_id`，刷新列表和编辑回填仍可见。
6. 重启 `backend`、`web`、`minio` 后再次访问同一 `/media/{object_key}`，确认 MinIO 持久化有效。

### MinIO 生产策略

- 生产 MinIO 使用 Docker named volume `minio-data` 持久化。
- `minio-init` 只创建一个 `OBJECT_STORAGE_BUCKET`，并设置 anonymous `none`。
- 桶内继续使用 `images/`、`videos/`、`videos/covers/`、`processed/` 等前缀；禁止为不同业务随意新增 Bucket。

## VPS 生产部署（外部 MySQL + 外部对象存储）

若客户同时提供 MySQL 8.0+ 与外部 MinIO、自建 S3 兼容服务、腾讯云 COS 或火山云 TOS，使用 `docker-compose.prod.external.yml`。该文件只启动 `backend` 与 `web`，不会启动 `mysql`、`minio`、`minio-init`。

### 外部对象存储前置检查

| 检查项 | 要求 |
|---|---|
| Provider | `OBJECT_STORAGE_PROVIDER` 使用 `minio`、`s3-compatible`、`tencent-cos`、`volcengine-tos` 等值；`tencent-cos` 使用腾讯云 `qcloud_cos` 官方 SDK，其余云厂商或 MinIO 使用 S3 兼容适配层 |
| Endpoint | `OBJECT_STORAGE_ENDPOINT` 可从 VPS backend 容器访问，例如 S3 兼容 host:port 或云厂商 endpoint，不含 `http://` / `https://`；腾讯 COS 公网示例为 `cos.ap-guangzhou.myqcloud.com`，内网 endpoint 仅适用于同地域腾讯云内网可达环境 |
| Region | COS/TOS 等云厂商按 bucket 所在区域设置 `OBJECT_STORAGE_REGION`；腾讯广州 COS 使用 `ap-guangzhou`；外部 MinIO 可留空 |
| TLS | HTTPS 场景设置 `OBJECT_STORAGE_SECURE=true`；仅内网明文测试可设为 `false` |
| Bucket | `OBJECT_STORAGE_BUCKET` 已提前创建，继续采用一个项目一个 Bucket |
| 权限 | `OBJECT_STORAGE_ACCESS_KEY` / `OBJECT_STORAGE_SECRET_KEY` 对该 Bucket 具备最小读写权限 |
| 访问风格 | `OBJECT_STORAGE_PATH_STYLE=true` 适合 MinIO；S3 兼容云厂商 virtual-host 风格可设为 `false`；`tencent-cos` 官方 SDK 不依赖该开关 |
| 自动建桶 | 云上对象存储生产环境设置 `OBJECT_STORAGE_AUTO_CREATE_BUCKET=false` |
| 前缀 | 继续使用 `images/`、`videos/`、`videos/covers/`、`processed/` 等对象前缀 |
| 网络 | VPS 到外部 MinIO endpoint 的端口、安全组、白名单已放行 |

### 外部对象存储上传耗时诊断

后端会在上传接口输出 `media_upload_timing` 阶段日志。若视频上传在管理端 99% 或“正在保存视频，请稍候”停留较久，优先查看同一次请求的阶段耗时：

```text
stage=file_read_done
stage=validation_done
stage=storage_put_start
stage=storage_put_done
```

若 `file_read_done` 与 `validation_done` 只有毫秒级，而 `storage_put_done stage_ms` 达到数十秒，说明瓶颈在 Backend 到对象存储的写入链路，不在浏览器上传、FastAPI 读取文件或业务校验。2026-07-24 生产环境中，约 23 MB 视频写入腾讯 COS 观测到 `storage_put_done stage_ms` 约 64 秒，等效吞吐约 360 KB/s。

`OBJECT_STORAGE_PROVIDER=tencent-cos` 已使用腾讯云 `qcloud_cos` 官方 SDK；若使用公网 endpoint 仍慢，应检查服务器出口带宽、VPS 所在地域、到 COS 区域的公网链路和云厂商安全/限速策略。`cos-internal.ap-guangzhou.myqcloud.com` 仅适合同地域腾讯云内网可达环境；非腾讯云或不同地域 VPS 使用该 endpoint 会导致对象存储不可用。

旧 Django 项目若上传体验不同，不应只按框架差异判断。该项目同样是服务端中转上传 COS，但传统 Django Admin 表单不会展示 99% 保存阶段，且旧服务器到 COS 的网络路径可能不同。需要使用同一视频文件在两台服务器上分别记录 `put_object` 阶段耗时后再比较。

服务端中转架构无法避免“浏览器上传完成后 Backend 再上传对象存储”的等待。若生产视频上传必须显著缩短等待，应通过 OpenSpec Change 设计受控直传：后端签发短期凭证或预签名 URL，前端直传 COS/TOS/S3，后端再校验并保存 `object_key`。

### 外部服务型生产环境变量

```env
TILESFST_BACKEND_IMAGE=tilesfst-backend:v0.0.4
TILESFST_WEB_IMAGE=tilesfst-web:v0.0.4
APP_ENV=production
APP_DEBUG=false
APP_SECRET_KEY=replace-with-secret
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=120
JWT_REMEMBER_ME_EXPIRE_DAYS=7
DATABASE_URL=mysql+pymysql://tiles_user:replace-with-secret@mysql.example.com:3306/tilesfst?charset=utf8mb4
ADMIN_USERNAME=admin
ADMIN_INITIAL_PASSWORD=replace-with-first-login-password
ADMIN_RESET_PASSWORD_ON_STARTUP=false
OBJECT_STORAGE_PROVIDER=s3-compatible
OBJECT_STORAGE_ENDPOINT=object-storage.example.com
OBJECT_STORAGE_ACCESS_KEY=replace-with-external-access-key
OBJECT_STORAGE_SECRET_KEY=replace-with-external-secret-key
OBJECT_STORAGE_SECURE=true
OBJECT_STORAGE_BUCKET=tilesfst
OBJECT_STORAGE_REGION=replace-with-region-if-required
OBJECT_STORAGE_PATH_STYLE=false
OBJECT_STORAGE_AUTO_CREATE_BUCKET=false
HOST_PORT_BACKEND=8000
HOST_PORT_WEB=3000
UPLOAD_CLIENT_MAX_BODY_SIZE=512m
UPLOAD_CLIENT_BODY_TIMEOUT_SECONDS=600
UPLOAD_PROXY_CONNECT_TIMEOUT_SECONDS=60
UPLOAD_PROXY_SEND_TIMEOUT_SECONDS=600
UPLOAD_PROXY_READ_TIMEOUT_SECONDS=600
UPLOAD_SEND_TIMEOUT_SECONDS=600
UPLOAD_PROXY_REQUEST_BUFFERING=off
```

### 外层 HTTPS Nginx 上传反代

生产域名外层 HTTPS 反代也必须对上传路径单独加长超时，并放在通用 `location /` 前。否则 COS 中已写入对象后，浏览器仍可能在 60 秒默认网关窗口收到 `504`。

```nginx
server {
    listen 443 ssl;
    server_name tilesfst.wjoyhappy.site;

    ssl_certificate     /etc/nginx/certs/tilesfst/tilesfst.wjoyhappy.site_bundle.crt;
    ssl_certificate_key /etc/nginx/certs/tilesfst/tilesfst.wjoyhappy.site.key;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    client_max_body_size 512m;

    location /api/v1/admin/uploads/ {
        proxy_pass http://127.0.0.1:3000;
        client_max_body_size 512m;
        client_body_timeout 600s;
        proxy_connect_timeout 60s;
        proxy_send_timeout 600s;
        proxy_read_timeout 600s;
        send_timeout 600s;
        proxy_request_buffering off;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
        proxy_set_header X-Forwarded-Host $host;
    }

    location / {
        proxy_pass http://127.0.0.1:3000;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
        proxy_set_header X-Forwarded-Host $host;
    }
}
```

变更后执行：

```bash
nginx -t
systemctl reload nginx
docker compose -f docker-compose.prod.external.yml up -d --build web
```

若使用自建 MinIO 生产编排，将最后一行替换为 `docker compose -f docker-compose.prod.yml up -d --build web`。外层与容器内必须同时生效，才算完成上传 99%/504 类问题的代理层修复。

### 启动与校验

```bash
cp .env.example .env
# 编辑 .env，替换 DATABASE_URL 与外部对象存储连接信息
docker compose -f docker-compose.prod.external.yml config
docker compose -f docker-compose.prod.external.yml up -d --build
```

外部服务型生产冒烟：

1. `docker compose -f docker-compose.prod.external.yml config --services` 仅应输出 `backend`、`web`。
2. 打开 `http://<host>:<HOST_PORT_BACKEND>/health`，确认后端健康。
3. 使用默认管理员登录管理端。
4. 完成一次品牌 Logo 或 SKU 图片上传，确认对象写入外部 `OBJECT_STORAGE_BUCKET`。
5. 访问上传响应中的 `/media/{object_key}`，确认由 backend 受控读取对象。

说明：

- 外部云上对象存储场景不会自动创建 Bucket；Bucket、region、权限、TLS、访问风格和网络白名单由运维前置准备。
- Web 仍通过 `/media/` 反代 backend，前端不直连对象存储写入。
- 该部署同样不挂载 `./data/sqlite`，生产结构化数据全部写入外部 MySQL。

## V4 环境变量与数据目录

初始化本地环境：

```bash
cp .env.example .env
# 编辑 OBJECT_STORAGE_PROVIDER 与 OBJECT_STORAGE_*；云上对象存储无需启用 MinIO profile
./scripts/docker-up.sh
```

Docker Compose 会使用：

```text
.env.example
src/backend/.env.docker
data/sqlite/
data/minio/          # 仅自建 MinIO profile 启动时作为持久化卷
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

## 对象存储单桶策略

使用一个项目一个 Bucket：

```env
OBJECT_STORAGE_BUCKET=tilesfst
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
