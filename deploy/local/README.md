---
purpose: 本地部署矩阵
content: 六种本地开发部署环境、前置条件和启动方式
source: REQ-0093 standardize-deployment-environment-matrix
created_at: 2026-08-03 19:10:00
updated_at: 2026-08-06 00:00:00
---

# 本地部署矩阵

本地域复用 `deploy/local/compose.yml`。该文件以根目录 `docker-compose.yml` 为本地/demo 拓扑基线，保持 `tilesfst-backend`、`tilesfst-web`、`tilesfst-minio`、`tilesfst-minio-init`、`self-hosted-storage` profile、默认端口、`data/` 卷和 `UPLOAD_*` Nginx 变量一致。SQLite 环境不要求本机 MySQL；MySQL 环境要求本机已有可访问 MySQL 8.0+。只有 `*-minio-managed` 环境会启用项目自建 MinIO profile。

长期运行服务使用 `restart: unless-stopped` 支持异常退出后自动拉起；`tilesfst-minio-init` 使用 `restart: on-failure`，只在初始化失败时重试。

| 环境 ID | 数据库 | 对象存储 | profile | env 示例 |
|---|---|---|---|---|
| `sqlite-minio-managed` | SQLite | 项目自建 MinIO | `self-hosted-storage` | `deploy/local/sqlite-minio-managed.env.example` |
| `sqlite-minio-external` | SQLite | 本机已 Docker 部署 MinIO | 无 | `deploy/local/sqlite-minio-external.env.example` |
| `sqlite-tencent-cos` | SQLite | 腾讯云 COS | 无 | `deploy/local/sqlite-tencent-cos.env.example` |
| `mysql-minio-managed` | 本机 MySQL | 项目自建 MinIO | `self-hosted-storage` | `deploy/local/mysql-minio-managed.env.example` |
| `mysql-minio-external` | 本机 MySQL | 本机已 Docker 部署 MinIO | 无 | `deploy/local/mysql-minio-external.env.example` |
| `mysql-tencent-cos` | 本机 MySQL | 腾讯云 COS | 无 | `deploy/local/mysql-tencent-cos.env.example` |

启动示例：

```bash
./deploy/scripts/up.sh local sqlite-minio-managed
./deploy/scripts/up.sh local mysql-tencent-cos
./deploy/scripts/down.sh local
```

所有 local 启动环境默认同时启用 `docs-site` profile，并启动 `tilesfst-docs-site`。文档站默认访问 `http://localhost:3001`，可通过 `HOST_PORT_MINTLIFY_DOCS` 覆盖。Mintlify 预览缓存不作为业务数据持久化，仅留在容器临时文件系统内，不写宿主机 `~/.mintlify*`。

真实本地 env 可复制到 `deploy/local/<environment>.env` 或继续使用示例文件进行 `docker compose config` 校验。真实 env 文件已被 `.gitignore` 与目录校验阻断，禁止提交。

若只是使用项目默认本地/demo 拓扑，可直接从根目录运行：

```bash
docker compose up -d --build tilesfst-backend tilesfst-web
docker compose --profile self-hosted-storage up -d --build tilesfst-backend tilesfst-web tilesfst-minio tilesfst-minio-init
docker compose --profile docs-site up -d --build tilesfst-docs-site
```

变更本地 Compose 文档或 env 示例后，至少校验：

```bash
docker compose config --quiet
TILESFST_DEPLOY_ENV_FILE=sqlite-minio-managed.env.example docker compose --env-file deploy/local/sqlite-minio-managed.env.example --profile self-hosted-storage -f deploy/local/compose.yml config --quiet
```
