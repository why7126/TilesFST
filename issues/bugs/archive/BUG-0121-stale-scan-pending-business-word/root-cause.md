---
bug_id: BUG-0121-stale-scan-pending-business-word
created_at: 2026-08-06 11:41:11
updated_at: 2026-08-06 11:42:10
classification: code
---

# 直接原因

`scripts/sprint_close_stale_scan.py` 的 `_line_has_issue_intermediate_word()` 使用单一正则扫描已闭环 Issue 子文档，并将独立英文 P 词 作为中间态词直接匹配。该判断没有区分结构化状态字段、流程说明与普通业务正文，因此会把“SKU P-word 图片正式化”这类业务短语误报为 `issue-subdocument-stale-state`。

# 根本原因

Sprint close stale scan 的中间态检测策略过于粗粒度：它把 Issue 子文档里的自然语言正文与状态元数据视为同等风险上下文，缺少字段级、表格级或流程语义级的判定边界。

现有测试覆盖了已闭环 Issue 子文档残留 验收未完成、归档未完成等真实中间态应阻断的场景，但缺少“业务正文出现 P-word 应放行”的反向用例，导致误报未被回归测试捕获。

# 触发条件

- Sprint 关联的 REQ 或 BUG 已闭环，关联 Change 已归档。
- 该 Issue 子文档正文包含独立英文 P 词，例如“SKU P-word 图片正式化”。
- 执行 `python scripts/check-sprint-close-stale-scan.py --sprint <sprint-id>`，或通过 `python scripts/validate-sprint-archive-readiness.py --sprint <sprint-id>` 间接触发 stale scan。

# 分类

- 类型：code
- 模块：workflow governance / Sprint archive readiness
- 风险性质：归档门禁误报

# 修复方向

- 将普通正文中的 英文 P 词 从无上下文全局阻断词中移除，或将其限制到明确状态字段、状态表格、验收状态字段和流程说明上下文。
- 保留对 评审中、提案阶段、实现完成但归档未闭环、迭代中、验收未完成、实现未完成、归档未完成 等真实中间态残留的阻断。
- 增加成对回归测试：业务正文 `SKU P-word 图片正式化` 放行；结构化状态字段或流程表格中的 P-word 语义继续阻断。
