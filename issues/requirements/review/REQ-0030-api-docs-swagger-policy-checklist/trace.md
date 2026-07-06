---
requirement_id: REQ-0030-api-docs-swagger-policy-checklist
status: in_sprint
priority: P2
created_at: 2026-07-04 15:42:05
updated_at: 2026-07-05 07:55:25
lifecycle_stage: review
lifecycle:
  captured: 2026-07-04 15:42:05
  generated: 2026-07-04 22:13:25
  completed: 2026-07-04 22:19:09
  reviewed: 2026-07-04 22:26:20
  approved: 2026-07-04 22:26:20
iteration: sprint-005
openspec_changes:
  - change_id: update-api-docs-swagger-policy-checklist
    type: update
    status: proposed
    created_at: 2026-07-05 07:55:25
related_requirements:
  - REQ-0022-admin-api-docs-menu
related_bugs:
  - BUG-0051-api-docs-swagger-ui-link-wrong
knowledge_base_refs:
  - docs/knowledge-base/retrospectives/sprint-004-retrospective.md
cross_cutting_tags: []
readiness: Ready
readiness_notes: 已补齐 requirement、user-stories、business-flow、acceptance 与 trace；本需求为 API/docs 治理 checklist，不生成 prototype，不命中管理端 UI 横切标签。
---

# Trace

## 当前状态

- 状态：in_sprint
- 阶段：review
- 优先级：P2
- 来源：Sprint 004 复盘行动项 / 用户输入
- 父需求：REQ-0022-admin-api-docs-menu
- 关联 BUG：BUG-0051-api-docs-swagger-ui-link-wrong
- Knowledge-base：读取 `docs/knowledge-base/README.md` 与 `docs/knowledge-base/retrospectives/sprint-004-retrospective.md`；本 REQ 不命中 UI 横切标签，无 AC-XCUT。
- Readiness：Ready，已纳入 `sprint-005`，OpenSpec Change 已创建：`update-api-docs-swagger-policy-checklist`。

## 关联需求

| REQ | 关系 | 说明 |
|---|---|---|
| REQ-0022-admin-api-docs-menu | parent | 父能力，提供 `/admin/api-docs` 页面、Swagger 入口与生产调试策略 |
| REQ-0023-api-docs-swagger-detail-link | related | 相邻能力，补充行级 Swagger operationId 深链 |

## 关联缺陷

| BUG | 严重等级 | 状态 | 关联 Change | 说明 |
|---|---|---|---|---|
| BUG-0051-api-docs-swagger-ui-link-wrong | high | done | fix-api-docs-swagger-ui-link-wrong | 经验来源：Web 代理未覆盖 `/docs` 导致 Swagger 入口进入 Web 首页 |

## Knowledge-base Cross-cutting Report

| 标签 | 引用文档 | 将写入 acceptance 的 AC 条数 |
|---|---|---:|
| N/A（API/docs governance） | `docs/knowledge-base/retrospectives/sprint-004-retrospective.md` | 0 |

说明：本 REQ 不新增管理端 CRUD 列表、表单、弹窗或媒体上传 UI，不触发 `admin-list` / `admin-form` / `admin-modal` / `media-upload` 横切 AC；主要引用 Sprint 004 A-006 复盘行动项。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-05 07:55:25 | /req-opsx REQ-0030 | 创建 OpenSpec Change `update-api-docs-swagger-policy-checklist`，生成 proposal、design、tasks、trace 与 specs delta。 |
| 2026-07-04 22:30:20 | /sprint-propose sprint-005 | 纳入 Sprint 005 正式范围；OpenSpec Change 尚未创建，下一步 `/req-opsx REQ-0030-api-docs-swagger-policy-checklist`。 |
| 2026-07-04 22:27:13 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-07-04 22:26:20 | /req-review --approve | 需求评审通过，范围、验收、依赖、UI 策略与重复关系检查均通过；准备从 plan 迁移到 review。 |
| 2026-07-04 22:19:09 | /req-complete | 补齐 user-stories、business-flow、acceptance，并扩写 trace；判定为 API/docs 治理 REQ，不命中 UI 横切标签，Knowledge-base gate 为 N/A。 |
| 2026-07-04 22:13:25 | /req-generate | 生成 `requirement.md` PRD 草案，明确接口文档页模板 checklist 的范围、Web 代理、生产 `Try It Out` 策略、安全边界与后续同步对象。 |
| 2026-07-04 15:42:05 | /req-capture | 创建需求记录，作为 `REQ-0022` 的后续 refinement，记录接口文档页模板 checklist 需覆盖 Swagger Web 代理与生产 `Try It Out` 策略。 |
