---
note: workflow-sync — 6/6 Change 已 archive；0 applied；待人工 sign-off
sprint_id: sprint-012
title: Sprint 012 Acceptance Report
status: completed
created_at: 2026-07-26 15:15:24
updated_at: 2026-07-26 17:38:21
---

# Sprint 012 Acceptance Report

## 验收范围

| 类型 | ID | Change | 状态 |
|---|---|---|---|
| REQ | REQ-0071-request-snapshot-logging | update-request-snapshot-logging | archived |
| REQ | REQ-0072-client-request-identity-standard | standardize-client-request-identity | archived |
| REQ | REQ-0073-task-trace-parent-request-model | fix-task-trace-parent-request-model | archived |
| REQ | REQ-0074-task-trace-coverage-expansion | update-task-trace-coverage-expansion | archived |
| REQ | REQ-0075-audit-log-task-trace-linking | link-audit-logs-to-task-trace | archived |
| REQ | REQ-0076-observability-dashboard | add-observability-dashboard | archived |

## 验收清单

| AC | 验收项 | 验收标准 | 证据 |
|---|---|---|---|
| AC-001 | Snapshot 生成 | 每个可采集 API 请求均生成统一 Request Snapshot，并关联对应请求日志记录 | 待实现与测试 |
| AC-002 | Snapshot 字段完整 | Snapshot 至少包含 method、path、route template、query 白名单摘要、body schema 摘要、业务资源标识、status code、error code、duration、操作者、客户端、环境、请求开始时间和响应结束时间 | 待实现与测试 |
| AC-003 | 跨端兼容 | 后台管理端、店主 Web 展示端和微信小程序请求使用兼容 Snapshot 字段结构，无法提供字段以空值或 `未采集` 表达 | 待实现与测试 |
| AC-004 | route template 降级 | route template 能稳定表达 FastAPI 路由模板；无法识别时有明确降级值，不把带查询串的 path 当作唯一上下文 | 待实现与测试 |
| AC-005 | query 白名单 | query 参数只按白名单采集；未列入白名单的字段默认忽略或只记录字段名 | 待实现与测试 |
| AC-006 | body 摘要 | body 只保存 schema 摘要、字段类型、字段数量、长度、业务安全字段或脱敏结果，不保存原始敏感 body | 待实现与测试 |
| AC-007 | 敏感字段不落库 | Authorization、Cookie、密码、Token、真实密钥、数据库 DSN、MinIO AccessKey/SecretKey、内部路径、原始文件名不得进入 Snapshot | 待实现与测试 |
| AC-008 | 敏感接口白名单 | 上传、登录、认证、系统设置等敏感接口采用更严格字段白名单，并有测试证明敏感字段未落库 | 待实现与测试 |
| AC-009 | 错误请求上下文 | 错误请求能在 Snapshot 中关联 status code、业务 error code、duration、route template、client type、actor 和错误摘要 | 待实现与测试 |
| AC-010 | 慢请求识别 | 慢请求可通过 `duration_ms` 被识别，并与现有日志审计策略保持一致 | 待实现与测试 |
| AC-011 | 日志详情展示 | 管理端日志详情展示 Request Snapshot 分组：请求信息、输入摘要、业务资源、响应结果、操作者 / 客户端、环境与时间 | 待实现与测试 |
| AC-012 | 空态与解析失败 | Snapshot 缺少字段、metadata 为空或 JSON 解析失败时，日志列表和详情页仍可展示基础字段，不出现页面崩溃 | 待实现与测试 |
| AC-013 | 权限边界 | 日志详情访问继续受系统管理员或等价权限控制，未授权角色访问返回 403 或管理端无权限页 | 待实现与测试 |
| AC-014 | 性能边界 | Snapshot 扩展后，日志列表分页和详情查询在 demo 数据量下无明显性能退化；生产实现说明索引或 JSON 字段查询策略 | 待实现与测试 |
| AC-015 | 契约同步 | SQLite demo schema、MySQL schema、Pydantic Schema、API 响应、OpenAPI / Orval、接口文档和测试在实现阶段保持同步 | 待实现与测试 |
| AC-016 | 三端客户端类型 | Web 管理端、店主 Web 前台和微信小程序普通 API 请求分别稳定记录为 `web_admin`、`web_catalog`、`wechat_miniapp` | `src/backend/tests/test_product_usage_logging.py`、`src/web/src/features/auth/api/auth-api.test.ts`、`tests/test_miniapp_static.py` 通过 |
| AC-017 | 可信 request_id | 后端每次请求继续生成可信 `request_id`，响应头返回 `x-request-id`，错误响应、异常日志和请求日志保持一致 | `test_request_logging_records_admin_api_request` 覆盖客户端 `x-request-id` 不覆盖可信 ID |
| AC-018 | 客户端请求标识边界 | 客户端请求标识保存为独立 `client_request_id` 或 metadata 字段，不得覆盖后端可信 `request_id` | request_logs schema/repository/schema docs 与 `test_request_logging_records_admin_api_request` 覆盖 |
| AC-019 | 非法客户端标识降级 | 客户端请求标识缺失、非法或超长时不得导致 500，不污染 JSON metadata，也不得放宽权限边界 | `test_request_logging_client_request_id_degrades_safely` 通过 |
| AC-020 | 小程序 fallback 策略 | 小程序 fallback base URL 重试时客户端请求标识复用或重建规则已文档化，并具备对应验收用例 | `src/miniapp/services/api.ts` / `.js` 在 `request()` 内生成一次 `clientRequestId`，`tests/test_miniapp_static.py` 覆盖 |
| AC-021 | 日志审计请求身份展示 | 日志审计列表或详情展示客户端类型、后端可信 `request_id` 与客户端请求标识，并能从字段名或文案区分两类 ID | `src/web/src/pages/admin/LogAuditPage.test.tsx` 覆盖列表列、详情 Snapshot 字段和响应头语义 |
| AC-022 | 长 ID 复制与布局 | 请求标识长字段单行截断、完整复制、fixed toast 反馈，不引起筛选区、表格或详情布局位移 | `LogAuditPage.test.tsx` 覆盖 `request_id`、`client_request_id`、`task_trace_id` 复制与 fixed toast |
| AC-023 | admin-list 横切回归 | 日志审计变更后保留分页 DOM、指标卡 DOM、fixed toast、无 `window.confirm`，移动端筛选和表格不溢出 | `LogAuditPage.test.tsx` 保留分页 DOM、指标卡 DOM、fixed toast、无原生确认框 |
| AC-024 | 任务型接口清单 | 首批接入清单至少评估保存 SKU、批量操作、导入导出、媒体处理、异步任务和复杂查询六类场景，并记录优先级、任务类型、关键步骤、预期 span 和未纳入原因 | 待实现 |
| AC-025 | 任务上下文与 span | 首批任务型接口生成或透传同一个 `task_trace_id`，关键步骤写入可排序 span，失败、超时和部分成功能定位到失败节点 | 待实现 |
| AC-026 | 管理端复杂任务反馈 | 管理端复杂任务在成功、失败、处理中或部分成功状态展示或支持复制 `task_trace_id`；无 trace 时保持旧交互，不显示空错误态 | 待实现与前端测试 |
| AC-027 | 任务型接口契约与安全同步 | 若新增响应字段或存储字段，OpenAPI、Orval、SQLite/MySQL schema、DB/API 文档和测试同步；metadata 脱敏且不保存完整敏感请求体 | 待实现 |
| AC-028 | 审计写入任务字段 | `AuditLogRepository.insert()` 或等价入口支持可选 `task_trace_id` 与 `task_type`，任务型审计操作写入字段，无任务上下文保持兼容 | 待实现 |
| AC-029 | 敏感审计写入点清单 | 系统设置、品牌证书、媒体/上传、SKU、Banner 等审计写入点完成接入评估，任务型操作复用当前 Task Trace | 待实现与设计/任务清单确认 |
| AC-030 | audit 类型日志详情联动 | audit 类型日志存在 `task_trace_id` 时，日志审计详情展示 Task Trace 分组或等价入口；无任务字段时不报错 | 待实现与前端测试 |
| AC-031 | 审计任务字段安全与 schema | audit log metadata 脱敏，任务字段不参与权限判断；SQLite/MySQL `audit_logs.task_trace_id` 与 `task_type` 字段、索引和迁移路径一致 | 待实现与 schema drift / 安全测试 |
| AC-032 | Task Trace 主请求关联 | 每个由 API 请求触发的 Task Trace 记录触发主请求 `request_id`，字段语义为 `parent_request_id`，且来自后端请求上下文 | 待实现 |
| AC-033 | span 请求关联 | 有请求上下文的 task span 写入当前 `request_id`；无直接请求上下文的内部节点保留安全兜底，不展示误导性跳转 | 待实现 |
| AC-034 | 双向定位 | 日志详情可从主请求 `request_id` 展示关联 Task Trace，也可从 Task Trace span 的 `request_id` 定位到对应请求日志 | 待实现 |
| AC-035 | REQ-0073 契约同步 | 若新增 `parent_request_id`、span `request_id` 或任务摘要字段，OpenAPI、Orval、DB 文档、API 文档和测试同步 | 待实现 |
| AC-036 | 链路观测入口与权限 | 管理端提供日志审计与链路观测入口，仅系统管理员或具备日志审计权限的角色可访问 | 待实现 |
| AC-037 | 统一摘要与统计口径 | 页面展示请求日志、行为事件、审计操作和 Task Trace 统一摘要；摘要、分布、排行和明细入口与当前筛选条件保持同一统计口径 | 待实现 |

## 测试计划

```bash
uv run pytest src/backend/tests/test_product_usage_logging.py
pnpm --dir src/web exec vitest run src/pages/admin/LogAuditPage.test.tsx
openspec validate update-request-snapshot-logging --strict
openspec validate standardize-client-request-identity --strict
```

若实现阶段修改数据库 schema 或 MySQL migration，还需补充并运行：

```bash
uv run pytest tests/test_mysql_migrations.py tests/test_mysql_schema_drift.py
```

若实现阶段更新 OpenAPI / Orval，还需运行：

```bash
bash scripts/generate-openapi-client.sh
```

REQ-0072 实现时还需补充并运行：

```bash
uv run pytest src/backend/tests/test_product_usage_logging.py tests/test_mysql_migrations.py tests/test_mysql_schema_drift.py
pnpm --dir src/web exec vitest run src/pages/admin/LogAuditPage.test.tsx
uv run pytest tests/test_miniapp_static.py
```

REQ-0074 实现时还需补充并运行：

```bash
uv run pytest src/backend/tests/test_product_usage_logging.py
pnpm --dir src/web exec vitest run src/pages/admin/LogAuditPage.test.tsx
bash scripts/generate-openapi-client.sh
openspec validate update-task-trace-coverage-expansion --strict
```

REQ-0075 实现时还需补充并运行：

```bash
uv run pytest src/backend/tests/test_product_usage_logging.py tests/test_mysql_migrations.py tests/test_mysql_schema_drift.py
pnpm --dir src/web exec vitest run src/web/src/pages/admin/LogAuditPage.test.tsx
bash scripts/generate-openapi-client.sh
openspec validate link-audit-logs-to-task-trace --strict
```

REQ-0073 实现时还需补充并运行：

```bash
uv run pytest src/backend/tests/test_product_usage_logging.py tests/test_media_storage.py
pnpm --dir src/web exec vitest run src/web/src/pages/admin/LogAuditPage.test.tsx
bash scripts/generate-openapi-client.sh
openspec validate fix-task-trace-parent-request-model --strict
```

## 已执行验证

| 时间 | 命令 | 结果 |
|---|---|---|
| 2026-07-26 15:15:24 | /sprint-propose | Sprint 012 创建，REQ-0071 纳入 planning |
| 2026-07-26 15:17:24 | /sprint-propose | REQ-0072 纳入 Sprint 012 planning |
| 2026-07-26 15:34:18 | /sprint-propose | REQ-0074 改纳入 Sprint 012 planning |
| 2026-07-26 15:40:00 | /sprint-propose | REQ-0075 改纳入 Sprint 012 planning |
| 2026-07-26 15:45:00 | /sprint-propose | REQ-0073 改纳入 Sprint 012 planning |
| 2026-07-26 15:48:23 | `uv run pytest src/backend/tests/test_product_usage_logging.py tests/test_mysql_migrations.py tests/test_mysql_schema_drift.py tests/test_miniapp_static.py` | 52 passed, 41 warnings |
| 2026-07-26 15:48:23 | `pnpm --dir src/web exec vitest run src/features/auth/api/auth-api.test.ts src/pages/admin/LogAuditPage.test.tsx` | 2 files passed, 17 tests passed |
| 2026-07-26 15:48:23 | `openspec validate standardize-client-request-identity --strict` | passed |
| 2026-07-26 15:48:23 | `python scripts/validate-directory-structure.py` | passed |

## 当前结论

Sprint 012 范围内 6 个 Change 均已归档，关联 6 个 REQ 均已进入 archive 阶段。`python scripts/validate-sprint-archive-readiness.py --sprint sprint-012` 结果 PASS；AI usage post-command hook 已刷新 `data/ai-usage/sprints/sprint-012.json`，模式为 `actual`，`command_run_count=1`，`warning_count=0`。
