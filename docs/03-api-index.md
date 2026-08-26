---
purpose: 接口文档
content: API 索引、认证接口、错误码与 Orval 维护规则
source: Sprint 001 实现 / OpenSpec auth & api-governance
update_method: API 新增或变更时同步更新；变更后运行 Orval
created_at: 2026-06-13 00:00:00
updated_at: 2026-08-25 23:20:00
note: 错误码运行时值见 `src/backend/app/core/exceptions.py`；登记表见 `docs/standards/error-codes.md`
---

# API 接口索引

## 1. 通用约定

### 1.1 基础路径

```text
/api/v1
```

### 1.2 统一响应结构（认证等已实现 envelope 的接口）

成功：

```json
{
  "code": 0,
  "message": "success",
  "data": { }
}
```

错误：

```json
{
  "code": 40101,
  "message": "账号或密码错误",
  "data": null
}
```

管理端表单 API 的框架请求校验失败默认返回 HTTP 422，响应体仍使用统一 envelope：

```json
{
  "code": 40001,
  "message": "请求参数无效",
  "data": {
    "errors": [
      {
        "field": "username",
        "message": "Field required",
        "type": "missing",
        "location": ["body", "username"]
      }
    ]
  }
}
```

`data.errors[]` 用于 Web 管理端字段错误映射；无法映射时降级为全局 toast、弹窗固定错误区或上传控件错误态。响应不得只返回 FastAPI / Pydantic 默认 `detail`。

### 1.3 认证头

需登录接口：

```http
Authorization: Bearer <access_token>
```

### 1.4 OpenAPI 与前端客户端

| 资源 | 路径 |
|---|---|
| OpenAPI JSON | `/openapi.json` |
| Swagger UI | `/docs` |
| 健康检查 | `GET /health`（无 `/api/v1` 前缀） |

前端类型与客户端：

```bash
./scripts/generate-openapi-client.sh
```

配置：`src/web/orval.config.ts` → 输出 `src/web/src/shared/api/generated.ts`

---

## 2. API 分组

| 分组 | 路径前缀 | 认证 | 说明 | Sprint 001 状态 |
|---|---|---|---|---|
| 认证 | `/api/v1/auth` | 部分 | 登录、当前用户、退出 | ✓ 已实现 |
| 个人资料 | `/api/v1/profile` | 是（admin/employee） | 当前用户资料 self-service、操作记录 | ✓ Sprint 003 |
| 管理端个人设置 | `/api/v1/admin/profile` | 是（admin/employee） | 自助修改密码 | ✓ Sprint 003 |
| 微信小程序 | `/api/v1/miniapp` | 否 | 首页聚合、公开分类树、公开商品搜索、公开证书聚合列表、搜索联想/完整搜索、公开商品/SKU 详情 | ✓ Sprint 008/009 |
| 瓷砖（展示） | `/api/v1/tiles` | 否 | 列表、详情 | 桩实现（返回空/示例） |
| 管理端瓷砖 | `/api/v1/admin/tiles` | 是（admin/employee） | 创建瓷砖 | 桩实现 |
| 管理端用户 | `/api/v1/admin/users` | 是（仅 admin） | 用户 CRUD、状态、重置密码 | ✓ Sprint 002 |
| 管理端系统设置 | `/api/v1/admin/system-settings` | 是（仅 admin） | 分组配置 GET/PATCH/reset、审计 recent | ✓ Sprint 003 |
| 管理端接口文档 | `/api/v1/admin/api-docs` | 是（仅 admin） | 运行时接口目录、OpenAPI/Swagger/Orval 映射、非 `/api/v1` 路由清单 | ✓ Sprint 004 |
| 管理端 Dashboard | `/api/v1/admin/dashboard` | 是（admin/employee） | 首页数据概览：SKU、品牌、Banner、用户指标 | ✓ Sprint 010 |
| 管理端日志审计 | `/api/v1/admin/logs` | 是（仅 admin） | API 请求日志、产品行为事件、审计操作统一查询与详情 | ✓ Sprint 004 |
| 产品行为事件 | `/api/v1/usage-events` | 可选登录 | 前端上报人为定义的产品使用埋点事件 | ✓ Sprint 004 |
| 真实用户性能事件 | `/api/v1/performance-events` | 否 | Web 与微信小程序真实用户加载耗时 RUM 上报 | ✓ Sprint 022 |
| 管理端性能观测 | `/api/v1/admin/performance-events` | 是（仅 admin） | RUM 筛选候选值、样本聚合、慢页面排行与样本明细 | ✓ Sprint 022/023 |
| 管理端品牌 | `/api/v1/admin/brands` | 是（admin/employee） | 品牌 CRUD、启停、条件删除 | ✓ Sprint 002 |
| 管理端品牌证书 | `/api/v1/admin/brand-certificates` | 是（admin/employee） | 证书 CRUD、显示/隐藏、软删除、有效状态 summary | ✓ Sprint 007 |
| 管理端 Banner | `/api/v1/admin/banners` | 是（admin/employee） | Banner CRUD、上下线、条件删除、summary | ✓ Sprint 003 |
| 管理端专题（只读） | `/api/v1/admin/topics` | 是（admin/employee） | 专题列表（Banner 跳转关联） | ✓ Sprint 003 |
| 管理端类目 | `/api/v1/admin/tile-categories` | 是（admin/employee） | 类目树、CRUD、启停、条件删除 | ✓ Sprint 002 |
| 管理端 SKU | `/api/v1/admin/tile-skus` | 是（admin/employee） | SKU CRUD、上下架、素材、筛选 summary | ✓ Sprint 002 |
| 管理端规格 | `/api/v1/admin/tile-specs` | 是（admin/employee） | 瓷砖规格 CRUD、启停、条件删除、summary | ✓ Sprint 003 |
| 管理端上传 | `/api/v1/admin/uploads` | 是 | 头像（admin/employee）；品牌 Logo、Banner 图、SKU 图片/视频（admin/employee） | ✓ Sprint 002/003，MinIO 单桶存储 |
| 媒体 | `/api/v1/media` | — | 规划中的统一媒体 API | 未实现 |

\* `uploads` 路由通过后端鉴权接口写入 `MINIO_BUCKET`，不允许前端直连未授权 MinIO。

## 3.1 认证与当前用户

实现：`src/backend/app/api/v1/auth.py`

| 方法 | 路径 | 认证 | 说明 |
|---|---|---|---|
| POST | `/api/v1/auth/login` | 否 | 用户名密码登录 |
| GET | `/api/v1/auth/me` | Bearer | 获取当前用户 |
| PATCH | `/api/v1/auth/me/theme` | Bearer | 更新当前用户界面主题偏好 |
| POST | `/api/v1/auth/logout` | Bearer | 登出 |

`GET /api/v1/auth/me` 与登录响应中的 `data.user` 返回 `theme_mode`，取值：

```text
system | dark_flagship
```

历史 `light` / `comfort_dark` 偏好值会在读取或更新兼容路径中分别归一为 `system` / `dark_flagship`，不再作为对外可选值暴露。

更新主题偏好请求：

```json
{
  "theme_mode": "dark_flagship"
}
```

成功响应：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": "user-id",
    "username": "admin",
    "display_name": "系统管理员",
    "role": "admin",
    "status": "active",
    "theme_mode": "dark_flagship"
  }
}
```

错误：

| 场景 | HTTP | code | message |
|---|---:|---:|---|
| 未登录或 Token 无效 | 401 | 40102 | 登录已过期，请重新登录 |
| 当前用户已禁用 | 403 | 30010 | 账号已被禁用 |
| `theme_mode` 不在允许枚举内 | 400 | 40001 | 无效的主题模式 |

新增或变更本组接口后必须重新导出 `src/web/openapi.json` 并运行 `./scripts/generate-openapi-client.sh`。

### 3.4 管理端用户（Sprint 002）

实现：`src/backend/app/api/v1/admin_users.py`  
OpenSpec：`openspec/changes/add-user-management/`

| 方法 | 路径 | 认证 |
|---|---|---|
| GET | `/api/v1/admin/users` | Bearer（admin） |
| POST | `/api/v1/admin/users` | Bearer（admin） |
| GET | `/api/v1/admin/users/{id}` | Bearer（admin） |
| PATCH | `/api/v1/admin/users/{id}` | Bearer（admin） |
| POST | `/api/v1/admin/users/{id}/reset-password` | Bearer（admin） |
| PATCH | `/api/v1/admin/users/{id}/status` | Bearer（admin） |

列表查询参数：`page`、`page_size`（10/20/50）、`keyword`（匹配 `username`、`display_name`、`email`、`phone`）、`role`、`status`、`login_filter`。

用户对象含 `email`、`phone`、`is_protected` 与 `protected_reason`。`email`、`phone` 仅作为联系信息，不要求唯一，不参与登录身份识别。当 `is_protected=true` 时，前端 MUST 保持编辑、重置密码、冻结/解冻、删除按钮可见但禁用，并以 `protected_reason` 作为提示。

创建请求体：`username`、`display_name`、`role`、`avatar_object_key`、`email`、`phone`。  
更新请求体：`display_name`、`role`、`avatar_object_key`、`email`、`phone`。  
`email`、`phone` 允许传 `null` 或空字符串清空；邮箱按通用邮箱格式校验，手机号采用宽松格式，仅允许数字、空格、`+`、`-`。

创建成功 `data` 含 `user` 与一次性 `initial_password`。

创建用户校验：

| 场景 | HTTP | code | message |
|---|---:|---:|---|
| 用户名长度不足或超长 | 400 | 40010 | 用户名长度须为 4–32 位 |
| 用户名格式非法 | 400 | 40010 | 用户名须以小写字母开头，仅含小写字母、数字、_、-、. |
| 用户名连续特殊符号 | 400 | 40010 | 用户名不允许连续特殊符号 |
| 用户名为系统保留字 | 400 | 40010 | 用户名为系统保留字 |
| 用户名重复 | 409 | 40910 | 用户名已存在 |
| 系统保底管理员账号被编辑、重置密码或变更状态 | 403 | 30060 | 系统保底管理员账号不允许执行该操作 |

用户名规则由后端业务校验统一返回 `{ code, message, data }`，不得仅返回 FastAPI 默认 422 `detail`。

框架级请求校验失败（如缺少 `role`、路径或查询参数类型不合法）返回 `422 / code=40001`，`data.errors[]` 包含 `field`、`message`、`type`、`location`。

### 3.4.1 管理端系统设置（Sprint 003）

实现：`src/backend/app/api/v1/admin_system_settings.py`  
OpenSpec：`openspec/changes/add-system-settings/`

| 方法 | 路径 | 认证 |
|---|---|---|
| GET | `/api/v1/admin/system-settings/{group}` | Bearer（admin） |
| PATCH | `/api/v1/admin/system-settings/{group}` | Bearer（admin） |
| POST | `/api/v1/admin/system-settings/{group}/reset` | Bearer（admin） |
| GET | `/api/v1/admin/system-settings/audit/recent` | Bearer（admin） |

`group` ∈ `basic` \| `security` \| `media` \| `notification` \| `audit`。响应 `data` 为 `{ group, data: { ...effective fields } }`；媒体分组可写 `max_image_size_mb`、`max_video_size_mb`、`max_file_size_mb`、`allowed_image_types`、`allowed_video_types`、`thumbnail_max_size_kb`、`display_max_size_kb`，并含只读 `minio_bucket`、`object_key_rule`。`thumbnail_max_size_kb=0` 表示不限制；正整数表示后续新生成图片缩略图尽量不超过该 KB 目标，保存设置不自动重建历史 `.thumb` 对象。`display_max_size_kb` 默认 `768`，与缩略图目标独立，只影响后续新生成 `.display` 详情展示图；历史 `.display` 需通过媒体维护任务显式重生成。

### 3.4.2 管理端接口文档（Sprint 004）

实现：`src/backend/app/api/v1/admin_api_docs.py`  
OpenSpec：`openspec/changes/add-admin-api-docs-menu/`

| 方法 | 路径 | 认证 |
|---|---|---|
| GET | `/api/v1/admin/api-docs` | Bearer（admin） |

响应 `data.routes` 汇总 FastAPI 运行时路由，覆盖：

- `/api/v1/*` 下所有业务接口；
- `/health` 健康检查；
- `/media/{object_key:path}` 媒体直出路由（支持 `GET`/`HEAD`，`include_in_schema=false`，不生成 Orval 方法）；图片响应返回 `Cache-Control`、`ETag`，并返回脱敏观测头 `X-Media-Resolved-Key-Hash` 与 `X-Media-Fallback`，用于区分 `.thumb` 是否实际回退原图；
- `/openapi.json`、`/docs`、`/redoc` 等 FastAPI 文档相关非 `/api/v1` 路由。

单条路由字段：`method`、`path`、`tag`、`summary`、`auth_requirement`、`included_in_openapi`、`operation_id`、`orval_method_name`、`source`、`missing_orval_reason`。

前端页面：`/admin/api-docs`，仅 `admin` 可访问；入口位于管理端 SYSTEM 分组「系统设置」下方。

OpenAPI/Orval 关系：

- OpenAPI JSON：`/openapi.json` 与 `src/web/openapi.json`；
- Swagger UI：`/docs`；
- Orval 配置：`src/web/orval.config.ts`；
- 前端生成客户端：`src/web/src/shared/api/generated.ts`；
- 已纳入 OpenAPI 且具备 `operationId` 的接口展示 camelCase Orval 方法名；schema 外路由展示「未生成」及原因。

Swagger 在线调试策略：`APP_ENV` 为 `local`、`development`、`dev`、`demo`、`test` 时允许 `Try It Out`；其他环境展示 Swagger 文档入口，但 FastAPI `swagger_ui_parameters.tryItOutEnabled=false`，管理端页面标记为生产只读。

本接口不返回数据库 DSN、MinIO AccessKey/SecretKey、JWT、原始环境变量值或其他敏感配置。

Swagger Web 代理与生产只读 checklist：

- Swagger 主入口使用同源 `/docs`；行级接口深链使用 `/docs#/{tag}/{operationId}` 或等价同源编码路径。
- Web 层必须确保 `/docs`、`/redoc`、`/openapi.json` 以及 Swagger UI 所需后端文档资源不会被 SPA fallback 接管。
- Vite dev proxy、Docker Web Nginx 与生产反向代理策略需要在相关 Change 的 design、acceptance 或 trace 中记录；生产不可验证时记录具体 N/A 原因。
- 生产或生产等价环境可展示 Swagger 文档，但 `Try It Out` 必须由后端环境策略禁用、隐藏或保持只读，不得只依赖前端文案。
- Swagger 链接、hash、query、localStorage 新键、页面文案与验收记录不得包含 Bearer Token、JWT Secret、数据库 DSN、MinIO 凭据或真实环境变量值。

### 3.4.2a 管理端 Dashboard（Sprint 010 / BUG-0079）

实现：`src/backend/app/api/v1/admin_dashboard.py`  
OpenSpec：`openspec/changes/fix-admin-dashboard-overview-real-data/`

| 方法 | 路径 | 认证 |
|---|---|---|
| GET | `/api/v1/admin/dashboard/summary` | Bearer（admin/employee） |

响应 `data` 为 `AdminDashboardSummary`，包含 `sku_total`、`brand_total`、`banner_total`、`user_total` 四个指标。每个指标结构为 `{ value, description, visible }`。

- `sku_total` 统计 `tiles` 当前记录数。
- `brand_total` 统计 `brands` 当前记录数。
- `banner_total` 统计当前有效 Banner：状态在线、在展示时间窗口内，且展示端与位置合法。
- `user_total` 仅 `admin` 返回真实用户数；`employee` 返回 `visible=false`，前端以隐藏态展示，避免越权泄露。

前端页面：`/admin/dashboard` 数据概览区使用 Orval 方法 `getAdminDashboardSummaryApiV1AdminDashboardSummaryGet`，不得再引用 `dashboardMetrics` mock 数据；请求失败时展示错误态与重试入口。

### 3.4.3 管理端日志审计（Sprint 004 / REQ-0024）

实现：`src/backend/app/api/v1/admin_logs.py`、`src/backend/app/api/v1/usage_events.py`  
OpenSpec：`openspec/changes/add-product-usage-logging/`

| 方法 | 路径 | 认证 |
|---|---|---|
| GET | `/api/v1/admin/logs` | Bearer（admin） |
| GET | `/api/v1/admin/logs/observability` | Bearer（admin） |
| GET | `/api/v1/admin/logs/{log_id}` | Bearer（admin） |
| POST | `/api/v1/usage-events` | 可选 Bearer（admin/employee 匿名均可上报） |

`GET /api/v1/admin/logs` 查询参数：

| 参数 | 说明 |
|---|---|
| `page` / `page_size` | 分页，`page_size` 1–100，默认 20 |
| `log_type` | `request` / `usage_event` / `audit` |
| `keyword` | 匹配摘要、路径、request_id、client_request_id、behavior_trace_id、事件名、操作人 |
| `actor_user_id` | 操作人 ID |
| `client_type` | 客户端类型，当前统一为 `web_admin`、`web_catalog`、`wechat_miniapp`，未知请求头记录为 `unknown` |
| `status_code` | HTTP 状态码 100–599 |
| `result` | `success` / `failed` |
| `resource_id` | 资源 ID，匹配 metadata |
| `path_or_request_id` | API path、request_id、client_request_id、behavior_trace_id、parent_behavior_event_id 或 task_trace_id 模糊匹配 |
| `behavior_trace_id` | 精确匹配一次界面行为链路 ID；直接 API 调用无界面行为来源时为空 |
| `task_trace_id` | 精确匹配 Task Trace 任务链路 ID |
| `start_time` / `end_time` | ISO8601 时间字符串 |

列表响应 `data.metrics` 返回当日摘要：`today_logs`、`api_errors`、`slow_requests`、`sensitive_ops`；`data.items` 同时包含请求日志、行为事件、既有 `audit_logs` 的统一列表行。列表行返回 `actor_name` 与 `actor_username`，管理端列表和详情抽屉的「操作者」均使用 `actor_username` 单行展示账号，避免显示名和账号混淆。请求日志行额外返回 `client_request_id`，该字段来自 `x-client-request-id` 或请求体 `client_request_id`，只用于辅助排障，不覆盖服务端可信 `request_id`。界面触发的日志行额外返回 `behavior_trace_id` 与 `parent_behavior_event_id`，用于串联同一次页面访问、点击或表单提交触发的一个或多个 API 请求；直接 API 调用这两个字段为空。若日志关联任务链路，列表行额外返回 `task_trace_id`、`task_type`、`task_status`、`task_duration_ms`、`task_slowest_span_name`，用于上传等长耗时任务排障。管理端日志审计页默认按最近1天查询，时间范围筛选固定为最近5分钟、10分钟、30分钟、1小时、3小时、6小时、12小时、1天、2天、3天和7天，不提供全部时间。日志列表表头单行展示，追踪字段列顺序为 `request_id`、`client_request_id`、`behavior_trace_id`、`task_trace_id`。BUG-0127 后，接口响应契约保持兼容；后端在指定 `log_type` 时优先使用对应日志表查询，混合日志查询将时间范围、操作者、客户端、状态或结果、behavior_trace_id、request_id 和 Task Trace ID 等条件下推到各日志表子查询，摘要指标使用独立低成本聚合，避免首屏被无条件三表 UNION、全量计数排序或同步统一源指标聚合阻塞。

`GET /api/v1/admin/logs/observability` 与日志列表共用筛选口径，额外支持 `behavior_trace_id`、`request_id`、`task_trace_id` 精确定位；响应 `data` 包含 `summary`、`distributions`、`endpoint_errors`、`rankings`、`trace_results` 和 `thresholds`。`trace_results` 会返回命中的 `behavior_trace_id`、请求日志 ID / `request_id`、任务链路 ID 集合，用于展示“界面行为 -> 请求 -> 任务 -> 节点”的链路；直接 API 调用可从 `request_id` 进入 `task_traces.parent_request_id -> task_trace_spans`。当前慢请求与慢任务阈值均为 1000ms；该接口仅返回聚合指标和已脱敏摘要，不返回原始 metadata、请求体或内部路径。未命中追踪 ID 时 `trace_results.reason=not_found`，接口本身仍返回 `200 / code=0`。截至 2026-07-26，管理端 `/admin/logs` 已按产品调整移除链路观测页面模块，前端不展示该聚合接口入口；日志列表、筛选、详情抽屉和 Task Trace 时间线仍保留。

`GET /api/v1/admin/logs/{log_id}` 返回详情抽屉数据，按 `basic`、`request`、`actor`、`operation`、`tracking`、`metadata` 分组展示，并保留 `request_id`、`behavior_trace_id` 与 `parent_behavior_event_id` 用于链路排查。请求日志详情额外返回 `request_snapshot`，结构包含 `request`、`input`、`resource`、`response`、`actor`、`timing` 与 `raw_json`：`request` 记录 method、path、route_template、route_match_status、request_id、client_request_id、behavior_trace_id、parent_behavior_event_id、trusted_request_id_header、client_request_id_header、behavior_trace_id_header、behavior_event_id_header；`input` 记录 query 白名单摘要、body schema 摘要和 redaction_summary；`resource` 记录 resource_type、resource_id、id_source；`response` 记录 status_code、error_code、duration_ms、result、error_summary；`actor` 记录 actor_user_id、actor_username、actor_role、client_type、ip_summary、user_agent_summary；`timing` 记录 environment、started_at、finished_at。历史日志、metadata 为空或 metadata JSON 解析失败时，`request_snapshot` 使用空值 / 未采集 / `parse_error` 表达，不影响核心日志详情展示。详情抽屉字段标签旁展示说明图标，hover 或键盘 focus 时使用 fixed tooltip 显示字段含义，避免被右侧抽屉边界裁切。若存在 `task_trace_id`、请求 `request_id` 或 `behavior_trace_id` 触发过 Task Trace，响应额外包含 `task_trace` 和 `related_task_traces[]`；任务摘要包含 `task_trace_id`、`parent_request_id`、`behavior_trace_id`、任务类型、状态、耗时、资源、错误码和摘要，`related_task_traces[]` 支持一个主请求触发多个任务摘要；每个 span 包含 `span_name`、`status`、`started_at`、`ended_at`、`duration_ms`、`request_id`、`behavior_trace_id`、`error_code`、`summary`、`is_slowest`。未找到返回 `404 / code=30070`。

`POST /api/v1/usage-events` 请求体：

```json
{
  "event_name": "media_upload",
  "page_path": "/admin/tile-skus/sku_843291",
  "session_id": "sess_abc",
  "request_id": "req_79f1c2b4a8d04e31",
  "client_request_id": "web:client-request-abc123",
  "behavior_trace_id": "bt:8c0186d2-9c5f-4f0f-9ad2-b5f623060f21",
  "behavior_event_id": "be:cc4b9185-d375-45fd-8d3d-851e77f95f31",
  "task_trace_id": "task_upload_video_abcdef1234567890",
  "task_type": "upload_video",
  "duration_ms": 1280,
  "properties": {
    "module": "SKU 管理",
    "entity_type": "tile_sku",
    "entity_id": "sku_843291",
    "changed_fields": ["gallery_images", "main_image"]
  }
}
```

`behavior_trace_id` 表示一次界面行为链路，`behavior_event_id` 表示单条行为事件。Web 前端生成这两个 ID 后，在短时间窗口内通过 `x-behavior-trace-id` 与 `x-behavior-event-id` 透传给该行为触发的后续 API 请求；后端请求日志保存为 `request_logs.behavior_trace_id` 与 `request_logs.parent_behavior_event_id`。直接 API 调用无需伪造行为事件，保持 `behavior_trace_id` 为空并使用后端可信 `request_id` 进入任务链路。`duration_ms` 为行为本身耗时毫秒数，适用于页面加载、查询、详情加载、上传、保存等有过程耗时的行为；瞬时行为可省略，列表显示 `-`。

行为事件由产品/研发人为定义 `event_name` 与属性。当前后端白名单包含：`page_view`、`search_submit`、`filter_change`、`detail_view`、`copy_request_id`、`entity_create`、`entity_update`、`entity_delete`、`status_change`、`media_upload`、`login_success`、`login_failed`、`api_error`、`product_detail_view`、`home_share`、`product_share`、`home_contact_click`、`product_contact_click`、`miniapp_home_search_click`、`miniapp_home_quick_entry_click`、`miniapp_home_new_product_click`、`miniapp_home_hot_product_click`、`miniapp_home_waterfall_product_click`、`miniapp_home_favorite_visual_click`、`miniapp_certificate_tab_click`、`certificate_list_page_view`、`certificate_list_load`、`certificate_list_refresh`、`certificate_list_load_more`、`certificate_list_retry`、`certificate_click`、`certificate_preview_click`、`certificate_load_failed`、`miniapp_home_waterfall_load`、`miniapp_home_waterfall_load_failed`、`miniapp_home_waterfall_end_reached`、`sku_detail_view`、`sku_media_swipe`、`sku_image_preview`、`sku_video_play`、`sku_video_fullscreen_click`、`sku_video_fullscreen_enter`、`sku_video_fullscreen_exit`、`sku_video_fullscreen_failed`、`sku_video_action_menu_open`、`sku_video_action_cancel`、`sku_video_action_share`、`sku_video_action_save`、`sku_video_save_success`、`sku_video_save_failed`、`sku_favorite`、`sku_unfavorite`、`sku_share_click`、`sku_brand_click`、`sku_recommend_click`、`sku_load_error`、`category_page_view`、`primary_category_click`、`secondary_category_click`、`category_load_failed`、`product_list_page_view`、`product_list_item_exposure`、`product_list_item_click`、`product_list_filter_open`、`product_list_filter_apply`、`product_list_sort_change`、`product_list_refresh`、`product_list_load_more`、`product_list_load_failed`、`search_page_view`、`search_input`、`search_suggestion_exposure`、`search_suggestion_click`、`search_result_exposure`、`search_result_click`、`search_filter_apply`、`search_no_result`、`search_history_click`、`search_history_delete`、`search_history_clear`。后端会拒绝未定义事件、缺少必填属性或包含敏感字段（如 password、token、secret、authorization、cookie、raw_payload、raw_filename、raw_object_key、object_key、raw_response、internal_path）的上报，返回 `400 / code=40001`。

### 3.4.4 真实用户页面加载性能（Sprint 022 / REQ-0107）

实现：`src/backend/app/api/v1/performance_events.py`
OpenSpec：`openspec/changes/add-real-user-page-load-rum/`

| 方法 | 路径 | 认证 |
|---|---|---|
| POST | `/api/v1/performance-events` | 否 |
| GET | `/api/v1/admin/performance-events/filter-options` | Bearer（admin） |
| GET | `/api/v1/admin/performance-events/summary` | Bearer（admin） |
| GET | `/api/v1/admin/performance-events/samples` | Bearer（admin） |

`POST /api/v1/performance-events` 请求体：

```json
{
  "events": [
    {
      "client_type": "web_admin",
      "page_key": "admin/performance",
      "metric_name": "full_load",
      "duration_ms": 1280,
      "sample_rate": 1,
      "app_version": "0.1.0",
      "network_type": "4g",
      "device_class": "desktop",
      "request_id": "rum-locally-generated-id",
      "occurred_at": "2026-08-10T00:00:00Z"
    }
  ]
}
```

上报接口只接收页面、指标、耗时、版本、网络、设备类别和客户端生成 `request_id` 等安全摘要，不接收 Header、Cookie、Authorization、完整请求体、完整响应体、手机号、openid、token、签名 URL 或 raw payload；命中敏感字段返回 `400 / code=40001`。Web RUM 的 `app_version` 与管理端左上角产品版本徽标同源；`network_type` 优先取浏览器网络类型 API，浏览器不支持时允许为空并在管理端显示“未知”。小程序 RUM 使用 `wx.getNetworkType` 获取 `network_type`，仅获取失败时上报 `unknown`。上报失败不影响 Web 或小程序主流程。

`GET /api/v1/admin/performance-events/filter-options` 查询参数仅接收 `start_time` / `end_time`。响应 `data` 固定返回 6 大筛选维度：`client_types`、`app_versions`、`page_keys`、`device_classes`、`network_types`、`metrics`；每个候选项包含 `value`、`label`，动态采样维度额外包含 `count`。`client_types` 与 `metrics` 来自后端枚举，`app_versions`、`page_keys`、`device_classes`、`network_types` 按时间范围从 RUM 样本聚合候选值；候选值不随端类型、版本、页面、设备、网络或指标筛选级联收敛。

`GET /api/v1/admin/performance-events/summary` 查询参数：

| 参数 | 说明 |
|---|---|
| `client_type` | `web_admin` / `web_catalog` / `wechat_miniapp` |
| `metric_name` | 指标名，如 `first_content_ready`、`full_load`、`app_launch_ready`、`api_duration` |
| `page_key` | 页面或接口 key 精确筛选 |
| `app_version` | 版本精确筛选 |
| `network_type` | 网络类型精确筛选 |
| `device_class` | 设备类别精确筛选 |
| `start_time` / `end_time` | ISO 时间范围 |
| `min_samples` | 慢页面排行最小样本量，默认 20 |
| `page` | 聚合维度页码，默认 1 |
| `page_size` | 每页聚合行数，1–100，默认 20 |
| `limit` | 兼容旧调用的每页聚合行数；新页面使用 `page/page_size` |

响应 `data.items[]` 按 `client_type + page_key + metric_name + app_version + network_type + device_class` 聚合返回 `sample_count`、`average_ms`、`max_ms`、`p50_ms`、`p75_ms`、`p95_ms`、`p99_ms`；响应同时返回 `total`、`page`、`page_size`、`total_pages` 和 `total_events`，用于管理端聚合列表后端真实分页。`data.slow_pages[]` 与当前页聚合行保持一致并按 P95 降序。管理端页面 `/admin/performance` 使用候选值接口展示“时间范围 > 端类型 > 版本号 > 页面 > 网络 > 指标”筛选区；候选值接口仍返回 `device_classes`，但设备不作为本期筛选控件展示。聚合接口展示“页面 > 版本号 > 端类型 > 设备 > 网络 > 指标 > 样本 > P50 > P75 > P95 > P99 > 状态 > 操作”字段顺序、摘要、慢页面排行、空态、错误态、样本不足态和分页。

`GET /api/v1/admin/performance-events/samples` 使用同一组安全筛选参数（不含 `min_samples`），并支持 `page`、`page_size` 与兼容旧调用的 `limit`；响应返回 `total`、`page`、`page_size`、`total_pages` 和最近样本明细 `items[]`：`id`、`client_type`、`page_key`、`metric_name`、`duration_ms`、`app_version`、`network_type`、`device_class`、`request_id`、`occurred_at`、`server_received_at`。管理端性能观测页从聚合列表右侧冻结“操作”列点击“查看样本”，跳转到 `/admin/performance/samples` 独立样本页；样本页使用管理端列表页样式展示上下文“页面 > 版本号 > 端类型 > 设备 > 网络 > 指标”和样本表“页面 > 版本号 > 端类型 > 设备 > 网络 > 指标 > 耗时 > 事件时间 > 接收时间 > request_id”、后端真实分页控件，并允许复制 `request_id`。日志审计不承载 RUM 单次明细。该接口不得返回完整 URL、Header、Cookie、签名 URL、raw payload、用户隐私或内部鉴权字段。

小程序事件要求：

| event_name | 必填 properties | 说明 |
|---|---|---|
| `product_detail_view` | `product_id`、`page_path`、`client_type` | 商品详情访问，用于热销统计 |
| `home_share` | `page_path`、`client_type` | 首页分享 |
| `product_share` | `product_id`、`page_path`、`client_type` | 商品分享 |
| `home_contact_click` | `page_path`、`contact_type`、`client_type` | 首页或门店咨询点击 |
| `product_contact_click` | `product_id`、`page_path`、`contact_type`、`client_type` | 商品详情咨询点击 |
| `miniapp_home_search_click` | `page_path`、`client_type` | 首页搜索入口点击 |
| `miniapp_home_quick_entry_click` | `page_path`、`entry_key`、`client_type` | 首页四入口点击 |
| `miniapp_home_new_product_click` | `product_id`、`page_path`、`client_type` | 新品推荐商品点击 |
| `miniapp_home_hot_product_click` | `product_id`、`page_path`、`client_type` | 热销推荐商品点击 |
| `miniapp_home_waterfall_product_click` | `product_id`、`page_path`、`client_type` | 全部产品瀑布流商品点击 |
| `miniapp_home_favorite_visual_click` | `product_id`、`page_path`、`client_type` | 非持久化收藏视觉点击或收藏占位 Tab 触达 |
| `miniapp_certificate_tab_click` | `page_path`、`client_type` | 证书 Tab 点击 |
| `certificate_list_page_view` | `page_path`、`client_type` | 证书列表页曝光 |
| `certificate_click` / `certificate_preview_click` | `certificateId`、`page_path`、`client_type` | 证书卡片点击与预览点击 |
| `certificate_load_failed` | `page_path`、`client_type` | 证书列表或证书图片加载失败 |
| `miniapp_home_waterfall_load` | `page_path`、`page`、`page_size`、`client_type` | 全部产品瀑布流加载 |
| `miniapp_home_waterfall_load_failed` | `page_path`、`page`、`reason`、`client_type` | 全部产品瀑布流加载失败 |
| `miniapp_home_waterfall_end_reached` | `page_path`、`page`、`total`、`client_type` | 全部产品瀑布流无更多 |
| `sku_detail_view` | `sku_id`、`page_path`、`client_type` | SKU 详情页成功展示 |
| `sku_media_swipe` | `sku_id`、`page_path`、`media_type`、`client_type` | SKU 详情媒体切换 |
| `sku_image_preview` | `sku_id`、`page_path`、`client_type` | SKU 图片全屏预览 |
| `sku_video_play` | `sku_id`、`page_path`、`client_type` | SKU 视频播放 |
| `sku_video_fullscreen_click` / `sku_video_fullscreen_enter` / `sku_video_fullscreen_exit` / `sku_video_fullscreen_failed` | `sku_id`、`page_path`、`client_type` | SKU 视频全屏入口点击、进入、退出和失败 |
| `sku_video_action_menu_open` / `sku_video_action_cancel` / `sku_video_action_share` / `sku_video_action_save` | `sku_id`、`page_path`、`client_type` | SKU 视频长按操作菜单、取消、分享和保存动作 |
| `sku_video_save_success` / `sku_video_save_failed` | `sku_id`、`page_path`、`client_type` | SKU 视频保存到相册成功或失败 |
| `sku_favorite` / `sku_unfavorite` | `sku_id`、`page_path`、`client_type` | SKU 粒度收藏状态变更 |
| `sku_share_click` | `sku_id`、`page_path`、`client_type` | SKU 分享点击 |
| `sku_brand_click` | `sku_id`、`brand_id`、`page_path`、`client_type` | SKU 详情品牌入口点击 |
| `sku_recommend_click` | `sku_id`、`target_sku_id`、`recommend_type`、`page_path`、`client_type` | SKU 推荐卡点击 |
| `sku_load_error` | `sku_id`、`page_path`、`error_code`、`stage`、`client_type` | SKU 详情加载失败 |
| `category_page_view` | `page_path`、`has_cache`、`client_type` | 分类页访问 |
| `primary_category_click` | `category_id`、`category_index`、`page_path`、`client_type` | 一级分类点击 |
| `primary_category_product_list_click` | `category_id`、`category_name`、`category_level`、`sourcePage`、`category_index`、`page_path`、`client_type` | 一级分类商品列表入口点击 |
| `secondary_category_click` | `category_id`、`parent_category_id`、`category_index`、`page_path`、`client_type` | 二级分类点击，商品列表入口需补充 `category_name`、`category_level`、`sourcePage` 与 `action` |
| `category_load_failed` | `page_path`、`error_code`、`has_cache`、`client_type` | 分类树加载失败 |
| `product_list_page_view` | `page_path`、`sourcePage`、`sort`、`pageSize`、`requestId`、`client_type` | 商品列表页访问 |
| `product_list_item_exposure` | `skuId`、`sourcePage`、`positionIndex`、`requestId`、`client_type` | 商品卡片曝光 |
| `product_list_item_click` | `skuId`、`sourcePage`、`positionIndex`、`requestId`、`client_type` | 商品卡片点击 |
| `product_list_filter_open` | `sourcePage`、`filterSnapshot`、`sort`、`requestId`、`client_type` | 商品列表筛选打开 |
| `product_list_filter_apply` | `sourcePage`、`filterSnapshot`、`sort`、`resultCount`、`requestId`、`client_type` | 商品列表筛选应用 |
| `product_list_sort_change` | `sourcePage`、`filterSnapshot`、`sort`、`resultCount`、`requestId`、`client_type` | 商品列表排序切换 |
| `product_list_refresh` | `sourcePage`、`page`、`pageSize`、`resultCount`、`requestId`、`client_type` | 商品列表下拉刷新 |
| `product_list_load_more` | `sourcePage`、`page`、`pageSize`、`resultCount`、`requestId`、`client_type` | 商品列表加载更多 |
| `product_list_load_failed` | `sourcePage`、`page`、`pageSize`、`errorCode`、`requestId`、`client_type` | 商品列表加载失败 |
| `search_page_view` | `page_path`、`sourcePage`、`requestId`、`client_type` | 搜索页访问 |
| `search_input` | `keyword`、`normalizedKeyword`、`scope`、`sourcePage`、`requestId`、`client_type` | 搜索输入 |
| `search_suggestion_exposure` | `keyword`、`normalizedKeyword`、`scope`、`resultCount`、`sourcePage`、`requestId`、`client_type` | 联想曝光 |
| `search_suggestion_click` | `keyword`、`normalizedKeyword`、`scope`、`entityType`、`sourcePage`、`requestId`、`client_type` | 联想点击 |
| `search_result_exposure` | `keyword`、`normalizedKeyword`、`scope`、`entityType`、`resultCount`、`sourcePage`、`requestId`、`client_type` | 结果曝光 |
| `search_result_click` | `keyword`、`normalizedKeyword`、`scope`、`entityType`、`sourcePage`、`requestId`、`client_type` | 结果点击 |
| `search_filter_apply` | `keyword`、`normalizedKeyword`、`scope`、`filterSnapshot`、`resultCount`、`sourcePage`、`requestId`、`client_type` | 搜索筛选应用 |
| `search_no_result` | `keyword`、`normalizedKeyword`、`scope`、`resultCount`、`sourcePage`、`requestId`、`client_type` | 搜索无结果 |
| `search_history_click` / `search_history_delete` | `keyword`、`normalizedKeyword`、`scope`、`sourcePage`、`requestId`、`client_type` | 搜索历史操作 |
| `search_history_clear` | `scope`、`sourcePage`、`requestId`、`client_type` | 清空搜索历史 |

小程序事件不得提交聊天内容、Authorization header、Cookie、原始手机号、raw payload、raw object key、原始响应体或内部路径。SKU 详情收藏事件只记录 SKU 粒度业务事实和必要上下文；分类页事件只记录分类 ID、索引、错误码和是否有缓存等必要信息；商品列表事件只记录来源页面、分类/品牌/关键词、筛选快照、排序、分页、结果数量、SKU ID、位置索引和 requestId 等必要上下文；搜索事件只记录关键词、归一化关键词、scope、实体类型、结果数量、来源页面、筛选快照和 requestId 等必要上下文。埋点失败不得阻断小程序浏览、分享、收藏、推荐跳转、分类切换、商品列表加载、筛选、排序、刷新、加载更多、详情跳转、搜索输入、联想、结果展示、筛选、无结果页或瀑布流加载主流程。

### 3.5 微信小程序公开接口（Sprint 008/009）

实现：`src/backend/app/api/v1/miniapp.py`
OpenSpec：`openspec/specs/miniapp-home/`、`openspec/specs/miniapp-search/`、`openspec/specs/miniapp-product-list-page/`、`openspec/specs/miniapp-certificate-list-page/`

| 方法 | 路径 | 认证 | 说明 |
|---|---|---|---|
| GET | `/api/v1/miniapp/home` | 否 | 首页聚合数据：门店摘要、Banner、快捷入口、服务区、新品、热销 |
| GET | `/api/v1/miniapp/categories/tree?depth=2` | 否 | 公开分类树：最多两级启用分类、排序、兼容 `coverUrl` 和数据版本号 |
| GET | `/api/v1/miniapp/brands` | 否 | 公开品牌列表与品牌页轮播，支持 `page`、`pageSize` |
| GET | `/api/v1/miniapp/brands/{brand_id}` | 否 | 公开品牌主页/详情信息：品牌图片、名称、简介、公开商品数、公开证书数 |
| GET | `/api/v1/miniapp/brands/{brand_id}/certificates` | 否 | 当前品牌可公开证书列表，返回受控证书预览 URL |
| GET | `/api/v1/miniapp/certificates` | 否 | 公开证书聚合列表，仅支持 `page`、`pageSize` |
| GET | `/api/v1/miniapp/certificates/{certificate_id}` | 否 | 公开证书详情，返回媒体组、品牌入口、分享信息和受控文件 URL |
| GET | `/api/v1/miniapp/products` | 否 | 公开商品列表，支持 `categoryId`、`categoryLevel`、`keyword`、`brandId`、`spec`、`priceRange`、`sort`、`page`、`pageSize`，兼容 `filter_type`、`filter_value`、`section` |
| GET | `/api/v1/miniapp/search/home` | 否 | 搜索首页数据：热门搜索词；最近搜索由小程序本机保存 |
| GET | `/api/v1/miniapp/search/suggestions` | 否 | 搜索实时联想，支持 `keyword`、`scope`、`limit`、`request_id`；仅返回品牌与 SKU 联想 |
| GET | `/api/v1/miniapp/search` | 否 | 完整搜索，支持 `keyword`、`tab`、分页、品牌/类目/规格/价格筛选和 `request_id`；小程序结果页仅展示综合、品牌、SKU、证书 Tab |
| GET | `/api/v1/miniapp/products/{product_id}` | 否 | 公开商品详情 |
| GET | `/api/v1/miniapp/skus/{sku_id}` | 否 | SKU 详情聚合数据：主体、媒体、品牌、收藏状态、分享数据、同系列和同品牌推荐；`brand.brand_logo_thumbnail_url` 供详情品牌卡优先展示 |
| PUT | `/api/v1/miniapp/skus/{sku_id}/favorite` | 否 | SKU 粒度幂等设置收藏状态，body: `{ client_id, favorite }` |

`GET /api/v1/miniapp/home` 响应 `data`：

```json
{
  "store": {"name": "菲尚特瓷砖馆", "description": "质感空间，由砖而生"},
  "banners": [
    {
      "id": 1,
      "title": "质感空间，由砖而生",
      "image_url": "/media/banners/home.display.webp",
      "thumbnail_url": "/media/banners/home.thumb.webp",
      "display_url": "/media/banners/home.display.webp",
      "jump_type": "product",
      "target_id": 1
    }
  ],
  "shortcuts": [{"key": "select", "title": "选瓷砖", "filter_type": "all"}],
  "services": [{"key": "store", "title": "门店服务", "action_type": "none"}],
  "new_products": [],
  "hot_products": []
}
```

公开商品卡片只返回允许展示字段：`product_id`、`product_name`、`sku_code`、`cover_image`、`specification`、`category_name`、`brand_name`、`style_tags`、`applicable_spaces`、`color_family`、`price_display`、`is_new`、`is_hot`、`is_recall_pinned`。接口不得返回后台内部字段、库存管理字段、内部备注、对象存储 raw object key 或敏感配置。

`GET /api/v1/miniapp/products` 请求支持分类、搜索、品牌、规格、价格区间和排序上下文：`categoryId`、`categoryLevel=primary|secondary`、`keyword`、`brandId`、`spec`、`priceRange`（如 `100-200`、`200-`）、`sort=default|latest|price_asc|price_desc`、`page`、`pageSize`。`categoryLevel=primary` 表示聚合该一级分类下所有启用二级分类的公开 SKU，不只返回直接挂载在一级分类下的 SKU；`categoryLevel=secondary` 或未传时保持二级分类精确查询语义。品牌过滤、分类查询和普通关键词查询在 `sort=default` 且非 `section=new|hot` 时，默认按 `COALESCE(tiles.published_at, tiles.created_at) ASC, tiles.id ASC` 返回，优先使用 SKU 发布时间 `published_at`，历史空值使用 `created_at` 兜底；若这些入口存在生效召回置顶 SKU，后端会在分页前按 `recall_pin_sort_order ASC` 将最多 4 个 SKU 排在普通结果前，置顶资格必须先满足公开条件和当前请求筛选，并在对应商品卡片返回 `is_recall_pinned: true` 供小程序展示“置顶”角标。该规则不改变无筛选首页全部产品列表、搜索页普通联想、新品榜召回、热销榜热度排序或价格排序；这些入口即使 SKU 有召回配置也返回 `is_recall_pinned: false`，且接口不暴露内部召回配置字段。接口兼容旧参数 `filter_type`、`filter_value` 和 `section=new|hot`，供首页瀑布流和历史入口继续调用。响应 `data` 包含 `items`、`total`、`page`、`page_size`、`has_more` 和 `facets`；`facets` 提供可用 `brands`、`categories`、`specs`、`price_ranges` 选项。服务端只返回 `tiles.status=PUBLISHED`、`brands.status=ENABLED`、`tile_categories.status=ENABLED`、启用规格或无规格的 SKU，并过滤后台内部字段、库存管理、内部备注、未授权素材、raw object key、Authorization header、Cookie 或敏感配置。`has_more` 用于小程序商品列表页和首页全部产品瀑布流判断是否继续触底加载；若无更多数据，小程序端必须停止追加请求并展示无更多状态。

`GET /api/v1/miniapp/search/suggestions` 响应 `data` 包含 `keyword`、`normalized_keyword`、`request_id` 与 `suggestions[]`。`suggestions[]` 仅包含 `brand` 和 `sku` 类型，字段为 `id`、`text`、`entity_type`、`target_id`、`target_path`、`scope`；最近搜索、普通关键词、类目、规格和证书不得进入联想结果。

`GET /api/v1/miniapp/search` 响应 `data` 包含 `tabs[]`、`best_match`、`sections[]`、`facets`、`items`、`total`、`page`、`page_size`、`has_more` 与 `recommended_keywords`。`best_match` 可返回 `entity_type=sku|brand|certificate`：SKU 编码或 SKU 名称直接命中优先，其次品牌名精确命中，最后证书名称或证书编号精确命中；未满足上述直接命中时返回 `null`。小程序结果页按综合、品牌、SKU、证书展示 Tab，不展示类目 Tab；综合 Tab 按最佳匹配、品牌、SKU、证书顺序展示非 0 条分区，品牌/SKU/证书单独 Tab 直接展示卡片内容，不再展示分区标题和数量。完整搜索中的 SKU 结果会在公开过滤和关键词匹配后应用召回置顶排序，最多 4 个生效置顶 SKU 排在 SKU 结果前部；搜索实时联想、热门词、最近搜索、品牌结果和证书结果不受该配置影响，公开响应不返回召回状态或排序解释字段。完整搜索会二次过滤公开状态：只返回 `tiles.status=PUBLISHED`、`brands.status=ENABLED`、`tile_categories.status=ENABLED`、启用规格和可公开证书，不暴露后台内部字段、内部备注、raw object key 或敏感配置。v1 不新增管理端搜索配置中心、后台热门词维护、同义词维护、自然语言词典维护、搜索统计管理页或 `/api/admin/search/*`。

首页 Banner 数据来自管理端 Banner 管理能力：仅返回 `status=ONLINE`、展示端为 `MINIAPP_HOME`（管理端文案显示“小程序”）、展示位置为 `MINIAPP_HOME_CAROUSEL`（首页轮播）、且满足有效期的记录，并按 `sort_order`、`updated_at` 排序。小程序 Banner 轮播图属于首屏大图展示位，目标规格为 `display`；小程序端普通展示优先使用 `display_url`，其次 `thumbnail_url`，两者缺失时使用安全视图占位；`image_url` 保留兼容并承载同一轻量 URL，优先与 `display_url` 对齐，不作为原图 fallback。公开 `jump_type` 支持 `product`、`brand`、`search`、`store`、`none`，其中 `brand` 使用 `target_id` 跳转品牌详情页。接口会净化自动生成或兼容导入的内部 Banner 标题，例如 `internal-*MINIAPP*`、`*NO_JUMP*` 类标识不得作为公开 `title` 或 `search_keyword` 暴露；搜索型 Banner 只有存在安全公开标题时才返回 `search_keyword`。若没有可用 Banner，接口可返回空数组，小程序端降级到本地默认 Hero。

`GET /api/v1/miniapp/brands` 响应 `data` 包含 `banners[]`、`items[]`、`total`、`page`、`page_size` 和 `has_more`。`banners[]` 仅来自 `MINIAPP_BRAND_LIST_CAROUSEL`（品牌列表页轮播）安全字段，支持 `jump_type=brand` + `target_id` 跳转品牌详情页；品牌列表页无轮播数据时返回空数组，不使用首页轮播兜底。品牌列表页轮播返回 `thumbnail_url`、`display_url` 和兼容 `image_url`，普通展示优先消费 `display_url`，缺失或不可读时降级到 `thumbnail_url`，不得回退原图或不存在的本地静态占位图。`items[]` 返回启用品牌的安全字段：`brand_id`、`brand_name`、`brand_short_name`、`brand_logo_url`、`brand_logo_thumbnail_url`、`brand_entry_path`、`product_count`、`leaf_category_names`、`leaf_categories`、`description`、`available`；`brand_logo_thumbnail_url` 为同目录 `.thumb` 派生 URL，列表/卡片普通展示只使用该缩略图，缺失、不可读或加载失败时展示占位，不回退 `brand_logo_url` 原图；小程序公开列表和详情接口默认不下发原图 Logo。`product_count`、`leaf_category_names` 与 `leaf_categories` 使用同一批小程序公开 SKU 过滤条件（`tiles.status=PUBLISHED`、品牌启用、类目启用、规格启用或为空），`leaf_categories[]` 返回去重后的所有上架/公开 SKU 绑定末级类目 ID 与名称并按类目排序，`leaf_category_names[]` 保留名称集合；品牌有公开商品时必然有商品关联类目，`product_count=0` 的启用品牌仍可展示且类目集合为空。接口不得返回品牌后台备注、raw object key、内部审计字段、Authorization header、Cookie 或敏感配置。

`GET /api/v1/miniapp/brands/{brand_id}` 响应 `data` 包含单品牌主页公开信息，并返回 `product_path` 与 `certificate_count` 供小程序品牌主页展示。品牌主页顶部品牌图位为 Hero 大图展示位，响应提供独立 `brand_hero_display_url` 与 `brand_hero_thumbnail_url`，小程序端普通展示优先消费 `brand_hero_display_url`，缺失或加载失败时降级到 `brand_hero_thumbnail_url`，再降级到安全视图占位或品牌名占位；不得回退 `brand_logo_url` 原图、`preview_url`、旧 `url`、语义不明 `image_url` 或不存在的本地静态占位图。品牌列表、品牌卡、详情页品牌入口等小 Logo 场景仍只消费 `brand_logo_thumbnail_url`，缺失时展示占位，不回退 `brand_logo_url` 原图。品牌不存在、停用、无公开 SKU 或不可公开时返回 `404 / code=30030`。

`GET /api/v1/miniapp/brands/{brand_id}/certificates` 响应 `data.items[]` 只包含当前品牌可公开证书，字段为 `certificate_id`、`certificate_name`、`certificate_type`、`certificate_no`、`issuer`、`brand_name`、`file_url`、`thumbnail_url`。当证书存在 `main_image` 时，`file_url` 优先返回主图原图 URL；无主图时回退 legacy 证书文件 URL；该字段仅供证书详情、预览或打开动作使用，不作为卡片图片兜底。图片类证书同步返回同目录 `.thumb` 派生 `thumbnail_url`，PDF 返回 `null`；品牌详情证书 Tab 等卡片入口仅可使用 `thumbnail_url` 或占位，缺缩略图或图片加载失败时不得请求 `file_url`。隐藏、删除、停用品牌证书不会返回；响应不得暴露 `file_key`、后台备注、审计字段、raw object key、Authorization header、Cookie 或敏感配置。

`GET /api/v1/miniapp/certificates` 响应 `data` 包含 `items[]`、`total`、`page`、`page_size` 和 `has_more`，请求仅支持分页参数 `page`、`pageSize`。`items[]` 字段为 `certificate_id`、`certificate_name`、`certificate_type`、`certificate_type_label`、`brand_id`、`brand_name`、`file_url`、`thumbnail_url`、`file_name`、`file_mime_type`、`file_kind`、`effective_date`、`expiry_date`、`validity_status`、`validity_status_label`；聚合列表为了避免卡片误拉原文件，`file_url` 返回 `null`，`thumbnail_url` 仅在图片证书存在同目录 `.thumb` 派生图时返回。小程序证书卡片仅展示证书名称、品牌名称和证书类型，并在 `file_kind=image` 时优先使用 `thumbnail_url` 渲染主图，缩略图缺失、不可读或加载失败时展示占位，不得回退 `file_url`、原图或原文件 URL。接口只返回未删除、`is_visible=true` 且所属品牌 `status=ENABLED` 的证书，排序为 `sort_order ASC, updated_at DESC, id DESC`；响应不得暴露 `file_key`、后台备注、审计字段、内部用户字段、raw object key、Authorization header、Cookie 或敏感配置。

`GET /api/v1/miniapp/certificates/{certificate_id}` 响应 `data` 包含单张公开证书详情：列表安全字段、`brand`、`media[]`、`main_media`、`description`、`remark` 和 `share`。`remark` 为公开备注说明，空值或 `null` / `undefined` 占位值返回 `null`。`media[]` 字段为 `media_id`、`media_type=image|pdf|unknown`、`url`、`preview_url`、`thumbnail_url`、`display_url`、`original_url`、`file_name`、`file_mime_type`、`sort_order`、`is_main`；多图证书按主图优先、其余图片按 `sort_order ASC, id ASC` 排序，旧单文件证书回退到 legacy `file_url`。图片证书的 `display_url` 用于详情顶部普通展示，`url` 保留兼容且只承载 `display_url` 或 `thumbnail_url` 等安全展示 URL，缺少展示图和缩略图时返回空字符串并由小程序占位或失败态兜底；图片预览使用 `original_url` 或 `preview_url`。PDF/文档证书不生成图片 `display_url`、`thumbnail_url` 或 `original_url`，继续通过文件打开、占位或失败态展示。`brand` 返回 `brand_id`、`brand_name`、`brand_logo_thumbnail_url`、`brand_entry_path` 和 `available`；`brand_logo_thumbnail_url` 为品牌 Logo 同目录缩略图 URL，供证书详情页复用 `brand-card` 普通展示优先消费，缺失时小程序使用品牌卡统一占位，不得 fallback 到品牌 Logo 原图。`share` 返回分享标题、分享路径、分享图和摘要。小程序证书详情页标题固定为“证书详情”，证书名称面板不重复展示品牌名称，所属品牌入口复用 `brand-card` 展示和跳转；证书信息展示备注说明但不展示有效期，底部不提供固定“预览文件”或“分享证书”按钮。接口只返回未删除、`is_visible=true` 且所属品牌 `status=ENABLED` 的证书；不存在、隐藏、软删除或所属品牌停用时返回 `404 / code=30030`。响应不得暴露审计字段、内部用户字段、`file_key`、raw object key、本机路径、bucket 内部信息、Authorization header、Cookie 或敏感配置。

`GET /api/v1/miniapp/categories/tree?depth=2` 响应 `data` 包含 `version` 与 `items[]`。`items[]` 只返回 `status=ENABLED` 且 `level<=2` 的类目，一级和二级分别按 `sort_order ASC, created_at ASC, id ASC` 排序；一级节点字段为 `id`、`name`、`sort`、`children`，二级节点字段为 `id`、`name`、`coverUrl`、`sort`。`coverUrl` 为兼容字段，当前小程序分类列表页不渲染二级类目图片；后端返回统一安全占位 URL `/media/miniapp/category-placeholder.webp`，不自动取 SKU 商品主图，不暴露 `description`、`sku_count`、`path`、raw object key、Authorization header、Cookie 或后台内部备注。

公开商品卡片的 `cover_image` 来自 SKU 主图（`tile_images.is_main=1` 优先），返回后端受控读取 URL，不得暴露对象存储 raw object key。列表场景优先返回与原图同目录、文件名以 `.thumb` 区分的缩略图 URL，例如 `/media/images/default/tiles/pending/<uuid>.thumb.jpg`；若该缩略图对象缺失，后端 `/media/{object_key}` 读取会回退同目录原图，公开列表不得返回已知不可访问的 `/media/thumbnails/default/tiles/pending/<uuid>.jpg`。`price_display` 来自 SKU `reference_price` 格式化结果：正数显示为 `¥xx.xx`，缺失、空值或非正数显示为 `暂无参考价`。

`GET /api/v1/miniapp/skus/{sku_id}` 只返回公开 SKU（`tiles.status=PUBLISHED`）字段，响应包含 `brand`、`media[]`、`image_count`、`video_count`、`category_path`、`parameters`、`remark`、`favorite`、`same_series_recommendations`、`same_brand_recommendations` 和 `share`。`remark` 为公开备注说明，空值或 `null` / `undefined` 占位值返回 `null`；小程序商品详情页将备注说明作为商品参数模块内的参数行展示，不单独渲染独立备注模块。图片、视频、品牌 Logo 与分享图 URL 必须是后端返回的安全访问 URL；图片 `media[]` 的 `url` 为商品详情页首屏普通展示 URL，只承载 `display_url` 或 `thumbnail_url`，`preview_url` 保留原图用于点击预览；商品列表、商品卡片和推荐位优先使用与原图同目录的 `.thumb` 派生 URL，Banner 和 `share.image_url` 优先使用 `.display` 或等价展示图并可降级到 `.thumb`，缺轻量图时返回空值或由小程序占位，不默认下发原图；视频 `media[]` 的 `url` 保持原视频资源，`cover_url` 优先使用商品主图或首张图片的同目录 `.thumb` 缩略图作为播放前封面兜底，不新增 raw object key。响应不得包含 raw object key、库存管理字段、后台内部备注、Authorization header、Cookie 或敏感配置。SKU 不存在、下架或不可公开时返回 `404 / code=30030`。

`PUT /api/v1/miniapp/skus/{sku_id}/favorite` 使用 `client_id` 与 `sku_id` 唯一约束实现幂等收藏/取消收藏；重复提交返回目标状态，不产生重复收藏记录。SKU 不存在、下架或不可公开时返回 `404 / code=30030`；请求体校验失败返回 `422 / code=40001`。

### 3.6 管理端品牌（Sprint 002）

实现：`src/backend/app/api/v1/admin_brands.py`  
OpenSpec：`openspec/changes/add-brand-management/`

| 方法 | 路径 | 认证 |
|---|---|---|
| GET | `/api/v1/admin/brands` | Bearer（admin/employee） |
| POST | `/api/v1/admin/brands` | Bearer（admin/employee） |
| GET | `/api/v1/admin/brands/{id}` | Bearer（admin/employee） |
| PUT | `/api/v1/admin/brands/{id}` | Bearer（admin/employee） |
| POST | `/api/v1/admin/brands/{id}/enable` | Bearer（admin/employee） |
| POST | `/api/v1/admin/brands/{id}/disable` | Bearer（admin/employee） |
| DELETE | `/api/v1/admin/brands/{id}` | Bearer（admin/employee） |

列表查询参数：`page`、`page_size`（20/50/100）、`keyword`、`status`（`ENABLED`/`DISABLED`）。  
响应 `data.summary`：`total`、`enabled_count`、`disabled_count`、`unlinked_sku_count`。

删除规则：仅 `sku_count=0` 且 `status=DISABLED` 时允许；否则 `code=30012`。

品牌 Logo 上传：`POST /api/v1/admin/uploads/brand-logos`（admin/employee；JPG/PNG/WebP）。成功响应包含 `thumbnail_key`、`thumbnail_url`，缩略图与原图同目录并以 `.thumb` 文件名区分；缩略图内容读取 `media.thumbnail_max_size_kb` effective 策略，但 URL / Key 规则不变。

上传接口缺少必填 `file` 或文件参数形状非法时返回 `422 / code=40001` 的统一校验 envelope；业务文件类型、大小错误仍保留上传领域错误码。

### 3.6.1 管理端品牌证书（Sprint 007）

实现：`src/backend/app/api/v1/admin_brand_certificates.py`  
OpenSpec：`openspec/changes/add-brand-certificate-management/`

| 方法 | 路径 | 认证 |
|---|---|---|
| GET | `/api/v1/admin/brand-certificates` | Bearer（admin/employee） |
| POST | `/api/v1/admin/brand-certificates` | Bearer（admin） |
| GET | `/api/v1/admin/brand-certificates/{certificate_id}` | Bearer（admin/employee） |
| PUT | `/api/v1/admin/brand-certificates/{certificate_id}` | Bearer（admin） |
| POST | `/api/v1/admin/brand-certificates/{certificate_id}/show` | Bearer（admin） |
| POST | `/api/v1/admin/brand-certificates/{certificate_id}/hide` | Bearer（admin） |
| DELETE | `/api/v1/admin/brand-certificates/{certificate_id}` | Bearer（admin） |

列表参数：`page`、`page_size`（20/50/100）、`keyword`、`brand_id`、`type`、`validity_status`、`display_status`。响应 `data.items[]` 包含 `file_url`、`file_key`、`thumbnail_url`、`brand_name`、`validity_status`、`display_status`、`images[]`、`main_image`；列表缩略图优先使用 `main_image.thumbnail_url`，无图片时回退 legacy `thumbnail_url` / `file_url` 字段。管理端品牌证书列表不提供单独“预览”行操作，预览/查看能力以后续详情入口或文件打开策略为准。`data.summary` 包含 `total`、`valid_count`、`expiring_soon_count`、`expired_count`。

创建/更新请求体包含 `brand_id`、`name`、`sort_order`、`type`、`file`、`images[]`、`is_permanent`、`effective_date`、`expiry_date`、`is_visible` 等字段；`file` 用于 PDF/文档或旧单文件兼容，`images[]` 用于 JPG/PNG/WebP 多图，最多 9 张。有图片时必须且只能有一张 `is_main=true`，保存后按 `sort_order` 连续回填；若只传图片不传 `file`，后端以主图回填 legacy `file_*` 字段。非长期有效证书必须提供 `expiry_date`。错误码：`30013` 不存在、`30014` 同品牌名称重复、`40024` 日期非法、`40025` 文件/图片缺失、`40026` 主图非法、`40027` 图片/文件引用非法、`30010` 品牌不存在。

证书文件上传：`POST /api/v1/admin/uploads/brand-certificates`（admin；JPG/PNG/WebP/PDF；大小使用 `MAX_FILE_SIZE_MB` / `media.max_file_size_mb` effective 值）。JPG/PNG/WebP 成功响应包含同目录 `.thumb` 缩略图 `thumbnail_key`、`thumbnail_url`，缩略图内容读取 `media.thumbnail_max_size_kb` effective 策略；PDF 返回 `null` 并由前端使用文件占位。

### 3.5b 管理端 Banner（Sprint 003）

实现：`src/backend/app/api/v1/admin_banners.py`、`admin_topics.py`  
OpenSpec：`openspec/changes/add-banner-management/`

| 方法 | 路径 | 认证 |
|---|---|---|
| GET | `/api/v1/admin/banners` | Bearer（admin/employee） |
| POST | `/api/v1/admin/banners` | Bearer（admin/employee） |
| GET | `/api/v1/admin/banners/{id}` | Bearer（admin/employee） |
| PUT | `/api/v1/admin/banners/{id}` | Bearer（admin/employee） |
| POST | `/api/v1/admin/banners/{id}/online` | Bearer（admin/employee） |
| POST | `/api/v1/admin/banners/{id}/offline` | Bearer（admin/employee） |
| DELETE | `/api/v1/admin/banners/{id}` | Bearer（admin/employee） |
| GET | `/api/v1/admin/topics` | Bearer（admin/employee） |

列表查询参数：`page`、`page_size`（10/20/50）、`keyword`、`display_client`、`status`、`time_status`。当前 `display_client` 仅支持 `MINIAPP_HOME`（管理端显示“小程序”）；Banner 保存仅允许 `MINIAPP_HOME_CAROUSEL`（首页轮播）与 `MINIAPP_BRAND_LIST_CAROUSEL`（品牌列表页轮播）。列表项返回 `image_url` 原图 URL 与 `image_thumbnail_url` 同目录 `.thumb` 缩略图 URL，管理端列表优先使用缩略图，缺失或加载失败时回退原图，详情/编辑继续保留原图语义。列表项返回只读 `jump_target_label` 供管理端“跳转对象”列展示：品牌详情为品牌名称，SKU 详情为 SKU 名称，专题页为专题名称，外部链接为 URL，无跳转或目标不可用时为 `-`；`keyword` 可匹配位置、外部链接、品牌名称、SKU 名称、专题名称和内部标题兼容字段。创建/更新请求体支持 `jump_type=SKU_DETAIL|BRAND_DETAIL|EXTERNAL_LINK|TOPIC_PAGE|NO_JUMP`，其中品牌详情使用 `brand_id` 作为唯一跳转目标，图片来源可使用品牌 `logo_object_key` 对应的 `brand_logo` 或自定义上传。旧 Web 首页、专题页和历史运营位 Banner 业务记录由迁移清理，不物理删除 MinIO 对象。生产 MySQL `banners` 表结构未完成兼容迁移或保存链路数据库写入异常时，接口返回 `503 / code=30055`，不暴露 SQL、DSN 或内部堆栈。
响应 `data.summary`：`total`、`filtered_count`、`online_count`、`pending_count`。  
Banner 图上传：`POST /api/v1/admin/uploads/banner-images`（`images/default/banners/...`）。

### 3.6 管理端瓷砖类目（Sprint 002）

实现：`src/backend/app/api/v1/admin_tile_categories.py`
OpenSpec：`openspec/changes/add-tile-category-management/`

| 方法 | 路径 | 认证 |
|---|---|---|
| GET | `/api/v1/admin/tile-categories/tree` | Bearer（admin/employee） |
| GET | `/api/v1/admin/tile-categories` | Bearer（admin/employee） |
| POST | `/api/v1/admin/tile-categories` | Bearer（admin/employee） |
| GET | `/api/v1/admin/tile-categories/{id}` | Bearer（admin/employee） |
| PUT | `/api/v1/admin/tile-categories/{id}` | Bearer（admin/employee） |
| POST | `/api/v1/admin/tile-categories/{id}/enable` | Bearer（admin/employee） |
| POST | `/api/v1/admin/tile-categories/{id}/disable` | Bearer（admin/employee） |
| DELETE | `/api/v1/admin/tile-categories/{id}` | Bearer（admin/employee） |

列表参数：`page`、`page_size`（10/20/50）、`keyword`、`status`、`level`（仅 1/2）、`parent_id`（含子孙扁平分页）。
树节点 `sku_count` 为含子级汇总 SKU 数，`children_count` 为直接子类目数量；列表行 `sku_count` 为当前节点直接绑定数。管理端类目树右侧计数应使用 `children_count`，“全部类目”入口显示顶层类目数量，不得用 `sku_count` 商品数量替代。管理端类目最多允许创建二级类目；`POST /api/v1/admin/tile-categories` 请求不再要求或信任客户端提交 `code`，后端创建时自动生成 `CAT-` 前缀唯一编码并在响应对象中返回。类目名称创建 / 更新时最多 15 个字符，支持中文、英文、数字和常见特殊字符（`-`、`_`、`/`、`&`、`()`、`·`、`.`、`+`、`#`、`:`、`，`、`、`），不允许空格、换行、制表符或不可见控制字符；同一 `parent_id` 下名称重复返回 `409 / code=30024`。若 `parent_id` 指向二级类目，返回 `422 / code=30023`。

### 3.7 管理端瓷砖 SKU（Sprint 002）

实现：`src/backend/app/api/v1/admin_tile_skus.py`  
OpenSpec：`openspec/changes/add-tile-sku-management/`

| 方法 | 路径 | 认证 |
|---|---|---|
| GET | `/api/v1/admin/tile-skus` | Bearer（admin/employee） |
| POST | `/api/v1/admin/tile-skus` | Bearer（admin/employee） |
| GET | `/api/v1/admin/tile-skus/{id}` | Bearer（admin/employee） |
| PUT | `/api/v1/admin/tile-skus/{id}` | Bearer（admin/employee） |
| POST | `/api/v1/admin/tile-skus/{id}/publish` | Bearer（admin/employee） |
| POST | `/api/v1/admin/tile-skus/{id}/unpublish` | Bearer（admin/employee） |
| DELETE | `/api/v1/admin/tile-skus/{id}` | Bearer（admin/employee） |

列表参数：`page`、`page_size`（10/20/50/100）、`keyword`、`brand_id`、`category_id`、`status`、`material_completeness`；`category_id` 按类目子树筛选，传父类目时包含自身及所有子孙类目的 SKU。
响应 `data.summary`：`total`、`published_count`、`needs_completion_count`、`draft_count`。
列表项返回 `main_image_url`、`main_image_thumbnail_url`、`main_image_display_url`、`main_image_original_url`。管理端 SKU 列表优先使用缩略图，缺失或加载失败时按 `display -> original/main_image_url` 回退；详情、编辑与上传预览优先使用 `display_url`，高清预览或下载语义保留 `original_url`。SKU 图片详情项同步返回 `thumbnail_url`、`display_url`、`original_url`，请求体仍只保存 `object_key`、`url`、`is_main`、`sort_order`，多规格 URL 由后端媒体服务按对象 key 派生或按直出配置生成。列表项返回 `published_at`，表示最近一次上架/恢复上架时间；从未发布、发布时间为空或历史数据缺失时返回 `null`。已下架等非 `PUBLISHED` 状态若存在历史 `published_at`，管理端列表、详情与下架响应仍返回该历史发布时间，便于运营继续查看最近一次发布成功时间。REQ-0103 起，创建、更新、详情和列表项返回召回置顶运营配置字段：`recall_pin_sort_order`、`recall_pin_starts_at`、`recall_pin_ends_at`；请求体可提交同名字段，`recall_pin_sort_order` 只能为正整数，未填或传 `null` 时按 `9999` 保存，低于 `9999` 且处于有效期内才参与小程序普通商品列表和完整搜索 SKU 结果置顶。`recall_pin_starts_at=null` 表示立即可生效，`recall_pin_ends_at=null` 表示长期有效；开始时间晚于结束时间返回 `422 / code=40001`。管理端 SKU 列表排序不因召回字段改变。

创建请求 `save_mode`：`draft`（仅名称必填）| `create`（全必填）。  
错误码：`30031` 编码重复、`30032` 删除禁止、`30033` 上架禁止。

SKU 素材上传：`POST /api/v1/admin/uploads/tile-images`、`POST /api/v1/admin/uploads/tile-videos`（可选 `tile_id` 查询参数）。

创建/更新请求体含 `spec_id`（`save_mode=create` 必填；须为 ENABLED 规格）。  
错误码：`30031` 编码重复、`30032` 删除禁止、`30033` 上架禁止。

REQ-0074 起，`POST /api/v1/admin/tile-skus`、`PUT /api/v1/admin/tile-skus/{id}`、`POST /api/v1/admin/tile-skus/{id}/publish`、`POST /api/v1/admin/tile-skus/{id}/unpublish` 的成功响应 `data` 额外返回可选 `task_trace_id` 与 `task_type`，任务类型分别为 `sku_create`、`sku_update`、`sku_publish`、`sku_unpublish`。这些接口复用统一 `ApiResponse`，不新增任务状态查询接口、不新增错误码；业务失败仍按既有错误码返回，并在 Task Trace 中记录失败 span。管理端 SKU 表单成功态不在弹窗内展示或复制 `task_trace_id`；需要排障时，可通过日志审计 `task_trace_id` 精确筛选或在日志详情中查看任务时间线。
REQ-0079 起，`POST /api/v1/admin/tile-skus/{id}/publish` 每次成功都会刷新 `published_at`，恢复上架视为重新发布；`unpublish` 不清空数据库历史值。REQ-0087 验收返修后，`unpublish` 响应、管理端列表与详情在非 `PUBLISHED` 状态下仍返回历史 `published_at`，从未发布或历史值缺失时才返回 `null`。

### 3.8 管理端瓷砖规格（Sprint 003）

实现：`src/backend/app/api/v1/admin_tile_specs.py`  
OpenSpec：`openspec/changes/add-tile-spec-management/`

| 方法 | 路径 | 认证 |
|---|---|---|
| GET | `/api/v1/admin/tile-specs` | Bearer（admin/employee） |
| POST | `/api/v1/admin/tile-specs` | Bearer（admin/employee） |
| GET | `/api/v1/admin/tile-specs/{id}` | Bearer（admin/employee） |
| PUT | `/api/v1/admin/tile-specs/{id}` | Bearer（admin/employee） |
| POST | `/api/v1/admin/tile-specs/{id}/enable` | Bearer（admin/employee） |
| POST | `/api/v1/admin/tile-specs/{id}/disable` | Bearer（admin/employee） |
| DELETE | `/api/v1/admin/tile-specs/{id}` | Bearer（admin/employee） |

列表参数：`page`、`page_size`（10/20/50）、`keyword`（匹配 `display_name`）、`status`（`ENABLED`/`DISABLED`）。  
响应 `data.summary`：`total`、`enabled_count`、`disabled_count`。  
`display_name` 由服务端按 `{width_mm}×{length_mm}mm` 生成。

删除规则：仅 `sku_count=0` 且 `status=DISABLED` 时允许；否则 `code=30042`。  
错误码：`30040` 不存在、`30041` 尺寸重复、`30042` 删除禁止、`30043` 规格已停用。

历史 SKU 迁移：`scripts/migrate_tile_spec_ids.py --dry-run` / `--apply`（匹配 `tiles.size` → `spec_id`）。

---

## 3. 认证接口（Sprint 001）

实现：`src/backend/app/api/v1/auth.py`  
OpenSpec：`openspec/specs/auth/spec.md`

### 3.1 用户登录

| 方法 | 路径 | 认证 |
|---|---|---|
| POST | `/api/v1/auth/login` | 否 |

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| username | string | 是 | 登录用户名 |
| password | string | 是 | 密码 |
| remember_me | boolean | 否 | 默认 `false`；`true` 时 token 有效期 7 天 |

**成功响应 `data`**

| 字段 | 说明 |
|---|---|
| access_token | JWT |
| token_type | 固定 `Bearer` |
| expires_in | 秒；默认 7200（2h），remember_me 为 604800（7d） |
| user | `{ id, username, display_name, role, status }` |

**示例**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "access_token": "eyJ...",
    "token_type": "Bearer",
    "expires_in": 7200,
    "user": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "username": "admin",
      "display_name": "系统管理员",
      "role": "admin",
      "status": "active"
    }
  }
}
```

**错误**

| HTTP | code | message | 场景 |
|---|---|---|---|
| 400 | 40001 | 请求参数无效 | Pydantic 校验失败 |
| 401 | 40101 | 账号或密码错误 | 凭证错误 |
| 403 | 40301 | 账号已停用，请联系管理员 | status=`disabled` |

### 3.2 当前用户

| 方法 | 路径 | 认证 |
|---|---|---|
| GET | `/api/v1/auth/me` | Bearer |

**成功 `data`：** `{ id, username, display_name, role, status }`

**错误**

| HTTP | code | 场景 |
|---|---|---|
| 401 | 40102 | 未携带 token、token 无效或过期 |
| 403 | 40301 | 用户已禁用 |

### 3.3 退出登录

| 方法 | 路径 | 认证 |
|---|---|---|
| POST | `/api/v1/auth/logout` | Bearer |

**成功 `data`：** `{ "success": true }`

客户端 MUST 清除本地 token。服务端 JWT 无状态，不维护服务端会话黑名单（本期）。

### 个人资料 self-service（Sprint 003）

实现：`src/backend/app/api/v1/profile.py`  
OpenSpec：`openspec/changes/add-admin-profile-page/`

| 方法 | 路径 | 认证 |
|---|---|---|
| GET | `/api/v1/profile/me` | Bearer（admin/employee） |
| PATCH | `/api/v1/profile/me` | Bearer（admin/employee） |
| GET | `/api/v1/profile/me/activities` | Bearer（admin/employee） |

PATCH 可更新：`display_name`（2–32）、`email`、`phone`、`remark`（≤200）、`avatar_object_key`。  
禁止更新：`username`、`role`、`status`（extra=forbid → 422）。  
`store_owner` → 403。

校验错误码：`40013`（`PROFILE_VALIDATION_ERROR`）。

activities 默认返回最近 **5** 条，按 `created_at` 降序。

### 管理端修改密码（Sprint 003）

实现：`src/backend/app/api/v1/admin_profile.py`  
OpenSpec：`openspec/changes/add-admin-password-change/`

| 方法 | 路径 | 认证 |
|---|---|---|
| POST | `/api/v1/admin/profile/password` | Bearer（admin/employee） |

**请求体：** `{ "old_password": string, "new_password": string }`  
**成功 `data`：** `{ "success": true }`

改密成功后 `users.token_version` 递增，JWT `tv` claim 失效旧 token；客户端 MUST 清除本地 token 并重新登录。

校验错误码：`30060`（系统保底管理员账号不允许执行改密）、`40020`（原密码错误）、`40021`（策略）、`40022`（弱密码）、`40023`（与原密码相同）、`42901`（限流）。

`40021` 策略失败响应保持统一 envelope，并在 `data` 中提供前端可识别的策略详情：

```json
{
  "code": 40021,
  "message": "新密码至少需要 5 位字符；新密码需要包含英文字符",
  "data": {
    "violations": ["min_length", "missing_letter"],
    "policy": {
      "min_length": 5,
      "max_length": 32,
      "require_letter": true,
      "require_digit": true
    }
  }
}
```

`violations` 稳定枚举：`min_length`、`max_length`、`missing_letter`、`missing_digit`。响应不得包含明文密码。

---

## 4. 角色与权限

| role | 管理端 API | 说明 |
|---|---|---|
| admin | ✓ | 系统管理员 |
| employee | ✓ | 企业内部员工 |
| store_owner | ✗（40302） | 预留，本期拒绝管理端 |

依赖：`require_admin_access`（`src/backend/app/core/deps.py`）

---

## 5. 瓷砖接口（桩 / 待 Sprint 002+）

### 5.1 公开列表与详情

| 方法 | 路径 | 响应模型 | 说明 |
|---|---|---|---|
| GET | `/api/v1/tiles` | `TileListItem[]` | 当前返回 `[]` |
| GET | `/api/v1/tiles/{tile_id}` | `TileDetail` | 当前返回示例数据 |

> 注：上述接口 **未** 使用 `{ code, message, data }` envelope，返回裸 Pydantic 模型；后续 `add-tile-catalog` change 应统一。

### 5.2 管理端创建

| 方法 | 路径 | 认证 | 说明 |
|---|---|---|---|
| POST | `/api/v1/admin/tiles` | admin/employee | 请求体 `TileCreate`，当前返回示例 `TileDetail` |

---

## 6. 上传接口

上传接口均使用 `multipart/form-data`，字段名为 `file`，成功响应 `data` 至少保持 `{ object_key, url, thumbnail_key, thumbnail_url, display_key, display_url, original_url, task_trace_id, task_type }`；非图片或不生成多规格图的上传返回对应字段 `null`。证书文件额外返回 `file_key`、`file_url`、`file_name`、`mime_type`、`size`。图片上传、视频上传、文件上传首批写入 Task Trace span，覆盖 `frontend_upload_start`、`frontend_upload_body_done`、`api_receive`、`validate_file`、`storage_put_object`、`db_create_media`、`post_process`、`api_response`、`frontend_done/failed`。

| 方法 | 路径 | 认证 | 对象前缀 | 说明 |
|---|---|---|---|---|
| POST | `/api/v1/admin/uploads` | admin | `original/default/avatars/` | 头像上传 |
| POST | `/api/v1/admin/uploads/brand-logos` | admin/employee | `original/default/brands/logos/` | 品牌 Logo 上传 |
| POST | `/api/v1/admin/uploads/tile-images` | admin/employee | `original/default/tiles/{tile_id|pending}/images/` | SKU 图片上传 |
| POST | `/api/v1/admin/uploads/tile-videos` | admin/employee | `videos/default/tiles/{tile_id|pending}/` | SKU 视频上传 |
| POST | `/api/v1/admin/uploads/brand-certificates` | admin | `files/default/brand-certificates/` | 品牌证书 JPG/PNG/WebP/PDF 上传 |

媒体读取默认保持 `/media/{object_key}` URL 语义，由后端从对象存储受控读取；图片 `.thumb` 或 `.display` 缺失时可回退同目录原图。`OBJECT_STORAGE_DIRECT_READ_ENABLED=true` 时，后端媒体适配层可返回短期对象存储直出读取 URL，过期时间由 `OBJECT_STORAGE_DIRECT_READ_EXPIRES_SECONDS` 控制且限制在 60-3600 秒；前端和小程序仍只能消费后端返回的 URL，不得拼接 endpoint、bucket 或持有永久密钥。视频读取支持 `Range` 请求并返回 `206 Partial Content`、`Content-Type: video/*`、`Accept-Ranges: bytes` 与 `Content-Range`；`HEAD /media/{object_key}` 返回媒体元信息头但不返回文件内容，用于微信小程序原生视频预览、保存和转发前的资源探测。该路由不进入 OpenAPI，不生成 Orval 方法。

上传错误：

| HTTP | code | 场景 |
|---|---|---|
| 400 | 50002 | 文件类型不允许 |
| 400 | 50003 | 文件大小超限 |
| 400 | 50004 | 品牌证书文件类型不允许 |
| 400 | 50005 | 品牌证书文件超过 effective 文件大小上限 |
| 502 | 50001 | MinIO 不可用、Bucket 初始化失败或对象写入失败 |

---

## 7. 错误码速查（认证）

运行时 code 定义：`src/backend/app/core/exceptions.py`

| HTTP | code | 常量（exceptions） | 典型 message |
|---|---|---|---|
| 400 | 40001 | AuthInvalidRequestError | 请求参数无效 |
| 401 | 40101 | AuthInvalidCredentialsError | 账号或密码错误 |
| 401 | 40102 | AuthUnauthorizedError | 未登录或登录已过期 |
| 403 | 40301 | AuthUserDisabledError | 账号已停用，请联系管理员 |
| 403 | 40302 | AuthForbiddenError | 无权限访问 |

完整登记与分段规则：`docs/standards/error-codes.md`

---

## 8. 环境变量（认证相关）

| 变量 | 说明 |
|---|---|
| `APP_SECRET_KEY` | JWT 签名密钥 |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | 默认 120 |
| `JWT_REMEMBER_ME_EXPIRE_DAYS` | 默认 7 |
| `ADMIN_USERNAME` | 默认管理员用户名，默认 `admin` |
| `ADMIN_INITIAL_PASSWORD` | 首次启动种子 admin 密码；显式恢复时作为新密码来源 |
| `ADMIN_RESET_PASSWORD_ON_STARTUP` | 默认 `false`；显式恢复默认管理员密码时临时启用 |

见根目录 `.env.example`

---

## 9. 维护规则

API 变更时 MUST：

1. 更新本文件
2. 更新对应 `openspec/changes/*/specs/` 或归档到 `openspec/specs/`
3. 运行 `./scripts/generate-openapi-client.sh`
4. 补充 `tests/integration/api/` 或 `src/backend/tests/`

遵循：`rules/api.md`、`docs/standards/api-governance.md`

## 10. 相关标准文档

接口**清单**以本文为准；设计与治理细则见 `docs/standards/`：

| 文档 | 说明 |
|------|------|
| [standards/api-governance.md](standards/api-governance.md) | REST、统一 envelope、OpenAPI First |
| [standards/error-codes.md](standards/error-codes.md) | 错误码分段与登记表 |
| [standards/openapi-rules.md](standards/openapi-rules.md) | FastAPI 注解要求 |
| [standards/authentication.md](standards/authentication.md) | JWT 鉴权 |
| [standards/file-upload.md](standards/file-upload.md) | 上传与 MinIO |

总索引：[docs/README.md](README.md)
