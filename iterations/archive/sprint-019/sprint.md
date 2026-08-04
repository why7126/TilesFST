---
note: workflow-sync — workflow-sync 自动同步 — 11/11 Change archived；0 applied；Sprint `completed`
sprint_id: sprint-019
title: Sprint 019 工作流证据与 Fact Sheet summary 治理
status: completed
lifecycle_stage: archive
created_at: 2026-08-04 00:00:00
updated_at: 2026-08-04 23:12:32
owner: product
---

# Sprint 019 工作流证据与 Fact Sheet summary 治理

## 1. Sprint 目标

本 Sprint 承接 `sprint-018` 复盘行动项与近期发布治理反馈，正式纳入两个 workflow 治理 Change、三个需求治理 Change 和六个 BUG 修复 Change：归档证据 trace/fallback、Fact Sheet compact summary、管理端列表字段 adapter 检查表、小程序 Network 面板发布清单、生产媒体维护作业入口、证书图片对象 key 前缀修复、usage docs 前置版本 SemVer 排序修复、Fact Sheet AI usage fresh gate snapshot 修复、小程序品牌类目两列对齐修复、小程序返回首页按钮二次点击回归修复，以及生产历史媒体对象漂移修复。

正式范围：

- `auto-archive-trace-fallback`
- `add-compact-fact-sheet-summary-for-large-sprints`
- `BUG-0112-certificate-image-object-key-prefix` / `fix-certificate-image-object-key-prefix`
- `BUG-0111-usage-docs-previous-version-semver-sort` / `fix-usage-docs-previous-version-semver-sort`
- `BUG-0113-fact-sheet-ai-usage-fresh-gate-snapshot` / `fix-fact-sheet-ai-usage-fresh-gate-snapshot`
- `BUG-0114-miniapp-brand-list-category-column-alignment` / `fix-miniapp-brand-list-category-column-alignment`
- `BUG-0115-miniapp-home-button-regression-after-second-click` / `fix-miniapp-home-button-repeat-click-regression`
- `REQ-0095-admin-list-field-display-adapter-checklist` / `standardize-admin-list-field-display-adapters`
- `REQ-0096-miniapp-network-panel-release-checklist` / `update-miniapp-network-panel-release-checklist`
- `REQ-0097-prod-compose-media-maintenance-job` / `add-prod-media-maintenance-jobs`
- `BUG-0116-prod-media-historical-object-drift` / `fix-prod-media-historical-object-drift`

### auto-archive-trace-fallback 要点

- 为已归档 Change 缺失 `trace.md` 的场景补齐最小可追溯证据。
- 可写归档目录优先生成最小 `trace.md`，记录 Change ID、归档路径、状态、归档时间来源、任务完成摘要和自动生成标记。
- 不可写或不适合写入时输出结构化 fallback 摘要，供工具链机器判定闭环。
- 保持 legacy archive path、incomplete tasks、缺失 tasks 和 Issue 未闭环等既有 blocker 不被放宽。
- 不影响业务 API、数据库、Web、小程序、MinIO 或 Orval。

### add-compact-fact-sheet-summary-for-large-sprints 要点

- `scripts/generate-sprint-fact-sheet.py --summary` 默认输出 compact AI usage 摘要。
- 10+ Change Sprint summary 默认不得输出完整 `usage_matrices.rows` 或四张 usage matrix 明细。
- 完整矩阵继续通过 `--fields ai_usage_snapshot.usage_matrices` 按需读取。
- `/sprint-exps` 默认使用 compact Token Usage Fact Sheet summary。

### BUG-0112 / fix-certificate-image-object-key-prefix 要点

- 图片类品牌证书 key 必须归入 `images/` 标准前缀，PDF/文档类证书继续归入 `files/`。
- 修复证书图片上传、证书多图保存、缩略图生成和历史对象审计/迁移脚本的前缀分流。
- 同步对象存储、媒体、文件上传、Skill 和测试口径，避免后续 Change 继续沿用旧前缀。
- 媒体验收必须覆盖 key、object、URL、render 四联 evidence。

### REQ-0097 / add-prod-media-maintenance-jobs 要点

- 建立生产 Docker Compose 环境下的媒体历史维护作业入口，优先纳入 `deploy/prod/compose.tencent-cos.yml` 部署矩阵。
- 明确 `tilesfst-maintenance` 或等价受控维护入口策略，避免生产临时挂载未评审脚本后直接 apply。
- 维护任务必须支持外部 MySQL、腾讯云 COS / S3 兼容对象存储 provider、dry-run/apply、limit/batch、幂等和脱敏输出。
- 执行前要求 MySQL 快照与对象存储 bucket/prefix 快照，执行后输出媒体四联/五联验收摘要。
- 不影响 Web、小程序、管理端 UI、API 或数据库 schema；若实现引入镜像/Compose/env 变更，必须同步部署文档、镜像治理和测试。

## 2. Scope

本 Sprint 正式范围按“需求 / BUG / Change”分组维护。需求与 BUG 表展示业务范围项，Change 表展示对应 OpenSpec 执行单，避免在一个超宽表中混排导致预览不可读。

| 类型 | 编号 | 标题 | 状态 | 估算 | 说明 |
|---|---|---|---|---:|---|
| REQ | REQ-0095-admin-list-field-display-adapter-checklist | 管理端列表字段展示统一 adapter 检查表 | done | 1 人天 | archived `standardize-admin-list-field-display-adapters`（2026-08-04 09:08:00） |
| REQ | REQ-0096-miniapp-network-panel-release-checklist | 小程序网络面板验证纳入发布准备清单 | done | 1 人天 | archived `update-miniapp-network-panel-release-checklist`（2026-08-04 09:29:34） |
| REQ | REQ-0097-prod-compose-media-maintenance-job | 生产 Docker Compose 环境支持媒体历史数据维护任务安全执行 | done | 5 人天 | archived `add-prod-media-maintenance-jobs`（2026-08-04 20:28:00） |
| BUG | BUG-0112-certificate-image-object-key-prefix | 证书图片对象 key 未归入 images 前缀 | done | 3 人天 | archived `fix-certificate-image-object-key-prefix`（2026-08-04 09:23:49） |
| BUG | BUG-0111-usage-docs-previous-version-semver-sort | usage docs 前置版本候选使用字符串排序可能选错版本 | done | 1 人天 | archived `fix-usage-docs-previous-version-semver-sort`（2026-08-04 08:56:25） |
| BUG | BUG-0113-fact-sheet-ai-usage-fresh-gate-snapshot | Fact Sheet AI usage fresh gate 与已刷新 snapshot 状态不一致 | done | 2 人天 | archived `fix-fact-sheet-ai-usage-fresh-gate-snapshot`（2026-08-04 08:52:00） |
| BUG | BUG-0114-miniapp-brand-list-category-column-alignment | 小程序品牌列表页品牌类目两列未分别左对齐 | done | 1 人天 | archived `fix-miniapp-brand-list-category-column-alignment`（2026-08-04 09:29:33） |
| BUG | BUG-0115-miniapp-home-button-regression-after-second-click | 小程序返回首页按钮第二次点击失效回归 | done | 1 人天 | archived `fix-miniapp-home-button-repeat-click-regression`（2026-08-04 09:30:14） |
| BUG | BUG-0116-prod-media-historical-object-drift | 生产历史媒体对象与缩略图存在规范漂移 | done | 3 人天 | archived `fix-prod-media-historical-object-drift`（2026-08-04 20:20:00） |
| Change | auto-archive-trace-fallback | auto archive trace fallback | archived | 3 人天 | archived `auto-archive-trace-fallback`（2026-08-04 00:00:00） |
| Change | add-compact-fact-sheet-summary-for-large-sprints | add compact fact sheet summary for large sprints | archived | 3 人天 | archived `add-compact-fact-sheet-summary-for-large-sprints`（2026-08-04 08:48:37） |

<!-- workflow-sync:scope-requirements:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| REQ-0095 | 管理端列表字段展示统一 adapter 检查表 | P1 | done | archived `standardize-admin-list-field-display-adapters`（2026-08-04 09:08:00） |
| REQ-0096 | 小程序网络面板验证纳入发布准备清单 | P1 | done | archived `update-miniapp-network-panel-release-checklist`（2026-08-04 09:29:34） |
| REQ-0097 | 生产 Docker Compose 环境支持媒体历史数据维护任务安全执行 | P1 | done | archived `add-prod-media-maintenance-jobs`（2026-08-04 20:28:00） |
<!-- workflow-sync:scope-requirements:end -->

<!-- workflow-sync:scope-bugs:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| BUG-0112 | 证书图片对象 key 未归入 images 前缀 | high | done | archived `fix-certificate-image-object-key-prefix`（2026-08-04 09:23:49） |
| BUG-0111 | usage docs 前置版本候选使用字符串排序可能选错版本 | medium | done | archived `fix-usage-docs-previous-version-semver-sort`（2026-08-04 08:56:25） |
| BUG-0113 | Fact Sheet AI usage fresh gate 与已刷新 snapshot 状态不一致 | medium | done | archived `fix-fact-sheet-ai-usage-fresh-gate-snapshot`（2026-08-04 08:52:00） |
| BUG-0114 | 小程序品牌列表页品牌类目两列未分别左对齐 | medium | done | archived `fix-miniapp-brand-list-category-column-alignment`（2026-08-04 09:29:33） |
| BUG-0115 | 小程序返回首页按钮第二次点击失效回归 | high | done | archived `fix-miniapp-home-button-repeat-click-regression`（2026-08-04 09:30:14） |
| BUG-0116 | 生产历史媒体对象与缩略图存在规范漂移 | high | done | archived `fix-prod-media-historical-object-drift`（2026-08-04 20:20:00） |
<!-- workflow-sync:scope-bugs:end -->

<!-- workflow-sync:scope-changes:start -->
| Change ID | 关联需求 | 状态 | Sprint 目标 |
|---|---|---|---|
| `auto-archive-trace-fallback` | — | archived | archived `auto-archive-trace-fallback`（2026-08-04 00:00:00） |
| `add-compact-fact-sheet-summary-for-large-sprints` | — | archived | archived `add-compact-fact-sheet-summary-for-large-sprints`（2026-08-04 08:48:37） |
| `fix-certificate-image-object-key-prefix` | BUG-0112-certificate-image-object-key-prefix | archived | archived `fix-certificate-image-object-key-prefix`（2026-08-04 09:23:49） |
| `fix-usage-docs-previous-version-semver-sort` | BUG-0111-usage-docs-previous-version-semver-sort | archived | archived `fix-usage-docs-previous-version-semver-sort`（2026-08-04 08:56:25） |
| `fix-fact-sheet-ai-usage-fresh-gate-snapshot` | BUG-0113-fact-sheet-ai-usage-fresh-gate-snapshot | archived | archived `fix-fact-sheet-ai-usage-fresh-gate-snapshot`（2026-08-04 08:52:00） |
| `standardize-admin-list-field-display-adapters` | REQ-0095-admin-list-field-display-adapter-checklist | archived | archived `standardize-admin-list-field-display-adapters`（2026-08-04 09:08:00） |
| `update-miniapp-network-panel-release-checklist` | REQ-0096-miniapp-network-panel-release-checklist | archived | archived `update-miniapp-network-panel-release-checklist`（2026-08-04 09:29:34） |
| `fix-miniapp-brand-list-category-column-alignment` | BUG-0114-miniapp-brand-list-category-column-alignment | archived | archived `fix-miniapp-brand-list-category-column-alignment`（2026-08-04 09:29:33） |
| `fix-miniapp-home-button-repeat-click-regression` | BUG-0115-miniapp-home-button-regression-after-second-click | archived | archived `fix-miniapp-home-button-repeat-click-regression`（2026-08-04 09:30:14） |
| `add-prod-media-maintenance-jobs` | REQ-0097-prod-compose-media-maintenance-job | archived | archived `add-prod-media-maintenance-jobs`（2026-08-04 20:28:00） |
| `fix-prod-media-historical-object-drift` | BUG-0116-prod-media-historical-object-drift | archived | archived `fix-prod-media-historical-object-drift`（2026-08-04 20:20:00） |
<!-- workflow-sync:scope-changes:end -->

REQ：`REQ-0095`、`REQ-0096` 已纳入正式范围；BUG：`BUG-0112`、`BUG-0111`、`BUG-0113`、`BUG-0114`、`BUG-0115` 已纳入正式范围，优先级高于新增体验能力；当前完成度与验收风险以 Scope 表状态、关联 Change 和 acceptance-report 为准。

REQ：`REQ-0095`、`REQ-0096`、`REQ-0097` 已纳入正式范围；BUG：`BUG-0112`、`BUG-0111`、`BUG-0113`、`BUG-0114`、`BUG-0115`、`BUG-0116` 已纳入正式范围，优先级高于新增体验能力；当前完成度与验收风险以 Scope 表状态、关联 Change 和 acceptance-report 为准。

Change：已回填 9 个范围项关联 Change，另有 2 个纯 Change；9 archived，0 applied，0 in_progress，2 proposed。所有已纳入范围项均已关联 Change；执行开发与归档时以 Scope 表逐项状态为准。

## 3. 工作量与容量

| 项 | 值 |
|---|---:|
| developers | 2 |
| testers | 1 |
| capacity_person_days | 30 |
| estimated_story_points | 24 |
| estimated_person_days | 24 |
| capacity_usage | 80.00% |
| fix_buffer_person_days | 6 |
| fix_buffer_ratio | 20.00% |

容量门禁：Pass。`project.yaml` 未提供显式 Sprint 容量，沿用 sprint-018 已确认容量基线 2 dev + 1 tester / 30 人天。本 Sprint 当前纳入 2 个 workflow 治理 Change、3 个需求治理 Change 和 6 个 BUG 修复 Change，估算 24 人天，占用 80.00%，低于 30 人天容量并保留 6 人天缓冲；fix buffer 已从 30.00% 降至 20.00%，后续实现需优先控制生产 apply evidence 和 blocked 风险。

## 4. 里程碑

| 阶段 | 目标日期 | 交付 |
|---|---|---|
| 规划确认 | 2026-08-04 00:00:00 | Sprint 四件套、Change trace 与 Workflow Sync 完成 |
| 实现完成 | 2026-08-05 18:00:00 | 最小 trace 生成、结构化 fallback、Fact Sheet compact summary 接入完成 |
| 验证完成 | 2026-08-06 18:00:00 | pytest、OpenSpec 文档校验、Sprint scope 校验完成 |
| 验收归档 | 2026-08-07 18:00:00 | Change 验收通过并完成 `/opsx-archive` |

## 5. 风险

| 风险 | 缓解 |
|---|---|
| 自动生成的最小 trace 被误认为原始人工 trace | Frontmatter 和正文必须标记 `auto_generated_minimal_archive_trace`，并记录证据来源 |
| fallback 摘要变成宽松豁免，掩盖真实 blocker | 保持 incomplete tasks、缺失 tasks、legacy archive path 和 Issue 未闭环门禁不变 |
| 历史归档事实不足导致时间或状态推断不可靠 | 明确 `timestamp_source`，无法推断时返回 blocker 或要求人工补齐 |
| 多个调用方重复实现 fallback 拼装 | 归档证据校验脚本或共享模块集中输出结构化结果，调用方只消费摘要 |
| summary 过度裁剪导致 `/sprint-exps` 无法判断矩阵是否可用 | 保留 `usage_matrices_summary`，完整矩阵通过 fields 按需读取 |
| 证书图片 key 迁移不完整导致展示 404 | 历史对象迁移必须先 dry-run，apply 后复核 key/object/URL/render 四联 evidence |
| 只修上传不修脚本导致旧前缀复发 | 将缩略图回填、历史审计、规范和 Skill 一并纳入 tasks 与验收 |
| BUG-0116 与生产维护入口存在依赖 | 复用 `add-prod-media-maintenance-jobs` 的受控入口；若入口未完成，生产 apply 只能记录 blocked，先完成本地等价 dry-run 与二次审计 |

## 6. 知识库承接

| 来源 | 承接动作 |
|---|---|
| `docs/knowledge-base/retrospectives/sprint-018-retrospective.md` | 承接 `T-018-004`：archived Change 缺 `trace.md` 时自动生成最小归档 trace 或结构化 fallback 摘要。 |
| `docs/knowledge-base/retrospectives/sprint-018-retrospective.md` | 承接 `T-018-002`：10+ Change Sprint compact summary，避免默认输出完整 usage matrices。 |
| `docs/knowledge-base/retrospectives/sprint-018-retrospective.md` | 承接 `T-018-003`：小程序 DevTools/体验版 Network evidence 前置到 release/miniapp 发布准备清单。 |
| `docs/knowledge-base/retrospectives/sprint-018-retrospective.md` | 继续使用 summary-first 和 warning-driven 读取策略，避免为历史归档缺口全量扫描 `openspec/archive/**`。 |
| `rules/agent-context-budget.md` | 实现与验收优先使用精确 Change ID、归档路径和聚焦测试输出。 |
| `docs/knowledge-base/best-practices/admin-media-upload-chain.md` | BUG-0112 必须覆盖上传状态机、`object_key` 与 `/media/` 代理一致性、Docker Web 边界和媒体四联 evidence。 |

## 7. 横切预防清单

- [ ] workflow：归档证据校验必须区分 `trace-present`、`auto-generated-minimal-trace`、`fallback-summary-pass` 和 blocker。
- [ ] workflow：最小 trace 不得伪造人工验收结论，无法确认字段必须标记 unknown 或待人工复核。
- [ ] workflow：结构化 fallback 摘要必须机器可读，不能只输出自由文本。
- [ ] testing：pytest 覆盖可写自动 trace、不可写 fallback、证据不足 blocker 和既有 blocker 不被放宽。
- [ ] context-budget：不得宽泛扫描全部 archive；按 sprint/change 精确路径读取。
- [ ] docs：若调整 workflow 技能或治理规则，需同步对应技能说明和相关长期治理文档。
- [ ] workflow：Fact Sheet summary 默认只输出 compact AI usage 摘要，不携带完整矩阵 rows。
- [ ] workflow：fields 模式能读取完整 `ai_usage_snapshot.usage_matrices`。
- [ ] media-upload：证书图片 key/object/URL/render 四联验收齐全，图片归 `images/`、PDF 归 `files/`。
- [ ] media-upload：历史对象迁移脚本必须 dry-run/apply/幂等复核，输出不得泄露敏感信息。
- [ ] docs：媒体、对象存储、文件上传和 Skill 口径必须同步，避免证书图片继续使用 `files/`。
- [ ] miniapp-release：DevTools Network 与体验版 Network 作为人工 checklist 输出，不得被自动门禁标记为通过。
- [ ] miniapp-release：Network evidence 不得包含 token、Cookie、Authorization header、真实密钥、真实客户数据或未脱敏隐私。

## 8. 依赖 ASCII 树

```text
auto-archive-trace-fallback
├── openspec/archive/2026-08-04-auto-archive-trace-fallback/proposal.md
├── openspec/archive/2026-08-04-auto-archive-trace-fallback/design.md
├── openspec/archive/2026-08-04-auto-archive-trace-fallback/tasks.md
├── openspec/archive/2026-08-04-auto-archive-trace-fallback/specs/agent-workflow-tooling/spec.md
├── scripts/validate-archive-evidence.py
├── scripts/workflow_sync/**
└── tests/*archive* / tests/*workflow*

add-compact-fact-sheet-summary-for-large-sprints
├── openspec/archive/2026-08-04-add-compact-fact-sheet-summary-for-large-sprints/proposal.md
├── openspec/archive/2026-08-04-add-compact-fact-sheet-summary-for-large-sprints/design.md
├── openspec/archive/2026-08-04-add-compact-fact-sheet-summary-for-large-sprints/tasks.md
├── openspec/archive/2026-08-04-add-compact-fact-sheet-summary-for-large-sprints/specs/agent-workflow-tooling/spec.md
├── openspec/archive/2026-08-04-add-compact-fact-sheet-summary-for-large-sprints/trace.md
├── scripts/generate-sprint-fact-sheet.py
├── .agents/skills/sprint-exps/SKILL.md
└── tests/test_generate_sprint_fact_sheet.py

fix-certificate-image-object-key-prefix
├── openspec/archive/2026-08-04-fix-certificate-image-object-key-prefix/proposal.md
├── openspec/archive/2026-08-04-fix-certificate-image-object-key-prefix/design.md
├── openspec/archive/2026-08-04-fix-certificate-image-object-key-prefix/tasks.md
├── openspec/archive/2026-08-04-fix-certificate-image-object-key-prefix/specs/object-storage/spec.md
├── openspec/archive/2026-08-04-fix-certificate-image-object-key-prefix/specs/brand-certificate-management/spec.md
├── openspec/archive/2026-08-04-fix-certificate-image-object-key-prefix/specs/media-acceptance-template/spec.md
├── issues/bugs/archive/BUG-0112-certificate-image-object-key-prefix/
├── scripts/*certificate* / scripts/*object*
└── tests/*brand_certificate* / tests/*media*

```

## 9. 发布计划

该 Sprint 默认随下一个产品版本发布。两个 workflow Change 不影响业务 API、数据库、Web、小程序、MinIO、Orval 或 Docker Compose。`BUG-0112` 会影响媒体对象 key、品牌证书图片/文件分流、历史对象迁移和多端展示验收；若实现调整 API 响应字段或 Schema，必须同步 OpenAPI / Orval / API 文档和测试。发布前重点验证归档证据校验、Sprint close readiness、Workflow Sync、Fact Sheet compact summary，以及证书图片 key/object/URL/render 四联证据。

## 10. 关联文档

## 11. 关闭记录

Sprint 已于 2026-08-04 23:08:58 完成归档关闭：11/11 Change archived，117/117 tasks 完成；readiness、stale scan 和 issue promote gate 均已通过。归档后目录迁移为 `iterations/archive/sprint-019/`。

| 类型 | 路径 |
|---|---|
| Change | `openspec/archive/2026-08-04-auto-archive-trace-fallback/` |
| Change | `openspec/archive/2026-08-04-add-compact-fact-sheet-summary-for-large-sprints/` |
| BUG | `issues/bugs/archive/BUG-0112-certificate-image-object-key-prefix/` |
| Change | `openspec/archive/2026-08-04-fix-certificate-image-object-key-prefix/` |
| Spec delta | `openspec/archive/2026-08-04-auto-archive-trace-fallback/specs/agent-workflow-tooling/spec.md` |
| Spec delta | `openspec/archive/2026-08-04-add-compact-fact-sheet-summary-for-large-sprints/specs/agent-workflow-tooling/spec.md` |
| Spec delta | `openspec/archive/2026-08-04-fix-certificate-image-object-key-prefix/specs/object-storage/spec.md` |
| Spec delta | `openspec/archive/2026-08-04-fix-certificate-image-object-key-prefix/specs/brand-certificate-management/spec.md` |
| Spec delta | `openspec/archive/2026-08-04-fix-certificate-image-object-key-prefix/specs/media-acceptance-template/spec.md` |
| Sprint 复盘来源 | `docs/knowledge-base/retrospectives/sprint-018-retrospective.md` |
| Sprint 经验复盘 | `docs/knowledge-base/retrospectives/sprint-019-retrospective.md` |
