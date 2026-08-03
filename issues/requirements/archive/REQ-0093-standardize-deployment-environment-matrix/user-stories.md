---
requirement_id: REQ-0093-standardize-deployment-environment-matrix
title: 标准化部署环境矩阵与 deploy 目录治理 - 用户故事
created_at: 2026-08-03 18:31:16
updated_at: 2026-08-03 18:31:16
owner: product
---

# 用户故事

## US-001 本地开发者选择部署组合

作为本地开发者，我希望通过稳定的环境 ID 选择 SQLite/MySQL 与 MinIO/COS 组合，以便不用反复猜测 `.env`、profile 和 Compose 参数。

验收要点：

- 本地 6 种环境均有明确 ID、env 示例和启动命令。
- 默认本地环境能保持开箱即用。
- 外部 MySQL / 外部 MinIO / 腾讯云 COS 场景不会误启项目内 MinIO。

## US-002 测试按环境矩阵复现问题

作为测试或验收人员，我希望能按环境矩阵复现指定部署组合，以便验证数据库、对象存储和 Web/API 链路在不同配置下行为一致。

验收要点：

- 每个环境 ID 都能映射到唯一的 env 示例和 Compose 入口。
- 校验脚本能在启动前提示缺失或危险配置。
- 验证结果能说明当前使用 SQLite/MySQL、MinIO/COS 和是否启用了 self-hosted-storage profile。

## US-003 运维区分生产与本地配置边界

作为实施或运维人员，我希望生产部署配置与本地配置分目录维护，以便避免把本地 SQLite、示例密钥或自动建桶策略带入生产。

验收要点：

- `deploy/prod/` 只包含生产 env 示例、生产 Compose 和生产说明。
- 生产示例必须要求 MySQL、腾讯云 COS、非示例密钥和 `OBJECT_STORAGE_AUTO_CREATE_BUCKET=false`。
- 真实 `.env`、真实连接串和真实密钥不得进入仓库。

## US-004 发布负责人追踪部署文件影响

作为发布负责人，我希望部署目录调整后，镜像构建计划和 manifest 仍能追踪实际使用的 Compose 与 env 示例，以便部署变更不会绕过发布门禁。

验收要点：

- `/image-prepare` 能把 `deploy/` 下 Compose、脚本和 env 示例纳入输入文件 hash。
- `/image-build` manifest 记录实际使用的 Compose 文件。
- Compose 或部署脚本漂移后，发布确认能识别镜像证据过期。

## US-005 AI Agent 按目录规则维护部署资产

作为 AI Agent，我希望 `deploy/` 的职责、边界和禁止事项明确写入规则，以便后续新增部署环境时不会随意新增顶层目录、复制脚本或泄露敏感配置。

验收要点：

- `rules/directory-structure.md` 和 `AGENTS.md` 明确允许并约束 `deploy/`。
- 新增部署环境优先新增 env 示例和矩阵条目，不复制全套 Compose。
- `scripts/docker-up.sh` / `scripts/docker-down.sh` 仅保留兼容 wrapper，不重复承载复杂逻辑。
