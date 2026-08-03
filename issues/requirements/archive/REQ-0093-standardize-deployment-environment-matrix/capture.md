---
req_id: REQ-0093-standardize-deployment-environment-matrix
status: done
created_at: 2026-08-03 10:44:00
updated_at: 2026-08-03 20:47:04
recorded_by: product
source: /opsx-explore 部署环境治理讨论
priority_hint: P1
parent_requirement:
captured_via: req-capture
classification_rationale: 用户希望按探索结论中的中期方案落地，将多种本地开发与生产部署组合沉淀为正式部署治理能力，涉及目录结构、环境矩阵、Compose 组合、脚本和文档同步，属于新增治理需求而非缺陷。
---

# 一句话

标准化部署环境矩阵，并在必要时通过 OpenSpec Change 正式引入一级 `deploy/` 目录来承载环境配置、Compose 组合与部署校验脚本。

# 原始描述

目前已经有多个不同的环境需要部署，是否应该独立创建一个一级目录 deploy，里面区分不同环境的部署脚本，比如现在已有的部署环境包括：

- 本地开发环境
  - sqlite + 自建 minio
  - sqlite + 本机已 Docker 部署的 minio
  - sqlite + 腾讯云 COS
  - 本机已 Docker 部署的 mysql + 自建 minio
  - 本机已 Docker 部署的 mysql + 本机已 Docker 部署 minio
  - 本机已 Docker 部署的 mysql + 腾讯云 COS
- 生产环境
  - 本机已 Docker 部署的 mysql + 腾讯云 COS

探索结论倾向于中期方案：若部署治理继续膨胀，应通过 OpenSpec Change 正式引入 `deploy/`，并按能力维度组合，而不是为每个环境复制一套脚本。

# 背景

当前项目已有 `docker-compose.yml`、`docker-compose.prod.yml`、`docker-compose.prod.external.yml`、`scripts/docker-up.sh` 与 `.env.example`，能够覆盖本地开发、生产自建 MinIO 和生产外部对象存储等场景。但随着 SQLite/MySQL、托管 MinIO/外部 MinIO/腾讯云 COS、开发/生产等组合增加，环境配置、启动方式、前置条件和校验规则缺少统一命名与矩阵化治理。

由于当前目录规范尚未允许新增顶层 `deploy/`，如果要引入该目录，必须先通过 OpenSpec Change 更新目录结构规范、AGENTS 和部署文档，避免绕过目录治理直接扩展顶层目录。

# 影响范围

- 顶层目录结构与 `rules/directory-structure.md`。
- `AGENTS.md` 中目录边界与部署入口说明。
- `docs/02-deployment.md` 中部署矩阵、启动命令、生产安全边界和环境变量说明。
- `docker-compose*.yml` 的职责边界、组合方式和注释维护规范。
- `.env.example`、部署环境示例文件和真实 `.env` 禁止提交边界。
- `scripts/docker-up.sh`、`scripts/docker-down.sh` 或未来 `deploy/scripts/` 启停与校验入口。
- SQLite/MySQL、MinIO/S3 兼容存储、腾讯云 COS 的配置组合与校验门禁。
- Docker Compose 验证、对象存储连通性验证和生产误配置防护。

# 待澄清

- [ ] 是否确认新增一级 `deploy/` 目录，还是先继续放在 `scripts/`、根 Compose 和 `docs/02-deployment.md` 内治理。
- [ ] `deploy/` 若引入，是否采用 `environments/`、`compose/`、`scripts/` 三段式结构。
- [ ] 环境 ID 是否采用 `local-sqlite-minio-managed`、`local-sqlite-minio-external`、`local-sqlite-tencent-cos`、`local-mysql-minio-managed`、`local-mysql-minio-external`、`local-mysql-tencent-cos`、`prod-mysql-tencent-cos`。
- [ ] 本机已 Docker 部署的 MySQL / MinIO 是否定义为 external service，还是纳入本项目 Compose profile 管理。
- [ ] 生产环境中“本机已 Docker 部署的 mysql”是否表示项目外部前置 MySQL 容器，还是未来需要项目级 Compose 管理 MySQL。
- [ ] 腾讯云 COS 是否继续通过 `OBJECT_STORAGE_PROVIDER=tencent-cos` 与官方 SDK 接入，或需要独立部署 profile / smoke。
- [ ] 是否需要提供 `validate-env.sh` / Python 校验脚本，用于阻止生产 SQLite、COS 自动建桶、云密钥示例值、MinIO profile 误启等风险。

# 建议验收要点

- [ ] 明确部署环境矩阵，每个环境具备稳定 ID、适用场景、数据库 provider、对象存储 provider、Compose 文件、profile、必填密钥和启动命令。
- [ ] 如新增 `deploy/`，必须同步更新 `rules/directory-structure.md`、`AGENTS.md`、`docs/02-deployment.md`，并通过目录结构校验。
- [ ] `deploy/` 结构按能力维度组合，避免为 7 个环境复制 7 套几乎相同的脚本。
- [ ] 环境示例文件只包含示例值和注释，不包含真实 `.env`、密钥、生产私有域名、数据库连接串或客户数据。
- [ ] 本地 SQLite + 自建 MinIO、本地 SQLite + 外部 MinIO、本地 SQLite + 腾讯云 COS、本地 MySQL + 自建 MinIO、本地 MySQL + 外部 MinIO、本地 MySQL + 腾讯云 COS、生产 MySQL + 腾讯云 COS 均有可执行或可验证的启动说明。
- [ ] 生产环境必须阻止 SQLite 回退，并要求显式 MySQL `DATABASE_URL`、非示例密钥、云 bucket 已前置创建和 `OBJECT_STORAGE_AUTO_CREATE_BUCKET=false`。
- [ ] 对象存储仍遵守单 Bucket + 前缀策略，前端不得直连未授权对象存储。
- [ ] Docker Compose、环境变量、部署文档和测试/校验脚本保持同步；涉及部署变更时说明是否需要 Docker Compose 验证。

# 探索结论

（/req-explore 后人工确认写入）
