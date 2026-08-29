---
created_at: 2026-08-27 00:00:00
updated_at: 2026-08-27 00:49:46
---

# 任务

- [x] 复核 `LogAuditPage.tsx` 中 `DetailSection` 与 `SnapshotRows` 的字段行结构，确认基础信息、请求信息和 Request Snapshot 共用或等价使用安全布局。
- [x] 调整 `log-audit.css` 中 `.detail-row`、Snapshot 行和 `.field-help-label` 的布局策略，使长字段名和值不重叠。
- [x] 保留字段说明图标 hover/focus tooltip、可访问名称和键盘聚焦能力。
- [x] 补充前端测试或组件级断言，覆盖 `parent_behavior_event_id`、`client_request_id`、`behavior_trace_id`、`task_trace_id` 同时展示的日志详情。
- [x] 补充桌面视口截图或 Playwright 视觉证据，证明 `parent_behavior_event_id` 不再和值重叠。
- [x] 补充窄宽度或移动端视口截图/测试，证明详情抽屉可滚动、无横向失控、字段名和值不遮挡。
- [x] 运行前端聚焦测试、Design System 校验和 OpenSpec 校验。
- [x] 回填 BUG-0145 验收结果，记录截图、测试和 N/A 边界。
- [x] 评估是否需要沉淀 `docs/knowledge-base/incidents/`；若无跨页面复用价值，记录 N/A 原因。

## 执行备注

- 前端聚焦测试：`pnpm --dir src/web --pm-on-fail=warn exec vitest run src/pages/admin/LogAuditPage.test.tsx`，17 个用例通过。
- 视觉证据：`implementation/evidence/log-detail-field-overlap-desktop.png`、`implementation/evidence/log-detail-field-overlap-narrow.png`。
- Design System：已运行 `python scripts/validate-design-system.py`；当前项目存在既有 baseline 违规，本次变更未新增裸 Hex，聚焦检查未发现新增 token 违规。
- OpenSpec：`openspec validate fix-admin-log-detail-field-overlap --strict` 通过。
- 事故知识库：N/A。该问题为单页日志详情布局约束缺失，已通过 Change trace 和测试固化，无需沉淀跨页面 incident。
