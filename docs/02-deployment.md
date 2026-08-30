---
purpose: 部署文档
content: 部署组件、环境变量和运行方式
source: AI自动生成初稿，项目团队确认
update_method: 项目初始化后由人工确认；后续由AI辅助更新并经人工Review
created_at: 2026-06-13 00:00:00
updated_at: 2026-08-30 09:55:00
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

SKU 图片上传会在后端生成同目录 `.thumb` 缩略图和 `.display` 详情展示图。后端运行依赖包含 Pillow，用于 JPG、PNG、WebP 解码、等比缩小和重编码；Docker 构建通过 `src/backend/uv.lock` 还原该依赖，部署环境无需额外手工安装系统外 Python 包。默认媒体 URL 仍走 `/media/{object_key}` 受控读取；如启用 `OBJECT_STORAGE_DIRECT_READ_ENABLED=true`，后端只返回短期对象存储直出读取 URL，前端不得持有对象存储永久密钥。

## 环境变量

参考 `.env.example`。

## 生产镜像包交付

`tilesfst-release-v0.0.1` 的 `linux/amd64` 镜像构建、离线交付包、外部 MySQL / 外部对象存储云服务器部署与冒烟验证流程，见 [08-production-image-release.md](08-production-image-release.md)。

正式发布涉及镜像交付或 Docker/Compose/数据库 schema/migration 等构建输入变化时，先执行 `/image-prepare <version>` 生成 `releases/<version>/image-build-plan.json`，再执行 `/image-build <version>` 复用下方脚本构建镜像并生成 `releases/<version>/image-manifest.json`。`/release-publish` 会使用 plan/manifest 校验版本、tag 和 input hash 是否仍一致。

正式部署或升级前 SHOULD 生成版本升级计划。每次正常发布默认生成并校验 `fresh -> <to-version>` 与 `<previous-release-version> -> <to-version>` 两类计划；计划目标环境跟随 `release.json.release_target.environment`。开发环境发布使用 development 目标计划，生产发布需单独生成或校验 production 目标计划。跨版本升级计划不默认生成，只有用户明确指定来源旧版本时才通过 `/upgrade-plan --from <old-version> --to <to-version>` 或等价脚本命令生成。

```bash
python scripts/validate-release-upgrade.py plan --from fresh --to vX.Y.Z --target development
python scripts/validate-release-upgrade.py plan --from <previous-release-version> --to vX.Y.Z --target development
python scripts/validate-release-upgrade.py validate-plan --plan releases/vX.Y.Z/upgrade-plans/<from>-to-vX.Y.Z.<target>.json
```

升级计划位于 `releases/<to-version>/upgrade-plans/`，用于区分：

- 首次部署：`fresh -> <to-version>`，按目标环境校验目标 release、目标镜像、env、数据库初始化、对象存储配置、Compose config 和部署后 smoke。
- 相邻升级：`<previous-version> -> <to-version>`，按目标环境校验 env diff、`TILESFST_IMAGE_TAG` 切换、DB drift/smoke、备份、重启和升级后 smoke。
- 跨版本升级：`<old-version> -> <to-version>`，由用户按需手工生成，必须聚合中间版本 DB、env、Docker、API、对象存储和维护任务影响；缺少演练或证据时标记为 `cross-version-upgrade-requires-manual-review` 或 `unsupported`。

三类部署均复用同一目标版本 backend / web 镜像，不为首次部署、相邻升级或跨版本升级分别构建不同业务镜像。开发环境计划不得替代生产发布计划；生产回滚前必须确认旧镜像、旧 env 摘要、DB 备份、对象存储影响和回滚后 smoke；DB 回滚不得脱离备份恢复或已验证反向迁移策略。

推荐使用脚本 + env 的方式构建生产镜像：

```bash
cp scripts/build-images.env.example scripts/build-images.env
# 编辑 scripts/build-images.env，设置 IMAGE_BUILD_TAG、IMAGE_BUILD_PLATFORM、基础镜像源等
./scripts/build-images.sh
```

也可传入自定义 env 文件：

```bash
./scripts/build-images.sh /path/to/build-images.env
```

`scripts/build-images.env` 属于本地构建配置，已加入 `.gitignore`；可提交的变量示例为 `scripts/build-images.env.example`。

## 产品文档 `/docs` 访问边界

产品版本公告和按需生成的产品使用文档事实源位于 `releases/`，其中产品使用文档只在用户确认需要时生成到 `releases/vX.Y.Z/usage-docs/`。`mintlify/` 是公开文档站源目录，站点页面由 release 快照同步或投影到 `mintlify/docs/vX.Y.Z/` 与 `mintlify/docs/latest/`，公告投影到 `mintlify/releases/vX.Y.Z/announcement.mdx`，共享截图资产位于 `mintlify/assets/screenshots/`。项目计划通过 `域名/docs` 浏览公开文档，但仓库内只维护 Mintlify 源文件、导航配置和发布校验材料，不提交外部 DNS、托管平台账号、生产私有域名、密钥或凭据。

`域名/docs` 可由以下任一部署方式承载：

- Mintlify 或等价静态文档平台配置 base path 为 `/docs`。
- Cloudflare / Vercel / CDN rewrite 将 `/docs/**` 转发到 Mintlify 文档站。
- 外层 Nginx 反向代理将 `/docs/**` 转发到文档站或静态文档构建产物。
- 本地或演示环境启用 Docker Compose `docs-site` profile 启动 Mintlify 预览服务。

若发布时尚未确认 `/docs` 的真实承载方式，`/release-prepare <version>` 必须在 `release.json` 记录 blocker 或待确认项。公开产品使用文档只能包含产品使用说明、功能入口、操作注意事项和版本差异；内部运维、API、数据库、对象存储凭据、生产私有域名或敏感配置不得混入公开文档。

## Docker Compose 部署方案

本项目默认支持 Docker Compose 本地开发、演示部署和生产等价校验。根目录 `docker-compose.yml` 是本地/demo 编排事实源；其他 Compose 文档和 `deploy/local/compose.yml` 的服务名、端口、profile、卷挂载与上传 Nginx 变量必须以它为基线同步。

根目录 `docker-compose.yml` 的默认拓扑：

- 默认服务：`tilesfst-backend`、`tilesfst-web`。
- 可选本地对象存储：启用 `self-hosted-storage` profile 后启动 `tilesfst-minio`、`tilesfst-minio-init`。
- 本地默认文档站预览：local 启动脚本默认启用 `docs-site` profile 并启动 `tilesfst-docs-site`。
- 默认宿主机端口：Backend `HOST_PORT_BACKEND:-8000`，Web `HOST_PORT_WEB:-3000`，MinIO API `HOST_PORT_MINIO_API:-9000`，MinIO Console `HOST_PORT_MINIO_CONSOLE:-9001`，Mintlify docs-site `HOST_PORT_MINTLIFY_DOCS:-3001`。
- 本地持久化目录：`data/sqlite/`、`data/processed/`、`data/tmp/`；仅启用项目自建 MinIO 时使用 `data/minio/`。
- Web 容器运行时仅替换 `UPLOAD_*` Nginx 变量，避免误替换 Nginx 内置变量。
- Compose project name 固定为 `tilesfst`；本地脚本同样显式使用 `--project-name tilesfst`，避免因入口目录不同生成 `local_*` 或 `projecttilesfst_*` 网络、镜像与容器标签。
- 长期运行服务统一配置 `restart: unless-stopped`，支持异常退出后自动拉起；MinIO 初始化任务配置 `restart: on-failure`，仅失败时重试，成功后不重复执行。

### deploy 环境矩阵

中期部署入口集中在 `deploy/`：

- `deploy/local/compose.yml`：本地六种环境复用同一拓扑，并以根目录 `docker-compose.yml` 为基线；通过 env 示例和 `self-hosted-storage` profile 区分数据库与对象存储。
- `deploy/prod/compose.tencent-cos.yml`：生产外部 MySQL + 腾讯云 COS 拓扑，不启动本地 MinIO，默认通过 `docs-site` profile 启动 `tilesfst-docs-site`。
- `deploy/scripts/up.sh` / `deploy/scripts/down.sh`：按 `<domain> <environment>` 解析 env、Compose、profile 并执行校验。
- `deploy/scripts/validate-env.py`：阻断生产 SQLite、示例密钥、`APP_DEBUG=true`、COS 自动建桶和 MinIO profile 错配。
- 根目录 `docker-compose.prod.yml` 与 `docker-compose.prod.external.yml` 保留为 VPS/离线交付兼容入口；新生产矩阵优先使用 `deploy/prod/compose.tencent-cos.yml`。

| 环境 ID | 数据库 | 对象存储 | 启动命令 |
|---|---|---|---|
| `local-sqlite-minio-managed` | SQLite | 项目自建 MinIO | `./deploy/scripts/up.sh local sqlite-minio-managed` |
| `local-sqlite-minio-external` | SQLite | 本机已 Docker 部署 MinIO | `./deploy/scripts/up.sh local sqlite-minio-external` |
| `local-sqlite-tencent-cos` | SQLite | 腾讯云 COS | `./deploy/scripts/up.sh local sqlite-tencent-cos` |
| `local-mysql-minio-managed` | 本机 MySQL | 项目自建 MinIO | `./deploy/scripts/up.sh local mysql-minio-managed` |
| `local-mysql-minio-external` | 本机 MySQL | 本机已 Docker 部署 MinIO | `./deploy/scripts/up.sh local mysql-minio-external` |
| `local-mysql-tencent-cos` | 本机 MySQL | 腾讯云 COS | `./deploy/scripts/up.sh local mysql-tencent-cos` |
| `prod-mysql-tencent-cos` | 外部 MySQL | 腾讯云 COS | `./deploy/scripts/up.sh prod mysql-tencent-cos` |

环境变量差异通过 `deploy/local/*.env.example` 或 `deploy/prod/*.env.example` 表达；服务拓扑差异通过 Compose 和 profile 表达，不为本地六种环境复制六份完整 Compose。env 示例必须按环境标识、应用安全、数据库、镜像、对象存储、端口等主题分组，并在变量注释中写明候选值或候选格式。真实 env 文件禁止提交。

### 生产媒体维护任务

`deploy/prod/compose.tencent-cos.yml` 提供 `maintenance` profile 下的 `tilesfst-maintenance` 服务，用于在生产等价镜像内执行媒体维护任务。该服务复用后端镜像、外部 MySQL 与腾讯云 COS env 示例，不启动本地 MinIO，也不要求把仓库根目录脚本 bind-mount 到生产容器。日常运维优先使用 `deploy/scripts/media-maintenance.sh` 包装入口；后端包内 `python -m app.modules.media.maintenance` 保持为容器内真实执行入口。

默认命令为只读对象 Key 审计：

```bash
./deploy/scripts/media-maintenance.sh prod mysql-tencent-cos object-key-audit --limit 100
```

维护入口支持 dry-run 优先的任务：`object-key-audit`、`backfill-brand-certificate-thumbnails`、`backfill-image-variants`、`formalize-pending-tile-images`、`migrate-certificate-image-keys` 和 `media-drift-reconcile`。`bug-0116-media-drift` 仅作为历史兼容别名保留，不作为生产推荐命令。写入数据库或对象存储时必须显式追加 `--apply --confirm-backup`，并在执行前完成 MySQL 与对象存储 bucket/prefix 备份。任务输出只允许记录统计摘要、对象 Key hash、标准前缀、任务状态和媒体验收摘要，不得输出数据库连接串、对象存储密钥、Authorization header、Cookie、真实 `.env` 内容或本机绝对路径。

### 服务组成

| 服务 | 容器名 | 端口 | 说明 |
|---|---|---|---|
| tilesfst-backend | tilesfst-backend | 8000 | FastAPI 后端服务 |
| tilesfst-web | tilesfst-web | 3000 | React Web 展示端与管理端 |
| tilesfst-minio | tilesfst-minio | 9000 / 9001 | 本地自建对象存储与控制台，仅 `self-hosted-storage` profile 启动 |
| tilesfst-docs-site | tilesfst-docs-site | 3001 | Mintlify 文档站预览，仅 `docs-site` profile 启动 |
| tilesfst-maintenance | tilesfst-maintenance | 无 | 生产媒体维护作业，仅 `maintenance` profile 按需 `run --rm` 启动 |

### 启动命令

默认兼容启动命令转调 `local-sqlite-minio-managed`：

```bash
./scripts/docker-up.sh
```

- 当选择 `*-tencent-cos`、`*-minio-external` 等云上或外部对象存储环境时，只启动 `tilesfst-backend` 与 `tilesfst-web`，不会启动本地 `minio` / `minio-init`。
- 当选择 `*-minio-managed` 环境时，脚本会启用 `self-hosted-storage` profile 并启动项目自建 MinIO。
- 若不使用脚本，根目录本地云对象存储场景直接执行 `docker compose up -d --build tilesfst-backend tilesfst-web`；本地自建 MinIO 场景执行 `docker compose --profile self-hosted-storage up -d --build tilesfst-backend tilesfst-web tilesfst-minio tilesfst-minio-init`。
- 本地启动脚本默认同时启动 `tilesfst-docs-site`。文档站默认访问 `http://localhost:${HOST_PORT_MINTLIFY_DOCS:-3001}`。
- 若只需要单独启动公开文档站，先确认 `mintlify/docs.json` 与 `mintlify/docs/**` 已生成，再执行 `docker compose --profile docs-site up -d --build tilesfst-docs-site`。该服务使用 `deploy/docs-site/Dockerfile` 构建本地可复用 docs-site 镜像，镜像内预装 Mintlify CLI；Mintlify 预览缓存不作为业务数据持久化，仅留在容器临时文件系统内，不写宿主机 `~/.mintlify*`。
- 同时启动业务系统和文档站可执行 `docker compose --profile docs-site up -d --build tilesfst-backend tilesfst-web tilesfst-docs-site`；若还需要本地 MinIO，再叠加 `--profile self-hosted-storage` 并显式包含 `tilesfst-minio tilesfst-minio-init`。

### Mintlify 文档站部署选择

生产默认启动 Compose 内 `tilesfst-docs-site`，也可按实际部署改为外部 Mintlify 托管、静态托管、CDN rewrite 或反向代理。未确认生产承载方式时，`/release-prepare <version>` 必须记录 blocker 或待确认项。

发布范围包含 `docs-site` service、Compose profile、`HOST_PORT_MINTLIFY_DOCS`、`DOCS_SITE_NODE_BASE_IMAGE`、`TILESFST_DOCS_SITE_IMAGE_REPOSITORY`、`MINTLIFY_CLI_VERSION` 或文档站 Dockerfile 时，必须记录 Docker Compose config 校验；若涉及镜像交付输入，按发布规范评估 `/image-prepare` 与 `/image-build`。真实 Mintlify 账号、token、生产域名和外部托管凭据不得写入仓库。

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
- 当 `OBJECT_STORAGE_PROVIDER=tencent-cos`、`volcengine-tos` 或 `s3-compatible` 时，默认 `docker compose up` / `./scripts/docker-up.sh` 不启动本地 `tilesfst-minio` 和 `tilesfst-minio-init`。
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
| `docker-compose.yml` | 本地/demo 编排事实源：tilesfst-backend、tilesfst-web、可选 self-hosted-storage、可选 docs-site；Compose project name 固定为 `tilesfst` |
| `docker-compose.prod.yml` | VPS 生产兼容编排（外部 MySQL + 自建 MinIO） |
| `docker-compose.prod.external.yml` | VPS 生产兼容编排（外部 MySQL + 外部 MinIO/S3 兼容或云上对象存储） |
| `mintlify/docs.json` | Mintlify 文档站唯一主配置 |
| `mintlify/site-manifest.json` | 文档站版本投影与共享截图摘要 |
| `deploy/local/compose.yml` | 本地环境矩阵 Compose；服务拓扑与根目录 `docker-compose.yml` 保持一致 |
| `deploy/prod/compose.tencent-cos.yml` | 当前推荐生产拓扑：外部 MySQL + 腾讯云 COS |
| `deploy/local/*.env.example` | 本地环境矩阵 env 示例 |
| `deploy/prod/*.env.example` | 生产 env 示例 |
| `deploy/scripts/` | 部署 up/down/validate 入口 |
| `src/backend/Dockerfile` | 后端镜像构建 |
| `src/backend/.env.docker` | 后端Docker环境变量 |
| `src/web/Dockerfile` | Web镜像构建 |
| `src/web/nginx.conf.template` | Web容器运行时Nginx模板，支持上传反代超时环境变量 |
| `src/web/nginx.conf` | Web静态资源与API代理配置默认参考 |

### 配置注释维护规范

- `docker-compose*.yml`、`deploy/**/*.yml`、`src/backend/Dockerfile`、`src/web/Dockerfile`、`.env`、`.env.example`、`deploy/**/*.env.example`、`src/backend/.env.example`、`src/backend/.env.docker` 必须保留解释性注释。
- 后续新增或修改 service、environment、ports、volumes、networks、构建阶段、启动命令或环境变量时，必须同步更新邻近注释。
- 注释用于说明用途、默认值含义、生产安全边界、持久化影响和端口映射关系，不得写入真实密钥、真实客户数据或敏感生产地址。

### 注意事项

- 本地自建 MinIO 的默认账号密码仅用于开发环境；云上对象存储场景不会启动本地 MinIO。
- `TILESFST_IMAGE_TAG` 用于生产 Compose 与离线交付 Compose 的统一镜像版本；默认 backend/web 共用同一个 tag。本地开发 `docker-compose.yml` 直接从源码 build，不依赖该变量。
- `TILESFST_BACKEND_IMAGE_REPOSITORY` / `TILESFST_WEB_IMAGE_REPOSITORY` 仅用于覆盖镜像仓库名；发版只改版本时无需修改。
- 生产环境必须更换密钥，并使用安全的配置管理方式。
- 本地开发与演示默认 SQLite；生产环境必须使用外部 MySQL `DATABASE_URL`。
- **大文件上传（图片/视频/文档）**：后端通过 `MAX_IMAGE_SIZE_MB`、`MAX_VIDEO_SIZE_MB`、`MAX_FILE_SIZE_MB` 与 `ALLOWED_*_TYPES` 限制（见根目录 `.env.example`）。Web 容器 Nginx 使用 `src/web/nginx.conf.template` 渲染运行时配置，并在 `/api/v1/admin/uploads` 无尾斜杠精确路径和 `/api/v1/admin/uploads/` 子路径上单独设置 `UPLOAD_CLIENT_MAX_BODY_SIZE`（默认 `512m`）、`UPLOAD_PROXY_SEND_TIMEOUT_SECONDS` / `UPLOAD_PROXY_READ_TIMEOUT_SECONDS` / `UPLOAD_SEND_TIMEOUT_SECONDS`（默认 `600` 秒）和 `UPLOAD_PROXY_REQUEST_BUFFERING`（默认 `off`）。无尾斜杠入口必须直接反代到后端同路径，不得返回 301/302/307/308 或生成丢失宿主机端口的重定向。修改模板、默认配置或上传反代变量后 MUST **重建并重启 Web 镜像**（`docker compose build tilesfst-web && docker compose up -d tilesfst-web`），仅重启 tilesfst-backend 不会更新 Nginx 配置。详见 `docs/standards/file-upload.md`。
- 修改任一 Compose 文件、deploy env 示例、Dockerfile 或上传代理变量后，必须至少执行对应的 `docker compose config` 校验；涉及根目录本地基线时同时校验 `docker compose config --quiet`。

## VPS 生产部署（外部 MySQL + 自建 MinIO）

生产部署使用 `docker-compose.prod.yml`，仅启动 `tilesfst-backend`、`tilesfst-web`、`tilesfst-minio`、`tilesfst-minio-init`，不内嵌 MySQL 服务。客户需提前提供 MySQL 8.0+ 实例。

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
TILESFST_IMAGE_TAG=v0.0.4
TILESFST_BACKEND_IMAGE_REPOSITORY=tilesfst-backend
TILESFST_WEB_IMAGE_REPOSITORY=tilesfst-web
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
OBJECT_STORAGE_ENDPOINT=tilesfst-minio:9000
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
6. 重启 `tilesfst-backend`、`tilesfst-web`、`minio` 后再次访问同一 `/media/{object_key}`，确认 MinIO 持久化有效。

### MinIO 生产策略

- 生产 MinIO 使用 Docker named volume `minio-data` 持久化。
- `minio-init` 只创建一个 `OBJECT_STORAGE_BUCKET`，并设置 anonymous `none`。
- 桶内继续使用 `images/`、`videos/`、`videos/covers/`、`processed/` 等前缀；禁止为不同业务随意新增 Bucket。

## VPS 生产部署（外部 MySQL + 外部对象存储）

若客户同时提供 MySQL 8.0+ 与外部 MinIO、自建 S3 兼容服务、腾讯云 COS 或火山云 TOS，使用 `docker-compose.prod.external.yml`。该文件只启动 `tilesfst-backend` 与 `tilesfst-web`，不会启动 `mysql`、`tilesfst-minio`、`tilesfst-minio-init`。

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
TILESFST_IMAGE_TAG=v0.0.4
TILESFST_BACKEND_IMAGE_REPOSITORY=tilesfst-backend
TILESFST_WEB_IMAGE_REPOSITORY=tilesfst-web
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

生产域名外层 HTTPS 反代也必须对上传路径单独加长超时，并放在通用 `location /` 前。外层代理必须同时覆盖 `/api/v1/admin/uploads` 无尾斜杠精确路径和 `/api/v1/admin/uploads/` 子路径；无尾斜杠头像上传入口不得被 301 到丢失端口的地址。否则 COS 中已写入对象后，浏览器仍可能在 60 秒默认网关窗口收到 `504`。

```nginx
server {
    listen 443 ssl;
    server_name tilesfst.wjoyhappy.site;

    ssl_certificate     /etc/nginx/certs/tilesfst/tilesfst.wjoyhappy.site_bundle.crt;
    ssl_certificate_key /etc/nginx/certs/tilesfst/tilesfst.wjoyhappy.site.key;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    client_max_body_size 512m;

    location = /api/v1/admin/uploads {
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

1. `docker compose -f docker-compose.prod.external.yml config --services` 仅应输出 `tilesfst-backend`、`tilesfst-web`。
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
