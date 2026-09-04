---
note: workflow-sync — workflow-sync 自动同步 — 7/7 Change archived；0 applied；Sprint `active`
title: sprint-029 规划
created_at: 2026-08-30 15:36:34
updated_at: 2026-08-31 14:27:26
---

# sprint-029 规划

## 1. 目标

### Sprint 目标编号列表

- enforce-product-version-release-gates
- simplify-single-release-target-governance
- automate-product-version-release-prepare
- make-release-propose-next-step-prepare
- converge-release-prepare-automation
- deactivate-environment-tiered-evidence-gates
- rename-evidence-source-specs

### enforce-product-version-release-gates 要点

强化发布流程产品版本号门禁，避免后续 release 在 Web 或小程序用户可见版本号未对齐时进入发布确认。

### simplify-single-release-target-governance 要点

收敛发布治理为单一项目发布语义，移除 development / production 发布目标分支、生产环境专属门禁和升级计划目标环境后缀。

### automate-product-version-release-prepare 要点

将 `PRODUCT_VERSION` 同步自动化前移到 `/release-prepare`，发布确认只校验不写版本，`/image-prepare` 前强制版本源已对齐。

### make-release-propose-next-step-prepare 要点

将 `/release-propose` 默认下一步调整为 `/release-prepare`，`/release-status` 仅作为只读状态面板和阻塞排查入口。

### converge-release-prepare-automation 要点

收敛发布准备自动化策略：`/release-propose` 默认声明公告、usage docs 与升级路径决策，`/release-prepare` 统一生成和校验，`/release-publish` 只确认。

### deactivate-environment-tiered-evidence-gates 要点

将环境分层 evidence 从默认 workflow 阻断门禁降级为手动证据来源诊断工具，保留脚本能力但不再自动应用。

## 2. Scope

| 类型 | 编号 | 标题 | 状态 | 估算 | 说明 |
|---|---|---|---|---:|---|
| Change | enforce-product-version-release-gates | enforce product version release gates | archived | 1 人天 | archived `enforce-product-version-release-gates`（2026-08-30 23:59:59） |
| Change | simplify-single-release-target-governance | simplify single release target governance | archived | 1 人天 | archived `simplify-single-release-target-governance`（2026-08-30 23:59:59） |
| Change | automate-product-version-release-prepare | automate product version release prepare | archived | 1 人天 | archived `automate-product-version-release-prepare`（2026-08-30 23:59:59） |
| Change | make-release-propose-next-step-prepare | make release propose next step prepare | archived | 1 人天 | archived `make-release-propose-next-step-prepare`（2026-08-31 23:59:59） |
| Change | converge-release-prepare-automation | converge release prepare automation | archived | 1 人天 | archived `converge-release-prepare-automation`（2026-08-31 09:17:22） |
| Change | deactivate-environment-tiered-evidence-gates | deactivate environment tiered evidence gates | archived | 1 人天 | archived `deactivate-environment-tiered-evidence-gates`（2026-08-31 10:31:39） |
| Change | rename-evidence-source-specs | rename evidence source specs | archived | 1 人天 | archived `rename-evidence-source-specs`（2026-08-31 14:06:32） |

<!-- workflow-sync:scope-requirements:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
<!-- workflow-sync:scope-requirements:end -->

<!-- workflow-sync:scope-bugs:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
<!-- workflow-sync:scope-bugs:end -->

<!-- workflow-sync:scope-changes:start -->
| Change ID | 关联需求 | 状态 | Sprint 目标 |
|---|---|---|---|
| `enforce-product-version-release-gates` | — | archived | archived `enforce-product-version-release-gates`（2026-08-30 23:59:59） |
| `simplify-single-release-target-governance` | — | archived | archived `simplify-single-release-target-governance`（2026-08-30 23:59:59） |
| `automate-product-version-release-prepare` | — | archived | archived `automate-product-version-release-prepare`（2026-08-30 23:59:59） |
| `make-release-propose-next-step-prepare` | — | archived | archived `make-release-propose-next-step-prepare`（2026-08-31 23:59:59） |
| `converge-release-prepare-automation` | — | archived | archived `converge-release-prepare-automation`（2026-08-31 09:17:22） |
| `deactivate-environment-tiered-evidence-gates` | — | archived | archived `deactivate-environment-tiered-evidence-gates`（2026-08-31 10:31:39） |
| `rename-evidence-source-specs` | — | archived | archived `rename-evidence-source-specs`（2026-08-31 14:06:32） |
<!-- workflow-sync:scope-changes:end -->

REQ：无 已纳入正式范围；BUG：无 已纳入正式范围，优先级高于新增体验能力；当前完成度与验收风险以 Scope 表状态、关联 Change 和 acceptance-report 为准。

Change：已回填 0 个范围项关联 Change，另有 6 个纯 Change；6 archived，0 applied，0 in_progress，0 proposed。所有已纳入范围项均已关联 Change；执行开发与归档时以 Scope 表逐项状态为准。

## 3. 工作量与容量

| 项 | 值 |
|---|---:|
| 容量基线 | 30 人天 |
| 估算 | 6 SP / 6 人天 |
| 容量占用 | 20% |
| fix 缓冲 | 24 人天 / 80% |

## 4. 横切预防清单

- `product_data_collection_observability`: not_applicable。
- `affected_layers`: 无。
- `reason`: 本 Sprint 只包含发布治理、命令技能和校验脚本变更，不修改 API、DB、Web、小程序请求封装、日志审计、行为埋点或 Task Trace。
- `validation`: 通过 OpenSpec、目录结构、上下文预算、release validator 聚焦测试、Workflow Sync 和 AI Usage hook 验证。
