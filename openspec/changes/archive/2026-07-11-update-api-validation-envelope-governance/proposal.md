## Why

管理端表单 API 仍可能在进入业务逻辑前返回 FastAPI / Pydantic 默认 422 `detail`，导致前端表单错误展示、OpenAPI / Orval 类型和测试断言出现横切漂移。REQ-0031 已评审通过，需要把统一错误 envelope 从局部用户管理约束扩展为管理端创建、编辑、提交、上传类接口的治理契约。

## What Changes

- 管理端表单 API 的框架请求校验失败 MUST 返回统一 `{ code, message, data }` envelope，默认保留 HTTP 422 参数校验语义。
- `data.errors[]` SHOULD 提供字段级错误信息，至少覆盖 `field`、`message`、`type`、`location`，并过滤敏感输入、密钥、真实路径和完整对象 key。
- 既有业务 `AppError`、领域错误码、HTTP 状态和文案 MUST 不被通用校验 handler 覆盖。
- OpenAPI / Orval MUST 表达统一校验错误契约，管理端表单 API 不得继续把默认 `HTTPValidationError.detail` 作为前端唯一契约。
- Web 管理端 MUST 通过统一或等价错误解析策略优先读取 envelope `message`，并安全处理 `data.errors[]` 字段错误。
- 后端、前端、OpenAPI / Orval、文档和日志审计相关测试要求同步纳入变更任务。

## Capabilities

### New Capabilities

- 无。

### Modified Capabilities

- `api-governance`: 扩展统一响应信封、OpenAPI / Orval、错误码和日志安全治理要求，覆盖管理端表单 API 与 multipart 上传参数校验失败。
- `web-client`: 增加管理端表单和上传控件对统一校验错误 envelope 的解析、字段错误映射和稳定展示要求。
- `testing`: 增加管理端表单校验错误 envelope 的后端、前端、OpenAPI / Orval 与安全回归测试要求。

## Impact

- 后端：FastAPI 全局 `RequestValidationError` 或等价校验异常处理、错误模型、OpenAPI response metadata、请求日志兼容性。
- Web 管理端：Axios / Orval 错误解析、表单字段错误映射、toast / inline 错误 / 上传失败态。
- API：管理端 JSON 表单和 `multipart/form-data` 上传接口的 422 响应体契约变化；不引入 `/api/v2`。
- 数据库：不涉及 SQLite / MySQL schema、迁移或初始化数据。
- 存储：不改变 MinIO 单桶策略、对象 key 生成和授权上传链路。
- 小程序：无影响。
- 测试与文档：需要补充 pytest、Vitest 或等价前端测试、OpenAPI / Orval 生成检查、API 治理文档和错误码文档同步检查。
