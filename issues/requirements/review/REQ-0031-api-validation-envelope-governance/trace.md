---
requirement_id: REQ-0031-api-validation-envelope-governance
status: approved
priority: P1
created_at: 2026-07-04 21:52:59
updated_at: 2026-07-05 14:44:22
lifecycle_stage: review
lifecycle:
  captured: 2026-07-04 21:52:59
  generated: 2026-07-05 07:57:01
  completed: 2026-07-05 14:37:08
  reviewed: 2026-07-05 14:43:39
  approved: 2026-07-05 14:43:39
iteration: null
openspec_changes: []
related_requirements:
  - REQ-0000-build-api-standard
related_bugs: []
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-form-page-consistency.md
  - docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md
  - docs/knowledge-base/best-practices/admin-media-upload-chain.md
  - docs/knowledge-base/retrospectives/sprint-004-retrospective.md
cross_cutting_tags:
  - admin-form
  - admin-modal
  - media-upload
prototype_strategy: none - API governance / no new UI surface; UI impact covered by AC-XCUT
---

# Trace

## 当前状态

- 状态：approved
- 阶段：review
- 优先级：P1
- 来源：用户输入
- 父需求：REQ-0000-build-api-standard
- 原型策略：无新增页面或视觉原型；错误展示影响通过 `acceptance.md` 的横切 AC 约束

## 文档完整性

| 文档 | 状态 | 说明 |
|---|---|---|
| `capture.md` | done | 已记录原始需求和父需求。 |
| `requirement.md` | done | 已生成 PRD，明确 scope、FR、风险和状态。 |
| `user-stories.md` | done | 已补齐角色、价值和用户故事验收要点。 |
| `business-flow.md` | done | 已补齐异常流、OpenAPI / Orval、前端展示、上传和日志流程。 |
| `acceptance.md` | done | 已补齐功能 AC 与 knowledge-base 横切 AC。 |
| `trace.md` | done | 已同步状态、知识库引用、横切标签和变更记录。 |

## Knowledge-base Cross-cutting Report

| 标签 | 引用 | 落地方式 |
|---|---|---|
| admin-form | `docs/knowledge-base/best-practices/admin-form-page-consistency.md` | 转化为 AC-XCUT-001 至 AC-XCUT-003，约束错误展示稳定性、单一保存 CTA 和禁止 `window.alert/confirm`。 |
| admin-modal | `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md` | 转化为 AC-XCUT-004 至 AC-XCUT-005，约束弹窗 class 使用、宽度和短视口滚动不回归。 |
| media-upload | `docs/knowledge-base/best-practices/admin-media-upload-chain.md` | 转化为 AC-XCUT-006 至 AC-XCUT-008，约束上传状态机、失败展示和 Docker `:3000` 边界验证。 |
| sprint-retro | `docs/knowledge-base/retrospectives/sprint-004-retrospective.md` | 转化为 AC-XCUT-009，回应 Sprint 004 A-007 API governance 行动项。 |

## Traceability

| 需求点 | 用户故事 | 业务流 | 验收标准 |
|---|---|---|---|
| 统一校验错误 envelope | US-001、US-002、US-004 | 2、3 | AC-001 至 AC-005 |
| 首批管理端表单 API 覆盖 | US-003、US-004 | 1、2 | AC-006 至 AC-009 |
| OpenAPI / Orval 同步 | US-002、US-004 | 4 | AC-010 至 AC-012 |
| 前端错误解析与展示 | US-002、US-003 | 5 | AC-013 至 AC-016、AC-XCUT-001 至 AC-XCUT-005 |
| 安全、日志与兼容性 | US-005、US-006 | 8、9 | AC-017 至 AC-020 |
| 上传校验错误 | US-007 | 6 | AC-009、AC-XCUT-006 至 AC-XCUT-008 |

## 变更记录

| 2026-07-05 14:44:22 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-04 21:52:59 | /req-capture | 创建需求记录，记录统一 422 参数校验错误 envelope 需扩展到所有管理端表单 API，并作为 API 治理延展进入后续 `/req-explore` 与 `/req-generate`。 |
| 2026-07-05 07:57:01 | /req-generate | 生成 `requirement.md` PRD 草案，明确管理端表单 API 校验错误 envelope、`data.errors[]`、OpenAPI / Orval 同步和测试覆盖范围。 |
| 2026-07-05 14:37:08 | /req-complete | 补齐 `user-stories.md`、`business-flow.md`、`acceptance.md`，引入 admin-form、admin-modal、media-upload 知识库横切 AC，并将需求推进到待评审。 |
| 2026-07-05 14:43:39 | /req-review --approve | 评审通过，生成 `review.md`，状态更新为 `approved`，并准备从 `plan/` 迁移到 `review/`。 |
