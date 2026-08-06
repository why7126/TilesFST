---
purpose: Docker 基线说明
content: Compose 服务、脚本与目录约定
source: initialize-project / project.yaml
update_method: 部署架构变更时同步更新
created_at: 2026-06-13 00:00:00
updated_at: 2026-08-05 23:29:59
---

# Docker 基线

本项目采用根目录 `docker-compose.yml` + 各服务 Dockerfile 的 Compose 本地/demo 部署模式。根目录 Compose 是本地基线；环境矩阵入口见 `deploy/README.md`，生产入口优先见 `deploy/prod/compose.tencent-cos.yml`。

## 服务

| 服务 | 镜像/构建 | 端口（宿主机默认） |
|------|-----------|-------------------|
| tilesfst-backend | `src/backend/Dockerfile` | 8000 |
| tilesfst-web | `src/web/Dockerfile` + nginx | 3000 |
| tilesfst-minio | `minio/minio`，仅 `self-hosted-storage` profile | 9000 / 9001 |
| tilesfst-minio-init | `minio/mc`，仅 `self-hosted-storage` profile | — |
| tilesfst-docs-site | `deploy/docs-site/Dockerfile`，预装 Mintlify CLI，仅 `docs-site` profile | 3001 |

## 脚本

```bash
./scripts/docker-up.sh
./scripts/docker-down.sh
```

## 环境变量

见根目录 `.env.example`；运行时复制为 `.env`（禁止提交）。

## 数据卷

```text
data/sqlite
data/minio          # 仅项目自建 MinIO profile
data/processed
data/tmp
```

## 文档

- `docs/02-deployment.md`
- `deploy/README.md`
- `docker-compose.yml`

## 说明

按 `rules/directory-structure.md`，不在根目录新增 `docker/` 业务目录；Compose 与 Dockerfile 位置见上表。
