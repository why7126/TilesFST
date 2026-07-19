---
title: 用户故事
purpose: REQ-0039 XL 管理端页面分层验收模板用户故事
content: 面向产品、研发、测试与 AI Agent 的模板使用场景
source: requirement.md
owner: product
status: done
created_at: 2026-07-16 09:06:14
updated_at: 2026-07-16 09:37:04
---

# 用户故事

## US-001 产品负责人生成复杂页面验收标准

作为产品负责人，我希望在规划 XL 管理端页面时有一套分层验收模板，以便在 PRD 和验收标准阶段提前识别 DB、API、上传、Orval、Web、Docker 和 UI 横切风险。

验收要点：

- 模板提供层级矩阵，能标记每层 gate 为 required 或 N/A。
- 模板要求每个 N/A 都写明原因，避免遗漏被误判为不适用。
- 模板可被复制到后续 REQ 的 `acceptance.md` 或 OpenSpec Change 验收材料。

## US-002 后端开发确认 DB/API/上传边界

作为后端开发，我希望模板明确 DB、API 与上传 gate 的必检项，以便在实现前判断是否需要迁移、Schema、错误码、接口文档、MinIO 前缀和测试同步。

验收要点：

- DB gate 覆盖表结构、迁移、SQLite/MySQL 差异、Repository/Service 和测试。
- API gate 覆盖统一响应、错误码、鉴权、OpenAPI 和接口文档。
- 上传 gate 覆盖后端授权、MIME/大小、对象 key、失败态和 Docker Nginx 边界。

## US-003 前端开发确认 Orval/Web/UI 交付范围

作为前端开发，我希望模板明确 Orval、Web 页面交互和横切 UI gate，以便复杂页面不会遗漏生成类型、列表/表单/弹窗/上传状态和 Design System 约束。

验收要点：

- Orval gate 明确 contract 变化时必须导出 OpenAPI 并生成客户端。
- Web gate 覆盖列表、筛选、分页、表单、弹窗、抽屉、权限和前端状态。
- UI gate 覆盖 semantic token、DS modal、fixed toast、无裸 Hex、无布局抖动。

## US-004 测试人员按层记录验收证据

作为测试或验收人员，我希望模板要求每层 gate 记录证据，以便评审和回归时能快速判断哪些层已验证、哪些层阻塞、哪些层确认为 N/A。

验收要点：

- 每层 gate 有状态、owner、证据、N/A 理由和剩余风险。
- 验收证据可记录命令摘要、接口响应摘要、截图、测试结果和 Docker 验证结果。
- 成功路径不复制长日志或生成物全文。

## US-005 AI Agent 在后续命令中复用模板

作为 AI Agent，我希望模板有稳定结构和知识库引用，以便后续 `/req-complete`、`/req-opsx`、`/opsx-apply` 能复用同一套检查口径，减少重复探索和历史问题复发。

验收要点：

- `trace.md` 包含 `knowledge_base_refs` 与 `cross_cutting_tags`。
- `acceptance.md` 包含可测试的 `AC-XCUT-*` 横切条目。
- 后续 Change 的 `design.md` 可引用这些 refs 并逐项说明落实或 N/A。
