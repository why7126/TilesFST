---
req_id: REQ-0031-api-validation-envelope-governance
status: captured
created_at: 2026-07-04 21:52:59
updated_at: 2026-07-04 21:52:59
recorded_by: product
source: 用户输入
priority_hint: P1
parent_requirement: REQ-0000-build-api-standard
---

# 一句话

将统一 422 参数校验错误 envelope 设计扩展到所有管理端表单 API，确保管理端表单校验失败时均返回 `{ code, message, data }`，避免 FastAPI 默认 `detail` 结构泄漏到前端交互。

# 原始描述

/req-capture API validation envelope governance 将统一 422 envelope 设计扩展到所有管理端表单 API

补充上下文：

- 当前 API 治理要求统一响应结构 `{ code, message, data }`，但部分 Pydantic 参数校验仍可能返回 FastAPI 默认 422 `detail`。
- 管理端表单 API 覆盖用户、品牌、类目、SKU、规格、Banner、系统设置、个人资料、修改密码、上传等创建/编辑/提交类接口。
- 需求目标是统一后端校验错误 envelope，并让前端 Orval 类型、表单错误提示、接口文档和测试用例保持一致。
- 本需求属于 API 治理与错误码治理延展，不直接新增业务表单能力。

# 待澄清

- [ ] 统一 422 envelope 是否保持 HTTP 422，还是将 Pydantic 校验失败映射为 HTTP 400 + `40001`；若两者并存，需要明确边界。
- [ ] 字段级错误是否放入 `data.errors[]`，以及字段路径、错误类型、用户可读文案的结构是否需要稳定成 OpenAPI Schema。
- [ ] “所有管理端表单 API”的首批范围是否包含 `multipart/form-data` 上传接口、密码修改、系统设置 PATCH、个人资料 PATCH。
- [ ] 是否需要新增专用错误码，或继续复用 `40001` / 领域级 `400xx` 错误码。
- [ ] 前端表单是否需要统一从 envelope 中解析字段级错误并回填到控件下方。

# 探索结论

（/req-explore 后人工确认写入）
