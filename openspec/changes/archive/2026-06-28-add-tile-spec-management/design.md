## Context

- **现状**：`admin-nav.ts` 无「瓷砖规格」；无 `tile_specs` 表；`TileSkuFormModal` 规格为自由文本 `<input>`；`tiles.size` TEXT 无 FK。
- **依赖**：`add-admin-home`（Shell）；`add-brand-management`（列表/启停/删除模式）；`add-tile-sku-management`（SKU 弹窗 MODIFIED）；`fix-brand-status-confirm`（启停确认）。
- **原型来源**（优先级，MUST 声明）：
  1. `issues/requirements/archive/REQ-0009-tile-spec-management/prototype/web/tile-size-management.html`
  2. `issues/requirements/archive/REQ-0009-tile-spec-management/prototype/web/tile-size-management.png`（**待导出**）
  3. `issues/requirements/archive/REQ-0009-tile-spec-management/prototype/web/tile-size-management-modal.html`
  4. `issues/requirements/archive/REQ-0009-tile-spec-management/prototype/web/tile-size-management-modal.png`（**待导出**）
  5. `prototype/web/tile-size-management-context.md`
  6. `issues/requirements/archive/REQ-0009-tile-spec-management/acceptance.md`
  7. `rules/ui-design.md`
  8. `openspec/specs/`

## Conflict Resolution

| 检查项 | HTML v2 | PRD v2 | acceptance | 决议 |
|--------|---------|--------|------------|------|
| 页面标题 | 瓷砖规格 | 瓷砖规格 | AC-001 | 一致 |
| 指标卡 | 总数/启用/停用/未关联SKU | 同左 | AC-005 | 一致；废弃 v1「标准砖/大板」 |
| 筛选 | 关键词+状态 | 无规格类型 | AC-007 | 以 v2 HTML/PRD 为准 |
| 表格列 | 无规格类型；含状态 | 同左 | AC-010 | 一致 |
| 删除 tooltip | 品牌文案 | 同左 | AC-017 | 一致 |
| SKU 下拉 | context 引用 | FR-010 | AC-026 | 实现页验收，无独立 prototype HTML |
| PNG | **缺失** | Partially Ready | AC-045 | HTML gate 先验收；apply 前导出 PNG |

## Goals / Non-Goals

**Goals:**

- `/admin/tile-specs` 与 list/modal HTML 在 1440×1024 并排验收 pass。
- CSS Port：`tile-spec-management.css`；Shell 复用 `AdminLayout` + 品牌页启停确认模式。
- 完整 Tile Specs API + migration + SKU `spec_id` + Orval + 测试。
- `admin`/`employee` 可维护规格；`store_owner` 403。

**Non-Goals:**

- 导出、批量、跳页、规格类型弹窗编辑、inch 单位 UI。
- 前台/小程序规格展示。
- 停用规格强制解绑已有 SKU。

## Decisions

### D1：CSS Port（路径 A，与 add-brand-management 一致）

- **决策**：新增 `features/admin/styles/tile-spec-management.css`，自 `tile-size-management*.html` port；列表/弹窗/分页对齐 `BrandManagementPage`。
- **理由**：prototype 含完整 metric-grid、状态列、启停操作、720px 弹窗与实时 `display_name` 生成。
- **备选**：纯 `AdminListPage` + Tailwind — 与 prototype 像素差风险大，不采用。

### D2：权限模型

| 角色 | 规格管理 |
|---|---|
| `admin` | CRUD + enable/disable + 条件删除 |
| `employee` | 同上 |
| `store_owner` | 403 |

- API：`require_admin_access`（与 brands 一致）。

### D3：API 设计

```text
GET    /api/v1/admin/tile-specs              # keyword, status, page, page_size + summary
POST   /api/v1/admin/tile-specs              # 创建；unit=mm；默认 ENABLED
GET    /api/v1/admin/tile-specs/{id}
PUT    /api/v1/admin/tile-specs/{id}
POST   /api/v1/admin/tile-specs/{id}/enable
POST   /api/v1/admin/tile-specs/{id}/disable
DELETE /api/v1/admin/tile-specs/{id}       # sku_count=0 AND DISABLED
```

- 错误码：`TILE_SPEC_DUPLICATED`、`TILE_SPEC_DELETE_FORBIDDEN`、`TILE_SPEC_NOT_FOUND`、`TILE_SPEC_DISABLED`（新建 SKU 选停用规格）。

### D4：数据模型

```sql
tile_specs (
  id INTEGER PRIMARY KEY,
  width_mm INTEGER NOT NULL,
  length_mm INTEGER NOT NULL,
  thickness_mm REAL,
  unit TEXT NOT NULL DEFAULT 'mm',
  display_name TEXT NOT NULL,
  sort_order INTEGER NOT NULL DEFAULT 100,
  status TEXT NOT NULL CHECK (status IN ('ENABLED','DISABLED')),
  sku_count INTEGER NOT NULL DEFAULT 0,
  remark TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  UNIQUE(width_mm, length_mm, unit)
)

-- tiles 新增
spec_id INTEGER REFERENCES tile_specs(id)
```

- `display_name = f"{width_mm}×{length_mm}{unit}"` 服务端生成。
- 删除：物理删除（确认弹窗）；服务端 `TILE_SPEC_DELETE_FORBIDDEN`。

### D5：SKU 联动

- Create/update SKU：`spec_id` 必填（`save_mode=create`）；`size` 服务端同步。
- 新建 SKU：所选 spec MUST `ENABLED`。
- 编辑 SKU：保留已绑定 **DISABLED** spec 的 `spec_id` 允许保存非规格字段；换绑 MUST 选 ENABLED。
- Publish：`spec_id` 非空且 `size` 非空。
- `sku_count`：SKU create/delete/change spec_id 时 ±1。

### D6：迁移

- 脚本解析 `tiles.size` 如 `900×1800mm` → 匹配 `tile_specs` 或按需 seed 常见规格后回填。
- 失败：`spec_id=NULL`，保留 `size`；编辑时强制选手动规格后再保存/上架。

### D7：前端结构

```text
AdminLayout
  └─ TileSpecManagementPage (/admin/tile-specs)
       ├─ page-header + metric-grid + filter + table + pagination
       ├─ TileSpecFormModal (720px)
       ├─ StatusConfirmDialog (启停，对齐 BrandManagementPage)
       └─ DeleteConfirmDialog
TileSkuFormModal (MODIFIED)
  └─ spec <select> from GET tile-specs?status=ENABLED
```

- `admin-nav.ts`：`{ id: 'tile-spec', label: '瓷砖规格', path: '/admin/tile-specs' }` 插入 category 与 banner 之间。
