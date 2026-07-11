---
note: workflow-sync — workflow-sync 自动同步 — 7/7 Change archived；0 applied；Sprint `completed`
sprint_id: sprint-006
title: Sprint 006 迭代规划
status: completed
lifecycle_stage: archive
created_at: 2026-07-11 17:50:09
updated_at: 2026-07-11 20:17:47
owner: product
source: /sprint-propose sprint-006
---

# Sprint 006 迭代规划

## Sprint 目标

本 Sprint 聚焦三条主线：提升管理端视觉舒适度与复制交互稳定性，补齐 Sprint / OpenSpec 归档治理门禁，并建立 AI Token 使用量事实源，降低后续复盘和工作流审计歧义。

正式纳入范围：

- `REQ-0020-theme-comfort-refine`
- `REQ-0032-clipboard-copy-helper-best-practice`
- `REQ-0033-acceptance-report-summary-ac-reference`
- `REQ-0034-ai-token-usage-observability`
- `BUG-0062-archive-issue-subdoc-status-consistency`
- `BUG-0063-archived-change-trace-fallback-summary`
- `BUG-0064-theme-selector-sidebar-placement`

## Scope

<!-- workflow-sync:scope-requirements:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| REQ-0020 | Web / 管理端主题舒适度优化与主题切换 | P1 | done | archived `update-theme-comfort-refine`（2026-07-11 17:38:23） |
| REQ-0032 | Clipboard 复制交互沉淀共享 helper 或 best-practice | P1 | done | archived `add-clipboard-copy-helper-best-practice`（2026-07-11 16:13:54） |
| REQ-0033 | acceptance-report 拆分最终验收摘要与原始 AC 引用 | P1 | done | archived `update-acceptance-report-summary-ac-reference`（2026-07-11 16:15:03） |
| REQ-0034 | AI 命令 Token 使用量观测与 Sprint 复盘接入 | P1 | done | archived `add-ai-token-usage-observability`（2026-07-11 17:16:46） |
<!-- workflow-sync:scope-requirements:end -->

<!-- workflow-sync:scope-bugs:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| BUG-0062 | 归档后 issue 子文档状态一致性检查缺失 | high | done | archived `fix-archive-issue-subdoc-status-consistency`（2026-07-11 16:13:13） |
| BUG-0063 | archived Change 缺失 trace.md 时归档验证摘要兜底检查缺失 | high | done | archived `fix-archive-trace-fallback-summary-gate`（2026-07-11 17:01:42） |
| BUG-0064 | 界面主题选择器未放在侧边栏用户头像上方 | medium | done | archived `fix-theme-selector-sidebar-placement`（2026-07-11 19:58:53） |
<!-- workflow-sync:scope-bugs:end -->

<!-- workflow-sync:scope-changes:start -->
| Change ID | 关联需求 | 状态 | Sprint 目标 |
|---|---|---|---|
| `update-theme-comfort-refine` | REQ-0020-theme-comfort-refine | archived | archived `update-theme-comfort-refine`（2026-07-11 17:38:23） |
| `add-clipboard-copy-helper-best-practice` | REQ-0032-clipboard-copy-helper-best-practice | archived | archived `add-clipboard-copy-helper-best-practice`（2026-07-11 16:13:54） |
| `update-acceptance-report-summary-ac-reference` | REQ-0033-acceptance-report-summary-ac-reference | archived | archived `update-acceptance-report-summary-ac-reference`（2026-07-11 16:15:03） |
| `add-ai-token-usage-observability` | REQ-0034-ai-token-usage-observability | archived | archived `add-ai-token-usage-observability`（2026-07-11 17:16:46） |
| `fix-archive-issue-subdoc-status-consistency` | BUG-0062-archive-issue-subdoc-status-consistency | archived | archived `fix-archive-issue-subdoc-status-consistency`（2026-07-11 16:13:13） |
| `fix-archive-trace-fallback-summary-gate` | BUG-0063-archived-change-trace-fallback-summary | archived | archived `fix-archive-trace-fallback-summary-gate`（2026-07-11 17:01:42） |
| `fix-theme-selector-sidebar-placement` | BUG-0064-theme-selector-sidebar-placement | archived | archived `fix-theme-selector-sidebar-placement`（2026-07-11 19:58:53） |
<!-- workflow-sync:scope-changes:end -->

## 工作量

| 项 | 值 |
|---|---:|
| 容量 | 30 人天 |
| 估算 | 26.0 人天 |
| 容量占用 | 87% |
| Story Points | 39 |
| add/update 主能力数量 | 4 |
| BUG/fix 缓冲 | 7.0 人天 / 27% |

容量门禁结论：`pass_with_risk`。总估算未超过容量，但 fix 缓冲仍低于 30% 建议值；执行期只接受 P0/P1 且阻断归档、安全边界或已纳入主题主线验收的追加项，其他项延后到后续 Sprint。

## 估算明细

| ID | Change | Size | SP | 人天 | 说明 |
|---|---|---:|---:|---:|---|
| REQ-0020 | update-theme-comfort-refine | XL | 13 | 8.0 | 涉及 Web、API、DB、Orval、设计系统与视觉验收矩阵 |
| BUG-0062 | fix-archive-issue-subdoc-status-consistency | M | 3 | 3.0 | 脚本门禁、技能说明、pytest |
| BUG-0063 | fix-archive-trace-fallback-summary-gate | M | 3 | 3.0 | readiness gate、技能说明、脚本级回归 |
| BUG-0064 | fix-theme-selector-sidebar-placement | S | 2 | 1.0 | 管理端主题选择器位置迁移到侧边栏用户头像上方 |
| REQ-0032 | add-clipboard-copy-helper-best-practice | M | 5 | 3.0 | Web helper、代表场景迁移、Vitest |
| REQ-0033 | update-acceptance-report-summary-ac-reference | M | 5 | 3.0 | acceptance-report 模板、workflow sync、fact sheet |
| REQ-0034 | add-ai-token-usage-observability | L | 8 | 5.0 | session 解析、脱敏事实源、聚合与复盘接入 |

## 里程碑

| 目标日期 | 里程碑 | 验收 |
|---|---|---|
| 2026-07-14 18:00:00 | 治理门禁先行 | BUG-0062、BUG-0063 相关脚本模型与失败报告设计完成 |
| 2026-07-17 18:00:00 | Web 横切能力闭环 | REQ-0032 helper 与代表场景测试完成；REQ-0020 主题 token/API/DB 方案稳定 |
| 2026-07-22 18:00:00 | Sprint 文档与 Token 事实源闭环 | REQ-0033、REQ-0034 主要脚本与测试完成 |
| 2026-07-25 17:50:09 | 验收准备 | Workflow Sync check、OpenSpec validate、相关 pytest/Vitest 与必要 Docker smoke 完成 |

## 风险

| 风险 | 影响 | 缓解 |
|---|---|---|
| 主题舒适度 Change 触达 Web、API、DB、Orval | 可能挤压治理脚本交付时间 | 先确认账号级偏好最小 API；变更期间必须同步 OpenAPI/Orval/tests |
| fix 缓冲低于 30% | 新增 P0/P1 缺陷会压缩 REQ-0034 或 REQ-0020 | Sprint 执行期冻结非阻断追加项；BUG-0064 已与 REQ-0020 主题主线相关，后续继续追加需替换范围 |
| Token 使用量解析涉及本地 session 数据 | 有泄露 prompt、绝对路径或敏感输出风险 | 只持久化脱敏统计、hash、相对路径和 warning；测试覆盖 redaction |
| 归档门禁变严格 | 历史 archive 残留状态可能造成误判 | 门禁只针对待迁入 archive 的候选 issue；历史清理另行评审 |

## 知识库承接

来自 `docs/knowledge-base/retrospectives/sprint-005-retrospective.md` 的 open 行动项：

| 行动项 | 本 Sprint 承接 |
|---|---|
| A-001 归档后 issue 子文档状态一致性检查 | `BUG-0062` / `fix-archive-issue-subdoc-status-consistency` |
| A-002 Clipboard 复制交互沉淀共享 helper 或 best-practice | `REQ-0032` / `add-clipboard-copy-helper-best-practice` |
| A-003 Sprint 容量超限硬提示 | 本次容量门禁显式记录 `capacity_usage` 与 fix 缓冲风险 |
| A-005 acceptance-report 最终摘要与原始 AC 引用拆分 | `REQ-0033` / `update-acceptance-report-summary-ac-reference` |
| A-006 archived Change trace 缺失兜底摘要门禁 | `BUG-0063` / `fix-archive-trace-fallback-summary-gate` |
| Token 使用分析真实计量缺失 | `REQ-0034` / `add-ai-token-usage-observability` |

## 横切预防清单

适用 best-practices：

- `docs/knowledge-base/best-practices/admin-list-page-consistency.md`
- `docs/knowledge-base/best-practices/admin-form-page-consistency.md`
- `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md`
- `docs/knowledge-base/best-practices/admin-media-upload-chain.md`

验收 gate 摘要：

- 管理端列表改动必须保留 `page-summary`、`page-right`、指标卡 DOM 契约与 fixed toast。
- 管理端表单/设置类改动只允许一处保存 CTA，恢复默认或 dirty 放弃必须使用 DS modal。
- 管理端弹窗不得同时挂载 `modal-card` 与专属类，须验证 1440px Computed width 与矮视口滚动。
- 触碰媒体上传时必须覆盖 `idle -> uploading -> done / failed`、即时回显、控件内错误和 Docker 3000 边界；未触碰上传链路则在验收中标记 N/A。

## 依赖 ASCII 树

```text
sprint-006
├── governance-first
│   ├── BUG-0062 -> fix-archive-issue-subdoc-status-consistency
│   ├── BUG-0063 -> fix-archive-trace-fallback-summary-gate
│   └── REQ-0033 -> update-acceptance-report-summary-ac-reference
├── web-experience
│   ├── REQ-0032 -> add-clipboard-copy-helper-best-practice
│   ├── REQ-0020 -> update-theme-comfort-refine
│   └── BUG-0064 -> fix-theme-selector-sidebar-placement
└── retrospective-observability
    └── REQ-0034 -> add-ai-token-usage-observability
```

## 发布计划

- 预计发布对象：后续 `v0.x` 产品版本汇总时纳入。
- 本 Sprint 涉及 API / DB / Orval：`REQ-0020` 若实现账号级主题偏好必须同步。
- 本 Sprint 涉及 Web / 管理端：`REQ-0020`、`REQ-0032`、`BUG-0064`。
- 本 Sprint 涉及小程序：无。
- 本 Sprint 涉及 Docker Compose：仅当 `REQ-0020` 同时改动 Web + Backend 时做 smoke 验证。

## 延后项（待评审）

无。本次用户指定的 6 个候选项均已评审或处于已评审后的 `in_sprint` 状态，且 Readiness 齐全。

## 迭代关闭记录

| 时间 | 命令 | 结论 |
|---|---|---|
| 2026-07-11 20:13:04 | `/sprint-archive sprint-006` | 7/7 Change archived；readiness PASS；Sprint `change` → `archive` |

## 关联文档

- `iterations/archive/sprint-006/sprint.yaml`
- `iterations/archive/sprint-006/release-note.md`
- `iterations/archive/sprint-006/acceptance-report.md`
- `docs/knowledge-base/retrospectives/sprint-006-retrospective.md`
- `docs/knowledge-base/retrospectives/sprint-005-retrospective.md`
- `docs/knowledge-base/best-practices/admin-list-page-consistency.md`
- `docs/knowledge-base/best-practices/admin-form-page-consistency.md`
- `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md`
- `docs/knowledge-base/best-practices/admin-media-upload-chain.md`
