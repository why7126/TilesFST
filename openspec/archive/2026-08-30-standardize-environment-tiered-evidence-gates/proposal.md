---
created_at: 2026-08-30 12:26:56
updated_at: 2026-08-30 12:26:56
---

# 提案

## 背景

开发阶段无法直接进入生产环境完成生产证据验证，但现有小程序、媒体和 BUG / Change 验收模板对真机、体验版 Network、生产接口和生产媒体证据的阻塞语义不够分层，容易让仅生产可得的证据阻塞开发归档。

本变更将“环境分层验收与生产证据后置”固化为治理契约，明确开发、体验版和生产发布各阶段 evidence 门禁边界：开发归档不得声称生产已通过，也不得被生产环境不可用阻塞；生产证据缺口必须以 `production_only_pending` 或发布阶段待办记录并在生产发布时重新校验。

## 变更内容

- 新增环境分层 evidence 字段口径：`target_environment`、`phase`、`blocking_scope` 和 `classification`。
- 明确开发验收、体验版验证、生产发布、发布后跟进四类阶段的可接受证据和禁止表述。
- 调整小程序 DevTools / 真机 / 体验版 Network 模板：开发阶段 DevTools evidence 可支撑开发验收，但不得等同体验版或生产通过。
- 调整媒体 BUG 四联与小程序媒体 Network 口径：生产对象、生产接口、生产 no-fallback 证据仅在生产发布或生产维护阶段强制。
- 同步 `opsx-apply`、`opsx-archive`、`miniapp-confirm`、`release-*` 等命令说明，避免把生产专属证据误判为开发归档 blocker。

## 能力范围

### 新增能力

- 无。

### 修改能力

- `agent-workflow-tooling`: 规范 workflow 命令对环境分层 evidence 的状态分类、归档阻塞范围和输出口径。
- `miniapp-device-evidence-template`: 规范小程序 DevTools、真机、体验版 Network 和生产发布证据的目标环境与阻塞边界。
- `media-acceptance-template`: 规范媒体类 BUG 和小程序媒体证据在开发、体验版与生产环境之间的后置语义。
- `product-release-management`: 衔接已有 `release_target.environment`，让生产专属证据只阻塞生产发布。
- `testing`: 规范测试证据与环境证据的等价边界。

## 影响范围

- 影响治理文档、规则、命令技能、OpenSpec delta spec、治理日志和相关文档索引。
- 不修改后端 API、数据库 schema、Web、小程序、管理端业务实现。
- 不需要 OpenAPI / Orval。
- 不需要 Docker Compose 验证。
