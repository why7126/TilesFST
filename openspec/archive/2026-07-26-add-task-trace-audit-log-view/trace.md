---
change_id: add-task-trace-audit-log-view
status: applied
change_type: add
created_at: 2026-07-25 12:02:45
updated_at: 2026-07-25 14:48:48
source_requirement: REQ-0069-upload-observability-trace-logs
iteration: sprint-011
related_bugs:
  - BUG-0085-admin-video-upload-stuck-at-99
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/best-practices/admin-media-upload-chain.md
  - docs/knowledge-base/retrospectives/sprint-010-retrospective.md
---

# Change Trace

```yaml
change_id: add-task-trace-audit-log-view
status: applied
change_type: add
created_at: 2026-07-25 12:02:45
updated_at: 2026-07-25 14:48:48
source_requirement: REQ-0069-upload-observability-trace-logs
iteration: sprint-011
related_bugs:
  - BUG-0085-admin-video-upload-stuck-at-99
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/best-practices/admin-media-upload-chain.md
  - docs/knowledge-base/retrospectives/sprint-010-retrospective.md
```

## Readiness

| 项 | 状态 | 说明 |
|---|---|---|
| proposal.md | done | 已生成 |
| design.md | done | 已生成 |
| specs | done | 修改 `product-usage-logging`、`object-storage` |
| tasks.md | done | 已生成 |
| source REQ | approved | `issues/requirements/archive/REQ-0069-upload-observability-trace-logs/` |
| sprint scope | done | 已纳入并归档至 `iterations/archive/sprint-011/` |

## Prototype Checklist

| 原型 | 状态 | 说明 |
|---|---|---|
| HTML | present | `issues/requirements/archive/REQ-0069-upload-observability-trace-logs/prototype/web/task-trace-log-detail.html` |
| context | present | `issues/requirements/archive/REQ-0069-upload-observability-trace-logs/prototype/web/task-trace-log-detail-context.md` |
| PNG | N/A | 已在验收记录写明：本 Change 以 HTML prototype、自动化测试、API evidence 与 Docker smoke 作为验收依据，不额外导出 PNG |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-25 13:21:43 | /sprint-propose | 纳入 `sprint-011`，补充 Sprint 容量、发布、验收与追踪范围。 |
| 2026-07-25 12:02:45 | /req-opsx | 从 REQ-0069 创建 OpenSpec Change，生成 proposal、design、delta specs、tasks 和 trace。 |

## 实现摘要

| 范围 | 结果 |
|---|---|
| 后端 Task Trace | 新增 `TaskTraceRepository` / `TaskTraceService`，落地 `task_traces`、`task_trace_spans`，并把 `task_trace_id` / `task_type` 串到 `request_logs`、`usage_events`、`audit_logs` |
| 上传链路 | 图片、视频、证书/文件上传生成 `task_trace_id`，记录 `frontend_upload_start`、`frontend_upload_body_done`、`api_receive`、`validate_file`、`storage_put_object`、`db_create_media`、`post_process`、`api_response`、`frontend_done/frontend_failed` |
| 审计日志 API | `GET /api/v1/admin/logs` 支持 `task_trace_id` 精确筛选，路径/request_id 组合筛选兼容 task_trace_id；详情返回 `task_trace` 时间线 |
| 管理端 UI | 日志审计页新增 Task Trace 筛选、列表摘要列、详情抽屉时间线与复制反馈，复用 fixed toast，保持无 Trace 日志兼容 |
| API / DB / 文档 | OpenAPI / Orval generated 已同步；`docs/03-api-index.md`、`docs/04-database-design.md`、`docs/standards/file-upload.md` 已同步 |
| 安全 | `task_trace_id` 不含原始文件名、手机号、密钥或可枚举自增序列；metadata 屏蔽 Authorization、Cookie、AccessKey、SecretKey、DSN、`.env`、内部绝对路径等敏感信息 |

## 横切引用

| 标签 | 证据 |
|---|---|
| admin-list | 日志审计页保留分页、指标卡、fixed toast、无 `window.confirm`；筛选区增加 `task_trace_id` 后仍使用响应式 grid 与横向滚动表格 |
| media-upload | 上传仍走后端鉴权和对象存储适配层；Docker Web 入口经 `http://127.0.0.1:3000` 验证小文件成功、超限文件统一 `50003`，并能通过审计日志回查 99% 后端保存节点 |

## 验证摘要

| 命令 / 场景 | 结果 |
|---|---|
| `python -m py_compile ...` | 后端修改文件与测试文件语法检查通过 |
| `uv run pytest src/backend/tests/test_product_usage_logging.py src/backend/tests/test_admin_brands.py` | 35 passed, 107 warnings |
| `uv run ruff check src/backend/app/repositories/task_trace_repository.py src/backend/app/services/task_trace_service.py src/backend/app/repositories/log_repository.py src/backend/app/services/log_service.py src/backend/app/api/v1/uploads.py src/backend/app/core/request_logging.py src/backend/app/schemas/logs.py src/backend/app/schemas/media.py src/backend/app/db/migrations.py src/backend/app/db/mysql_migrations.py` | passed |
| `pnpm --dir src/web exec vitest run src/pages/admin/LogAuditPage.test.tsx` | 12 passed |
| `bash scripts/generate-openapi-client.sh` | passed；`src/web/openapi.json` 与 `src/web/src/shared/api/generated.ts` 已更新 |
| `openspec validate add-task-trace-audit-log-view --strict` | passed |
| `docker compose --profile self-hosted-storage up -d --build` | backend / web / minio / minio-init 启动成功；期间发现并修复 SQLite 旧库新增索引先于迁移执行的问题 |
| Docker Web 上传 smoke `http://127.0.0.1:3000` | 小图上传 200、媒体读取 200、审计日志按 `task_trace_id` 回查 1 条、9 个上传节点完整；51MB 图片在当前 `MAX_IMAGE_SIZE_MB=50` 下返回 `400 / 50003` |
| `pnpm --dir src/web exec tsc --noEmit --ignoreDeprecations 6.0` | failed；剩余为既有项目级 Tailwind/Node/CSS 声明及其他测试 fixture 类型问题，非本 Change 新增阻塞 |
| `python scripts/validate-directory-structure.py` | passed；已清理本次 Ruff 校验生成的根目录临时缓存 `.ruff_cache` |

## N/A / Follow-up

| 项 | 结论 |
|---|---|
| PNG Golden Reference | N/A。本 Change 已有 HTML prototype、自动化测试、API evidence 与 Docker smoke；本次不再额外导出 PNG 作为实现阻塞 |
| 新增事故 / best-practice 文档 | N/A。`docs/standards/file-upload.md` 已补 99% / 504 Task Trace 诊断，`docs/knowledge-base/best-practices/admin-media-upload-chain.md` 已覆盖上传链路预防 |
