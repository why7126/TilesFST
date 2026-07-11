---
title: API 校验错误 envelope 治理扩展到管理端表单 API - Business Flow
purpose: 描述管理端表单 API 校验失败从请求、异常处理、响应、前端展示到测试验证的端到端流程
content: 业务流程、异常边界、OpenAPI/Orval 同步、日志与上传链路
source: requirement.md
update_method: /req-complete 生成；后续经 /req-review 调整
owner: product
status: pending_review
created_at: 2026-07-05 14:37:08
updated_at: 2026-07-05 14:37:08
---

# Business Flow

## 1. 总览

```text
管理端表单 / 弹窗 / 上传控件
  ↓
POST / PUT / PATCH / multipart 请求
  ↓
FastAPI 路由参数、Pydantic Schema、UploadFile 参数校验
  ↓
校验通过 ─────────────→ 进入业务逻辑 → 成功 envelope 或既有 AppError
  ↓ 校验失败
统一 RequestValidationError handler
  ↓
HTTP 422 + { code, message, data.errors[] }
  ↓
请求日志记录 4xx、request_id、错误码
  ↓
OpenAPI 导出 + Orval 客户端类型同步
  ↓
Web 管理端错误解析
  ↓
toast / 字段错误 / 弹窗内错误 / 上传控件失败态
```

## 2. 框架校验错误处理流程

1. 管理员在管理端提交创建、编辑、状态变更、系统设置、个人资料、密码或上传表单。
2. 请求到达 FastAPI 后，路由参数、查询参数、请求体 Schema 或 multipart 参数先由框架校验。
3. 若校验失败，框架抛出 `RequestValidationError` 或等价校验异常。
4. 后端全局异常处理器将原始错误归一化为项目 envelope：

```json
{
  "code": 40001,
  "message": "请求参数无效",
  "data": {
    "errors": [
      {
        "field": "body.name",
        "message": "名称不能为空",
        "type": "missing",
        "location": ["body", "name"]
      }
    ]
  }
}
```

5. HTTP 状态默认保留 422，以维持参数校验语义和日志筛选稳定。
6. 响应不得包含裸 `detail` 作为唯一错误结构；如保留 `detail` 兼容字段，统一 envelope 仍必须是前端与文档主契约。

## 3. 业务错误边界

| 错误来源 | 示例 | 处理原则 |
|---|---|---|
| 框架请求校验 | 缺少必填字段、字段类型错误、路径参数非法、上传缺文件 | 统一转换为参数错误 envelope，默认 HTTP 422。 |
| 业务 `AppError` | 用户名重复、受保护账号、文件类型不允许、类目最大深度 | 保持原错误码、HTTP 状态和文案，不被通用 handler 覆盖。 |
| 未预期异常 | 代码错误、外部依赖异常 | 沿用现有 5xx 错误治理，不纳入本需求范围。 |

## 4. OpenAPI 与 Orval 同步流程

1. 后端实现统一校验错误响应模型。
2. OpenAPI schema 中体现管理端表单 API 的 422 envelope 响应。
3. 运行 OpenAPI 导出脚本，更新 `src/web/openapi.json`。
4. 运行 Orval 生成前端客户端与类型。
5. 前端接口调用与错误解析以统一 envelope 为主契约，避免继续依赖 `HTTPValidationError.detail`。

## 5. 前端展示流程

1. Web 管理端收到 Axios / Orval 请求错误。
2. 统一错误解析函数读取响应体：
   - 优先读取 `message` 作为全局提示。
   - 若存在 `data.errors[]`，尝试按字段名映射到表单字段。
   - 无法映射字段时，降级为 toast 或弹窗内固定错误区。
3. 现有业务错误码仍按既有路径展示，不因本需求变成通用文案。
4. 表单错误展示必须沿用 Design System，不新增裸 Hex 或独立视觉体系。

## 6. 上传链路

1. 管理端上传控件构造 `multipart/form-data` 请求。
2. 若缺少 `file` 或文件参数类型非法，由框架校验进入统一 envelope。
3. 若文件存在但 MIME、大小、业务规则不允许，由既有上传业务错误处理，保持领域错误码。
4. 前端上传控件保持 `idle → uploading → done/failed` 状态机。
5. 失败时展示 envelope `message` 或上传业务错误文案；成功时同会话预览不受影响。

## 7. 与父需求边界

| 项目 | REQ-0000-build-api-standard | REQ-0031 本需求 |
|---|---|---|
| 定位 | 建立 API 治理基础规范 | 将校验错误 envelope 扩展为管理端表单 API 的具体治理要求 |
| 覆盖 | 通用统一响应、错误码、OpenAPI、Orval | 管理端创建/编辑/提交/上传类表单校验失败 |
| 输出 | 标准和基础能力 | 可实施的接口清单、错误结构、前端解析和测试验收 |
| 风险重点 | 项目整体契约一致性 | FastAPI 默认 422 `detail` 漂移、前端表单兜底错误、multipart 差异 |

## 8. 日志与审计流程

1. 参数校验失败作为 4xx 请求进入请求日志。
2. 默认保留 HTTP 422，便于继续筛选“参数校验错误”。
3. 日志中记录 request_id、路径、方法、状态码和项目错误码。
4. 错误响应和日志均不得记录密码、token、Authorization、MinIO 密钥、数据库连接串、真实文件路径或完整对象 key。

## 9. 不涉及流程

- 不新增业务表单字段或权限模型。
- 不修改 SQLite 表结构、迁移或样例数据。
- 不改变 MinIO 单桶策略和对象 key 生成规则。
- 不创建新的 Web 页面、弹窗组件或 Design System 组件。
- 不引入 `/api/v2` 或破坏现有 `/api/v1` 路径。
