---
purpose: 环境变量管理规范
content: .env.example维护、环境变量命名、安全边界、Docker Compose环境同步规则
source: AI自动生成初稿，项目团队确认
update_method: 新增服务、端口、密钥、第三方配置、对象存储、数据库或视频处理参数时更新
created_at: 2026-06-13 00:00:00
updated_at: 2026-08-03 19:10:00
note: .env.example 可提交，.env 禁止提交
---

# 环境变量管理规范

## 1. 基本原则

- 根目录必须提供 `.env.example`。
- 真实 `.env` 文件禁止提交Git。
- 新增任何环境变量时，必须同步更新 `.env.example`。
- 新增或修改任何 `.env` / `.env.example` / `.env.docker` 变量时，必须在变量上一行同步维护注释，说明用途、取值范围、默认值含义或安全边界。
- 新增或修改 Docker Compose、Dockerfile 配置时，必须为新增/调整的 service、environment、ports、volumes、networks、构建阶段和启动命令补充注释。
- Docker Compose 使用的变量必须在 `.env.example` 中有说明。
- `deploy/**/*.env.example` 可提交，真实 `deploy/**/*.env`、`deploy/**/*.env.local`、`deploy/**/*.env.prod` 禁止提交。
- `deploy/**/*.env.example` 必须按环境标识、应用安全、数据库、镜像、对象存储、端口等适用主题分组；每个非空变量行上一行必须说明用途、候选值或候选格式、默认值含义或安全边界。
- 生产部署 env 示例必须使用占位值，并明确禁止示例密钥、SQLite、`APP_DEBUG=true` 和 `OBJECT_STORAGE_AUTO_CREATE_BUCKET=true` 进入生产。
- Mintlify 文档站服务必须通过 `docs-site` 或等价 profile 启用；相关 `HOST_PORT_MINTLIFY_DOCS`、`MINTLIFY_NODE_IMAGE` 等变量必须在 `.env.example` 中说明，不得把真实托管 token、账号或生产域名写入仓库。
- 镜像构建使用的本地 env 示例必须放在 `scripts/build-images.env.example`；真实 `scripts/build-images.env` 禁止提交。
- 常规镜像发版路径下，`scripts/build-images.env.example` SHOULD 只要求修改 `IMAGE_BUILD_TAG`；输出目录 SHOULD 由 `IMAGE_BUILD_TAG` 默认推导到仓库外 `../releases/<version>/images/`，tar 文件名 SHOULD 由 `IMAGE_BUILD_TAG` 与 `IMAGE_BUILD_PLATFORM` 默认推导。
- `/image-prepare` MAY 从 `scripts/build-images.env.example` 创建真实本地 `scripts/build-images.env`，并 MAY 自动把安全白名单变量 `IMAGE_BUILD_TAG` 更新为当前发布版本；不得自动写入密钥、数据库连接串、对象存储凭据或任何未列入镜像构建安全摘要的变量。
- 不允许在代码、文档示例、测试中写入真实密钥。
- 生产 `APP_ENV=production` 时必须显式配置 MySQL `DATABASE_URL`，不得依赖 SQLite 回退。

## 2. 命名规范

环境变量使用大写蛇形命名：

```text
SERVICE_NAME_CONFIG_NAME
```

示例：

```text
MINIO_BUCKET_TILE_IMAGES
MAX_VIDEO_SIZE_MB
VITE_API_BASE_URL
```

## 3. AI更新规则

AI修改以下内容时，必须检查 `.env.example`：

- `docker-compose.yml`
- `docker-compose.prod.yml`
- `docker-compose.prod.external.yml`
- `deploy/local/compose.yml`
- `deploy/prod/compose.tencent-cos.yml`
- `deploy/**/*.env.example`
- `deploy/scripts/*`
- `scripts/build-images.env.example`
- `src/backend/.env.example`
- `src/backend/.env.docker`
- `src/web/package.json`
- `src/web/orval.config.ts`
- MinIO存储桶
- SQLite数据库路径
- MySQL `DATABASE_URL`
- 上传大小限制
- 视频处理配置
- image plan / manifest schema 或镜像构建输入 hash 规则
- Mintlify 文档站 Compose profile、端口、镜像或站点挂载目录

同时必须检查并维护注释：

- `.env.example`、`.env`、`deploy/**/*.env.example`、`src/backend/.env.example`、`src/backend/.env.docker` 中每个非空变量行上一行 SHOULD 有注释；新增变量 MUST 有注释。
- `docker-compose*.yml` 中新增或修改的服务、端口、卷、网络、环境变量 MUST 有邻近注释。
- `src/backend/Dockerfile`、`src/web/Dockerfile` 中新增或修改的 FROM、ENV、RUN、COPY、EXPOSE、CMD 等关键指令 MUST 有邻近注释。
- 注释不得包含真实密钥、真实生产域名、真实客户数据或无法公开的运维信息。

## 4. 安全要求

- `.env.example` 只能包含示例值。
- 密码必须使用明显的示例值，不得伪装成真实密码。
- 生产环境密钥应通过部署平台或密钥管理系统注入。
- `image-build-plan.json` 与 `image-manifest.json` 只能记录构建 env 安全摘要和输入 hash，不得记录 raw env、数据库连接串、密钥、Authorization header、Cookie、本机绝对路径或真实客户数据。
- `deploy/scripts/validate-env.py` 类校验脚本只能输出变量名、环境 ID、blocker 和修复建议，不得输出真实变量值。
