## Context

REQ-0031 要求管理端表单 API 在请求体、路径参数、查询参数或 `multipart/form-data` 参数校验失败时，返回项目统一 envelope，而不是只暴露 FastAPI / Pydantic 默认 `detail`。现有 `api-governance` 已要求公共 JSON API 使用 `{ code, message, data }`，`user-management` 也已有用户名校验的局部要求；本变更把该要求提升为管理端表单 API 的横切治理。

本需求无新增页面或视觉 prototype。原型与验收优先级冲突报告如下：

| 来源 | 结论 |
|---|---|
| `prototype/web/` | 不存在，N/A。 |
| PNG Golden Reference | 不存在，N/A。 |
| `*-context.md` | 不存在，N/A。 |
| `acceptance.md` | 作为本次 UI 展示、上传状态机、OpenAPI / Orval 和测试验收的最高具体来源。 |
| `rules/ui-design.md` | 约束 Web 管理端错误展示必须复用现有暗色 Design System，不新增裸 Hex 或独立错误卡片。 |
| `openspec/specs` | 作为现有能力基线；本 change 通过 delta spec 扩展。 |

## Goals / Non-Goals

**Goals:**

- 为管理端表单 API 建立统一校验错误 envelope，默认 HTTP 422，响应体包含 `code`、`message`、`data`。
- 为 `data.errors[]` 定义最小字段和敏感信息过滤边界。
- 保持业务 `AppError` 优先级，避免通用 handler 覆盖领域错误码。
- 让 OpenAPI / Orval、Web 错误解析、后端测试和前端测试对齐同一契约。
- 覆盖首批管理端表单接口：用户、品牌、类目、SKU、规格、Banner、系统设置、个人资料、修改密码和上传。

**Non-Goals:**

- 不新增具体业务表单字段、页面或弹窗。
- 不重构全部前端表单视觉。
- 不修改数据库结构、权限模型、MinIO 单桶策略或 `/api/v1` 路径。
- 不强制拆分所有历史业务错误码；除非实现新增错误码，否则沿用现有 `INVALID_PARAMETER` 或等价错误码。

## Decisions

### D1. UI 策略：Design System 兼容，不做 prototype port

本需求没有 HTML / PNG prototype，且 UI 影响集中在错误提示呈现。实现阶段 SHOULD 复用现有管理端 fixed toast、弹窗 inline 错误、字段错误或上传控件固定错误区；MUST 遵守 `rules/ui-design.md` semantic token 和既有组件边界。

替代方案是新增专用错误卡片或重做表单错误样式，但这会扩大 UI 范围并增加管理端弹窗宽度、短视口滚动和上传状态机回归风险，因此不采用。

### D2. 保留 HTTP 422，统一响应体 envelope

框架校验错误继续使用 HTTP 422 作为默认状态，以保留参数校验语义和日志审计筛选稳定性。响应体主契约改为：

```json
{
  "code": 40001,
  "message": "请求参数无效",
  "data": {
    "errors": []
  }
}
```

若后续实现决定映射为 HTTP 400，必须同步 OpenSpec、docs、日志筛选、测试断言和 OpenAPI / Orval 契约。

### D3. 全局校验异常 handler 只处理框架校验错误

实现阶段 SHOULD 在 FastAPI 全局异常处理层处理 `RequestValidationError` 或等价框架校验异常，并把字段路径、错误类型和归一化中文文案写入 `data.errors[]`。业务 `AppError`、认证授权错误、上传业务校验错误和领域错误码必须走既有路径，避免被通用参数错误覆盖。

### D4. OpenAPI / Orval 以 envelope 为管理端表单错误主契约

管理端表单 API 的 422 response metadata SHOULD 指向统一错误响应模型或等价 schema。导出 `src/web/openapi.json` 并运行 Orval 后，前端不应只看到默认 `HTTPValidationError.detail` 作为错误类型来源。生成物不得手工修改。

### D5. 字段级错误安全过滤

`data.errors[]` 只返回字段路径、可展示文案、错误类型和必要 location。实现不得返回原始密码、token、Authorization、MinIO 密钥、数据库连接串、真实文件路径、完整对象 key 或原始 multipart 文件内容。

## Risks / Trade-offs

- OpenAPI 已更新但运行时 handler 未覆盖 multipart → 通过上传缺文件和非法文件参数测试覆盖。
- 通用 handler 覆盖业务 `AppError` → 通过用户名重复、受保护账号、文件类型不允许或等价业务错误回归测试覆盖。
- 字段路径与前端表单字段不完全一致 → 前端无法映射时必须降级为全局 toast 或弹窗内固定错误区。
- HTTP 422 与 HTTP 400 决策漂移 → 默认保留 422；任何变更必须同步 docs、OpenSpec、日志和测试。
- 错误详情泄露敏感输入 → 后端错误归一化时过滤输入值，测试或审查清单覆盖敏感字段。

## Migration Plan

1. 实现统一校验错误模型和 `RequestValidationError` handler。
2. 为首批管理端表单 API 补齐 422 envelope response metadata。
3. 更新 Web 管理端错误解析，优先读取 envelope `message`，再处理 `data.errors[]`。
4. 导出 OpenAPI 并运行 Orval。
5. 补充后端、前端、安全和 OpenAPI / Orval 回归测试。
6. 更新 `docs/03-api-index.md`、`docs/standards/api-governance.md`，如新增错误码则同步 `docs/standards/error-codes.md` 与 `error_codes.py`。

回滚时可保留业务 `AppError` 路径不变，撤回全局校验 handler 和 422 response metadata；但回滚必须同步 OpenAPI / Orval 和前端错误解析，避免契约不一致。

## Open Questions

- 是否需要在实现阶段保留兼容性 `detail` 字段：允许保留，但统一 envelope 必须是文档、前端和测试主契约。
- 字段级中文文案是否按字段定制：本期只要求可展示中文和最小结构，字段定制可在后续治理细化。
