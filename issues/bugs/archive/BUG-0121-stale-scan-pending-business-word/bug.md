---
bug_id: BUG-0121-stale-scan-pending-business-word
title: stale scan 对业务词 P-word 误判为流程中间态
severity: medium
status: done
owner:
discovered_at: 2026-08-06 11:13:56
created_at: 2026-08-06 11:23:14
updated_at: 2026-08-06 13:08:31
environment: local
related_requirement:
related_change: fix-stale-scan-pending-business-word
---

# 现象

Sprint 归档 readiness 的 stale scan 会把 Issue 正文中的业务短语“SKU P-word 图片正式化”识别为流程中间态残留，导致普通业务描述被误判为归档 blocker。

当前扫描入口为 `scripts/check-sprint-close-stale-scan.py`，实际逻辑在 `scripts/sprint_close_stale_scan.py`。探索阶段确认 `_line_has_issue_intermediate_word()` 将独立英文 P 词 直接纳入 Issue 子文档中间态扫描，且扫描发生在已 `done` 且关联 Change 已 `archived` 的 Issue 子文档上。

# 复现步骤

1. 准备一个 Sprint，其关联 Issue 已处于 `done`，关联 Change 已处于 `archived`。
2. 在该 Issue 子文档正文中写入类似“业务说明：SKU P-word 图片正式化已完成。”的自然语言描述。
3. 执行 `python scripts/check-sprint-close-stale-scan.py --sprint <sprint-id>`，或通过 `python scripts/validate-sprint-archive-readiness.py --sprint <sprint-id>` 间接触发 stale scan。
4. 查看扫描结果中的 blocker。

# 期望 vs 实际

期望：普通正文中的业务词 英文 P 词 应按上下文判断，不应仅因独立出现就被视为 Issue 流程中间态残留。

实际：正文短语中的 英文 P 词 被识别为 `issue-subdocument-stale-state`，导致 Sprint close stale scan 返回 blocked。

# 影响范围

- `scripts/sprint_close_stale_scan.py` 的 Issue 子文档 stale 文案识别逻辑。
- `scripts/check-sprint-close-stale-scan.py` 的单独扫描结果。
- `scripts/validate-sprint-archive-readiness.py` 中包含的 Sprint archive readiness gate。
- Issue 文档写作规范：业务语义中的 英文 P 词、对象存储 P-word 路径等词汇可能被误伤。

# 严重等级说明

严重等级为 `medium`。该问题不会直接影响线上业务功能或数据安全，但会影响 Sprint 归档 readiness 的准确性：合法业务正文可能被阻断，增加归档返工成本；同时若简单放宽扫描，又可能削弱对真实评审中、提案阶段、实现完成但归档未闭环、验收未完成等中间态残留的治理能力。

# 建议验收要点

- 已归档 Issue 子文档的普通正文包含“SKU P-word 图片正式化”时，stale scan 不应报 blocker。
- 结构化状态字段、状态表格和流程说明中的中间态仍应被严格扫描，例如评审阶段、验收未完成、提案阶段、实现完成但归档未闭环、实现未完成、归档未完成等流程残留。
- Sprint archive readiness 调用 stale scan 时，应保留对真实中间态残留和 legacy `openspec/changes/archive/` canonical 引用的阻断能力。
