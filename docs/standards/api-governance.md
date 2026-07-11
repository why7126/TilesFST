---
purpose: API 治理体系
content: REST 设计原则、URL/Method/版本、统一返回与 OpenAPI First
source: rules/api.md / build-api-standard
update_method: API 规范变更时同步更新
created_at: 2026-06-13 00:00:00
updated_at: 2026-07-11 18:51:16
---

# API 治理体系

## 设计原则

| 原则 | 说明 |
|------|------|
| REST First | 资源导向 URL，禁止动词式路径 |
| 统一资源命名 | 复数名词、kebab-case 段 |
| 幂等性 | PUT/DELETE 幂等；POST 创建非幂等 |
| 向后兼容 | 破坏性变更走 `/api/v2` |
| OpenAPI First | FastAPI 注解完整，契约即 `openapi.json` |

## URL 规范

```text
/api/v1/tiles
/api/v1/tiles/{id}
/api/v1/auth/login
/api/v1/admin/tiles
/api/v1/uploads/images
```

禁止：`/getTiles`、`/queryTileList`、`/deleteById`

## HTTP Method

| Method | 场景 |
|--------|------|
| GET | 查询、列表、详情 |
| POST | 创建、登录、上传 |
| PUT | 全量更新 |
| PATCH | 部分更新 |
| DELETE | 删除 |

## 版本

当前统一前缀：`/api/v1/*`

## 统一返回结构

成功：

```json
{ "code": 0, "message": "success", "data": {} }
```

分页 `data`：

```json
{ "items": [], "page": 1, "page_size": 20, "total": 100 }
```

错误：

```json
{ "code": 40001, "message": "invalid parameter", "data": null }
```

实现见 `src/backend/app/schemas/common.py`、`app/core/exceptions.py`。

### 管理端表单校验错误

管理端表单、弹窗和上传 API 在 FastAPI / Pydantic 请求校验失败时 MUST 保留 HTTP 422，并返回统一响应信封，不得只暴露框架默认 `detail`：

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

`data.errors[]` 只允许返回 `field`、`message`、`type`、`location` 等可展示和排障字段，MUST NOT 返回原始密码、token、Authorization、MinIO 凭据、数据库连接串、真实文件路径、完整对象 key 或原始上传文件内容。

业务 `AppError` 优先级高于通用校验 handler；用户名重复、受保护账号、文件类型不允许等业务错误 MUST 保留原 HTTP 状态、错误码和文案。

## 错误码

见 `docs/standards/error-codes.md`、`src/backend/app/core/error_codes.py`。

## OpenAPI 与 Orval

1. 后端路由 MUST 设置 `response_model`、`summary`、`description`、`tags`
2. 导出 OpenAPI：`src/web/openapi.json`
3. 生成客户端：`./scripts/generate-openapi-client.sh`
4. 前端禁止手写接口类型

主题偏好、个人资料等当前用户 self-service 接口也属于 API contract：新增字段（如 `UserProfile.theme_mode`）或新增路径（如 `PATCH /api/v1/auth/me/theme`）必须同步 OpenAPI、Orval、`docs/03-api-index.md` 与相关前后端测试。

## API Docs / Swagger Checklist

后续 API docs refine、接口文档页模板化、Swagger 入口调整、Web 代理调整或生产部署文档调整时，Change 的 design、acceptance 或 trace MUST 记录：

| 检查项 | 要求 |
|---|---|
| 同源入口 | Swagger 主入口使用 `/docs` 或经 design 说明的等价同源 Web 路径；不得硬编码 `localhost:8000`、`backend:8000`、容器服务名或端口 |
| 行级深链 | 仅 `included_in_openapi=true` 且存在可用 `operation_id` 的路由可跳转；deep link 使用 `/docs#/{tag}/{operationId}` 或等价安全编码路径 |
| 不可跳转路由 | 非 OpenAPI 路由或缺失 `operation_id` 的路由保持可见但不可点击，不跳到通用 `/docs` |
| 代理路径 | 明确 `/docs`、`/redoc`、`/openapi.json` 与 Swagger UI 所需后端文档资源是否由 Web 层代理，且不被 SPA fallback 接管 |
| 环境矩阵 | 记录 Vite dev proxy、Docker Web Nginx、生产反向代理或生产等价 N/A 原因 |
| 生产门禁 | 生产文档 MAY 可见，但 `Try It Out` MUST 禁用、隐藏或保持只读，并由后端环境策略兜底 |
| 安全边界 | 链接、hash、query、localStorage 新键、页面文案和验收记录不得包含 token、JWT Secret、数据库 DSN、MinIO 凭据或真实环境变量值 |
| Orval 判断 | 说明是否新增或修改 API contract；若有 contract 变化，必须重新导出 OpenAPI 并运行 Orval；若无变化，明确记录无需 Orval |

## 鉴权

见 `docs/standards/authentication.md` — JWT，`Authorization: Bearer <token>`

## 文件上传

见 `docs/standards/file-upload.md` — `multipart/form-data`，后端授权 + MinIO

## 校验

```bash
python scripts/validate-api-standard.py
```

## 相关文档

- `rules/api.md`
- `docs/03-api-index.md`
- `docs/standards/openapi-rules.md`
- `docs/standards/error-codes.md`
