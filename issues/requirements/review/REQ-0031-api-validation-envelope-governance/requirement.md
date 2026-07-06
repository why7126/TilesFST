---
requirement_id: REQ-0031-api-validation-envelope-governance
title: API 校验错误 envelope 治理扩展到管理端表单 API
terminal: web-admin
version: v1
status: approved
owner: product
source: capture.md
priority: P1
parent_requirement: REQ-0000-build-api-standard
created_at: 2026-07-05 07:57:01
updated_at: 2026-07-05 14:43:39
---

# REQ-0031 API 校验错误 envelope 治理扩展需求文档

## 1. 需求背景

项目已通过 API 治理规范要求公开 JSON API 使用统一响应结构 `{ code, message, data }`，并在用户管理等局部能力中要求校验失败不得仅返回 FastAPI / Pydantic 默认 `detail`。但当前管理端表单 API 仍存在横切风险：请求体、路径参数、查询参数或 `multipart/form-data` 参数在进入业务逻辑前触发 Pydantic 校验时，可能返回框架默认 422 响应，导致前端表单只能显示兜底文案，OpenAPI / Orval 仍生成 `HTTPValidationError.detail` 契约，日志审计与测试也难以统一判断参数错误。

本需求将统一校验错误 envelope 从“局部业务约束”提升为管理端表单 API 的治理要求，使创建、编辑、提交、上传等管理端表单场景在参数校验失败时都能返回稳定、可展示、可测试的错误结构。

## 2. 目标用户

| 用户 | 诉求 |
|---|---|
| 企业内部管理员 / 运营人员 | 表单提交失败时看到明确中文错误，而不是通用失败或技术结构。 |
| Web 前端开发 | 通过统一响应结构和 Orval 类型稳定解析错误，减少页面级兜底分支。 |
| 后端开发 | 通过统一异常处理与错误码规则处理 Pydantic 校验错误，避免各路由重复补丁。 |
| QA / 测试人员 | 用一致断言覆盖管理端表单 API 的参数校验失败场景。 |
| 运维 / 排障人员 | 在请求日志和日志审计中按统一状态码、错误码和 request_id 定位参数错误。 |

## 3. 需求目标

- 管理端表单 API 的 Pydantic / FastAPI 参数校验失败必须返回统一 envelope。
- 默认推荐保留 HTTP 422 的参数校验语义，但响应体必须为 `{ code, message, data }`。
- 字段级错误允许进入 `data.errors[]`，用于前端表单精确展示和测试断言。
- OpenAPI 与 Orval 生成结果必须表达统一错误契约，不再把默认 `HTTPValidationError.detail` 作为管理端表单错误的唯一契约。
- 现有业务 `AppError` 错误码和文案不得被回退；领域级错误仍优先返回既有业务错误码。

## 4. 范围

### 4.1 包含

| 范围 | 说明 |
|---|---|
| 管理端 JSON 表单 API | 用户、品牌、类目、SKU、规格、Banner、系统设置、个人资料、修改密码等创建 / 编辑 / 提交类接口。 |
| 管理端上传 API | 头像、品牌 Logo、Banner 图、SKU 图片 / 视频等 `multipart/form-data` 接口中由框架参数校验触发的缺文件、字段类型错误。 |
| 公共异常治理 | `RequestValidationError` 或等价 FastAPI 校验异常必须统一转换为 envelope。 |
| 错误数据结构 | 明确 `code`、`message`、`data.errors[]` 的最小字段和中文展示原则。 |
| OpenAPI / Orval | 同步导出 OpenAPI 并生成前端类型，避免管理端表单继续依赖裸 `detail`。 |
| 测试 | 后端集成测试覆盖至少 3 类代表接口，前端 API 或表单测试覆盖统一解析路径。 |
| 文档 | 同步 API 索引、API 治理细则、错误码登记和相关 OpenSpec delta。 |

### 4.2 不包含

| 不包含 | 说明 |
|---|---|
| 新增业务表单能力 | 本需求不新增用户、品牌、SKU 等具体业务字段。 |
| 重构全部前端表单 UI | 只要求统一错误解析与展示入口，不重做页面视觉。 |
| 拆分所有历史错误码 | 允许继续复用 `40001` 等既有错误码；精细拆分可作为后续治理。 |
| 修改数据库结构 | 不涉及 SQLite / MySQL 表结构、迁移或数据初始化。 |
| 修改权限模型 | 不改变 admin / employee / store_owner 权限边界。 |
| 引入 API v2 | 本需求保持 `/api/v1` 兼容，不做破坏性版本升级。 |

## 5. 功能要求

### FR-001 统一校验错误 envelope

当管理端表单 API 因 FastAPI / Pydantic 请求校验失败返回 4xx 时，响应体必须包含：

```json
{
  "code": 40001,
  "message": "请求参数无效",
  "data": {
    "errors": []
  }
}
```

实现可保留 HTTP 422；如后续决定映射为 HTTP 400，必须在 OpenSpec、docs 和测试中统一说明。无论 HTTP 状态为 400 还是 422，响应体不得仅包含框架默认 `detail`。

### FR-002 字段级错误结构

`data.errors[]` 建议包含以下最小字段：

| 字段 | 类型 | 说明 |
|---|---|---|
| `field` | string | 面向前端表单的字段路径，例如 `username`、`body.name`、`file`。 |
| `message` | string | 可展示的中文错误文案。 |
| `type` | string | Pydantic / FastAPI 错误类型或项目归一化类型。 |
| `location` | string[] | 原始校验位置，便于调试和测试。 |

错误结构不得包含密码、token、Authorization、MinIO 密钥、数据库连接串、真实文件路径或完整上传对象 key 等敏感信息。

### FR-003 错误码策略

- 通用参数校验错误默认使用 `40001`（`INVALID_PARAMETER`）或等价已登记参数错误码。
- 系统设置、个人资料、密码、上传等已有领域级 `AppError` 必须保持原错误码和 HTTP 状态，不得被通用 handler 覆盖。
- 若新增专用错误码，必须同步 `src/backend/app/core/error_codes.py` 与 `docs/standards/error-codes.md`。
- 类目最大深度等已登记 HTTP 422 业务错误仍可保留自身业务码，例如 `30023`。

### FR-004 首批接口覆盖

首批必须覆盖以下管理端表单 API：

| 模块 | 代表接口 |
|---|---|
| 用户管理 | `POST /api/v1/admin/users`、`PATCH /api/v1/admin/users/{id}`、`PATCH /api/v1/admin/users/{id}/status` |
| 品牌管理 | `POST /api/v1/admin/brands`、`PUT /api/v1/admin/brands/{id}` |
| 类目管理 | `POST /api/v1/admin/tile-categories`、`PUT /api/v1/admin/tile-categories/{id}` |
| SKU 管理 | `POST /api/v1/admin/tile-skus`、`PUT /api/v1/admin/tile-skus/{id}` |
| 规格管理 | `POST /api/v1/admin/tile-specs`、`PUT /api/v1/admin/tile-specs/{id}` |
| Banner 管理 | `POST /api/v1/admin/banners`、`PUT /api/v1/admin/banners/{id}` |
| 系统设置 | `PATCH /api/v1/admin/system-settings/{group}`、`POST /api/v1/admin/system-settings/{group}/reset` |
| 个人资料 | `PATCH /api/v1/profile/me`、`POST /api/v1/admin/profile/password` |
| 上传 | `POST /api/v1/admin/uploads/*` 中缺少文件或文件参数非法的校验失败场景 |

### FR-005 OpenAPI / Orval 契约同步

API 变更完成后必须导出 `src/web/openapi.json` 并运行 Orval。生成结果中管理端表单 API 的校验失败响应必须能表达统一错误 envelope；不得继续把默认 `HTTPValidationError.detail` 作为前端唯一错误类型来源。

### FR-006 前端错误解析

Web 管理端必须存在统一或等价的错误解析策略：

- 优先读取 envelope 的 `message` 作为全局错误提示。
- 如 `data.errors[]` 能映射到表单字段，允许展示到对应字段下方。
- 对历史业务错误码继续兼容，不得破坏现有用户名、品牌、类目、SKU、规格、Banner、系统设置、个人资料和密码弹窗的错误提示。
- 前端不得依赖裸 `detail[0].msg` 作为唯一错误来源。

### FR-007 日志与审计兼容

参数校验失败应继续被请求日志记录为 4xx 失败请求。若保留 HTTP 422，日志审计中的“422 参数校验错误”筛选必须继续可用；若改为 HTTP 400，必须同步调整日志筛选文案、测试与文档。

### FR-008 回归测试要求

后端测试至少覆盖：

- JSON body 字段缺失或类型错误时返回统一 envelope。
- 查询 / 路径 / 枚举参数非法时返回统一 envelope。
- 上传接口缺少 `file` 或文件参数非法时返回统一 envelope。
- 既有业务 `AppError`（例如用户名重复、受保护账号、文件类型不允许）不被通用校验 handler 覆盖。

前端测试至少覆盖：

- API 层或表单层可以读取 envelope `message`。
- 如存在 `data.errors[]`，字段级错误可被映射或安全降级为全局错误。

## 6. UI 约束

本需求不新增页面和视觉原型。Web 管理端错误展示必须沿用现有管理端 Design System：

- 页面 toast、弹窗内错误、字段下方错误文案必须使用既有管理端样式。
- 不得新增裸 Hex、独立浅色错误卡片或与暗色旗舰风冲突的样式。
- 表单错误展示不得导致弹窗宽度、页脚按钮或列表布局异常跳动。
- 现有业务表单的客户端校验仍可先行拦截；服务端 envelope 是最终兜底契约。

## 7. 关联需求与规范

| 类型 | 关联项 | 说明 |
|---|---|---|
| 父需求 | `REQ-0000-build-api-standard` | API 标准治理基础。 |
| 相关规范 | `openspec/specs/api-governance/spec.md` | 已要求请求校验错误不得只暴露默认 `detail`。 |
| 相关规范 | `openspec/specs/user-management/spec.md` | 用户管理已局部要求用户名校验返回统一 envelope。 |
| 相关文档 | `docs/03-api-index.md` | 需同步管理端表单错误契约。 |
| 相关文档 | `docs/standards/api-governance.md` | 需补充校验错误 envelope 细则。 |
| 相关文档 | `docs/standards/error-codes.md` | 如新增或调整错误码需同步登记。 |
| 相关经验 | `docs/knowledge-base/retrospectives/sprint-004-retrospective.md` | Sprint 004 行动项 A-007。 |

## 8. 风险与约束

| 风险 | 说明 | 缓解 |
|---|---|---|
| OpenAPI 仍生成默认 `HTTPValidationError` | 运行时已统一但前端类型仍漂移。 | 将 OpenAPI / Orval 生成结果纳入验收。 |
| 字段级错误结构过度设计 | 一次性拆分所有领域错误码会扩大范围。 | 本期只定义最小 `data.errors[]`，领域错误码拆分后续治理。 |
| 上传接口差异 | `multipart/form-data` 与 JSON body 的校验路径不同。 | 首批只要求缺文件 / 参数非法统一 envelope，不改变上传业务校验。 |
| HTTP 400 与 422 决策不一致 | 日志审计、前端筛选、测试断言可能漂移。 | 本 PRD 推荐保留 HTTP 422；若变更必须同步文档与测试。 |
| 敏感信息泄露 | 原始 Pydantic input 可能包含敏感字段。 | `data.errors[]` 不得返回原始密码、token、密钥或完整路径。 |

## 9. 状态

```text
status: approved
lifecycle_stage: review
next: /req-opsx REQ-0031-api-validation-envelope-governance
```

本需求已通过 `/req-review --approve`。进入开发前必须执行 `/req-opsx REQ-0031-api-validation-envelope-governance` 创建 OpenSpec Change。
