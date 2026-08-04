---
requirement_id: REQ-0095-admin-list-field-display-adapter-checklist
acceptance_status: passed
created_at: 2026-08-04 08:35:48
updated_at: 2026-08-04 23:12:32
owner: product
source: requirement.md
---

# 验收标准

## 功能 AC

- [ ] AC-001 检查表包含 `image adapter`、`name adapter`、`fallback adapter` 三个独立章节，每个章节均包含检查项、适用列表、期望表现和验证方式。
- [ ] AC-002 首批覆盖列表至少包含品牌列表、证书列表、SKU 列表和 Banner 列表，并逐项标记 image/name/fallback 是否适用。
- [ ] AC-003 image adapter 明确缩略图优先、原图兜底、主图选择、无图态、加载失败态、容器尺寸和可访问性语义。
- [ ] AC-004 name adapter 明确主名称、辅助名称、关联对象名称、空名称、长名称截断和重复字段去重规则。
- [ ] AC-005 fallback adapter 区分“未设置”“无数据”“不适用”“加载失败”“未知枚举值”“无权限”等语义，不得全部混用同一文案。
- [ ] AC-006 检查表包含首批列表现状盘点，标记已有 helper、页面内判断、样式兜底、可复用逻辑和待治理分散逻辑。
- [ ] AC-007 检查表明确本需求不强制立即重构所有列表；如后续需要抽公共 adapter、组件或模板，必须进入 OpenSpec design 决策。
- [ ] AC-008 验收样例覆盖至少一种无图、一种图片加载失败、一种空名称、一种关联对象缺失和一种未知枚举值场景。
- [ ] AC-009 检查表要求图片缺失、加载失败、长名称和空值兜底不得造成表格行高、列宽、操作列或分页区域布局抖动。
- [ ] AC-010 若后续实现阶段出现接口响应字段、Schema 或排序/筛选契约变化，必须同步 OpenAPI、Orval、API 文档和测试；若无变化，验收记录需说明 N/A。

## 横切 AC（knowledge-base）

> 来源：`docs/knowledge-base/best-practices/admin-list-page-consistency.md` — 预防 Sprint 002/003 复发类缺陷

- [ ] AC-XCUT-001 后续涉及管理端列表页面改造时，分页 DOM 必须与用户管理基准对齐：左侧 `page-summary`，右侧 `page-right` 页码与每页条数；若本 Change 只产出检查表不改页面，记录为 N/A — 未改列表 DOM。
- [ ] AC-XCUT-002 后续涉及管理端列表操作反馈时，成功/失败反馈必须使用 fixed toast，不得使用文档流 notice 推挤 hero、筛选区或表格；若本 Change 只产出检查表不改交互反馈，记录为 N/A — 未改 toast 行为。
- [ ] AC-XCUT-003 后续涉及状态变更、启停、上架/下架、删除等危险操作时，必须使用 Design System confirm modal；本需求不得引入 `window.confirm`。
- [ ] AC-XCUT-004 后续实现检查表或代表页面验证时，必须检查源码中无新增 `window.confirm`，并保留列表页一致性回归说明。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-04 23:12:32
accepted_by: workflow-sync
source_change: standardize-admin-list-field-display-adapters
source_sprint: sprint-019
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

