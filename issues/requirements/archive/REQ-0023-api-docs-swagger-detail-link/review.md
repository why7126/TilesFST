---
review_id: REV-REQ-0023-001
requirement_id: REQ-0023-api-docs-swagger-detail-link
date: 2026-07-01 14:06:40
participants:
  - product
  - ai-agent
result: approved
created_at: 2026-07-01 14:06:40
updated_at: 2026-07-01 14:06:40
---

# REQ-0023 需求评审

## 评审结论

通过。`REQ-0023-api-docs-swagger-detail-link` 范围清晰，作为 `REQ-0022-admin-api-docs-menu` 的行级增强需求成立，不与 `BUG-0051-api-docs-swagger-ui-link-wrong` 重复。

本需求已明确：

- Swagger UI 必须跳转到具体 `operationId` 锚点。
- 行级查看必须新窗口打开，保留当前管理端筛选与登录上下文。
- `included_in_openapi=false` 或缺少 `operation_id` 的路由显示禁用态，不生成错误跳转。
- 不复制 token、不新增 Swagger 自动鉴权注入，不放宽生产环境 `Try It Out` 策略。
- 管理端列表页横切 AC 已引用 knowledge-base，并写入 acceptance。

## 评审清单

| 检查项 | 结果 | 说明 |
|---|---|---|
| 范围清晰，Out of Scope 明确 | 通过 | 不含接口编辑、Swagger 内嵌、非 OpenAPI 伪详情、token 注入 |
| 验收标准可测试 | 通过 | AC-001～AC-025 与 AC-XCUT-001～004 可在前端测试和人工验收中验证 |
| 优先级与依赖合理 | 通过 | P1；依赖 REQ-0022 已提供接口目录、`operation_id` 与 OpenAPI 状态 |
| UI 类原型或实现策略已决 | 通过 | 已提供轻量 HTML/context；以 REQ-0022 原型为视觉基线 |
| 无与现有 REQ 重复未说明 | 通过 | 与 BUG-0051 边界明确：BUG 修全局入口，本 REQ 做行级详情入口 |

## 条件通过项

- [ ] OpenSpec design 阶段 MUST 验证 FastAPI Swagger UI 实际 deepLinking hash 格式。
- [ ] 若实现新增后端字段（如 `swagger_url`），MUST 同步 OpenAPI、Orval、`docs/03-api-index.md` 与测试。
- [ ] 若仅前端构造链接，MUST 在 design/tasks 中明确无 API / Orval 变更。

## 下一步

1. `/req-opsx REQ-0023-api-docs-swagger-detail-link`
2. 可选：通过 `/sprint-propose` 纳入 Sprint；纳入前确认 sprint 横切预防清单覆盖 `admin-list`。
