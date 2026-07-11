---
requirement_id: REQ-0032-clipboard-copy-helper-best-practice
title: Clipboard 复制交互沉淀共享 helper 或 best-practice 用户故事
status: archived
created_at: 2026-07-11 16:04:55
updated_at: 2026-07-11 20:10:50
---

# User Stories

## US-001 管理员复制日志 request_id

作为企业内部管理员，我希望在日志审计列表中点击复制 `request_id` 后获得明确反馈，以便快速把请求编号交给排障人员。

验收要点：

- 点击复制有效 `request_id` 时，系统应调用统一复制 helper 并展示业务语义成功提示。
- Clipboard API 不存在或写入失败时，系统应展示手动复制指引，不得无反馈。
- 复制成功后应保持既有 `copy_request_id` 埋点行为。
- 空 `request_id` 行不得触发无效复制或误导性成功提示。

## US-002 管理员复制重置密码

作为企业内部管理员，我希望复制随机密码失败时输入框能自动选中文本，以便我可以立即手动复制并安全交付给用户。

验收要点：

- 点击复制密码时，系统应优先尝试 Clipboard API 自动复制。
- 自动复制失败或 API 不可用时，应聚焦并选中密码输入框。
- 弹窗内 `role="status"` 或等价可访问反馈应提示用户手动复制。
- 随机密码不得被写入日志、错误消息或全局埋点内容。

## US-003 前端开发复用复制 helper

作为前端开发人员，我希望有统一的复制 helper 和测试范式，以便新增复制入口时不再重复处理成功、失败、API 不存在和手动复制分支。

验收要点：

- helper 应返回结构化结果，至少能区分 `success`、`failed`、`unavailable`、`empty`。
- helper 不应耦合 toast、dialog、埋点或具体页面 DOM。
- helper 应支持可选 fallback 回调，用于选中文本或触发调用方自定义兜底。
- helper 应有独立单元测试覆盖主要浏览器能力分支。

## US-004 QA 验证复制交互回归

作为 QA，我希望用稳定清单验证复制交互，以便确认不同页面的失败路径、反馈文案和 fallback 没有回归。

验收要点：

- 测试应覆盖 Clipboard API 成功、reject、API 不存在、空值和 fallback 调用。
- 代表场景测试应覆盖日志审计列表与重置密码弹窗。
- 失败路径不得造成列表页布局位移或弹窗宽度/滚动回归。
- 知识库横切 AC 应在后续实现验收中逐项勾选。
