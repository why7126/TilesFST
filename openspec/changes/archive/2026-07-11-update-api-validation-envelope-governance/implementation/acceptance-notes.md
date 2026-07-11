---
title: API 校验错误 Envelope 实现验收记录
purpose: 记录 update-api-validation-envelope-governance 实现阶段验证结果与 N/A 理由
content: 测试、OpenAPI/Orval、Docker Web smoke 记录
source: /opsx-apply update-api-validation-envelope-governance
update_method: 实现验证变化时更新
created_at: 2026-07-11 10:00:30
updated_at: 2026-07-11 10:00:30
---

# 实现验收记录

## 已验证

| 项 | 结果 | 命令 / 说明 |
|---|---|---|
| 后端校验 envelope | pass | `uv run pytest tests/integration/api/test_validation_envelope.py` |
| 前端错误解析 | pass | `pnpm --dir src/web exec vitest run src/shared/api/error-envelope.test.ts` |
| API governance | pass | `python scripts/validate-api-standard.py` |
| OpenSpec | pass | `openspec validate update-api-validation-envelope-governance --strict` |
| OpenAPI / Orval | pass | `./scripts/generate-openapi-client.sh` |

## Docker Web `:3000` 上传校验 Smoke

N/A。本次实现未改 Docker Web Nginx、上传大小限制、MinIO 链路或前端上传状态机，只统一 FastAPI/Pydantic 缺 `file` 等请求校验错误 envelope，并已用后端集成测试覆盖 `POST /api/v1/admin/uploads/brand-logos` 缺文件返回 `422 / code=40001`。Docker Web `:3000` 端到端上传边界可在包含 Nginx 或上传容量配置变更的后续 change 中执行。
