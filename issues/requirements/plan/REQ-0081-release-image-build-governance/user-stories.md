---
requirement_id: REQ-0081-release-image-build-governance
title: 发布镜像准备与构建治理 - 用户故事
status: pending_review
created_at: 2026-07-29 10:07:04
updated_at: 2026-07-29 10:07:04
owner: product
---

# 用户故事

## US-001 发布负责人判断是否需要镜像

作为产品负责人或项目负责人，我希望发布准备阶段能根据发布影响范围判断本次是否需要镜像准备或镜像构建，以便避免数据库、Dockerfile、Compose 或构建脚本变化被遗漏。

验收要点：

- 能从 `release.json` 的 scope、impact_scope 和关联 Change 判断 `image_required`。
- 不需要镜像时必须有明确 rationale。
- 需要镜像时必须提示下一步 `/image-prepare <version>`。

## US-002 开发在构建前获得一致性计划

作为开发人员，我希望 `/image-prepare` 能生成镜像构建计划，列出版本、tag、Dockerfile、Compose、构建脚本、schema、migration 等输入，以便真实构建前先发现版本不一致或输入缺失。

验收要点：

- `image-build-plan.json` 记录非敏感构建输入和 hash。
- 版本、tag、构建 env、生产 Compose 的一致性问题会变成 blocker。
- Docker 不可用时不会伪造构建证据。

## US-003 运维构建并交付可追踪镜像包

作为实施或运维人员，我希望 `/image-build` 基于已通过的构建计划执行真实构建、验证和离线包导出，以便交付镜像包时有可审查的 manifest 和 sha256。

验收要点：

- `/image-build` 必须读取有效 `image-build-plan.json`。
- 构建后生成 `image-manifest.json`。
- manifest 记录 backend/web 镜像、平台、tarball、sha256、输入 hash 和验证摘要。

## US-004 发布确认阻断过期镜像证据

作为发布确认人，我希望 `/release-publish` 能校验镜像 manifest 是否与当前发布输入一致，以便阻止脚本、Dockerfile、schema 或 Compose 在构建后变更却仍继续发布。

验收要点：

- manifest 缺失、版本不一致、tag 不一致或输入 hash 漂移时必须阻断发布。
- 人工外部构建证据必须说明来源、校验方式和风险。
- 发布确认不得暴露真实密钥、`.env` 或数据库连接串。

## US-005 AI Agent 按命令依赖执行发布镜像治理

作为 AI Agent，我希望命令 Skill 中明确五个命令的依赖和职责边界，以便不在 `/release-prepare` 中偷跑重构建，也不在 `/image-build` 中自行猜测构建输入。

验收要点：

- `/release-propose` 负责发布范围。
- `/release-prepare` 负责发布门禁汇总。
- `/image-prepare` 负责构建前计划。
- `/image-build` 负责真实构建产物。
- `/release-publish` 负责最终确认与阻断。
