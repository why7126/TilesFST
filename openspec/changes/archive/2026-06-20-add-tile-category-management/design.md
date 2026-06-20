## Context

- **现状**：`admin-nav.ts` 中「瓷砖类目」无 `path`；`tile_categories` 表仅 `id`+`name` 桩；无类目 Admin API；Dashboard「新增类目」快捷操作为占位 toast。
- **依赖**：`add-admin-home`（`AdminLayout`、`admin-home.css`）；`add-user-management` / `add-brand-management`（列表/弹窗/分页 CSS Port 模式可参考）。
- **原型来源**（优先级，不可省略）：
  1. `issues/requirements/REQ-0005-tile-category-management/prototype/web/tile-category-management.html`
  2. `issues/requirements/REQ-0005-tile-category-management/prototype/web/tile-category-management.png`（待导出）
  3. `issues/requirements/REQ-0005-tile-category-management/prototype/web/tile-category-management-add.html`
  4. `issues/requirements/REQ-0005-tile-category-management/prototype/web/tile-category-management-add.png`（待导出）
  5. `prototype/web/prototype-context-list.md`、`prototype-context-add.md`
  6. `issues/requirements/REQ-0005-tile-category-management/acceptance.md`
  7. `rules/ui-design.md`
  8. `openspec/specs/`

## Conflict Resolution

| 检查项 | HTML | PNG | acceptance / PRD | 决议 |
|--------|------|-----|------------------|------|
| 导出功能 | 无 | — | AC-004 无导出 | 一致 |
| 列表工具栏 | 仅「调整排序」 | — | PRD §9 | 一致 |
| 删除入口 | 仅停用且 SKU=0 行展示 | — | AC-016~017 | 一致；启用行仅编辑+停用 |
| 弹窗宽 | 560px 单列 | 待 PNG | AC-023 | 以 HTML 为准 |
| 弹窗状态 | Switch「新增后立即启用」 | — | PRD §11 | 以 HTML 为准（与品牌弹窗无状态不同） |
| 每页条数 | 10/20/50 | — | AC-021 | 默认 page_size=10 |
| 类目树 SKU 数 | 节点右侧 tree-count | — | PRD §8 未细化 | **定稿**：树节点展示**含子级汇总** SKU 数；列表行展示**当前节点直接绑定**数 |
| 调整排序 | 按钮存在，无交互 HTML | — | trace 标注可能占位 | 本期 **占位**：点击 Toast「排序调整功能即将上线」；reorder API 留 Non-Goal |
| PNG Golden Reference | — | **缺失** | trace Partially Ready | 验收 gate 先用 HTML 并排；PNG 补齐后补 sign-off |

## Goals / Non-Goals

**Goals:**

- `/admin/tile-categories` 列表 + 类目树 + 弹窗与 HTML V2 在 1280×1024 并排验收 pass。
- CSS Port：`tile-category-management.css`，颜色 `var(--color-*)`；Shell 复用 `AdminLayout`。
- 完整 Admin Tile Categories API + 扩展 `tile_categories` 表 + Orval + 测试。
- `admin` 与 `employee` 可维护类目；`store_owner` 不可进管理端。
- ≥20 项 HTML/PNG checklist 写入 change `trace.md`。

**Non-Goals:**

- 导出、批量操作、四级类目、类目合并、多语言、前台目录预览。
- 拖拽排序与 `reorder` API（「调整排序」本期占位）。
- SKU 管理页面（`sku_count` 本期默认 0）。
- 细粒度 RBAC 能力点（本期 `require_admin_user`）。

## Decisions

### D1：CSS Port（路径 A，与 add-admin-home / add-user-management 一致）

- **决策**：新增 `src/web/src/features/admin/styles/tile-category-management.css`，自 list/add HTML port；Shell 复用 `admin-home.css`。
- **理由**：HTML V2 含完整 work-grid（tree 280px + table）、metric-grid、560px 单列弹窗；Tailwind 拼装 fidelity 风险高。
- **备选**：DS Primitives + `AdminListPage` — 无类目树组件，不采用。

### D2：权限模型

| 角色 | 类目管理 |
|---|---|
| `admin` | 全部 CRUD + enable/disable/delete |
| `employee` | 同上 |
| `store_owner` | 不可访问 |

- API：`require_admin_user`（admin + employee）。

### D3：API 设计

```text
GET    /api/v1/admin/tile-categories              # keyword, status, level, parent_id, page, page_size + summary
GET    /api/v1/admin/tile-categories/tree         # 完整树 + sku_count（含子级汇总）
POST   /api/v1/admin/tile-categories              # parent_id 可空；默认 ENABLED
GET    /api/v1/admin/tile-categories/{id}
PUT    /api/v1/admin/tile-categories/{id}
POST   /api/v1/admin/tile-categories/{id}/enable
POST   /api/v1/admin/tile-categories/{id}/disable
DELETE /api/v1/admin/tile-categories/{id}         # sku_count=0 AND DISABLED
```

- 错误码：`CATEGORY_CODE_DUPLICATED`、`CATEGORY_DELETE_FORBIDDEN`、`CATEGORY_MAX_DEPTH_EXCEEDED`、`CATEGORY_INVALID_SORT_ORDER`。
- 路径前缀：`/api/v1/admin/tile-categories`（`rules/api.md`）。

### D4：数据模型

```sql
tile_categories (
  id INTEGER PRIMARY KEY,
  parent_id INTEGER REFERENCES tile_categories(id),  -- NULL = 一级
  name TEXT NOT NULL,                                 -- max 30
  code TEXT NOT NULL UNIQUE,                          -- max 32, 建议 CAT-XXXX
  sort_order INTEGER NOT NULL,                        -- 正整数
  level INTEGER NOT NULL CHECK (level BETWEEN 1 AND 3),
  description TEXT,                                   -- max 200
  status TEXT NOT NULL CHECK (status IN ('ENABLED','DISABLED')),
  sku_count INTEGER NOT NULL DEFAULT 0,
  path TEXT NOT NULL,                                 -- 如「按材质 / 大理石瓷砖」
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
)
```

- **删除策略**：物理删除；服务端校验失败返回 `CATEGORY_DELETE_FORBIDDEN`。
- **level/path**：创建/更新时由 `parent_id` 计算；`path` 用于列表副行展示。
- **sku_count**：本期无 SKU 关联时固定 0。

### D5：类目树与列表联动

- 树 API 返回嵌套或平铺+`parent_id`；前端渲染 level-2/level-3 缩进。
- 选中「全部类目」：`parent_id` 不传或 `null`，列表展示全部（分页）。
- 选中节点 N：列表 `parent_id=N` 或 API 返回 N 及其子孙扁平列表（实现选其一，推荐 **子孙扁平 + 分页**）。

### D6：前端结构

```text
AdminLayout
  └─ TileCategoryManagementPage  (/admin/tile-categories)
       ├─ page-header（CATEGORY MANAGEMENT + 新增类目）
       ├─ metric-grid（4 指标）
       ├─ filter-card（名称/编码 + 状态 + 层级 + 查询/重置）
       ├─ work-grid
       │    ├─ CategoryTree（280px）
       │    └─ table-card（工具栏仅调整排序 + 表格 + 分页）
       ├─ CategoryFormModal（add/edit，560px）
       └─ DeleteCategoryDialog
```

- `admin-nav.ts`：`category` 项 `path: '/admin/tile-categories'`。
- Dashboard `DashboardQuickActions`：「新增类目」`navigate('/admin/tile-categories')`。

### D7：校验

- 类目名称：必填、1–30 字。
- 类目编码：必填、唯一；编辑时 code 是否可改：**本期不可改**（与 PRD「保存后不建议修改」一致）。
- 排序权重：正整数；错误「请输入正整数」。
- 上级为 level=3 时禁止创建子级。

## Risks / Trade-offs

| 风险 | 缓解 |
|------|------|
| 桩表迁移破坏现有 tiles FK | 迁移保留 id；新列 DEFAULT；文档化 |
| 树 SKU 汇总口径歧义 | D5 定稿含子级汇总 |
| PNG 缺失 | HTML 并排 + trace pending |
| 调整排序未定义 | 占位 Toast；reorder 留后续 change |
| 与用户/品牌样式分叉 | 共用 metric-card、modal、pagination class |

## Migration Plan

1. 迁移扩展 `tile_categories`（ALTER 或重建+seed）。
2. 部署 API → Orval → 前端。
3. 回滚：移除路由；表可保留。

## Open Questions

- [ ] sprint-003 排期 — 产品确认。
- [ ] PNG 导出 — 实现前或并行补齐。

## 验收 Gate

- 视口：**1280×1024**
- 对比源：HTML 原型（PNG 补齐后升级 golden reference）
- Checklist：见 `openspec/changes/add-tile-category-management/trace.md`（≥20 项）
