---
note: workflow-sync — workflow-sync 自动同步 — 5/5 Change archived；0 applied；Sprint `completed`
title: sprint-028 归档
created_at: 2026-08-30 08:50:35
updated_at: 2026-08-30 14:50:52
---

# sprint-028 归档

## 1. 目标

### Sprint 目标编号列表

- standardize-ai-usage-session-discovery
- BUG-0147-miniapp-certificate-list-images-missing
- add-release-status-decision-panel
- standardize-environment-tiered-evidence-gates
- enforce-environment-tiered-evidence-gates

### standardize-ai-usage-session-discovery 要点

将 `~/.codex/sessions` 明确为 AI Usage 默认 session 自动发现目录，统一 workflow-sync、sprint-archive、sprint-exps 等命令的成本分析提示口径，避免在本地 session 存在时误报无法做真实成本分析。

### BUG-0147-miniapp-certificate-list-images-missing 要点

修复生产小程序证书列表页图片类证书 `file_url` 与 `thumbnail_url` 均为空导致卡片全部显示“证书”占位的问题。范围覆盖后端 miniapp certificates API、证书媒体 key/URL/缩略图回填、历史媒体对象审计和小程序列表渲染验收。

### standardize-environment-tiered-evidence-gates 要点

制定环境分层验收与生产证据后置规范，明确开发、体验版、生产发布各阶段 evidence 门禁；生产环境不可用时不阻塞开发归档，但必须作为 `production_only_pending` 或发布阶段待办记录。

### enforce-environment-tiered-evidence-gates 要点

将环境分层验收与生产证据后置规范升级为强脚本门禁，接入归档 readiness 和发布 status/publish 校验，阻断开发证据冒充生产通过、体验版/真机 Network 缺 evidence 却标 passed、生产发布前未重新判定 `production_only_pending`。

## 2. Scope

| 类型 | 编号 | 标题 | 状态 | 估算 | 说明 |
|---|---|---|---|---:|---|
| BUG | BUG-0147-miniapp-certificate-list-images-missing | 小程序证书列表页图片不显示 | done | 3 人天 | archived `fix-miniapp-certificate-media-urls`（2026-08-30 11:46:57） |
| Change | standardize-ai-usage-session-discovery | standardize ai usage session discovery | archived | 1 人天 | archived `standardize-ai-usage-session-discovery`（2026-08-30 08:55:17） |
| Change | add-release-status-decision-panel | add release status decision panel | archived | 1 人天 | archived `add-release-status-decision-panel`（2026-08-30 23:59:59） |
| Change | standardize-environment-tiered-evidence-gates | standardize environment tiered evidence gates | archived | 1 人天 | archived `standardize-environment-tiered-evidence-gates`（2026-08-30 12:39:44） |
| Change | enforce-environment-tiered-evidence-gates | enforce environment tiered evidence gates | archived | 1 人天 | archived `enforce-environment-tiered-evidence-gates`（2026-08-30 12:55:22） |

<!-- workflow-sync:scope-requirements:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
<!-- workflow-sync:scope-requirements:end -->

<!-- workflow-sync:scope-bugs:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| BUG-0147 | 小程序证书列表页图片不显示 | high | done | archived `fix-miniapp-certificate-media-urls`（2026-08-30 11:46:57） |
<!-- workflow-sync:scope-bugs:end -->

<!-- workflow-sync:scope-changes:start -->
| Change ID | 关联需求 | 状态 | Sprint 目标 |
|---|---|---|---|
| `standardize-ai-usage-session-discovery` | — | archived | archived `standardize-ai-usage-session-discovery`（2026-08-30 08:55:17） |
| `fix-miniapp-certificate-media-urls` | BUG-0147-miniapp-certificate-list-images-missing | archived | archived `fix-miniapp-certificate-media-urls`（2026-08-30 11:46:57） |
| `add-release-status-decision-panel` | — | archived | archived `add-release-status-decision-panel`（2026-08-30 23:59:59） |
| `standardize-environment-tiered-evidence-gates` | — | archived | archived `standardize-environment-tiered-evidence-gates`（2026-08-30 12:39:44） |
| `enforce-environment-tiered-evidence-gates` | — | archived | archived `enforce-environment-tiered-evidence-gates`（2026-08-30 12:55:22） |
<!-- workflow-sync:scope-changes:end -->

REQ：无 已纳入正式范围；BUG：1 个已纳入正式范围，优先级高于新增体验能力；当前完成度与验收风险以 Scope 表状态、关联 Change 和 acceptance-report 为准。

Change：5 个范围内 Change 均已归档；BUG-0147 对应 OpenSpec Change `fix-miniapp-certificate-media-urls` 已归档闭环，当前 Sprint 已关闭。

## 3. 工作量与容量

| 项 | 值 |
|---|---:|
| 容量基线 | 30 人天 |
| 估算 | 4 SP / 4 人天 |
| 容量占用 | 13.33% |
| fix 缓冲 | 26 人天 / 86.67% |

## 4. 里程碑

| 阶段 | 目标 |
|---|---|
| OpenSpec | BUG-0147 fix Change 已创建并回填 sprint-028；治理 Change 已归档。 |
| 实现 | 修复 miniapp certificates API 的证书媒体 URL/缩略图回填链路，并保留 AI Usage 治理口径。 |
| 验证 | 运行后端 API/媒体回填相关测试，补齐 key/object/URL/render 四联证据、OpenSpec 语言、目录结构和 Sprint scope 校验。 |
| 归档 | 5 个范围内 Change 均已归档，Sprint 于 2026-08-30 14:44:32 关闭。 |

## 5. 风险

- 不能把原始 `~/.codex/sessions` JSONL、prompt、系统指令、developer 指令或工具输出正文写入仓库。
- 不能把 `estimated_fallback` 表述为真实 token 成本量化。
- 自动发现失败时必须给出可执行补救动作，而不是笼统说无法成本分析。
- 证书媒体缺陷不能只用 HTTP 200 判断修复完成，必须同时确认对象 key、公开 URL、缩略图字段和小程序端实际渲染。
- 历史证书媒体若存在空 URL 或旧 key 前缀，需要区分数据回填、对象缺失与 API 映射缺陷，避免只修端侧 fallback。

## 6. 知识库承接

- 最近复盘 `sprint-027` 提醒：媒体派生图验收必须检查 `Content-Type`、`Content-Length`、`x-media-fallback` 和端侧 render，不能把 `/media` HTTP 200 视为派生图已存在。
- 适用最佳实践：`miniapp-media-four-part-acceptance-practice`，BUG-0147 验收需覆盖 key、object、URL、render 四联证据。
- 适用最佳实践：`admin-media-upload-chain` 的媒体链路拆解方法可用于区分上传状态、对象存储 key、DB URL 字段和端侧消费边界。

## 7. 横切预防清单

- `product_data_collection_observability`: applicable。
- `affected_layers`: `backend_api`、`wechat_miniapp_request_flow`、`request_logs`、`maintenance_jobs`；若修复引入 Task Trace 或数据回填命令，还需覆盖 `task_traces`。
- `reason`: Sprint 范围包含 miniapp certificates API 媒体 URL 修复、证书历史媒体维护与请求链路观测验收，同时包含 AI Usage 与环境分层证据治理变更；运行时代码影响以 `fix-miniapp-certificate-media-urls` 为主，其余治理 Change 不修改业务 API、DB 或端侧请求封装。
- `validation`: Sprint 关闭前已通过 OpenSpec archive readiness、环境分层证据门禁、产品数据采集与链路观测门禁、AI Usage actual 快照刷新和 Workflow Sync；生产发布阶段证据按 release/publish 门禁另行复核。

## 8. 关联文档

- `openspec/archive/2026-08-30-standardize-ai-usage-session-discovery/`
- `openspec/archive/2026-08-30-fix-miniapp-certificate-media-urls/`
- `issues/bugs/archive/BUG-0147-miniapp-certificate-list-images-missing/`
- `.agents/skills/workflow-sync/SKILL.md`
- `.agents/skills/sprint-archive/SKILL.md`
- `.agents/skills/sprint-exps/SKILL.md`
- `rules/agent-context-budget.md`
- `scripts/ai_usage.py`

## 9. 复盘

- `docs/knowledge-base/retrospectives/sprint-028-retrospective.md`
