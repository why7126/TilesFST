## Why

Web 管理端已经在日志审计 `request_id` 复制和重置密码随机密码复制中分别处理 Clipboard API 成功、失败、API 不存在和手动复制兜底。复制逻辑继续散落会导致文案漂移、失败路径漏测，以及敏感内容被误写入日志或埋点的风险。

本 change 将 REQ-0032 评审通过的 Clipboard 复制交互沉淀为共享 helper / best-practice，确保后续新增复制入口先复用统一结果模型和测试口径。

## What Changes

- 新增 Web 管理端共享 Clipboard 复制 helper 能力，规范 `success`、`failed`、`unavailable`、`empty` 等结构化结果。
- 约束 helper 与 UI 解耦：helper 不直接绑定 toast、dialog、埋点或业务 DOM；调用方负责业务文案与副作用。
- 增加手动复制 fallback 约束，支持调用方在失败或 API 不存在时聚焦并选中文本。
- 将日志审计 `request_id` 与重置密码随机密码作为代表迁移/回归场景。
- 将 Sprint 005 Clipboard fallback 经验和 admin-list/admin-modal 横切 AC 纳入实现验收。
- 不新增后端 API、数据库表、Orval 生成、小程序复制适配或新的 toast/dialog 体系。

## Capabilities

### New Capabilities

- `clipboard-copy-helper`: Web 管理端共享 Clipboard 复制 helper、结果模型、fallback、安全与测试要求。

### Modified Capabilities

- `design-system`: 增加复制交互 best-practice 的设计系统预览/文档和 semantic token 约束。
- `web-client`: 增加重置密码弹窗复制随机密码对共享 helper 与手动 fallback 的要求。
- `product-usage-logging`: 明确日志审计 `request_id` 复制迁移到共享 helper 时仍保持 fixed toast、fallback 和成功后埋点边界。

## Impact

- **backend:** false，不新增或修改 API。
- **web:** true，后续实现将新增共享前端 helper，并迁移代表调用方。
- **miniapp:** false，小程序 Clipboard API 差异本期不纳入。
- **admin:** true，影响日志审计列表与用户管理重置密码弹窗的复制交互。
- **database:** false。
- **storage:** false。
- **api:** false，不需要 OpenAPI / Orval。
- **tests:** 需要 Vitest / Testing Library 覆盖 helper 与代表场景。
