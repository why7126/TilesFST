## Why

Sprint 007 的品牌证书管理能力一次性覆盖 DB、API、上传、Orval、Web、Docker 和横切 UI gate，暴露出 XL 管理端页面 Change 验收面宽、复盘成本高、模板化不足的问题。REQ-0039 已评审通过，需要将这套分层验收口径沉淀为正式 OpenSpec 能力，供后续复杂管理端页面复用。

## What Changes

- 新增 XL 管理端页面分层验收模板能力，定义复杂管理端页面的 gate 矩阵、状态字段、证据字段和 N/A 判定。
- 沉淀 DB、API、上传、Orval、Web、Docker、横切 UI 七层 gate 的标准验收要求。
- 要求模板引用管理端列表、表单、弹窗、媒体上传 best-practices，并保留 `knowledge_base_refs` 追溯。
- 明确该 Change 仅新增治理模板与文档/规范，不直接修改业务页面、运行时代码、DB/API、上传链路、Orval 或 Docker 配置。

## Capabilities

### New Capabilities

- `xl-admin-page-acceptance-template`: 定义 XL 管理端页面分层验收模板、gate 状态、N/A 规则、证据记录和横切 UI 验收引用。

### Modified Capabilities

- 无。

## Impact

- 影响文档与流程：新增长期标准文档或等价模板，并在 OpenSpec 规范中建立后续复杂管理端页面的引用口径。
- 影响后续 REQ/Change：复杂管理端页面在 `/req-complete`、`/req-opsx`、`/opsx-apply` 或验收报告中应引用该模板并逐层标记 required/N/A。
- 不影响运行时代码、API、数据库、小程序、Orval 生成物、Docker Compose 或 MinIO 配置。
