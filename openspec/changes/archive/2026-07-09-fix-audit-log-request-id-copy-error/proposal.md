---
created_at: 2026-07-09 08:18:00
updated_at: 2026-07-09 08:18:00
---

# Change: fix-audit-log-request-id-copy-error

## Why

BUG-0060 暴露出管理端日志审计页的 `request_id` 复制交互不够健壮：页面直接调用 Clipboard API 成功路径，缺少浏览器不支持、权限拒绝或写入失败时的兜底反馈，导致管理员无法稳定复制请求编号用于排障。

该能力来自 `REQ-0024-product-usage-logging`，原始验收要求 `request_id` 可复制，且反馈不造成布局位移。当前缺陷不阻断日志列表查询和详情查看，但会降低通过 `request_id` 串联前端反馈、接口响应和后端日志的效率。

## What Changes

- 修复日志审计页 `request_id` 复制交互，确保 Clipboard API 可用时写入完整 `request_id`。
- 增加 Clipboard API 不可用、浏览器拒绝写入或写入失败时的手动复制兜底。
- 保持复制成功、失败和兜底反馈使用 fixed toast 或等价固定层，不造成页面布局位移。
- 补充前端回归测试，覆盖成功复制、Clipboard API 不存在、`writeText` reject、空 `request_id` 防御和埋点行为。
- 不修改日志审计 API、数据库表结构、权限边界、OpenAPI/Orval 生成物。

## Impact

- 影响 Web 管理端日志审计页复制交互。
- 影响前端测试：`LogAuditPage.test.tsx` 或等价日志审计页测试需要新增失败兜底覆盖。
- 不影响后端 API 请求、响应、错误码。
- 不影响 SQLite/MySQL schema、迁移或数据模型。
- 不影响小程序、MinIO、媒体上传。
- 不需要执行 Orval。

## Rollback Plan

如实现后复制交互或 toast 行为出现回归，可回滚日志审计页复制函数和对应测试变更，恢复为原先仅提示复制失败的行为。

回滚后必须在 BUG-0060 trace 中记录风险仍存在，并保留临时规避：通过日志详情抽屉查看完整 `request_id` 后手动复制。
