## 背景

`BUG-0121-stale-scan-pending-business-word` 已确认：Sprint close stale scan 在已闭环 Issue 子文档中遇到普通业务短语“SKU pending 图片正式化”时，会把独立单词 `pending` 误判为流程中间态残留，并产生 `issue-subdocument-stale-state` blocker。

该问题来自 stale scan 对 Issue 子文档正文的中间态识别过于宽泛：它没有区分结构化状态字段、流程说明和普通业务正文。若简单放宽扫描，会削弱归档门禁对真实 `pending_review`、`proposed`、`applied`、`待验收` 等残留状态的阻断能力；因此需要收窄上下文，而不是关闭门禁。

## 变更内容

- 调整 Sprint close stale scan 对 Issue 子文档中 `pending` 的识别边界：普通业务正文中的 `pending` 不得直接触发 blocker。
- 保留对结构化状态字段、状态表格、流程说明和待办语义中的中间态阻断。
- 增加回归测试：业务正文 `SKU pending 图片正式化` 放行；结构化 `status: pending_review` 或 `acceptance_status: pending` 继续阻断。
- 确认 `check-sprint-close-stale-scan.py` 与 `validate-sprint-archive-readiness.py` 对 stale scan 判断保持一致。

## 能力范围

### 新增能力

无。

### 修改能力

- `agent-workflow-tooling`：补充 Sprint close 中间态文案扫描的业务词上下文边界。
- `sprint-planning-governance`：补充 Sprint close stale scan 门禁对业务正文 `pending` 例外与真实中间态阻断的要求。

## 影响

- 影响脚本：`scripts/sprint_close_stale_scan.py`、`scripts/check-sprint-close-stale-scan.py` 的扫描结果，以及 `scripts/validate-sprint-archive-readiness.py` 间接调用结果。
- 影响测试：`tests/test_sprint_close_stale_scan.py`。
- 影响文档治理：Issue 文档写作规范不再依赖人工避开业务词 `pending`。
- 不影响 API、数据库、Web、小程序、管理端运行时代码、Orval、对象存储或 Docker Compose。

## 回滚计划

- 若修复导致真实中间态残留漏报，回滚 `scripts/sprint_close_stale_scan.py` 的上下文识别调整，并保留新增测试中真实中间态阻断用例作为定位依据。
- 回滚后不得移除 Sprint archive readiness 的 stale scan 门禁；只允许恢复更严格的匹配策略并重新设计业务词例外。
