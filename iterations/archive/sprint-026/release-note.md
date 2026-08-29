---
title: sprint-026 发布说明
created_at: 2026-08-25 15:21:18
updated_at: 2026-08-28 16:15:59
publish_status: published
---

# sprint-026 发布说明

## 发布范围

| 类型 | 编号 | 标题 | 状态 | 说明 |
|---|---|---|---|---|
| BUG | BUG-0141-ai-usage-token-count-jsonl | AI usage extractor 未识别新版 token_count JSONL 导致 Sprint snapshot 缺失 | done | Change 已归档，AI usage snapshot actual 恢复 |
| BUG | BUG-0140-admin-current-user-avatar-missing-object | 当前登录用户头像引用缺失媒体对象 | done | Change 已归档，媒体四联验收通过 |
| BUG | BUG-0139-admin-avatar-upload-nginx-redirect-cors | 管理后台头像上传被 Nginx 301 重定向丢端口导致 CORS 拦截 | done | 修复 Change 已归档 |
| REQ | REQ-0123-upload-stage-trace-spans | 上传链路阶段级耗时写入 trace spans | done | OpenSpec Change 已归档 |
| REQ | REQ-0124-log-audit-behavior-trace-model | 日志审计补齐行为链路与任务链路采集模型 | done | Change 已归档 |
| REQ | REQ-0126-product-data-collection-observability-standard | 建立通用产品数据采集与链路观测规范 | done | OpenSpec Change 已归档 |
| REQ | REQ-0129-miniapp-sku-detail-actionbar-compact-favorite | 小程序商品详情页底部收藏按钮与操作栏紧凑化 | done | OpenSpec Change 已归档 |

## 预期发布影响

- 修复研发治理链路中 AI usage extractor 对新版 Codex session JSONL 的兼容性。
- 恢复 `sprint-025` 等 Sprint AI usage snapshot 的真实 token 统计能力。
- 保持原始 session JSONL 本机私有，不进入仓库或发布材料。
- 修复管理后台当前登录用户头像引用缺失对象导致的头像展示 404。
- 修复管理后台头像上传无尾斜杠路径经 Nginx 301 重定向丢失端口导致的 CORS 拦截。
- 增强头像上传和通用图片上传的阶段级可观测性，后续实现需将关键阶段耗时写入 task trace spans。
- 增强日志审计的数据采集与链路观测能力，支持从用户行为追踪到接口请求、任务链路和流程节点，并兼容直接 API 调用。
- 建立通用产品数据采集与链路观测规范，沉淀跨端行为事件、API 请求日志、Task Trace 分级覆盖、保留周期和脱敏边界。
- 优化小程序商品详情页底部操作栏，收藏按钮去掉可见第二行文字，压缩底部固定区域，并同步调整返回首页悬浮按钮 offset。

## 非发布范围

- BUG-0140 和 BUG-0139 不新增业务 API；如实现阶段改变接口响应、错误码或 Schema，必须同步 OpenAPI / Orval / API 文档。
- REQ-0123 默认不新增管理端可见 UI；若后续将 trace spans 暴露到上传响应、任务查询或管理端页面，必须同步 API / Orval / UI 验收。
- REQ-0124 不接入外部 APM、OpenTelemetry、第三方埋点平台、复杂 BI、实时大屏或告警推送。
- REQ-0124 不强制历史日志批量回填；历史日志以空行为链路兼容展示。
- REQ-0126 不直接改造所有历史产品，不接入外部 APM / OpenTelemetry，不建设第三方埋点平台、实时告警、BI 大屏、复杂用户画像或历史数据强制回填。
- REQ-0129 不改变收藏接口、收藏数据模型、分享能力、商品详情主体信息架构或行为埋点。
- 不修改数据库结构；如涉及历史头像 key 数据修复，必须记录 dry-run/apply/幂等摘要。
- 不影响小程序；管理端头像展示与上传链路需按媒体四联验收。
- 不提交原始 `~/.codex/sessions` JSONL。

## 发布门禁

- BUG-0141 对应 Change 完成 apply 与 archive。
- REQ-0123 对应 Change 完成 propose/apply/archive，并验证六阶段 task trace spans。
- REQ-0124 对应 Change 完成 propose/apply/archive，并验证界面触发一行为多请求、直接 API 调用、任务链路关联、三类链路 ID 查询、敏感字段脱敏和旧日志兼容。
- REQ-0126 对应 Change 完成 propose/apply/archive，并验证规范覆盖端、四层模型、直接 API、Task Trace 分级覆盖、默认保留周期、禁止采集字段和新产品接入 checklist。
- REQ-0129 对应 Change 完成 propose/apply/archive，并验证收藏按钮无可见第二行文字、底部操作栏高度压缩、返回首页悬浮按钮 actionbar offset、安全区和 320/375/430pt 视觉证据。
- BUG-0140 与 BUG-0139 对应 Change 完成 apply 与 archive。
- `tests/test_ai_usage.py` 新版 JSONL fixture 回归通过。
- `sprint-025` snapshot 可恢复为 `present` / `actual`，且 token totals 非零。
- BUG-0140 验证头像 key/object/URL/render 四联与缺失对象 fallback。
- BUG-0139 验证 Docker Web `http://localhost:3000` 下 `POST /api/v1/admin/uploads` 不再 301 丢端口，头像上传即时回显。
- REQ-0123 验证 `file_read`、`original_put_object`、`thumbnail_generate`、`thumbnail_put_object`、`display_generate`、`display_put_object` 写入结构化 trace spans，且失败阶段保留脱敏证据。
- REQ-0124 验证 `usage_events.behavior_trace_id`、`request_logs.behavior_trace_id`、`task_traces.parent_request_id` 与 `task_trace_spans` 可联动，并同步 DB / API / Orval / 管理端日志审计页验收。

## REQ-0124 发布验证摘要

- 已落地界面行为入口：`usage_events.behavior_trace_id -> request_logs.behavior_trace_id -> task_traces.parent_request_id -> task_trace_spans`。
- 已保留直接 API 入口：`request_logs.request_id -> task_traces.parent_request_id -> task_trace_spans`，`behavior_trace_id` 可为空。
- 已同步 `docs/03-api-index.md`、`docs/04-database-design.md`、OpenAPI / Orval，并通过后端与前端聚焦测试。
