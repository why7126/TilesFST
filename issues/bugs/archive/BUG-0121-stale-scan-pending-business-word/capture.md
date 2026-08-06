---
bug_id: BUG-0121-stale-scan-pending-business-word
status: done
created_at: 2026-08-06 11:13:56
updated_at: 2026-08-06 13:08:40
severity_hint: medium
environment: local
related_requirement:
related_bug:
---

# 现象

Sprint 归档 readiness 的 stale scan 将需求正文中的业务短语“SKU P-word 图片正式化”识别为 Issue 流程中间态残留，导致普通业务正文被误判为归档阻断项。

# 复现步骤

1. 在即将关闭的 Sprint 关联需求或 BUG 正文中出现类似“SKU P-word 图片正式化”的业务描述。
2. 执行 `python scripts/check-sprint-close-stale-scan.py --sprint <sprint-id>`，或通过 Sprint archive readiness 间接触发 stale scan。
3. 观察扫描结果是否把正文里的 英文 P 词 当作流程中间态残留。

# 期望 vs 实际

期望：普通正文中的业务词应按上下文判断，不应仅因出现 英文 P 词 就被判定为流程中间态残留；状态字段、状态表格和流程说明中的评审中、提案阶段、实现完成但归档未闭环等中间态仍应被严格扫描并按门禁阻断。

实际：需求正文中的业务短语“SKU P-word 图片正式化”被 stale scan 识别为 Issue 中间态残留，影响 Sprint 归档 readiness 判断，也让 Issue 文档写作规范对业务词使用产生误伤。

# 附件

暂无。
