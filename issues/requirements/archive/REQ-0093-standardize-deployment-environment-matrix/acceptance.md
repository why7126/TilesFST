---
requirement_id: REQ-0093-standardize-deployment-environment-matrix
title: 标准化部署环境矩阵与 deploy 目录治理 - 验收标准
acceptance_status: passed
created_at: 2026-08-03 18:31:16
updated_at: 2026-08-03 20:52:16
owner: product
---

# 验收标准

## 功能 AC

- [ ] AC-001：项目通过 OpenSpec Change 正式新增一级 `deploy/` 目录，并同步更新目录结构规则，禁止绕过规则直接创建顶层目录。
- [ ] AC-002：`deploy/` 至少包含 `README.md`、`local/`、`prod/`、`scripts/` 四类入口。
- [ ] AC-003：`deploy/local/` 至少定义 6 个本地环境示例：`sqlite-minio-managed`、`sqlite-minio-external`、`sqlite-tencent-cos`、`mysql-minio-managed`、`mysql-minio-external`、`mysql-tencent-cos`。
- [ ] AC-004：`deploy/prod/` 至少定义 `mysql-tencent-cos` 生产环境示例。
- [ ] AC-005：每个环境 ID 必须映射到 env 示例、Compose 文件、profile 策略、必填变量、安全边界和启动命令。
- [ ] AC-006：本地 6 种环境不得复制 6 份完整 Compose，必须复用 `deploy/local/compose.yml` 或等价“一拓扑一 Compose”结构。
- [ ] AC-007：生产腾讯云 COS 环境必须使用独立生产 Compose 或明确生产拓扑入口，不得依赖本地开发 Compose 隐式切换。
- [ ] AC-008：如保留生产自建 MinIO，应使用独立生产 Compose 或 profile，并明确数据卷、备份和 minio-init 边界。
- [ ] AC-009：根目录必须保留默认 `docker compose up` 兼容入口，或提供清晰等价 wrapper，避免破坏现有本地开发入口。
- [ ] AC-010：`scripts/docker-up.sh` 与 `scripts/docker-down.sh` 保留时只能作为兼容 wrapper，核心环境解析、校验和启动逻辑必须集中在 `deploy/scripts/`。
- [ ] AC-011：`deploy/scripts/up.sh` 支持按 `<domain> <environment>` 启动，例如 `local sqlite-minio-managed`、`local mysql-tencent-cos`、`prod mysql-tencent-cos`。
- [ ] AC-012：`deploy/scripts/down.sh` 支持按部署域停止，并说明是否保留本地 SQLite、MinIO 或生产数据卷。
- [ ] AC-013：`deploy/scripts/validate-env.py` 或等价脚本必须阻断生产 SQLite、生产 `APP_DEBUG=true`、示例密钥、COS 自动建桶和外部存储误启本地 MinIO profile。
- [ ] AC-014：所有 `deploy/**/*.env.example` 必须只包含示例值，按环境标识、应用安全、数据库、镜像、对象存储、端口等适用主题分组，且每个变量上一行保留用途、候选值或候选格式、默认值含义或安全边界注释。
- [ ] AC-015：`deploy/` 不得提交真实 `.env`、真实密钥、真实数据库连接串、真实对象存储凭据、真实客户数据或运行时数据。
- [ ] AC-016：`rules/directory-structure.md`、`AGENTS.md`、`docs/02-deployment.md`、`rules/environment.md` 必须同步描述 `deploy/` 目录职责、环境矩阵和安全边界。
- [ ] AC-017：部署 Compose 路径变化后，`/image-prepare` 与 `/image-build` 必须将实际使用的 Compose、脚本和 env 示例纳入 input hash 或 manifest。
- [ ] AC-018：`docs/02-deployment.md` 必须说明“一拓扑一 Compose + 一环境一 env 示例”原则，避免后续新增环境时复制整套 Compose。
- [ ] AC-019：对象存储配置仍遵守单 Bucket + 前缀策略，前端不得直连未授权对象存储。
- [ ] AC-020：目录结构校验脚本必须允许合法 `deploy/` 结构，并阻断未授权子目录、真实 env、运行时数据或大体积镜像包进入仓库。

## 非功能 AC

- [ ] AC-NF-001：部署命令输出必须摘要化展示环境 ID、Compose 文件、env 文件、profile、服务 URL 和 blocker，不输出敏感值。
- [ ] AC-NF-002：本地默认启动路径应保持低摩擦，开发者仍可用熟悉入口启动默认环境。
- [ ] AC-NF-003：新增部署目录不得破坏发布镜像治理、Docker Compose 文档、构建脚本和现有 CI/校验脚本引用。
- [ ] AC-NF-004：新增环境时应优先扩展 env 示例和矩阵文档，只有服务拓扑变化时才新增 Compose。
- [ ] AC-NF-005：部署相关文档与脚本必须遵守 `rules/agent-context-budget.md`，校验输出和失败日志默认摘要化。

## 横切 AC（knowledge-base）

本 REQ 为部署治理 / 目录治理 / 命令脚本能力，不涉及管理端 CRUD 列表、管理端表单页、管理端弹窗或媒体上传 UI 场景；Knowledge-base UI 横切标签为 N/A，本节不新增 AC-XCUT。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-03 20:52:16
accepted_by: workflow-sync
source_change: standardize-deployment-environment-matrix
source_sprint: sprint-018
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

