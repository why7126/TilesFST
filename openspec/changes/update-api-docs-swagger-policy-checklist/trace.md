---
change_id: update-api-docs-swagger-policy-checklist
status: proposed
created_at: 2026-07-05 07:55:25
updated_at: 2026-07-05 07:55:25
source_requirement: REQ-0030-api-docs-swagger-policy-checklist
sprint: sprint-005
---

# Trace

## 来源

| 项 | 说明 |
|---|---|
| REQ | `REQ-0030-api-docs-swagger-policy-checklist` |
| 父需求 | `REQ-0022-admin-api-docs-menu` |
| 关联 BUG | `BUG-0051-api-docs-swagger-ui-link-wrong` |
| 知识库 | `docs/knowledge-base/retrospectives/sprint-004-retrospective.md` A-006 |
| Sprint | `sprint-005` |

## 影响范围

| 能力 | 变更类型 | 说明 |
|---|---|---|
| `admin-api-docs` | MODIFIED | 固化接口文档页模板 checklist |
| `web-client` | MODIFIED | 固化同源 Swagger 入口、行级 deep link 与生产只读验收约束 |
| `deployment` | MODIFIED | 固化 dev / Docker / production 代理路径设计与验收约束 |
| `testing` | MODIFIED | 固化 Web 代理 smoke 与生产 `Try It Out` 验证记录门禁 |

## 状态记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-05 07:55:25 | /req-opsx REQ-0030 | 创建 `update-api-docs-swagger-policy-checklist`，生成 proposal、design、tasks 与 delta specs。 |
