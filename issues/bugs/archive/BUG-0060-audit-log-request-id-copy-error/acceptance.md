---
bug_id: BUG-0060-audit-log-request-id-copy-error
title: 日志审计页复制 request_id 时报错验收标准
status: implemented
severity: medium
created_at: 2026-07-09 08:06:13
updated_at: 2026-07-09 08:37:20
---

# BUG-0060 验收标准

## 回归验收

- [x] AC-001 管理员打开日志审计页后，带有 `request_id` 的日志记录仍展示复制按钮。
- [x] AC-002 点击复制按钮且 Clipboard API 可用时，完整 `request_id` 写入剪贴板。
- [x] AC-003 复制成功后展示固定位置成功反馈，不造成表格、分页或页面内容纵向位移。
- [x] AC-004 当 Clipboard API 不存在时，页面不抛出运行时错误，并给出手动复制指引或等价兜底。
- [x] AC-005 当 `writeText` 被浏览器拒绝或返回失败时，页面不抛出未捕获错误，并给出手动复制指引或等价兜底。
- [x] AC-006 无 `request_id` 的日志记录不展示复制按钮；若通过函数防御触发空值复制，提示“当前日志没有 request_id”或等价文案。
- [x] AC-007 复制成功时可上报 `copy_request_id` 使用行为事件；复制失败或兜底路径不得误报成功复制。
- [x] AC-008 修复后日志审计页既有筛选、分页、详情抽屉和日志列表渲染测试保持通过。

## 测试建议

- [x] 新增或更新 `LogAuditPage.test.tsx` 成功复制用例，断言 `writeText` 使用完整 `request_id`。
- [x] 新增 Clipboard API 不存在的失败兜底用例。
- [x] 新增 `writeText` reject 的失败兜底用例。
- [x] 保留既有成功路径的 `copy_request_id` 埋点断言。

## 验证记录

| 时间 | 项目 | 结果 |
|---|---|---|
| 2026-07-09 08:37:20 | `pnpm --dir src/web test src/pages/admin/LogAuditPage.test.tsx` | 通过，8 tests passed |
| 2026-07-09 08:37:20 | `openspec validate fix-audit-log-request-id-copy-error --strict` | 通过 |

## 非范围

- 不修改日志审计 API 契约。
- 不修改 `request_logs`、`usage_events`、`audit_logs` 表结构。
- 不改变日志审计页权限边界。
- 不新增对象存储、媒体或小程序能力。
