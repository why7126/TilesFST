---
note: workflow-sync — 2/12 Change 已 archive；9 applied；待人工 sign-off
title: sprint-026 验收报告
acceptance_status: pending
created_at: 2026-08-25 15:21:18
updated_at: 2026-08-26 21:03:51
---

# sprint-026 验收报告

## 验收范围

| 类型 | 编号 | 标题 | 验收状态 | 说明 |
|---|---|---|---|---|
| BUG | BUG-0141-ai-usage-token-count-jsonl | AI usage extractor 未识别新版 token_count JSONL 导致 Sprint snapshot 缺失 | applied，待归档（`fix-ai-usage-message-content-token-count` 14/14） | Change 已 apply，待 archive |
| BUG | BUG-0140-admin-current-user-avatar-missing-object | 当前登录用户头像引用缺失媒体对象 | done，已归档（`fix-admin-current-user-avatar-object-consistency` archived 2026-08-25 15:44:17） | Change 已 apply，待 archive |
| BUG | BUG-0139-admin-avatar-upload-nginx-redirect-cors | 管理后台头像上传被 Nginx 301 重定向丢端口导致 CORS 拦截 | done，已归档（`fix-admin-avatar-upload-nginx-redirect-cors` archived 2026-08-25 15:35:15） | 待创建修复 Change |
| REQ | REQ-0123-upload-stage-trace-spans | 上传链路阶段级耗时写入 trace spans | applied，待归档（`add-upload-stage-trace-spans` 14/14） | 待 `/req-opsx` 创建 OpenSpec Change |
| REQ | REQ-0124-log-audit-behavior-trace-model | 日志审计补齐行为链路与任务链路采集模型 | applied，待归档（`add-log-audit-behavior-trace-model` 28/28） | 后端、DB、Web、API 文档、Orval 与聚焦测试已完成 |
| REQ | REQ-0126-product-data-collection-observability-standard | 建立通用产品数据采集与链路观测规范 | applied，待归档（`add-product-data-collection-observability-standard` 15/15） | 待 `/req-opsx` 创建 OpenSpec Change |

## 验收门禁

- 新版 `payload.type=message`、`payload.role=user`、`payload.content` 文本片段列表可建立 command run。
- `payload.type=token_count` 且 token 用量位于 `payload.info.last_token_usage` 时，可归属到对应 command run。
- `sprint-025` snapshot 不再因 `required-metrics-empty` 失败。
- 脱敏与隐私边界通过：不持久化 prompt 原文、系统/开发者指令、工具输出正文、本机绝对路径、Authorization header、Cookie、`.env` 内容或密钥。
- BUG-0140 按媒体四联验收：头像 `object_key` 可追溯、对象存在、`/media/{object_key}` 可读、管理端头像 render/fallback 正常。
- BUG-0139 按 Docker Web 上传边界验收：`POST /api/v1/admin/uploads` 不再 301，端口不丢失，CORS 不再拦截，头像上传状态机与即时回显正常。
- REQ-0123 按上传 trace spans 验收：`file_read`、`original_put_object`、`thumbnail_generate`、`thumbnail_put_object`、`display_generate`、`display_put_object` 六阶段可追踪，日志不作为唯一事实源。
- REQ-0124 按链路采集模型验收：界面触发入口可从 `behavior_trace_id` 联动行为、请求、任务和流程节点；直接 API 调用在行为链路为空时仍可从 `request_id` 追踪任务链路；日志审计页按 `behavior_trace_id`、`request_id`、`task_trace_id` 查询并保持 admin-list 横切验收。
- REQ-0126 按通用采集与链路观测规范验收：覆盖小程序、店主端、App、Web 管理端和后端 API，明确业务行为事件、所有业务 API 请求日志、四层链路模型、直接 API 入口、标准数据结构、Task Trace 分级覆盖、默认保留周期、禁止采集字段和新产品接入 checklist。

## 验收结果

```yaml
acceptance_status: pending
accepted_at: null
accepted_by: null
evidence: []
failed_items: []
notes: 待 BUG-0141 archive，并待 REQ-0123、REQ-0124、REQ-0126、BUG-0140、BUG-0139 对应 Change apply/archive 后回填。
```

## REQ-0124 实现验证证据

- `uv run pytest src/backend/tests/test_product_usage_logging.py tests/test_mysql_schema_drift.py tests/test_mysql_migrations.py`：32 passed，覆盖行为链路字段、直接 API 空链路、任务 parent_request_id / spans、脱敏和 SQLite/MySQL 迁移。
- `corepack pnpm test -- LogAuditPage usage-tracking auth-api`：62 test files / 364 tests passed，覆盖前端透传、日志审计筛选、详情展示、复制 fixed toast 和 admin-list 结构。
- `bash scripts/generate-openapi-client.sh`：OpenAPI / Orval 已同步新增字段与查询参数。
