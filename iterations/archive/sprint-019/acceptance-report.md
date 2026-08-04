---
note: workflow-sync — 11/11 Change 已 archive；0 applied；待人工 sign-off
sprint_id: sprint-019
title: Sprint 019 验收报告
status: completed
created_at: 2026-08-04 00:00:00
updated_at: 2026-08-04 23:12:32
owner: product
---

# Sprint 019 验收报告

## 1. 验收范围

| 类型 | 编号 | 状态 | 验收入口 |
|---|---|---|---|
| Change | `auto-archive-trace-fallback` | archived | `openspec/archive/2026-08-04-auto-archive-trace-fallback/tasks.md` |
| Change | `add-compact-fact-sheet-summary-for-large-sprints` | archived | `openspec/archive/2026-08-04-add-compact-fact-sheet-summary-for-large-sprints/tasks.md` |
| Change | `fix-certificate-image-object-key-prefix` | archived | `openspec/archive/2026-08-04-fix-certificate-image-object-key-prefix/tasks.md` |
| Change | `fix-usage-docs-previous-version-semver-sort` | archived | `openspec/archive/2026-08-04-fix-usage-docs-previous-version-semver-sort/tasks.md` |
| Change | `fix-fact-sheet-ai-usage-fresh-gate-snapshot` | archived | `openspec/archive/2026-08-04-fix-fact-sheet-ai-usage-fresh-gate-snapshot/tasks.md` |
| Change | `standardize-admin-list-field-display-adapters` | archived | `openspec/archive/2026-08-04-standardize-admin-list-field-display-adapters/tasks.md` |
| Change | `update-miniapp-network-panel-release-checklist` | archived | `openspec/archive/2026-08-04-update-miniapp-network-panel-release-checklist/tasks.md` |
| Change | `fix-miniapp-brand-list-category-column-alignment` | archived | `openspec/archive/2026-08-04-fix-miniapp-brand-list-category-column-alignment/tasks.md` |
| Change | `fix-miniapp-home-button-repeat-click-regression` | archived | `openspec/archive/2026-08-04-fix-miniapp-home-button-repeat-click-regression/tasks.md` |
| Change | `add-prod-media-maintenance-jobs` | archived | `openspec/archive/2026-08-04-add-prod-media-maintenance-jobs/tasks.md` |
| Change | `fix-prod-media-historical-object-drift` | archived | `openspec/archive/2026-08-04-fix-prod-media-historical-object-drift/tasks.md` |

## 2. 验收标准

- [x] 可写归档目录缺少 `trace.md` 时，校验工具自动生成最小归档 trace。
- [x] 不可写或不适合写入场景输出结构化 fallback 摘要，字段足以机器判定闭环。
- [x] 证据不足时返回非零退出码并列出缺失字段和人工补齐动作。
- [x] incomplete tasks、缺失 tasks、legacy archive path 和 Issue 未闭环等既有 blocker 不被放宽。
- [x] 相关 pytest、OpenSpec 文档语言校验和 Sprint scope 校验通过。
- [x] `scripts/generate-sprint-fact-sheet.py --summary` 默认输出 `usage_matrices_summary`，不输出完整 `usage_matrices.rows`。
- [x] `--fields ai_usage_snapshot.usage_matrices` 能返回完整矩阵结构。
- [x] `/sprint-exps` Skill 默认使用 compact Token Usage Fact Sheet summary，完整矩阵按需读取。
- [x] Fact Sheet 与 AI usage 聚焦 pytest 通过。
- [x] 图片类品牌证书上传后原图 key 使用 `images/` 标准前缀，PDF/文档类证书继续使用 `files/`。
- [x] 证书图片缩略图与原图保持同一图片资源归属，不再生成 `files/default/brand-certificates/*.thumb.*`。
- [x] 历史证书图片 key 审计/迁移脚本支持 dry-run、apply 和幂等复跑。
- [x] 媒体四联验收覆盖 key、object、URL、render，且不暴露敏感信息。

## 3. 当前结论

最终结论：通过。Sprint 范围内 11 个 Change 均已归档，117/117 tasks 完成；`python scripts/validate-sprint-archive-readiness.py --sprint sprint-019` 与 Sprint close stale scan 均通过。Issue promote 检查显示无待迁移 Issue 包。

AI usage snapshot：Fact Sheet fresh gate 当前报告 `snapshot_status: stale`、`ai_usage_mode: estimated_fallback`，未使用真实 session JSONL 刷新；本次 Sprint close 以显式警告继续，后续如需真实成本分析，应运行 `python scripts/extract-ai-usage.py --session-jsonl <local-session.jsonl> --sprint sprint-019 --json`。
