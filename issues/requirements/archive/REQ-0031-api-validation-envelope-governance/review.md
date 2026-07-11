---
review_id: REV-REQ-0031-001
requirement_id: REQ-0031-api-validation-envelope-governance
date: 2026-07-05 14:43:39
participants: []
result: approved
created_at: 2026-07-05 14:43:39
updated_at: 2026-07-05 14:43:39
---

# REQ-0031 评审记录

## 评审结论

REQ-0031 评审通过，状态更新为 `approved`。

本需求作为 `REQ-0000-build-api-standard` 的治理扩展，范围聚焦于管理端表单 API 的 FastAPI / Pydantic 校验失败 envelope 化，目标、首批接口、错误结构、OpenAPI / Orval 同步、前端解析、安全边界和测试覆盖均已明确。需求不新增业务表单、不修改数据库、不调整权限模型、不引入 API v2，适合进入 `/req-opsx` 创建 OpenSpec Change。

## 评审检查清单

- [x] 范围清晰，Out of Scope 明确。
- [x] 验收标准可测试，覆盖后端、前端、OpenAPI / Orval、日志、安全和上传链路。
- [x] 优先级与依赖合理，P1，父需求为 `REQ-0000-build-api-standard`。
- [x] UI 类影响策略已决：无新增页面或视觉原型，错误展示沿用 Design System，并通过 AC-XCUT 约束管理端表单、弹窗和上传控件。
- [x] 无与现有 REQ 重复未说明；本需求明确为 API governance 的管理端表单校验错误扩展。

## 条件通过项

- [x] 后续 `/req-opsx` 必须在 OpenSpec delta 中明确默认保留 HTTP 422，若实现阶段改为 HTTP 400，必须同步 OpenSpec、docs、日志筛选和测试。
- [x] 后续实现必须同步 OpenAPI 与 Orval，避免继续以默认 `HTTPValidationError.detail` 作为管理端表单错误唯一契约。
- [x] 后续实现必须保留既有业务 `AppError` 的错误码、HTTP 状态和文案。
- [x] 后续实现必须覆盖 `multipart/form-data` 缺文件或文件参数非法场景，并保护上传控件状态机。

## 下一步

```text
/req-opsx REQ-0031-api-validation-envelope-governance
```
