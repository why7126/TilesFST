## 问题分析

`BUG-0121` 的直接原因是 `_line_has_issue_intermediate_word()` 将独立单词 `pending` 纳入全局中间态词匹配，并在已闭环 Issue 子文档中逐行扫描普通正文。该策略会把“SKU pending 图片正式化”这类对象存储业务语义误判为流程中间态残留。

根本原因是 stale scan 缺少上下文分层：结构化状态字段、状态表格、流程待办说明和普通业务正文被同一正则处理。

## 修复方案

1. 将 Issue 子文档 stale scan 拆分为更明确的判定：
   - 强中间态词继续全局阻断，例如 `pending_review`、`proposed`、`applied`、`in_sprint`、`待验收`、`待实现`、`待归档`。
   - 独立 `pending` 仅在结构化状态上下文中阻断，例如 frontmatter、fenced yaml、`status` / `acceptance_status` 字段、状态表格或明确流程待办说明。
   - 普通正文里的业务短语 `SKU pending 图片正式化` 不触发 blocker。
2. 保持 legacy archive path、active Change path、待 `/opsx-apply` / `/opsx-archive` 等既有阻断逻辑不变。
3. 在 `tests/test_sprint_close_stale_scan.py` 增加成对回归：
   - 已闭环 Issue 子文档普通正文包含 `SKU pending 图片正式化` 时通过。
   - 已闭环 Issue 子文档结构化状态字段残留 `status: pending_review` 或 `acceptance_status: pending` 时阻断。
   - readiness gate 通过 `validate-sprint-archive-readiness.py` 间接调用时口径一致。

## 测试策略

- 脚本级单测覆盖 `sprint_close_stale_scan.build_report()` 的 false positive 与 true positive。
- CLI 级测试覆盖 `check-sprint-close-stale-scan.py --json` 或等价输出。
- readiness 级测试可复用同一 fixture，确认 `validate-sprint-archive-readiness.py` 不因业务正文 `pending` 阻断。

## 风险与边界

- 风险：过度放宽 `pending` 可能漏报验收状态未回填。
- 缓解：保留 `acceptance_status: pending`、`status: pending_review`、状态表格和流程待办说明的阻断测试。
- 边界：本 Change 只修复治理脚本和测试，不修改业务 API、数据库、端侧 UI、对象存储适配层或部署配置。
