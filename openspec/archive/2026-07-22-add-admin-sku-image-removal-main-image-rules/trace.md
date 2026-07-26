---
change_id: add-admin-sku-image-removal-main-image-rules
status: proposed
type: update
created_at: 2026-07-22 09:31:00
updated_at: 2026-07-22 09:58:04
source_requirement: REQ-0066-admin-sku-image-removal-main-image-rules
source_issue: issues/requirements/archive/REQ-0066-admin-sku-image-removal-main-image-rules/
iteration: sprint-010
affected_specs:
  - tile-sku-management
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md
  - docs/knowledge-base/best-practices/admin-media-upload-chain.md
  - docs/knowledge-base/retrospectives/sprint-009-retrospective.md
cross_cutting_tags:
  - admin-modal
  - media-upload
prototype_refs:
  - issues/requirements/archive/REQ-0066-admin-sku-image-removal-main-image-rules/prototype/web/admin-sku-image-removal-main-image-rules.html
  - issues/requirements/archive/REQ-0066-admin-sku-image-removal-main-image-rules/prototype/web/admin-sku-image-removal-main-image-rules-context.md
png_checklist:
  required: false
  status: pending_optional_export
---

# Change Trace

## Requirement Readiness Report

| Item | Result |
|---|---|
| requirement.md | Ready |
| user-stories.md | Ready |
| business-flow.md | Ready |
| acceptance.md | Ready |
| review.md | approved |
| prototype/web | HTML + context ready; PNG optional |
| knowledge-base gate | Pass |

## Impact

```yaml
impact:
  backend: possible_regression_tests_only
  web: true
  miniapp: false
  admin: true
  database: false
  storage: association_only_no_physical_delete
  api: unlikely
capabilities:
  new: []
  modified:
    - tile-sku-management
change_type: update
strategy: state-normalize
```

## Conflict Report

优先级：HTML prototype > context.md > acceptance.md > requirement.md > ui-design.md > openspec/specs。

- HTML/context 要求“主图第一、移除主图后一张接任”；现有 spec 仅要求多图和主图唯一，未冲突，需补充。
- acceptance 要求不物理删除 MinIO 对象；现有 upload spec 未定义移除物理删除，需明确不删除对象文件。
- media-upload 横切 AC 中 Docker 边界上传只在触及上传链路时强制；本 change 默认只改移除与 payload 重排，可 N/A。
- admin-modal 横切 AC 与现有 SKU 弹窗正例一致，必须保持 `sku-modal-card` 专属类策略。

## Workflow

| 时间 | 事件 | 说明 |
|---|---|---|
| 2026-07-22 09:31:00 | /req-opsx | 从 REQ-0066 创建 OpenSpec Change |
| 2026-07-22 09:45:10 | /sprint-propose | 纳入 sprint-010，等待 /opsx-apply |
| 2026-07-22 09:58:04 | /opsx-apply | 完成 SKU 图片移除、主图前置、移除主图兜底、后端顺序 normalize 与测试 |

## Implementation Evidence

- Web 管理端：`TileSkuFormModal` 新增图片 normalize / remove helper；设主图后前置，移除任意图片，移除当前主图时后一张优先兜底，移除全部后保留继续添加入口。
- 后端：`TileSkuAdminService._normalize_images()` 保存时保证主图唯一、主图第一、`sort_order` 连续；PUT 空 images 仍清空 SKU 图片关联。
- API / DB / Orval：未新增或修改请求/响应字段，未修改数据库结构；不需要 OpenAPI / Orval。
- 对象存储：未触及上传接口、上传大小/MIME、MinIO 前缀或物理删除；Docker 边界上传验收 N/A。

## Test Evidence

- `pnpm --dir src/web exec vitest run src/features/admin/components/TileSkuFormModal.test.tsx`：1 file / 19 tests passed。
- `uv run pytest src/backend/tests/test_admin_tile_skus.py`：18 passed。

## Cross-cutting AC

| Tag | Result | Evidence |
|---|---|---|
| admin-modal | Pass | 仍仅挂载 `sku-modal-card`；既有 CSS 栈测试覆盖 `.sku-modal-card .modal-body` 滚动规则，未引入 `modal-card` 双类 |
| media-upload | Pass | 新增图片移除不改变上传链路；上传后图片即时回显且可移除；失败展示沿用既有控件内错误逻辑 |
