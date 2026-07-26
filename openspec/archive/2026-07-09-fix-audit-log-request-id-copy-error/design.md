---
created_at: 2026-07-09 08:18:00
updated_at: 2026-07-09 08:18:00
---

# Design: 日志审计页 request_id 复制兜底修复

## 背景

日志审计页用于管理员查询 API 请求日志、行为事件和审计操作。`request_id` 是排障链路的关键字段，用户需要稳定复制它来关联后端日志、接口错误响应和使用行为事件。

当前页面已提供复制按钮和固定 toast 反馈，但复制函数只覆盖 Clipboard API 成功路径。真实浏览器中 Clipboard API 可能不存在、受安全上下文限制、被权限策略拒绝，或写入操作返回失败。

## Root Cause

- 日志审计页直接调用 `navigator.clipboard.writeText(value)`，未先检查 `navigator.clipboard?.writeText` 是否存在。
- Clipboard API 失败时只显示通用失败提示，缺少可继续完成任务的手动复制兜底。
- 现有测试 mock 了 `navigator.clipboard.writeText` 成功路径，没有覆盖 Clipboard API 不存在或 reject 的失败路径。
- 项目中已有密码复制弹窗具备更稳健的 `writeText.call(navigator.clipboard, value)` 与手动选中兜底模式，但日志审计页未复用同类策略。

## Fix Strategy

### 复制能力

- 将 `request_id` 的完整值作为复制源，不使用短展示文本。
- 复制前检查 `navigator.clipboard?.writeText` 是否可用。
- Clipboard API 可用时，使用保持原生绑定的调用方式写入剪贴板。
- Clipboard API 不可用或写入失败时，提供手动复制兜底，例如：
  - 将完整 `request_id` 暴露在可选中文本或隐藏输入中并自动选中。
  - 或展示固定 toast，提示用户打开详情抽屉/选中文本后使用 Command/Ctrl + C。
- 空 `request_id` 不应触发写入；应保持已有“当前日志没有 request_id”防御提示或等价文案。

### 反馈与埋点

- 成功、失败、兜底反馈继续使用 `AdminToast` 或等价 fixed toast，不得插入文档流 notice。
- 只有 Clipboard API 写入成功时才上报 `copy_request_id` 成功事件。
- 失败或手动兜底路径不得误报成功复制；如未来需要失败埋点，应使用单独事件或明确属性，避免污染成功指标。

### 测试

新增或更新日志审计页 Vitest 用例：

- Clipboard API 可用且成功：断言写入完整 `request_id`、展示成功 toast、上报 `copy_request_id`。
- Clipboard API 不存在：断言不抛运行时错误，展示手动复制兜底反馈。
- `writeText` reject：断言不抛未捕获错误，展示手动复制兜底反馈，且不误报成功复制。
- 空 `request_id` 防御：断言提示用户且不调用 Clipboard API。
- 既有列表渲染、筛选、分页和详情抽屉测试继续通过。

## Compatibility

- API：无请求、响应、错误码或 OpenAPI 变更。
- Database：无 SQLite/MySQL schema 或迁移变更。
- Web 管理端：仅修复日志审计页复制交互。
- 小程序：不影响。
- Orval：无需执行。
- Docker Compose：无需验证，除非实现阶段选择做完整环境 smoke。

## Validation

- `pnpm --dir src/web test src/pages/admin/LogAuditPage.test.tsx`
- 如实现触碰共享复制工具或 toast 行为，补充运行相关组件测试。
- `openspec validate fix-audit-log-request-id-copy-error --strict`
