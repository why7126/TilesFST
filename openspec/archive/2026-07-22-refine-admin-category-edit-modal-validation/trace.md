---
change_id: refine-admin-category-edit-modal-validation
status: applied
created_at: 2026-07-22 09:32:00
updated_at: 2026-07-22 09:55:00
source_requirement: REQ-0067-admin-category-edit-modal-validation
iteration: sprint-010
change_type: update
owner: product
---

# Change Trace

## 来源

- REQ: `issues/requirements/archive/REQ-0067-admin-category-edit-modal-validation`
- Parent REQ: `REQ-0005-tile-category-management`
- Review: `issues/requirements/archive/REQ-0067-admin-category-edit-modal-validation/review.md`
- Sprint: `sprint-010`

## Readiness

| 项 | 结论 |
|---|---|
| REQ status | approved |
| Readiness | Partially Ready（best-practice 文档为 draft；不阻断 Change 创建） |
| Knowledge-base gate | Pass |
| Cross-cutting tags | admin-modal |

## Impact

```yaml
impact:
  backend: true
  web: true
  miniapp: false
  admin: true
  database: false
  storage: false
  api: true
capabilities:
  new: []
  modified:
    - tile-category-management
    - web-client
```

## Conflict Report

| Source | Finding | Resolution |
|---|---|---|
| prototype/web/category-edit-modal.html | 弹窗不提供编码输入，显示必填标识和字段级错误位置 | design D1/D2 采纳；web-client delta 更新新增/编辑弹窗 |
| prototype/web/context.md | 顶级类目用固定选项表达，二级类目不可作为上级 | design D1/D3 采纳；web-client delta 更新上级类目选择 |
| acceptance.md | AC-XCUT 覆盖 admin-modal 宽度、CSS cascade、矮视口滚动 | tasks 5.2-5.4 保留验收证据 |
| openspec/specs/tile-category-management | 旧规范要求 create 接受 code，name 最大 30 | delta 修改为后端生成 `CAT-` code，name 最大 10 |
| openspec/specs/web-client | 旧类目页规范只引用旧 add-modal 策略 | delta 增加 REQ-0067 类目弹窗字段和横切质量场景 |

## Prototype / Evidence Checklist

- [x] 管理端类目新增弹窗：无可填写编码输入，上级类目/名称/排序权重必填标识可见。证据：`CategoryFormModal.test.tsx`。
- [x] 管理端类目编辑弹窗：无可编辑编码输入，无法修改上级类目。证据：`CategoryFormModal.test.tsx`。
- [x] 1440px computed width：类目弹窗保持 560px。证据：`tile-category-management.css` 中 `.admin-shell .category-modal { width: 560px; }`，并由组件测试读取 CSS 合同断言。
- [x] 矮视口弹窗滚动：复用全局 `.modal-body` / `.modal-footer` 滚动与 footer 规则，组件测试读取 CSS 合同断言。
- [x] TSX/CSS cascade：`CategoryFormModal.tsx` 仅挂载 `category-modal`，未挂载 `modal-card`；组件测试断言无双类。
- [ ] PNG Golden Reference：optional，可在实现阶段按需导出。

## Implementation Notes

| 项 | 结论 |
|---|---|
| 编码生成算法 | 后端创建类目时生成 `CAT-` + 8 位大写随机十六进制后缀；最多重试 5 次，仍冲突时返回 `CATEGORY_CODE_DUPLICATED`。 |
| 名称重复规则 | 同一 `parent_id` 下按 `LOWER(name)` 做大小写不敏感查重；顶级类目以 `parent_id IS NULL` 为同层级。 |
| DB 迁移 | 不需要。`tile_categories.code` 保持 `UNIQUE NOT NULL`，仅创建请求契约和业务校验变化。 |
| Orval | 已运行 `./scripts/generate-openapi-client.sh`，`TileCategoryCreateRequest` 不再包含 `code`。 |
| 列表展示 | 管理端类目列表名称列第一行显示类目名称，第二行仅显示系统编码，不显示层级路径。 |

## 变更记录

| 时间 | 动作 | 说明 |
|---|---|---|
| 2026-07-22 09:32:00 | /req-opsx | 从 REQ-0067 创建 OpenSpec Change，状态 proposed |
| 2026-07-22 09:32:45 | /sprint-propose | 纳入 sprint-010 正式范围，等待 /opsx-apply |
| 2026-07-22 09:48:09 | /opsx-apply | 完成后端编码生成、名称校验、同层级唯一、管理端弹窗、OpenAPI/Orval、文档与 focused tests |
| 2026-07-22 09:55:00 | /opsx-apply follow-up | 根据用户反馈调整类目列表名称列第二行展示策略，并补充页面测试 |
