---
note: workflow-sync — workflow-sync 自动同步 — 2/3 Change archived；1 applied；Sprint `planning`
sprint_id: sprint-007
title: Sprint 007 迭代规划
status: planning
lifecycle_stage: change
created_at: 2026-07-11 23:39:00
updated_at: 2026-07-12 10:22:40
owner: product
source: /sprint-propose sprint-007
---

# Sprint 007 迭代规划

## Sprint 目标

本 Sprint 当前纳入三个流程治理 / 知识沉淀事项：

- `REQ-0036-clipboard-helper-best-practice-docs`：承接 Sprint 006 复盘行动项 A-005，为 Clipboard helper 建立长期 best-practice 文档，沉淀调用方文案、fallback 和敏感值边界。
- `REQ-0035-ai-usage-snapshot-sprint-close-exps`：承接 Sprint 006 复盘行动项 A-001，将 AI usage snapshot 生成纳入 Sprint close / exps 默认流程，避免继续 estimated fallback。
- `REQ-0037-auto-token-fact-source-for-workflow-commands`：继续承接 AI usage 观测链路，把 Token 事实源构建前移到每个 `/req-*`、`/bug-*`、`/opsx-*`、`/sprint-*` 命令的后置步骤。

同时保留 Sprint 006 A-004 横切 gate：后续新增任何主题相关页面时，必须复用 `REQ-0020-theme-comfort-refine` 的主题验收矩阵，并补充截图与 DOM 检查。

正式纳入范围：

- `REQ-0036-clipboard-helper-best-practice-docs` / `add-clipboard-helper-best-practice-docs`
- `REQ-0035-ai-usage-snapshot-sprint-close-exps` / `update-ai-usage-snapshot-sprint-close-exps`
- `REQ-0037-auto-token-fact-source-for-workflow-commands` / `add-auto-token-fact-source-for-workflow-commands`

## Scope

<!-- workflow-sync:scope-requirements:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| REQ-0036 | Clipboard helper best-practice 文档 | P2 | done | archived `add-clipboard-helper-best-practice-docs`（2026-07-12 00:30:43） |
| REQ-0035 | AI usage snapshot 纳入 Sprint close / exps 默认流程 | P1 | done | archived `update-ai-usage-snapshot-sprint-close-exps`（2026-07-12 00:55:20） |
| REQ-0037 | 工作流命令自动构建 AI Token 事实源 | P1 | in_sprint | apply 22/22；待 archive `add-auto-token-fact-source-for-workflow-commands` |
<!-- workflow-sync:scope-requirements:end -->

<!-- workflow-sync:scope-bugs:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
<!-- workflow-sync:scope-bugs:end -->

<!-- workflow-sync:scope-changes:start -->
| Change ID | 关联需求 | 状态 | Sprint 目标 |
|---|---|---|---|
| `add-clipboard-helper-best-practice-docs` | REQ-0036-clipboard-helper-best-practice-docs | archived | archived `add-clipboard-helper-best-practice-docs`（2026-07-12 00:30:43） |
| `update-ai-usage-snapshot-sprint-close-exps` | REQ-0035-ai-usage-snapshot-sprint-close-exps | archived | archived `update-ai-usage-snapshot-sprint-close-exps`（2026-07-12 00:55:20） |
| `add-auto-token-fact-source-for-workflow-commands` | REQ-0037-auto-token-fact-source-for-workflow-commands | applied | apply 22/22；待 archive `add-auto-token-fact-source-for-workflow-commands` |
<!-- workflow-sync:scope-changes:end -->

## 工作量

| 项 | 值 |
|---|---:|
| 容量 | 30 人天 |
| 估算 | 9.0 人天 |
| 容量占用 | 30% |
| Story Points | 15 |
| add/update 主能力数量 | 3 |
| BUG/fix 缓冲 | 21.0 人天 / 70% |

容量门禁结论：`pass`。`REQ-0036` 估算 1.0 人天，`REQ-0035` 估算 3.0 人天，`REQ-0037` 估算 5.0 人天，总计 9.0 / 30 人天；fix 缓冲 21 人天 / 70%，高于 30% 建议线。

## 估算明细

| 项 | Change | 优先级 | 规模 | SP | 人天 | 说明 |
|---|---|---|---|---:|---:|---|
| `REQ-0036-clipboard-helper-best-practice-docs` | `add-clipboard-helper-best-practice-docs` | P2 | S | 2 | 1.0 | 新增 Clipboard helper best-practice 文档与索引入口 |
| `REQ-0035-ai-usage-snapshot-sprint-close-exps` | `update-ai-usage-snapshot-sprint-close-exps` | P1 | M | 5 | 3.0 | Sprint close / exps 默认生成、校验和消费 AI usage snapshot |
| `REQ-0037-auto-token-fact-source-for-workflow-commands` | `add-auto-token-fact-source-for-workflow-commands` | P1 | L | 8 | 5.0 | `/req-*`、`/bug-*`、`/opsx-*`、`/sprint-*` 后置自动构建 Token 事实源 |

## 里程碑

| 目标日期 | 里程碑 | 验收 |
|---|---|---|
| 2026-07-15 18:00:00 | Clipboard best-practice 文档完成 | `docs/knowledge-base/best-practices/clipboard-fallback.md` 或等价文档完成，并同步索引入口 |
| 2026-07-18 18:00:00 | 主题验收 gate 固化 | 新增主题相关页面的 OpenSpec design/tasks 引用 `REQ-0020` 主题矩阵，并列出截图/DOM 检查 |
| 2026-07-21 18:00:00 | 工作流命令 Token fact source hook 完成 | source-command 后置 hook、command run / snapshot 刷新、失败降级和脱敏测试通过 |
| 2026-07-25 23:39:00 | 规划复核 | Workflow Sync check、OpenSpec validate 与容量门禁按实际纳入范围重新运行 |

## 风险

| 风险 | 影响 | 缓解 |
|---|---|---|
| 文档落位不清 | best-practice 若只写在 issue 或 README 小节，后续调用方不易发现 | 优先新增 `docs/knowledge-base/best-practices/clipboard-fallback.md`，并同步知识库 README 与 Web README 入口 |
| 敏感值示例泄露 | 示例若使用真实 Token、客户数据或生产签名 URL，会扩大安全风险 | 所有示例必须使用脱敏或虚构值；验收检查不得包含真实凭据 |
| 主题相关页面容易遗漏多主题验收 | 新页面可能只在默认主题下可用 | 强制复用 `REQ-0020` 的登录页、列表页、表单页、弹窗、媒体上传、`/design-system` 矩阵，并补截图/DOM gate |
| 截图验收缺少结构断言 | 视觉看似通过但分页、弹窗或 toast DOM 契约漂移 | 在 Playwright screenshot 外补 DOM 检查：分页结构、MetricCard、fixed toast、DS modal、弹窗 computed width |
| 工作流命令后置 hook 影响主流程稳定性 | 每个命令后自动构建 Token 事实源可能因本地 session 缺失而失败 | 设计为 warning / recommended action，默认不阻断主命令；仅 Sprint close 等收尾场景保留更强 gate |
| 自动构建输出反向增加上下文成本 | hook 若输出完整 snapshot 或工具日志，会抵消 Token 节省目标 | 成功路径只输出 status、usage_mode、计数、warning_count 和 recommended_action |

## 知识库承接

来自 `docs/knowledge-base/retrospectives/sprint-006-retrospective.md` 的 open 行动项：

| 行动项 | 本 Sprint 承接 |
|---|---|
| A-001 将 AI usage snapshot 生成纳入 Sprint close / exps 默认流程，避免继续 estimated fallback | 正式纳入 `REQ-0035` / `update-ai-usage-snapshot-sprint-close-exps` |
| A-001 后续深化：将 AI usage fact source 构建前移到每个工作流命令后置步骤 | 正式纳入 `REQ-0037` / `add-auto-token-fact-source-for-workflow-commands` |
| A-004 下一轮主题相关页面新增时，复用 `REQ-0020` 主题验收矩阵并补充截图/DOM 检查 | 作为本 Sprint 横切验收 gate；所有主题相关页面新增 Change 必须引用 `issues/requirements/archive/REQ-0020-theme-comfort-refine/acceptance.md` |
| A-005 为 Clipboard helper 建立 best-practice 文档，沉淀调用方文案、fallback 和敏感值边界 | 正式纳入 `REQ-0036` / `add-clipboard-helper-best-practice-docs`，输出长期 best-practice 文档与索引入口 |

## 横切预防清单

适用 best-practices：

- `docs/knowledge-base/best-practices/admin-list-page-consistency.md`
- `docs/knowledge-base/best-practices/admin-form-page-consistency.md`
- `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md`
- `docs/knowledge-base/best-practices/admin-media-upload-chain.md`

主题相关页面新增验收 gate：

- 复用 `REQ-0020` 四主题矩阵：`system`、`dark_flagship`、`comfort_dark`、`light`。
- 页面类型映射到 `REQ-0020` 的代表面：登录页、列表页、表单页、弹窗、媒体上传、`/design-system`；不适用项必须写明 N/A 原因。
- Playwright 或等价截图必须覆盖新增页面在关键视口下的四主题表现。
- DOM 检查必须覆盖适用契约：`page-summary` / `page-right` / `page-buttons`、`.metric-label` / `.metric-value` / `.metric-desc`、fixed toast、DS modal、弹窗 computed width 与矮视口滚动。
- 触碰上传链路时必须恢复媒体上传边界验收；未触碰时标记 N/A。

## 依赖 ASCII 树

```text
sprint-007
├── REQ-0036-clipboard-helper-best-practice-docs
│   └── add-clipboard-helper-best-practice-docs
│       ├── docs/knowledge-base/best-practices/clipboard-fallback.md
│       ├── docs/knowledge-base/README.md
│       └── src/web/README.md
├── REQ-0035-ai-usage-snapshot-sprint-close-exps
│   └── update-ai-usage-snapshot-sprint-close-exps
│       ├── snapshot status check
│       ├── sprint close/archive integration
│       ├── sprint-exps actual/fallback output
│       └── redaction + tests
├── REQ-0037-auto-token-fact-source-for-workflow-commands
│   └── add-auto-token-fact-source-for-workflow-commands
│       ├── unified post-command hook
│       ├── command run fact source
│       ├── sprint snapshot refresh
│       ├── source-command skill integration
│       └── failure fallback + redaction tests
└── cross-cutting-gate
    └── Sprint 006 A-004
        ├── reuse REQ-0020 theme acceptance matrix
        ├── add screenshot checks
        └── add DOM contract checks
```

## 发布计划

- 本 Sprint 当前发布对象为 Clipboard helper best-practice 文档与入口索引、AI usage snapshot 默认纳入 Sprint close / exps 的流程治理能力，以及工作流命令后置自动构建 Token fact source 的 Agent 流程能力。
- 后续如纳入主题相关页面新增，发布说明必须列出覆盖页面、主题矩阵、截图材料和 DOM 检查结果。

## 延后项（待评审或待齐套）

| 项 | 当前状态 | 延后原因 | 建议下一步 |
|---|---|---|---|
| `REQ-0027-mobile-page-adaptation` | approved / review | 已评审但尚未创建 OpenSpec Change，且 trace 标记 readiness 为 Partially Ready | `/req-opsx REQ-0027-mobile-page-adaptation` 后重新 `/sprint-propose` |
| `add-workflow-sync-summary-output` | proposal only | 缺 `design.md` / `tasks.md`，不满足 Change readiness | 补齐 OpenSpec Change artifacts 后纳入 |
| `reconcile-issue-residual-status` | proposal only | 缺 `design.md` / `tasks.md`，不满足 Change readiness | 补齐 OpenSpec Change artifacts 后纳入 |

## 关联文档

- `iterations/change/sprint-007/sprint.yaml`
- `iterations/change/sprint-007/release-note.md`
- `iterations/change/sprint-007/acceptance-report.md`
- `issues/requirements/archive/REQ-0036-clipboard-helper-best-practice-docs/`
- `openspec/changes/archive/2026-07-11-add-clipboard-helper-best-practice-docs/`
- `issues/requirements/review/REQ-0035-ai-usage-snapshot-sprint-close-exps/`
- `openspec/changes/archive/2026-07-11-update-ai-usage-snapshot-sprint-close-exps/`
- `issues/requirements/review/REQ-0037-auto-token-fact-source-for-workflow-commands/`
- `openspec/changes/add-auto-token-fact-source-for-workflow-commands/`
- `docs/knowledge-base/retrospectives/sprint-006-retrospective.md`
- `issues/requirements/archive/REQ-0020-theme-comfort-refine/acceptance.md`
- `docs/knowledge-base/best-practices/admin-list-page-consistency.md`
- `docs/knowledge-base/best-practices/admin-form-page-consistency.md`
- `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md`
- `docs/knowledge-base/best-practices/admin-media-upload-chain.md`
