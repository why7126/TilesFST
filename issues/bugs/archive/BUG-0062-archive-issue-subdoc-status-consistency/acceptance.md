---
bug_id: BUG-0062-archive-issue-subdoc-status-consistency
title: 归档后 issue 子文档状态一致性检查缺失验收标准
status: archived
severity: high
owner: product
created_at: 2026-07-11 16:05:13
updated_at: 2026-07-11 20:13:04
related_requirement:
related_change:
---

# 验收标准

## AC-001 归档前发现 BUG 子文档残留状态

- GIVEN 一个待归档 BUG 已满足 Change archived 与 trace done 条件。
- AND 该 BUG 包内任一子文档 frontmatter 或 YAML block 中存在 `status: draft`、`status: pending_review`、`status: in_sprint`、`status: applied`、`status: todo` 或 `status: open`。
- WHEN 执行 issue archive promote 或对应归档 readiness 检查。
- THEN 流程必须阻断归档。
- AND 输出具体文件路径与残留状态值。

## AC-002 归档前发现 REQ 子文档残留状态

- GIVEN 一个待归档 REQ 已满足 Change archived 与 trace done 条件。
- AND 该 REQ 包内任一子文档 frontmatter 或 YAML block 中存在非闭环状态。
- WHEN 执行 issue archive promote 或对应归档 readiness 检查。
- THEN 流程必须阻断归档。
- AND 输出具体文件路径与残留状态值。

## AC-003 无残留状态时允许归档

- GIVEN 待归档 issue 包内不存在非闭环状态残留。
- AND `trace.md` 状态、registry 状态、关联 Change 状态均满足归档条件。
- WHEN 执行 `/opsx-archive` 后的 promote 流程。
- THEN issue 可从 `review/` 迁入 `archive/`。
- AND `trace.md` 的 `lifecycle_stage` 更新为 `archive`。

## AC-004 检查覆盖 frontmatter 与 fenced YAML block

- GIVEN issue 子文档的状态可能出现在 Markdown frontmatter。
- AND 状态也可能出现在 fenced `yaml` block。
- WHEN 执行状态一致性检查。
- THEN 两类位置都必须被检查。
- AND 报告中应能区分或定位到具体文件。

## AC-005 归档流程输出可操作报告

- GIVEN 归档检查发现残留状态。
- WHEN 命令返回失败。
- THEN 输出必须包含 issue id、文件路径、状态值和建议处理方式。
- AND 不应只给出笼统的失败信息。

## AC-006 测试覆盖

- MUST 新增或更新测试，覆盖 BUG 包残留状态阻断。
- MUST 新增或更新测试，覆盖 REQ 包残留状态阻断。
- MUST 覆盖 frontmatter `status` 和 fenced YAML block `status`。
- MUST 覆盖无残留状态时 promote 成功。

## AC-007 非目标范围

- 本缺陷修复不应修改业务 API。
- 本缺陷修复不应修改数据库 schema。
- 本缺陷修复不应修改 Web、店主端或小程序业务 UI。
- 本缺陷修复不应直接批量改写历史 archive 包状态，历史清理应另行评审。
