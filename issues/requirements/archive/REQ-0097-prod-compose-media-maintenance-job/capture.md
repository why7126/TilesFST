---
requirement_id: REQ-0097-prod-compose-media-maintenance-job
status: done
created_at: 2026-08-04 10:25:13
updated_at: 2026-08-04 22:59:32
priority_hint: P1
source: 用户在 /opsx-explore 中确认线上使用 docker-compose.prod.external.yml + .env 部署，并询问生产历史媒体批处理应如何执行
parent_requirement: null
lifecycle_stage: plan
captured_via: capture
classification_rationale: 生产 Docker Compose 环境中安全执行媒体历史批处理需要镜像包含维护脚本、复用生产 env 注入、支持外部 MySQL 和对象存储、具备 dry-run/apply/审计流程；这是尚未完整交付的运维维护能力，归类为 REQ。
---

# 需求捕获

## 标题

生产 Docker Compose 环境支持媒体历史数据维护任务安全执行

## 背景

线上采用 `docker-compose.prod.external.yml` + `.env` 部署，后端服务为 `tilesfst-backend`，生产结构化数据使用外部 MySQL，媒体对象使用外部 MinIO/S3 兼容或云对象存储。

当前已有若干媒体历史处理脚本，但生产后端镜像构建上下文为 `src/backend`，镜像默认只复制 `app/`，根目录 `scripts/` 不一定在生产容器内可用。同时部分脚本仍偏 SQLite 或本地运行假设，不适合直接在生产外部 MySQL 环境执行。

## 目标

提供一种可审计、可回滚、可分批执行的生产维护任务入口，使媒体历史对象迁移、缩略图回填和二次审计可以在生产 Docker Compose 环境内执行，而不需要把生产 `.env` 或密钥下载到开发机。

## 影响范围

- `docker-compose.prod.external.yml` 或生产维护 Compose 配置。
- 后端生产镜像或专用 maintenance 镜像。
- 媒体历史处理脚本的生产 MySQL / 对象存储适配。
- 运维执行文档、备份与回滚说明。
- 媒体四联/五联验收记录。

## 初步方案线索

- 优先在生产服务器上通过 Docker Compose 临时任务容器执行，复用生产 `.env` 注入：
  - `docker compose --env-file .env -f docker-compose.prod.external.yml run --rm tilesfst-backend ...`
- 不建议将生产 `.env` 下载到本机长期使用或从本机执行生产写操作。
- 如果继续使用 `tilesfst-backend` 执行维护命令，需要确认镜像内是否包含维护脚本；否则应新增专用 maintenance 镜像/服务或将脚本纳入后端镜像。
- 生产外部 MySQL 场景下，证书图片 `files/` 到 `images/` 迁移不能直接使用仅支持 SQLite 的脚本 apply。

## 建议验收要点

- [ ] 生产维护任务可通过 Compose 一次性容器执行，不要求下载生产 `.env` 到开发机。
- [ ] 维护任务复用生产 env/secret 注入和 Compose 网络，不在仓库或日志中泄露密钥。
- [ ] 维护脚本支持外部 MySQL 与对象存储 provider，并保留 dry-run/apply 两阶段。
- [ ] 所有写操作支持分批、幂等、失败原因统计和二次审计。
- [ ] 执行前文档明确要求 MySQL 快照和对象存储 bucket/prefix 快照。
- [ ] 执行后输出媒体 key、object、URL、thumbnail benefit、render 的验收摘要。

## 待澄清

- 生产镜像发布策略：是将维护脚本纳入 `tilesfst-backend`，还是新增 `tilesfst-maintenance` 服务/镜像。
- 生产对象存储 provider 的具体类型和是否支持对象 copy/remove 的一致性语义。
- 是否允许在生产服务器上临时 bind mount `scripts/` 做只读审计，还是必须走正式镜像发布。
