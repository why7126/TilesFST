---
change_id: add-tile-spec-management
requirement_id: REQ-0009-tile-spec-management
status: archived
created_at: 2026-06-28 10:15:31
updated_at: 2026-06-28 13:30:00
---

# Change Trace — add-tile-spec-management

## 关联

| 字段 | 值 |
|---|---|
| REQ | REQ-0009-tile-spec-management |
| Sprint | sprint-003 |
| 依赖 | add-brand-management、add-tile-sku-management、fix-brand-status-confirm |
| MODIFIED | tile-sku-management、web-client、admin-dashboard |

## PNG / HTML 并排验收 Checklist

| # | 检查项 | prototype | 实现 | Pass |
|---|---|---|---|---|
| 1 | Shell + Sidebar「瓷砖规格」active | tile-size-management.html | `/admin/tile-specs` + admin-nav | ✓ |
| 2 | 4 指标卡（启用/停用） | tile-size-management.html | TileSpecManagementPage metrics | ✓ |
| 3 | 状态筛选（非规格类型） | tile-size-management.html | status filter（无规格类型） | ✓ |
| 4 | 表格状态列 + 启停操作 | tile-size-management.html | table + confirm | ✓ |
| 5 | 删除置灰 + tooltip | tile-size-management.html | canDeleteTileSpec + vitest | ✓ |
| 6 | 分页左共 x 条 | tile-size-management.html | Pagination（标准 `.pagination` DOM，fix-tile-spec-admin-ui） | ✓ |
| 7 | 弹窗 720px 字段网格 | tile-size-management-modal.html | TileSpecFormModal 720px（字段顺序 fix-tile-spec-admin-ui） | ✓ |
| 8 | 只读 display_name 实时生成 | tile-size-management-modal.html | previewName / buildDisplayName | ✓ |
| 9 | 无状态/规格类型字段 | tile-size-management-modal.html | 无 status/规格类型 | ✓ |
| 10 | SKU 弹窗规格 select | acceptance AC-026 | TileSkuFormModal + vitest | ✓ |
| 11 | 无裸 Hex | — | semantic token CSS port | ✓ |
| 12 | PNG Golden Reference | tile-size-management.png / modal.png | prototype/web/*.png 已存在 | ✓ |

**验收方式**

- Docker 冒烟：`scripts/smoke-tile-spec-docker.sh`（2026-06-28 通过：pytest 19、OpenAPI 4 routes、SPA 200）
- HTML gate：`src/web/src/features/admin/tile-spec-visual-checklist.test.ts`（12/12 vitest）
- 可选实现截图：`node scripts/capture-tile-spec-visual.mjs`（需 Playwright + Docker）

## 变更记录

| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-06-28 15:28:00 | fix follow-up | checklist #6/#7 由 fix-tile-spec-admin-ui 补齐标准分页与弹窗字段顺序 |
| 2026-06-28 13:05:00 | `/sprint-apply` | 后端/前端实现、pytest/vitest/build 通过；文档同步 |
| 2026-06-28 10:15:31 | `/req-opsx` | 创建 change add-tile-spec-management |
