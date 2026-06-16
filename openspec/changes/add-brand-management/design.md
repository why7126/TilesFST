## Context

- **现状**：`admin-nav.ts` 中「瓷砖品牌」无 `path`；无 `brands` 表与品牌 API；Dashboard「新增品牌」快捷操作为占位 toast。
- **依赖**：`add-admin-home`（`AdminLayout`、`admin-home.css`）；`add-user-management`（列表/弹窗/分页 CSS Port 模式可参考）。
- **原型来源**（优先级，不可省略）：
  1. `issues/requirements/REQ-0005-brand-management/prototype/web/brand-management.html`
  2. `issues/requirements/REQ-0005-brand-management/prototype/web/brand-management.png`（待导出）
  3. `issues/requirements/REQ-0005-brand-management/prototype/web/brand-management-modal.html`
  4. `issues/requirements/REQ-0005-brand-management/prototype/web/brand-management-modal.png`（待导出）
  5. `prototype/web/*-context.md`
  6. `issues/requirements/REQ-0005-brand-management/acceptance.md`
  7. `rules/ui-design.md`
  8. `openspec/specs/`

## Conflict Resolution

| 检查项 | HTML | PNG | acceptance / PRD | 决议 |
|--------|------|-----|------------------|------|
| 列表/筛选区标题 | 无「品牌列表」「品牌检索」 | — | AC-004 一致 | 一致 |
| 导出/批量 | 无 | — | PRD §2 删除 | 一致 |
| 弹窗状态字段 | 无 | — | AC-024 | 一致；创建默认 ENABLED 不在 UI 展示 |
| 弹窗宽 | 720px | 待 PNG | AC-020 | 以 HTML 为准 |
| 每页默认条数 | 20 | — | AC-018 20/50/100 | 默认 page_size=20 |
| 删除 tooltip 文案 | 固定中文 | — | AC-014 | 以 HTML/PRD 为准 |
| 表格「品牌」列 | Logo+名称+副标题 | — | PRD §8 | HTML 含 brand-sub；实现 MAY 用 description 首行或留空 |
| PNG Golden Reference | — | **缺失** | trace 标记 Partially Ready | 验收 gate 先用 HTML 并排；PNG 补齐后补 sign-off |

## Goals / Non-Goals

**Goals:**

- `/admin/brands` 列表 + 弹窗与 `brand-management.html` / `brand-management-modal.html` 在 1280×1024 并排验收 pass。
- CSS Port：`brand-management.css`，颜色 `var(--color-*)`；Shell 复用 `AdminLayout`。
- 完整 Admin Brands API + `brands` 表 + Orval + 测试。
- `admin` 与 `employee` 可维护品牌；`store_owner` 不可进管理端。
- ≥18 项 HTML/PNG checklist 写入 change `trace.md`。

**Non-Goals:**

- 导出、批量操作、国家/地区、品牌合并、多语言、SEO、前台品牌预览。
- SKU 管理页面（`sku_count` 本期默认 0，预留字段或子查询钩子）。
- 细粒度 RBAC 能力点（本期后端 `require_admin_user` 即可，权限点文档化供后续扩展）。

## Decisions

### D1：CSS Port（路径 A，与 add-admin-home / add-user-management 一致）

- **决策**：新增 `src/web/src/features/admin/styles/brand-management.css`，自 list/modal HTML port；Shell 复用 `admin-home.css`（`AdminLayout`）。
- **理由**：HTML V7 含完整 metric-grid、filter-row、表格、720px 双列弹窗；Tailwind 拼装 fidelity 风险高。
- **备选**：DS Primitives + `AdminListPage` — 与用户管理/原型像素差风险大，不采用。

### D2：权限模型

| 角色 | 品牌管理 |
|---|---|
| `admin` | 全部 CRUD + enable/disable/delete |
| `employee` | 同上（OPERATIONS 主数据维护） |
| `store_owner` | 不可访问管理端 |

- API 依赖：现有 `require_admin_user`（admin + employee），与用户管理 `require_system_admin` 区分。

### D3：API 设计

```text
GET    /api/v1/admin/brands                    # keyword, status, page, page_size + summary
POST   /api/v1/admin/brands                    # 创建；默认 status=ENABLED
GET    /api/v1/admin/brands/{id}
PUT    /api/v1/admin/brands/{id}
POST   /api/v1/admin/brands/{id}/enable
POST   /api/v1/admin/brands/{id}/disable
DELETE /api/v1/admin/brands/{id}               # sku_count=0 AND DISABLED
```

- 错误码：`BRAND_NAME_DUPLICATED`、`BRAND_DELETE_FORBIDDEN`、`BRAND_INVALID_SORT_ORDER` 等，登记 `api-governance`。
- 路径前缀：`/api/v1/admin/brands`（`rules/api.md`）。

### D4：数据模型

```sql
brands (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,           -- max 50
  sort_order INTEGER NOT NULL,         -- 正整数
  short_name TEXT,                     -- max 30
  english_name TEXT,                   -- max 80
  logo_object_key TEXT,
  description TEXT,                    -- max 500
  status TEXT NOT NULL CHECK (status IN ('ENABLED','DISABLED')),
  sku_count INTEGER NOT NULL DEFAULT 0,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
)
```

- **删除策略**：物理删除（PRD 确认弹窗「删除品牌」）；服务端校验失败返回 `BRAND_DELETE_FORBIDDEN`。
- **sku_count**：本期无 SKU 表时固定 0；后续 SKU 模块通过触发器/定时任务或查询更新。

### D5：Logo 存储

- 字段：`brands.logo_object_key`。
- 上传：扩展 `POST /api/v1/admin/uploads`，前缀 `brands/logos/`（或 `MINIO_PREFIX_BRAND_LOGOS`）；JPG/PNG/WebP。
- 列表：无 Logo 时品牌名称首字母缩写占位。

### D6：前端结构

```text
AdminLayout
  └─ BrandManagementPage  (/admin/brands)
       ├─ page-header（MASTER DATA + 新增品牌）
       ├─ metric-grid（4 指标）
       ├─ filter-card（关键词 + 状态 + 查询/重置）
       ├─ table-card + pagination（含 page_size 20/50/100）
       └─ BrandFormModal（add/edit，720px）
       └─ DeleteBrandDialog（确认）
```

- `admin-nav.ts`：`brand` 项 `path: '/admin/brands'`。
- Dashboard `DashboardQuickActions`：「新增品牌」`navigate('/admin/brands')` 或带 query 打开弹窗。

### D7：校验

- 品牌名称：必填、唯一、max 50；blur + submit + 服务端。
- 品牌排序：必填、正整数；错误文案「请输入正整数」。
- 弹窗：无状态、无国家/地区、无规则说明区块。

## Risks / Trade-offs

| 风险 | 缓解 |
|------|------|
| SKU 未实现导致 sku_count 恒为 0 | 文档化；删除规则仍可测；SKU 上线后更新 count |
| PNG 缺失延迟 golden gate | 先 HTML 并排；trace checklist 标注 pending PNG |
| 与用户管理样式分叉 | 共用 metric-card、pagination、modal 模式；抽取可复用 class |
| 物理删除误操作 | 前端双重条件 + 确认弹窗 + 服务端校验 |

## Migration Plan

1. 执行 schema 迁移创建 `brands` 表（可空表启动）。
2. 部署后端 API → 生成 Orval → 部署前端。
3. 回滚：移除路由与 API；`brands` 表保留或 DROP（按发布策略）。

## Open Questions

- [x] 纳入 sprint-002（2026-06-16）
- [ ] PNG 导出责任人 — 实现前或并行补齐 `brand-management.png` / `brand-management-modal.png`

## 验收 Gate

- 视口：**1280×1024**
- 对比源：HTML 原型（PNG 补齐后升级为 golden reference）
- Checklist：见 `openspec/changes/add-brand-management/trace.md`（≥18 项）
