---
purpose: 接口文档
content: API 索引、认证接口、错误码与 Orval 维护规则
source: Sprint 001 实现 / OpenSpec auth & api-governance
update_method: API 新增或变更时同步更新；变更后运行 Orval
created_at: 2026-06-13 00:00:00
updated_at: 2026-07-21 00:00:00
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
system | dark_flagship | comfort_dark | light
```

更新主题偏好请求：

```json
{
  "theme_mode": "comfort_dark"
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
    "theme_mode": "comfort_dark"
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

列表查询参数：`page`、`page_size`（10/20/50）、`keyword`（仅匹配 `username`、`display_name`）、`role`、`status`、`login_filter`。

用户对象含 `is_protected` 与 `protected_reason`。当 `is_protected=true` 时，前端 MUST 保持编辑、重置密码、冻结/解冻、删除按钮可见但禁用，并以 `protected_reason` 作为提示。

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

`group` ∈ `basic` \| `security` \| `media` \| `notification` \| `audit`。响应 `data` 为 `{ group, data: { ...effective fields } }`；媒体分组可写 `max_image_size_mb`、`max_video_size_mb`、`max_file_size_mb`、`allowed_image_types`、`allowed_video_types`，并含只读 `minio_bucket`、`object_key_rule`。

### 3.4.2 管理端接口文档（Sprint 004）

实现：`src/backend/app/api/v1/admin_api_docs.py`  
OpenSpec：`openspec/changes/add-admin-api-docs-menu/`

| 方法 | 路径 | 认证 |
|---|---|---|
| GET | `/api/v1/admin/api-docs` | Bearer（admin） |

响应 `data.routes` 汇总 FastAPI 运行时路由，覆盖：

- `/api/v1/*` 下所有业务接口；
- `/health` 健康检查；
- `/media/{object_key:path}` 媒体直出路由（`include_in_schema=false`，不生成 Orval 方法）；
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
| GET | `/api/v1/admin/logs/{log_id}` | Bearer（admin） |
| POST | `/api/v1/usage-events` | 可选 Bearer（admin/employee 匿名均可上报） |

`GET /api/v1/admin/logs` 查询参数：

| 参数 | 说明 |
|---|---|
| `page` / `page_size` | 分页，`page_size` 1–100，默认 20 |
| `log_type` | `request` / `usage_event` / `audit` |
| `keyword` | 匹配摘要、路径、request_id、事件名、操作人 |
| `actor_user_id` | 操作人 ID |
| `client_type` | 客户端类型，如 `admin_web`、`storefront_web`、`mini_program` |
| `status_code` | HTTP 状态码 100–599 |
| `result` | `success` / `failed` |
| `resource_id` | 资源 ID，匹配 metadata |
| `path_or_request_id` | API path 或 request_id |
| `start_time` / `end_time` | ISO8601 时间字符串 |

列表响应 `data.metrics` 返回当日摘要：`today_logs`、`api_errors`、`slow_requests`、`sensitive_ops`；`data.items` 同时包含请求日志、行为事件、既有 `audit_logs` 的统一列表行。

`GET /api/v1/admin/logs/{log_id}` 返回详情抽屉数据，按 `basic`、`request`、`actor`、`operation`、`tracking`、`metadata` 分组展示，并保留 `request_id` 用于链路排查。未找到返回 `404 / code=30070`。

`POST /api/v1/usage-events` 请求体：

```json
{
  "event_name": "media_upload",
  "page_path": "/admin/tile-skus/sku_843291",
  "session_id": "sess_abc",
  "request_id": "req_79f1c2b4a8d04e31",
  "duration_ms": 1280,
  "properties": {
    "module": "SKU 管理",
    "entity_type": "tile_sku",
    "entity_id": "sku_843291",
    "changed_fields": ["gallery_images", "main_image"]
  }
}
```

`duration_ms` 为行为本身耗时毫秒数，适用于页面加载、查询、详情加载、上传、保存等有过程耗时的行为；瞬时行为可省略，列表显示 `-`。

行为事件由产品/研发人为定义 `event_name` 与属性。当前后端白名单包含：`page_view`、`search_submit`、`filter_change`、`detail_view`、`copy_request_id`、`entity_create`、`entity_update`、`entity_delete`、`status_change`、`media_upload`、`login_success`、`login_failed`、`api_error`、`product_detail_view`、`home_share`、`product_share`、`home_contact_click`、`product_contact_click`、`miniapp_home_search_click`、`miniapp_home_quick_entry_click`、`miniapp_home_new_product_click`、`miniapp_home_hot_product_click`、`miniapp_home_waterfall_product_click`、`miniapp_home_favorite_visual_click`、`miniapp_certificate_tab_click`、`certificate_list_page_view`、`certificate_list_load`、`certificate_list_refresh`、`certificate_list_load_more`、`certificate_list_retry`、`certificate_click`、`certificate_preview_click`、`certificate_load_failed`、`miniapp_home_waterfall_load`、`miniapp_home_waterfall_load_failed`、`miniapp_home_waterfall_end_reached`、`sku_detail_view`、`sku_media_swipe`、`sku_image_preview`、`sku_video_play`、`sku_favorite`、`sku_unfavorite`、`sku_share_click`、`sku_brand_click`、`sku_recommend_click`、`sku_load_error`、`category_page_view`、`primary_category_click`、`secondary_category_click`、`category_load_failed`、`product_list_page_view`、`product_list_item_exposure`、`product_list_item_click`、`product_list_filter_open`、`product_list_filter_apply`、`product_list_sort_change`、`product_list_refresh`、`product_list_load_more`、`product_list_load_failed`、`search_page_view`、`search_input`、`search_suggestion_exposure`、`search_suggestion_click`、`search_result_exposure`、`search_result_click`、`search_filter_apply`、`search_no_result`、`search_history_click`、`search_history_delete`、`search_history_clear`。后端会拒绝未定义事件、缺少必填属性或包含敏感字段（如 password、token、secret、authorization、cookie、raw_payload、raw_filename、raw_object_key、object_key、raw_response、internal_path）的上报，返回 `400 / code=40001`。

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
| GET | `/api/v1/miniapp/products` | 否 | 公开商品列表，支持 `categoryId`、`categoryLevel`、`keyword`、`brandId`、`spec`、`priceRange`、`sort`、`page`、`pageSize`，兼容 `filter_type`、`filter_value`、`section` |
| GET | `/api/v1/miniapp/search/home` | 否 | 搜索首页数据：热门搜索词；最近搜索由小程序本机保存 |
| GET | `/api/v1/miniapp/search/suggestions` | 否 | 搜索实时联想，支持 `keyword`、`scope`、`limit`、`request_id`；仅返回品牌与 SKU 联想 |
| GET | `/api/v1/miniapp/search` | 否 | 完整搜索，支持 `keyword`、`tab`、分页、品牌/类目/规格/价格筛选和 `request_id`；小程序结果页仅展示综合、品牌、SKU、证书 Tab |
| GET | `/api/v1/miniapp/products/{product_id}` | 否 | 公开商品详情 |
| GET | `/api/v1/miniapp/skus/{sku_id}` | 否 | SKU 详情聚合数据：主体、媒体、品牌、收藏状态、分享数据、同系列和同品牌推荐 |
| PUT | `/api/v1/miniapp/skus/{sku_id}/favorite` | 否 | SKU 粒度幂等设置收藏状态，body: `{ client_id, favorite }` |

`GET /api/v1/miniapp/home` 响应 `data`：

```json
{
  "store": {"name": "菲尚特瓷砖馆", "description": "质感空间，由砖而生"},
  "banners": [
    {
      "id": 1,
      "title": "质感空间，由砖而生",
      "image_url": "/media/banners/home.webp",
      "jump_type": "product",
      "target_id": 1
    }
  ],
  "shortcuts": [{"key": "select", "title": "选瓷砖", "filter_type": "all"}],
  "services": [{"key": "wechat", "title": "联系门店", "action_type": "copy_wechat"}],
  "new_products": [],
  "hot_products": []
}
```

公开商品卡片只返回允许展示字段：`product_id`、`product_name`、`sku_code`、`cover_image`、`specification`、`category_name`、`brand_name`、`style_tags`、`applicable_spaces`、`color_family`、`price_display`、`is_new`、`is_hot`。接口不得返回后台内部字段、库存管理字段、内部备注、对象存储 raw object key 或敏感配置。

`GET /api/v1/miniapp/products` 请求支持分类、搜索、品牌、规格、价格区间和排序上下文：`categoryId`、`categoryLevel=primary|secondary`、`keyword`、`brandId`、`spec`、`priceRange`（如 `100-200`、`200-`）、`sort=default|latest|price_asc|price_desc`、`page`、`pageSize`。`categoryLevel=primary` 表示聚合该一级分类下所有启用二级分类的公开 SKU，不返回仅直接挂载在一级分类下的 SKU；`categoryLevel=secondary` 或未传时保持既有二级分类精确查询语义。接口兼容旧参数 `filter_type`、`filter_value` 和 `section=new|hot`，供首页瀑布流和历史入口继续调用。响应 `data` 包含 `items`、`total`、`page`、`page_size`、`has_more` 和 `facets`；`facets` 提供可用 `brands`、`categories`、`specs`、`price_ranges` 选项。服务端只返回 `tiles.status=PUBLISHED`、`brands.status=ENABLED`、`tile_categories.status=ENABLED`、启用规格或无规格的 SKU，并过滤后台内部字段、库存管理、内部备注、未授权素材、raw object key、Authorization header、Cookie 或敏感配置。`has_more` 用于小程序商品列表页和首页全部产品瀑布流判断是否继续触底加载；若无更多数据，小程序端必须停止追加请求并展示无更多状态。

`GET /api/v1/miniapp/search/suggestions` 响应 `data` 包含 `keyword`、`normalized_keyword`、`request_id` 与 `suggestions[]`。`suggestions[]` 仅包含 `brand` 和 `sku` 类型，字段为 `id`、`text`、`entity_type`、`target_id`、`target_path`、`scope`；最近搜索、普通关键词、类目、规格和证书不得进入联想结果。

`GET /api/v1/miniapp/search` 响应 `data` 包含 `tabs[]`、`best_match`、`sections[]`、`facets`、`items`、`total`、`page`、`page_size`、`has_more` 与 `recommended_keywords`。`best_match` 可返回 `entity_type=sku|brand|certificate`：SKU 编码或 SKU 名称直接命中优先，其次品牌名精确命中，最后证书名称或证书编号精确命中；未满足上述直接命中时返回 `null`。小程序结果页按综合、品牌、SKU、证书展示 Tab，不展示类目 Tab；综合 Tab 按最佳匹配、品牌、SKU、证书顺序展示非 0 条分区，品牌/SKU/证书单独 Tab 直接展示卡片内容，不再展示分区标题和数量。完整搜索会二次过滤公开状态：只返回 `tiles.status=PUBLISHED`、`brands.status=ENABLED`、`tile_categories.status=ENABLED`、启用规格和可公开证书，不暴露后台内部字段、内部备注、raw object key 或敏感配置。v1 不新增管理端搜索配置中心、后台热门词维护、同义词维护、自然语言词典维护、搜索统计管理页或 `/api/admin/search/*`。

首页 Banner 数据来自管理端 Banner 管理能力：仅返回 `status=ONLINE`、展示端为 `MINIAPP_HOME`（管理端文案显示“小程序”）、展示位置为 `MINIAPP_HOME_CAROUSEL`（首页轮播）、且满足有效期的记录，并按 `sort_order`、`updated_at` 排序。小程序端使用 `image_url` 渲染轮播图；公开 `jump_type` 支持 `product`、`brand`、`search`、`store`、`none`，其中 `brand` 使用 `target_id` 跳转品牌详情页。若没有可用 Banner，接口可返回空数组，小程序端降级到本地默认 Hero。

`GET /api/v1/miniapp/brands` 响应 `data` 包含 `banners[]`、`items[]`、`total`、`page`、`page_size` 和 `has_more`。`banners[]` 仅来自 `MINIAPP_BRAND_LIST_CAROUSEL`（品牌列表页轮播）安全字段，支持 `jump_type=brand` + `target_id` 跳转品牌详情页；品牌列表页无轮播数据时返回空数组，不使用首页轮播兜底。`items[]` 返回启用品牌的安全字段：`brand_id`、`brand_name`、`brand_short_name`、`brand_logo_url`、`brand_entry_path`、`product_count`、`description`、`available`；`product_count=0` 的启用品牌仍可展示。接口不得返回品牌后台备注、raw object key、内部审计字段、Authorization header、Cookie 或敏感配置。

`GET /api/v1/miniapp/brands/{brand_id}` 响应 `data` 包含单品牌主页公开信息，并返回 `product_path` 与 `certificate_count` 供小程序品牌主页展示。品牌不存在、停用、无公开 SKU 或不可公开时返回 `404 / code=30030`。

`GET /api/v1/miniapp/brands/{brand_id}/certificates` 响应 `data.items[]` 只包含当前品牌可公开证书，字段为 `certificate_id`、`certificate_name`、`certificate_type`、`certificate_no`、`issuer`、`brand_name`、`file_url`。隐藏、删除、停用品牌证书不会返回；响应不得暴露 `file_key`、后台备注、审计字段、raw object key、Authorization header、Cookie 或敏感配置。

`GET /api/v1/miniapp/certificates` 响应 `data` 包含 `items[]`、`total`、`page`、`page_size` 和 `has_more`，请求仅支持分页参数 `page`、`pageSize`。`items[]` 字段为 `certificate_id`、`certificate_name`、`certificate_type`、`certificate_type_label`、`brand_id`、`brand_name`、`file_url`、`file_name`、`file_mime_type`、`file_kind`、`effective_date`、`expiry_date`、`validity_status`、`validity_status_label`；小程序证书卡片仅展示证书名称、品牌名称和证书类型。接口只返回未删除、`is_visible=true` 且所属品牌 `status=ENABLED` 的证书，排序为 `sort_order ASC, updated_at DESC, id DESC`；响应不得暴露 `file_key`、后台备注、审计字段、内部用户字段、raw object key、Authorization header、Cookie 或敏感配置。

`GET /api/v1/miniapp/categories/tree?depth=2` 响应 `data` 包含 `version` 与 `items[]`。`items[]` 只返回 `status=ENABLED` 且 `level<=2` 的类目，一级和二级分别按 `sort_order ASC, created_at ASC, id ASC` 排序；一级节点字段为 `id`、`name`、`sort`、`children`，二级节点字段为 `id`、`name`、`coverUrl`、`sort`。`coverUrl` 为兼容字段，当前小程序分类列表页不渲染二级类目图片；后端返回统一安全占位 URL `/media/miniapp/category-placeholder.webp`，不自动取 SKU 商品主图，不暴露 `description`、`sku_count`、`path`、raw object key、Authorization header、Cookie 或后台内部备注。

公开商品卡片的 `cover_image` 来自 SKU 主图（`tile_images.is_main=1` 优先），不得暴露对象存储 raw object key。`price_display` 来自 SKU `reference_price` 格式化结果：正数显示为 `¥xx.xx`，缺失、空值或非正数显示为 `暂无参考价`。

`GET /api/v1/miniapp/skus/{sku_id}` 只返回公开 SKU（`tiles.status=PUBLISHED`）字段，响应包含 `brand`、`media[]`、`image_count`、`video_count`、`category_path`、`parameters`、`favorite`、`same_series_recommendations`、`same_brand_recommendations` 和 `share`。图片、视频、品牌 Logo 与分享图 URL 必须是后端返回的安全访问 URL，响应不得包含 raw object key、库存管理字段、后台内部备注、Authorization header、Cookie 或敏感配置。SKU 不存在、下架或不可公开时返回 `404 / code=30030`。

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

品牌 Logo 上传：`POST /api/v1/admin/uploads/brand-logos`（admin/employee；JPG/PNG/WebP）。

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

列表参数：`page`、`page_size`（20/50/100）、`keyword`、`brand_id`、`type`、`validity_status`、`display_status`。响应 `data.items[]` 包含 `file_url`、`file_key`、`brand_name`、`validity_status`、`display_status`；`data.summary` 包含 `total`、`valid_count`、`expiring_soon_count`、`expired_count`。

创建/更新请求体包含 `brand_id`、`name`、`sort_order`、`type`、`file`、`is_permanent`、`effective_date`、`expiry_date`、`is_visible` 等字段；非长期有效证书必须提供 `expiry_date`。错误码：`30013` 不存在、`30014` 同品牌名称重复、`40024` 日期非法、`40025` 文件缺失、`30010` 品牌不存在。

证书文件上传：`POST /api/v1/admin/uploads/brand-certificates`（admin；JPG/PNG/WebP/PDF，20MB）。

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

列表查询参数：`page`、`page_size`（10/20/50）、`keyword`、`display_client`、`status`、`time_status`。当前 `display_client` 仅支持 `MINIAPP_HOME`（管理端显示“小程序”）；Banner 保存仅允许 `MINIAPP_HOME_CAROUSEL`（首页轮播）与 `MINIAPP_BRAND_LIST_CAROUSEL`（品牌列表页轮播）。创建/更新请求体支持 `jump_type=SKU_DETAIL|BRAND_DETAIL|EXTERNAL_LINK|TOPIC_PAGE|NO_JUMP`，其中品牌详情使用 `brand_id` 作为唯一跳转目标，图片来源可使用品牌 `logo_object_key` 对应的 `brand_logo` 或自定义上传。旧 Web 首页、专题页和历史运营位 Banner 业务记录由迁移清理，不物理删除 MinIO 对象。
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
树节点 `sku_count` 为含子级汇总；列表行 `sku_count` 为当前节点直接绑定数。管理端类目最多允许创建二级类目；`POST /api/v1/admin/tile-categories` 请求不再要求或信任客户端提交 `code`，后端创建时自动生成 `CAT-` 前缀唯一编码并在响应对象中返回。类目名称创建 / 更新时最多 10 个字符，仅允许中文、英文、数字；同一 `parent_id` 下名称重复返回 `409 / code=30024`。若 `parent_id` 指向二级类目，返回 `422 / code=30023`。

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

列表参数：`page`、`page_size`（10/20/50/100）、`keyword`、`brand_id`、`category_id`、`status`、`material_completeness`。  
响应 `data.summary`：`total`、`published_count`、`needs_completion_count`、`draft_count`。

创建请求 `save_mode`：`draft`（仅名称必填）| `create`（全必填）。  
错误码：`30031` 编码重复、`30032` 删除禁止、`30033` 上架禁止。

SKU 素材上传：`POST /api/v1/admin/uploads/tile-images`、`POST /api/v1/admin/uploads/tile-videos`（可选 `tile_id` 查询参数）。

创建/更新请求体含 `spec_id`（`save_mode=create` 必填；须为 ENABLED 规格）。  
错误码：`30031` 编码重复、`30032` 删除禁止、`30033` 上架禁止。

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

上传接口均使用 `multipart/form-data`，字段名为 `file`，成功响应 `data` 至少保持 `{ object_key, url }`；证书文件额外返回 `file_key`、`file_url`、`file_name`、`mime_type`、`size`。

| 方法 | 路径 | 认证 | 对象前缀 | 说明 |
|---|---|---|---|---|
| POST | `/api/v1/admin/uploads` | admin | `original/default/avatars/` | 头像上传 |
| POST | `/api/v1/admin/uploads/brand-logos` | admin/employee | `original/default/brands/logos/` | 品牌 Logo 上传 |
| POST | `/api/v1/admin/uploads/tile-images` | admin/employee | `original/default/tiles/{tile_id|pending}/images/` | SKU 图片上传 |
| POST | `/api/v1/admin/uploads/tile-videos` | admin/employee | `videos/default/tiles/{tile_id|pending}/` | SKU 视频上传 |
| POST | `/api/v1/admin/uploads/brand-certificates` | admin | `files/default/brand-certificates/` | 品牌证书 JPG/PNG/WebP/PDF 上传 |

媒体读取保持 `/media/{object_key}` URL 语义，由后端从 MinIO 受控读取。

上传错误：

| HTTP | code | 场景 |
|---|---|---|
| 400 | 50002 | 文件类型不允许 |
| 400 | 50003 | 文件大小超限 |
| 400 | 50004 | 品牌证书文件类型不允许 |
| 400 | 50005 | 品牌证书文件超过 20MB |
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
