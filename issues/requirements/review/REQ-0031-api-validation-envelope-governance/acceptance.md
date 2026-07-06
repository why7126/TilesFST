---
title: API 校验错误 envelope 治理扩展到管理端表单 API - Acceptance Criteria
purpose: 定义 REQ-0031 进入评审、OpenSpec 转化和后续实现验收所需的可测试标准
content: 功能验收、接口验收、前端验收、安全验收、横切知识库验收
source: requirement.md
update_method: /req-complete 生成；后续经 /req-review 调整
owner: product
status: pending_review
created_at: 2026-07-05 14:37:08
updated_at: 2026-07-05 14:37:08
---

# Acceptance Criteria

## 1. API envelope

| ID | 验收标准 | 验证方式 |
|---|---|---|
| AC-001 | 管理端表单 API 的 FastAPI / Pydantic 请求校验失败 MUST 返回项目统一 envelope。 | 后端集成测试触发缺字段、类型错误、非法枚举。 |
| AC-002 | 校验失败响应体 MUST 包含 `code`、`message`、`data`，不得只包含默认 `detail`。 | 后端测试断言 JSON 根字段。 |
| AC-003 | 默认 SHOULD 保留 HTTP 422；如改为 HTTP 400，MUST 同步 OpenSpec、docs、日志筛选与测试。 | 评审记录和测试断言。 |
| AC-004 | `data.errors[]` SHOULD 包含 `field`、`message`、`type`、`location` 最小字段。 | 后端测试断言代表错误项。 |
| AC-005 | 既有业务 `AppError` MUST 保持原错误码、HTTP 状态和文案，不得被通用校验 handler 覆盖。 | 用户名重复、受保护账号、文件类型不允许等回归测试。 |

## 2. 首批接口覆盖

| ID | 验收标准 | 验证方式 |
|---|---|---|
| AC-006 | 用户管理 `POST /api/v1/admin/users`、`PATCH /api/v1/admin/users/{id}`、`PATCH /api/v1/admin/users/{id}/status` 的框架校验失败 MUST 返回统一 envelope。 | 后端集成测试。 |
| AC-007 | 品牌、类目、SKU、规格、Banner 创建与编辑接口的框架校验失败 MUST 返回统一 envelope。 | 后端集成测试或参数化测试。 |
| AC-008 | 系统设置、个人资料、修改密码接口的框架校验失败 MUST 返回统一 envelope。 | 后端集成测试。 |
| AC-009 | `POST /api/v1/admin/uploads/*` 中缺少文件或文件参数非法的框架校验失败 MUST 返回统一 envelope。 | multipart 边界测试。 |

## 3. OpenAPI / Orval

| ID | 验收标准 | 验证方式 |
|---|---|---|
| AC-010 | OpenAPI MUST 表达管理端表单 API 的统一校验错误 envelope 契约。 | 检查 `src/web/openapi.json` 或导出结果。 |
| AC-011 | Orval 生成结果 MUST 不再把默认 `HTTPValidationError.detail` 作为管理端表单错误的唯一契约来源。 | 运行 `scripts/generate-openapi-client.sh` 后检查生成类型。 |
| AC-012 | API 契约变更完成后 MUST 提交 OpenAPI 与 Orval 生成文件。 | git diff 与 CI 检查。 |

## 4. Web 管理端错误展示

| ID | 验收标准 | 验证方式 |
|---|---|---|
| AC-013 | Web 管理端错误解析 MUST 优先读取 envelope `message` 作为全局错误提示。 | 前端单元测试或组件测试。 |
| AC-014 | 如存在 `data.errors[]`，Web SHOULD 映射到字段错误；无法映射时 MUST 安全降级为全局错误。 | 前端测试覆盖可映射和不可映射两类场景。 |
| AC-015 | Web 管理端 MUST 不依赖裸 `detail[0].msg` 作为唯一错误来源。 | 代码审查和前端测试。 |
| AC-016 | 错误展示 MUST 沿用现有 Design System，不新增裸 Hex、独立错误卡片或破坏暗色旗舰风的样式。 | 代码审查和 UI 回归检查。 |

## 5. 安全、日志与兼容性

| ID | 验收标准 | 验证方式 |
|---|---|---|
| AC-017 | 错误响应 MUST 不包含密码、token、Authorization、MinIO 密钥、数据库连接串、真实文件路径或完整上传对象 key。 | 后端安全负例测试或审查清单。 |
| AC-018 | 参数校验失败 MUST 继续进入请求日志，并保留 request_id、路径、方法、状态码和项目错误码等排障信息。 | 请求日志测试或人工验证。 |
| AC-019 | 本需求 MUST 不修改 SQLite 表结构、迁移、权限模型、MinIO 单桶策略或 `/api/v1` 路径。 | 代码审查和迁移目录检查。 |
| AC-020 | 如新增或调整错误码，MUST 同步 `src/backend/app/core/error_codes.py` 与 `docs/standards/error-codes.md`。 | 文档与代码 diff 检查。 |

## 6. 测试覆盖

| ID | 验收标准 | 验证方式 |
|---|---|---|
| AC-021 | 后端测试 MUST 覆盖 JSON body 字段缺失或类型错误、路径 / 查询 / 枚举参数非法、multipart 缺文件或文件参数非法。 | pytest。 |
| AC-022 | 后端测试 MUST 覆盖至少一个既有业务 `AppError` 不被通用校验 handler 覆盖。 | pytest。 |
| AC-023 | 前端测试 MUST 覆盖 envelope `message`、`data.errors[]` 字段映射和全局兜底。 | vitest 或现有前端测试框架。 |
| AC-024 | API 变更后 SHOULD 运行目录结构校验、相关后端测试、前端类型生成和前端测试。 | CI 或本地命令记录。 |

## 7. 横切 AC（knowledge-base）

横切验收来源：

- `docs/knowledge-base/best-practices/admin-form-page-consistency.md`
- `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md`
- `docs/knowledge-base/best-practices/admin-media-upload-chain.md`
- `docs/knowledge-base/retrospectives/sprint-004-retrospective.md`

| ID | 标签 | 验收标准 | 验证方式 |
|---|---|---|---|
| AC-XCUT-001 | admin-form | 受影响的管理端表单错误展示 MUST 使用稳定的 toast、字段错误或固定错误区，不得导致表单主体、页脚或按钮布局明显跳动。 | UI 回归检查或组件测试。 |
| AC-XCUT-002 | admin-form | 若实现阶段触及完整页面表单，MUST 保持单一保存 CTA 规则，不得在 header 与 footer 同时新增重复保存入口。未触及页面表单时记录为 N/A。 | 代码审查。 |
| AC-XCUT-003 | admin-form | 若实现阶段触及重置或脏数据离开流程，MUST 使用 DS 弹窗能力，不得新增 `window.confirm` / `window.alert` 处理校验错误。未触及时记录为 N/A。 | 代码审查和 UI 检查。 |
| AC-XCUT-004 | admin-modal | 若实现阶段触及弹窗内错误展示，TSX MUST 不同时使用基础 `modal-card` 与功能特定 modal class，避免 CSS specificity 互相覆盖。 | 代码审查。 |
| AC-XCUT-005 | admin-modal | 弹窗错误展示 MUST 不改变既有弹窗计算宽度与短视口滚动行为。未触及弹窗时记录为 N/A。 | Playwright 或人工截图检查。 |
| AC-XCUT-006 | media-upload | 上传校验错误 envelope MUST 不破坏上传控件 `idle → uploading → done/failed` 状态机。 | 前端测试或手工上传回归。 |
| AC-XCUT-007 | media-upload | 上传失败展示 MUST 保持在上传控件固定错误区或稳定 toast 中；成功上传的同会话预览 MUST 不受失败分支影响。 | 前端测试或手工上传回归。 |
| AC-XCUT-008 | media-upload | 实现阶段 SHOULD 覆盖 Docker Web `:3000` 边界下的缺文件 / 非法文件参数验证；若未执行，MUST 在验收记录中说明原因。 | Docker 或本地验证记录。 |
| AC-XCUT-009 | sprint-retro | 本需求实现 MUST 回应 Sprint 004 A-007 行动项：请求校验错误不得只暴露默认 `detail`，并应沉淀到 API governance 文档。 | docs diff 与 OpenSpec delta 检查。 |

## 8. 退出条件

- `capture.md`、`requirement.md`、`user-stories.md`、`business-flow.md`、`acceptance.md`、`trace.md` 均存在且状态一致。
- `trace.md` 记录父需求、知识库引用、横切标签和原型策略。
- 本需求通过 `/req-review` 后，方可执行 `/req-opsx REQ-0031-api-validation-envelope-governance`。
- 未经 OpenSpec Change，不得直接修改 `src/`、`openspec/specs/` 或生成 Orval 产物。
