---
purpose: 部署环境矩阵入口
content: deploy 目录职责、环境 ID、Compose/env/script 分工
source: REQ-0093 standardize-deployment-environment-matrix
created_at: 2026-08-03 19:10:00
updated_at: 2026-08-06 00:00:00
---

# deploy 部署矩阵

`deploy/` 是部署环境矩阵、环境化 Compose、env 示例和部署脚本的主目录。根目录 `docker-compose.yml` 是本地/demo 编排事实源；`deploy/local/compose.yml` 必须跟随它的服务名、端口、profile、卷挂载和上传 Nginx 变量。根目录 `docker-compose.prod*.yml` 保留 VPS/离线交付兼容入口；新环境优先在 `deploy/` 下表达。

原则：

- 一拓扑一 Compose：服务拓扑变化才新增 Compose 或 profile。
- 一环境一 env 示例：变量差异通过 `*.env.example` 表达。
- 脚本集中：`deploy/scripts/` 负责环境解析、校验、up/down；旧 `scripts/docker-up.sh` 与 `scripts/docker-down.sh` 只做 wrapper。
- 本地基线同步：改动根目录 `docker-compose.yml` 后，同步检查 `deploy/local/compose.yml`、`docs/02-deployment.md`、`deploy/local/README.md` 和 `.env.example`。
- 项目名固定：所有 Compose 文件和部署脚本使用 `tilesfst` 作为 Compose project name，避免入口目录名影响网络、镜像前缀和容器 label。
- 服务自愈：长期运行服务使用 `restart: unless-stopped`；一次性初始化任务使用 `restart: on-failure`，失败重试、成功不循环。
- 安全优先：只提交 `.env.example`，不得提交真实 `.env`、密钥、数据库连接串、客户数据、运行时数据库、MinIO 数据或镜像包。

## 环境矩阵

| 环境 ID | 域 | 数据库 | 对象存储 | Compose | env 示例 |
|---|---|---|---|---|---|
| `local-sqlite-minio-managed` | local | SQLite | 项目自建 MinIO | `deploy/local/compose.yml` + `self-hosted-storage` | `deploy/local/sqlite-minio-managed.env.example` |
| `local-sqlite-minio-external` | local | SQLite | 本机已 Docker 部署 MinIO | `deploy/local/compose.yml` | `deploy/local/sqlite-minio-external.env.example` |
| `local-sqlite-tencent-cos` | local | SQLite | 腾讯云 COS | `deploy/local/compose.yml` | `deploy/local/sqlite-tencent-cos.env.example` |
| `local-mysql-minio-managed` | local | 本机 MySQL | 项目自建 MinIO | `deploy/local/compose.yml` + `self-hosted-storage` | `deploy/local/mysql-minio-managed.env.example` |
| `local-mysql-minio-external` | local | 本机 MySQL | 本机已 Docker 部署 MinIO | `deploy/local/compose.yml` | `deploy/local/mysql-minio-external.env.example` |
| `local-mysql-tencent-cos` | local | 本机 MySQL | 腾讯云 COS | `deploy/local/compose.yml` | `deploy/local/mysql-tencent-cos.env.example` |
| `prod-mysql-tencent-cos` | prod | 外部 MySQL | 腾讯云 COS | `deploy/prod/compose.tencent-cos.yml` | `deploy/prod/mysql-tencent-cos.env.example` |

## 命令

```bash
./deploy/scripts/up.sh local sqlite-minio-managed
./deploy/scripts/up.sh local mysql-tencent-cos
./deploy/scripts/up.sh prod mysql-tencent-cos
./deploy/scripts/down.sh local
./deploy/scripts/down.sh prod
```

兼容入口：

```bash
./scripts/docker-up.sh
./scripts/docker-down.sh
```

默认兼容入口等价于 `local sqlite-minio-managed`。

## Compose 入口选择

| 场景 | 推荐入口 |
|---|---|
| 最小本地/demo：SQLite + 外部或云上对象存储 | `docker compose up -d --build tilesfst-backend tilesfst-web` |
| 本地/demo：SQLite + 项目自建 MinIO | `docker compose --profile self-hosted-storage up -d --build tilesfst-backend tilesfst-web tilesfst-minio tilesfst-minio-init` |
| 本地默认启动：业务系统 + MinIO + 文档站 | `./scripts/docker-up.sh` |
| 单独启动本地文档站预览 | `docker compose --profile docs-site up -d --build tilesfst-docs-site` |
| 本地六环境矩阵 | `./deploy/scripts/up.sh local <environment>` |
| 当前生产目标：外部 MySQL + 腾讯云 COS + 文档站 | `./deploy/scripts/up.sh prod mysql-tencent-cos` |
| VPS/离线交付兼容 | `docker compose -f docker-compose.prod.yml config` 或 `docker compose -f docker-compose.prod.external.yml config` |
