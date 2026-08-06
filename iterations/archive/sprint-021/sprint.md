---
note: workflow-sync — workflow-sync 自动同步 — 10/10 Change archived；0 applied；Sprint `completed`
sprint_id: sprint-021
title: Sprint 021 Fact Sheet AI usage freshness 修复
status: completed
lifecycle_stage: archive
created_at: 2026-08-06 09:01:00
updated_at: 2026-08-06 17:17:37
---

# Sprint 021 Fact Sheet AI usage freshness 修复

## 1. 目标

本 Sprint 聚焦治理链路中的 1 个 P1 REQ、7 个 medium BUG 与 2 个直接治理 Change：修复 Fact Sheet AI usage freshness baseline 对未来计划日期的误判，吸收 OpenSpec 归档已知兼容 warning 噪音，修复 docs-site Mintlify 缓存 volume 导致的 EBUSY 启动失败，补齐归档同步阶段对子文档安全状态残留的自动处理，收敛 stale scan 对业务正文 `pending` 的误判，将 Sprint 目标编号列表与 Scope 一致性校验纳入正式范围，补齐 OpenSpec CLI stdout proposal warning 与真实多行 proposal warning 块的归档成功输出过滤缺口，统一所有 Change 在 `/opsx-apply` 前必须纳入 Sprint 的门禁，并统一下一步可执行命令的 REQ/BUG/Change 参数规范。

Sprint 目标编号列表：

- BUG-0118-fact-sheet-ai-usage-future-start-date-freshness
- fix-fact-sheet-ai-usage-start-date-freshness
- BUG-0119-openspec-archive-scaffold-warning-noise
- fix-openspec-archive-scaffold-warning-noise
- BUG-0120-docs-site-mintlify-cache-ebusy
- fix-docs-site-mintlify-cache-ebusy
- BUG-0122-archive-sync-issue-subdoc-residual-cleanup
- fix-archive-sync-issue-subdoc-residual-cleanup
- BUG-0121-stale-scan-pending-business-word
- REQ-0102-sprint-goal-scope-consistency-validation
- BUG-0123-openspec-archive-proposal-warning-stdout
- BUG-0124-openspec-archive-multiline-proposal-warning-stdout
- require-all-changes-sprint-before-apply
- standardize-next-step-issue-ids

### REQ-0102-sprint-goal-scope-consistency-validation 要点

- `validate-sprint-scope.py` 应校验 Sprint 目标编号列表与正式 Scope 一致。
- `sprint-020` / `REQ-0100` 漏列场景必须能复现失败并提示具体缺失项。
- `/sprint-propose` 与 Workflow Sync 规则需明确目标编号列表维护边界。
- 本需求可先纳入 Sprint，待 `/req-opsx REQ-0102` 创建 Change 后回填 `changes[]`。

### BUG-0118-fact-sheet-ai-usage-future-start-date-freshness 要点

- 未来计划 `start_date` / `end_date` 不得作为当前 snapshot 的 freshness blocker。
- `ai_usage_freshness_baseline.skipped[]` 应记录未来计划时间及原因。
- 完整 snapshot 继续输出 `actual` / `present`，陈旧 `updated_at` baseline 仍应阻止 stale snapshot。
- `sprint-020` 类场景必须回归。

### BUG-0119-openspec-archive-scaffold-warning-noise 要点

- OpenSpec 归档成功路径不应反复展示已知英文脚手架兼容 warning。
- 未知 stderr、语言校验失败和真实归档错误必须继续可见或阻断。

### BUG-0120-docs-site-mintlify-cache-ebusy 要点

- 移除 docs-site 对 `/home/node/.mintlify` 的 Docker named volume 直挂。
- 根、local、prod Compose 与部署文档、目录结构测试保持一致。
- docs-site 启动验证不再出现 `.mintlify` 到 `.mintlify-last` 的 EBUSY。

### BUG-0122-archive-sync-issue-subdoc-residual-cleanup 要点

- 归档同步或 promote 前置流程应处理已确认安全的 Issue 子文档状态残留。
- 缺少闭环证据、验收结论或语义不明的残留仍必须保留人工判断门禁。
- `capture.md` 中可安全同步的 `captured` 残留不应继续误阻断 `promote-issues-for-archive`。

### BUG-0121-stale-scan-pending-business-word 要点

- 普通业务正文中的 `pending` 不应被直接识别为 Issue 中间态残留。
- 结构化状态字段、状态表格和流程说明中的中间态仍必须严格阻断。
- Sprint archive readiness 与单独 stale scan 对该判断保持一致。

### BUG-0123-openspec-archive-proposal-warning-stdout 要点

- 归档中文优先 Change 时，stdout 不应展示已知 proposal scaffold warning。
- 未知 stdout/stderr 仍需保留并展示，避免吞掉真实异常或诊断信息。
- BUG-0119 已修复的自定义固定说明噪音不应回归。
- 本 BUG 可先纳入 Sprint，待 `/bug-opsx BUG-0123` 创建 Change 后回填 `changes[]`。

### BUG-0124-openspec-archive-multiline-proposal-warning-stdout 要点

- 真实 OpenSpec CLI 多行 proposal warning 块应被整体吸收。
- 未知 stdout/stderr 仍需保留并展示，避免吞掉真实异常或诊断信息。
- 当前单行 warning 回归测试不应失效。
- 本 BUG 可先纳入 Sprint，待 `/bug-opsx BUG-0124` 创建 Change 后回填 `changes[]`。

### require-all-changes-sprint-before-apply 要点

- 所有 OpenSpec Change 在 `/opsx-apply` 前都必须出现在 Sprint `changes[]`。
- `/opsx-propose` 或 `/spec-opt` 直接创建的非 REQ/BUG Change 不得再因“纯治理”豁免 Sprint Inclusion Gate。
- `opsx-apply`、`workflow-sync`、`spec-opt`、AGENTS、rules、docs 与校验脚本需同步防回退。

### standardize-next-step-issue-ids 要点

- REQ 来源的后续 `/opsx-apply`、`/opsx-archive` 引导统一使用原始 `REQ-*` 标识。
- BUG 来源的后续 `/opsx-apply`、`/opsx-archive` 引导统一使用原始 `BUG-*` 标识。
- 非 REQ/BUG Change 的 `/opsx-*` 引导继续使用 `<change-id>`。

## 2. Scope

| 类型 | 编号 | 标题 | 状态 | 估算 | 说明 |
|---|---|---|---|---:|---|
| REQ | REQ-0102-sprint-goal-scope-consistency-validation | Sprint 目标编号列表与 Scope 一致性校验 | done | 1 人天 | archived `update-sprint-goal-scope-consistency-validation`（2026-08-06 13:09:57） |
| BUG | BUG-0118-fact-sheet-ai-usage-future-start-date-freshness | Fact Sheet AI usage fresh gate 将未来 Sprint start_date 当作 snapshot 新鲜度下限 | done | 1 人天 | archived `fix-fact-sheet-ai-usage-start-date-freshness`（2026-08-06 10:59:20） |
| BUG | BUG-0119-openspec-archive-scaffold-warning-noise | OpenSpec 归档反复暴露英文脚手架兼容 warning | done | 1 人天 | archived `fix-openspec-archive-scaffold-warning-noise`（2026-08-06 10:54:33） |
| BUG | BUG-0120-docs-site-mintlify-cache-ebusy | tilesfst-docs-site Mintlify 缓存 volume 导致 EBUSY 启动失败 | done | 1 人天 | archived `fix-docs-site-mintlify-cache-ebusy`（2026-08-06 11:18:25） |
| BUG | BUG-0122-archive-sync-issue-subdoc-residual-cleanup | 归档同步阶段未自动清理安全 Issue 子文档状态残留 | done | 1 人天 | archived `fix-archive-sync-issue-subdoc-residual-cleanup`（2026-08-06 12:01:48） |
| BUG | BUG-0121-stale-scan-pending-business-word | stale scan 对业务词 P-word 误判为流程中间态 | done | 1 人天 | archived `fix-stale-scan-pending-business-word`（2026-08-06 12:48:10） |
| BUG | BUG-0123-openspec-archive-proposal-warning-stdout | OpenSpec CLI proposal warning 仍通过 stdout 出现在归档成功输出中 | done | 1 人天 | archived `fix-openspec-archive-proposal-warning-stdout`（2026-08-06 13:55:08） |
| BUG | BUG-0124-openspec-archive-multiline-proposal-warning-stdout | OpenSpec CLI 多行 proposal warning stdout 块仍出现在归档成功输出中 | done | 1 人天 | archived `fix-openspec-archive-multiline-proposal-warning-stdout`（2026-08-06 15:03:07） |
| Change | require-all-changes-sprint-before-apply | require all changes sprint before apply | archived | 1 人天 | archived `require-all-changes-sprint-before-apply`（2026-08-06 14:10:20） |
| Change | standardize-next-step-issue-ids | standardize next step issue ids | archived | 1 人天 | archived `standardize-next-step-issue-ids`（2026-08-06 14:30:23） |

<!-- workflow-sync:scope-requirements:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| REQ-0102 | Sprint 目标编号列表与 Scope 一致性校验 | P1 | done | archived `update-sprint-goal-scope-consistency-validation`（2026-08-06 13:09:57） |
<!-- workflow-sync:scope-requirements:end -->

<!-- workflow-sync:scope-bugs:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| BUG-0118 | Fact Sheet AI usage fresh gate 将未来 Sprint start_date 当作 snapshot 新鲜度下限 | medium | done | archived `fix-fact-sheet-ai-usage-start-date-freshness`（2026-08-06 10:59:20） |
| BUG-0119 | OpenSpec 归档反复暴露英文脚手架兼容 warning | medium | done | archived `fix-openspec-archive-scaffold-warning-noise`（2026-08-06 10:54:33） |
| BUG-0120 | tilesfst-docs-site Mintlify 缓存 volume 导致 EBUSY 启动失败 | medium | done | archived `fix-docs-site-mintlify-cache-ebusy`（2026-08-06 11:18:25） |
| BUG-0122 | 归档同步阶段未自动清理安全 Issue 子文档状态残留 | medium | done | archived `fix-archive-sync-issue-subdoc-residual-cleanup`（2026-08-06 12:01:48） |
| BUG-0121 | stale scan 对业务词 P-word 误判为流程中间态 | medium | done | archived `fix-stale-scan-pending-business-word`（2026-08-06 12:48:10） |
| BUG-0123 | OpenSpec CLI proposal warning 仍通过 stdout 出现在归档成功输出中 | medium | done | archived `fix-openspec-archive-proposal-warning-stdout`（2026-08-06 13:55:08） |
| BUG-0124 | OpenSpec CLI 多行 proposal warning stdout 块仍出现在归档成功输出中 | medium | done | archived `fix-openspec-archive-multiline-proposal-warning-stdout`（2026-08-06 15:03:07） |
<!-- workflow-sync:scope-bugs:end -->

<!-- workflow-sync:scope-changes:start -->
| Change ID | 关联需求 | 状态 | Sprint 目标 |
|---|---|---|---|
| `fix-fact-sheet-ai-usage-start-date-freshness` | BUG-0118-fact-sheet-ai-usage-future-start-date-freshness | archived | archived `fix-fact-sheet-ai-usage-start-date-freshness`（2026-08-06 10:59:20） |
| `fix-openspec-archive-scaffold-warning-noise` | BUG-0119-openspec-archive-scaffold-warning-noise | archived | archived `fix-openspec-archive-scaffold-warning-noise`（2026-08-06 10:54:33） |
| `fix-docs-site-mintlify-cache-ebusy` | BUG-0120-docs-site-mintlify-cache-ebusy | archived | archived `fix-docs-site-mintlify-cache-ebusy`（2026-08-06 11:18:25） |
| `fix-archive-sync-issue-subdoc-residual-cleanup` | BUG-0122-archive-sync-issue-subdoc-residual-cleanup | archived | archived `fix-archive-sync-issue-subdoc-residual-cleanup`（2026-08-06 12:01:48） |
| `update-sprint-goal-scope-consistency-validation` | REQ-0102-sprint-goal-scope-consistency-validation | archived | archived `update-sprint-goal-scope-consistency-validation`（2026-08-06 13:09:57） |
| `fix-stale-scan-pending-business-word` | BUG-0121-stale-scan-pending-business-word | archived | archived `fix-stale-scan-pending-business-word`（2026-08-06 12:48:10） |
| `fix-openspec-archive-proposal-warning-stdout` | BUG-0123-openspec-archive-proposal-warning-stdout | archived | archived `fix-openspec-archive-proposal-warning-stdout`（2026-08-06 13:55:08） |
| `require-all-changes-sprint-before-apply` | — | archived | archived `require-all-changes-sprint-before-apply`（2026-08-06 14:10:20） |
| `standardize-next-step-issue-ids` | REQ-0100-mintlify-docs-site-ia-content-experience | archived | archived `standardize-next-step-issue-ids`（2026-08-06 14:30:23） |
| `fix-openspec-archive-multiline-proposal-warning-stdout` | BUG-0124-openspec-archive-multiline-proposal-warning-stdout | archived | archived `fix-openspec-archive-multiline-proposal-warning-stdout`（2026-08-06 15:03:07） |
<!-- workflow-sync:scope-changes:end -->

BUG：`BUG-0118`、`BUG-0119`、`BUG-0120` 已纳入正式范围；Change：`fix-fact-sheet-ai-usage-start-date-freshness`、`fix-openspec-archive-scaffold-warning-noise`、`fix-docs-site-mintlify-cache-ebusy` 已纳入正式范围。执行开发前必须通过 `/opsx-apply --sprint auto` Sprint scope 门禁。

## 3. 工作量与容量

| 指标 | 值 |
|---|---:|
| 开发 | 2 |
| 测试 | 1 |
| 容量 | 30 人天 |
| 估算 | 10 SP / 10 人天 |
| 容量占用 | 33% |
| fix 缓冲 | 20 人天 |

容量门禁：Pass。当前范围低于容量上限，且保留 20 人天 fix 缓冲。

## 4. 里程碑

| 阶段 | 目标日期 | 说明 |
|---|---|---|
| 规划确认 | 2026-09-03 09:00:00 | 确认 BUG-0118 与 Change 范围 |
| 实现完成 | 2026-09-09 18:00:00 | 完成 Fact Sheet baseline 修复与聚焦测试 |
| 验收完成 | 2026-09-16 18:00:00 | 完成 sprint-020 类场景回归和文档同步 |
| Sprint 收尾 | 2026-09-17 18:00:00 | 准备归档与发布说明 |

## 5. 风险

| 风险 | 等级 | 缓解 |
|---|---|---|
| 修复过度放宽 stale gate | medium | 保留 stale `updated_at` 负向测试，`scripts/ai_usage.py` stale 判断不改语义 |
| 只修 start_date 遗漏 end_date 一致性 | low | 任务中保留 future end_date 回归，统一 skipped reason |
| sprint-020 复盘证据与 summary 口径不一致 | medium | 使用 sprint-020 类 fixture 或手工 summary 输出验收 |
| docs-site 预览需 Docker 环境验证 | medium | Compose config 与目录校验可本地执行；容器启动日志需在具备 Docker 权限环境验证 |

## 6. 知识库承接

| 来源 | 承接点 |
|---|---|
| docs/knowledge-base/retrospectives/sprint-020-retrospective.md | T-020-001 open 行动项直接纳入本 Sprint：修复 sprint-exps fresh gate 对未来计划 start_date 的误判 |
| docs/knowledge-base/retrospectives/sprint-020-retrospective.md | T-020-003 open 行动项直接纳入本 Sprint：修复 stale scan 对业务词 `pending` 的误判 |

## 7. 横切预防清单

| 标签 | 适用范围 | Gate |
|---|---|---|
| workflow-tooling | Fact Sheet、AI usage snapshot、sprint-exps | 不保存原始 session JSONL、prompt、系统/开发者指令或本机绝对路径 |
| testing | Fact Sheet baseline 回归 | 覆盖 future start_date、future end_date、stale updated_at 与 sprint-020 类场景 |
| sprint-archive-readiness | stale scan / archive readiness | 覆盖业务正文 `pending` 放行与结构化中间态阻断的成对回归 |
| context-budget | sprint-exps / Fact Sheet 输出 | 默认使用 compact summary，不输出完整 usage_matrices，除非显式请求 |

## 8. 依赖树

```text
BUG-0118-fact-sheet-ai-usage-future-start-date-freshness
└── fix-fact-sheet-ai-usage-start-date-freshness
    ├── scripts/generate-sprint-fact-sheet.py baseline 策略
    ├── tests/test_generate_sprint_fact_sheet.py
    └── agent-workflow-tooling delta spec
```

## 9. 发布计划

- 本 Sprint 不单独定义产品版本号。
- 若合入发布版本，需在 release note 中说明 Fact Sheet AI usage snapshot freshness baseline 修复。
- 不涉及 API、数据库、Web、小程序、管理端或 Docker Compose 发布说明。

## 10. 关联文档

- `issues/bugs/archive/BUG-0118-fact-sheet-ai-usage-future-start-date-freshness/`
- `openspec/archive/2026-08-06-fix-fact-sheet-ai-usage-start-date-freshness/`
- `docs/knowledge-base/retrospectives/sprint-020-retrospective.md`
- `docs/knowledge-base/retrospectives/sprint-021-retrospective.md`

## 11. 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-06 09:01:00 | `/sprint-propose` | 创建 sprint-021，纳入 BUG-0118 与 Change `fix-fact-sheet-ai-usage-start-date-freshness` |
| 2026-08-06 17:16:00 | `/sprint-archive` | 10/10 Change 已归档，readiness 与 stale scan 通过；Sprint change → archive。 |
| 2026-08-06 17:28:00 | `/sprint-exps` | 生成 Sprint 021 经验复盘并回链知识库。 |
