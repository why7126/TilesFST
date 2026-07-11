---
bug_id: BUG-0062-archive-issue-subdoc-status-consistency
title: 归档后 issue 子文档状态一致性检查缺失
severity: high
status: archived
owner: product
discovered_at: 2026-07-11 13:19:58
environment: local
related_requirement:
related_change:
created_at: 2026-07-11 16:01:10
updated_at: 2026-07-11 20:13:04
---

# 归档后 issue 子文档状态一致性检查缺失

## 现象

`/opsx-archive` 或 `/sprint-archive` 完成后，REQ / BUG 已迁入 `issues/**/archive/`，主 `trace.md` 与 registry 可显示 `done` / `archive`，但同一 issue 包内的子文档仍可能保留非闭环状态，例如 `draft`、`pending_review`、`in_sprint` 或 `applied`。

这会造成归档包内部状态互相矛盾：外层生命周期表达“已完成归档”，子文档却仍表达“草稿、待评审、迭代中或待归档”。

## 复现

1. 准备一个已经关联 Change 并满足归档条件的 REQ 或 BUG。
2. 在 issue 包内保留至少一个带状态字段的子文档，例如 `bug.md`、`requirement.md`、`acceptance.md`、`root-cause.md`、`workaround.md`、`user-stories.md` 或 `business-flow.md`。
3. 让该子文档 frontmatter 或 YAML block 中的 `status` 仍为 `draft`、`pending_review`、`in_sprint`、`applied` 等非归档闭环状态。
4. 执行 `/opsx-archive <change-id>` 或 `/sprint-archive <sprint-id>`。
5. 检查迁入 `issues/**/archive/` 后的 issue 子文档状态。

## 期望

- 归档前或归档过程中必须校验 issue 包内维护状态字段的子文档。
- 已归档 issue 包内不应残留 `draft`、`pending_review`、`in_sprint`、`applied`、`todo`、`open` 等非闭环状态。
- 若存在残留状态，归档流程应阻断并输出具体文件路径、字段位置和残留状态，提示先完成状态同步或文档修正。

## 实际

- `workflow-sync` 当前主要同步 `trace.md` 与 `_registry.yaml` 等主状态。
- `promote-issues-for-archive.py` 判断是否可迁入 `archive/` 时，主要依据 `trace_status` 和关联 Change 是否已归档。
- `promote-issue-stage.py` 执行目录迁移时只更新 `trace.md` 的 `lifecycle_stage`。
- 因此，issue 子文档中的旧状态不会阻断归档，也不会被归档流程报告为错误。

## 影响范围

- 影响 REQ 与 BUG 两类 issue 包。
- 影响 `/opsx-archive` 与 `/sprint-archive` 归档闭环质量。
- 影响后续 `/sprint-exps`、发布审计、Issue 追溯和人工复核可信度。
- 已有归档样本可复现：archive 目录中存在 `bug.md` 为 `draft`、`acceptance.md` 为 `pending_review`、`requirement.md` 为 `in_sprint` 等残留状态。

## 严重等级说明

严重等级为 high。该问题不直接影响线上业务功能，但会破坏 OpenSpec + Issue 工作流的归档事实源一致性，使已完成归档的包内仍留有未完成状态，容易掩盖实际未闭环文档或误导后续审计与复盘。
