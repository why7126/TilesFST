---
purpose: 接口文档
content: API 索引、认证接口、错误码与 Orval 维护规则
source: Sprint 001 实现 / OpenSpec auth & api-governance
update_method: API 新增或变更时同步更新；变更后运行 Orval
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
| 瓷砖（展示） | `/api/v1/tiles` | 否 | 列表、详情 | 桩实现（返回空/示例） |
| 管理端瓷砖 | `/api/v1/admin/tiles` | 是（admin/employee） | 创建瓷砖 | 桩实现 |
| 管理端用户 | `/api/v1/admin/users` | 是（仅 admin） | 用户 CRUD、状态、重置密码 | ✓ Sprint 002 |
| 管理端系统设置 | `/api/v1/admin/system-settings` | 是（仅 admin） | 分组配置 GET/PATCH/reset、审计 recent | ✓ Sprint 003 |
| 管理端品牌 | `/api/v1/admin/brands` | 是（admin/employee） | 品牌 CRUD、启停、条件删除 | ✓ Sprint 002 |
| 管理端 Banner | `/api/v1/admin/banners` | 是（admin/employee） | Banner CRUD、上下线、条件删除、summary | ✓ Sprint 003 |
| 管理端专题（只读） | `/api/v1/admin/topics` | 是（admin/employee） | 专题列表（Banner 跳转关联） | ✓ Sprint 003 |
| 管理端类目 | `/api/v1/admin/tile-categories` | 是（admin/employee） | 类目树、CRUD、启停、条件删除 | ✓ Sprint 002 |
| 管理端 SKU | `/api/v1/admin/tile-skus` | 是（admin/employee） | SKU CRUD、上下架、素材、筛选 summary | ✓ Sprint 002 |
| 管理端规格 | `/api/v1/admin/tile-specs` | 是（admin/employee） | 瓷砖规格 CRUD、启停、条件删除、summary | ✓ Sprint 003 |
| 管理端上传 | `/api/v1/admin/uploads` | 是 | 头像（admin/employee）；品牌 Logo、Banner 图、SKU 图片/视频（admin/employee） | ✓ Sprint 002/003，MinIO 单桶存储 |
| 媒体 | `/api/v1/media` | — | 规划中的统一媒体 API | 未实现 |

\* `uploads` 路由通过后端鉴权接口写入 `MINIO_BUCKET`，不允许前端直连未授权 MinIO。

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

创建成功 `data` 含 `user` 与一次性 `initial_password`。

### 3.4.1 管理端系统设置（Sprint 003）

实现：`src/backend/app/api/v1/admin_system_settings.py`  
OpenSpec：`openspec/changes/add-system-settings/`

| 方法 | 路径 | 认证 |
|---|---|---|
| GET | `/api/v1/admin/system-settings/{group}` | Bearer（admin） |
| PATCH | `/api/v1/admin/system-settings/{group}` | Bearer（admin） |
| POST | `/api/v1/admin/system-settings/{group}/reset` | Bearer（admin） |
| GET | `/api/v1/admin/system-settings/audit/recent` | Bearer（admin） |

`group` ∈ `basic` \| `security` \| `media` \| `notification` \| `audit`。响应 `data` 为 `{ group, data: { ...effective fields } }`；媒体分组含只读 `minio_bucket`、`object_key_rule`。

### 3.5 管理端品牌（Sprint 002）

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

列表查询参数：`page`、`page_size`（10/20/50）、`keyword`、`display_client`、`status`、`time_status`。  
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

列表参数：`page`、`page_size`（10/20/50）、`keyword`、`status`、`level`、`parent_id`（含子孙扁平分页）。  
树节点 `sku_count` 为含子级汇总；列表行 `sku_count` 为当前节点直接绑定数。

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

校验错误码：`40020`（原密码错误）、`40021`（策略）、`40022`（弱密码）、`40023`（与原密码相同）、`42901`（限流）。

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

上传接口均使用 `multipart/form-data`，字段名为 `file`，成功响应 `data` 保持 `{ object_key, url }`。

| 方法 | 路径 | 认证 | 对象前缀 | 说明 |
|---|---|---|---|---|
| POST | `/api/v1/admin/uploads` | admin | `original/default/avatars/` | 头像上传 |
| POST | `/api/v1/admin/uploads/brand-logos` | admin/employee | `original/default/brands/logos/` | 品牌 Logo 上传 |
| POST | `/api/v1/admin/uploads/tile-images` | admin/employee | `original/default/tiles/{tile_id|pending}/images/` | SKU 图片上传 |
| POST | `/api/v1/admin/uploads/tile-videos` | admin/employee | `videos/default/tiles/{tile_id|pending}/` | SKU 视频上传 |

媒体读取保持 `/media/{object_key}` URL 语义，由后端从 MinIO 受控读取。

上传错误：

| HTTP | code | 场景 |
|---|---|---|
| 400 | 50002 | 文件类型不允许 |
| 400 | 50003 | 文件大小超限 |
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
