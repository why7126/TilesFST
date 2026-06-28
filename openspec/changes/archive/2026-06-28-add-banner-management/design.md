## Context

- **现状**：`admin-nav.ts`「Banner 管理」无 `path`；Dashboard「新增 Banner」走 `onPlaceholder()`；无 `banners`/`topics` 表。
- **依赖**：`add-admin-home`（Shell、Dashboard）；`add-brand-management`（列表/启停/删除/确认模式）；`add-tile-sku-management`（`tile_images`、SKU 详情）；`update-object-storage-key-layout`（`images/` 前缀，同 Sprint 须对齐 Key 形态）。
- **原型来源**（优先级，MUST 声明）：
  1. `issues/requirements/archive/REQ-0016-banner-management/prototype/web/banner-management-list.html`
  2. `issues/requirements/archive/REQ-0016-banner-management/prototype/web/banner-management-list.png`
  3. `issues/requirements/archive/REQ-0016-banner-management/prototype/web/banner-management-modal-{sku-detail|external-link|topic-page|no-jump}.html`
  4. 对应 modal `*.png`
  5. `prototype/web/*-context.md`
  6. `issues/requirements/archive/REQ-0016-banner-management/acceptance.md`
  7. `rules/ui-design.md`
  8. `openspec/specs/`

## Conflict Resolution

| 检查项 | HTML/PNG | PRD v1 | acceptance | 决议 |
|--------|----------|--------|------------|------|
| 列表标题 | Banner管理 | Banner 管理 | AC-003 | 实现用「Banner 管理」（空格） |
| 跳转类型 Badge 样例 | 含「类目页」 | Out of Scope | AC-014 | 样例 MAY 展示；**不可创建**类目页类型 |
| 弹窗状态块 | 无 | 弹窗不含状态 | AC-026 | 一致；列表维护上线/下线 |
| 分页文案 | `1-10 / 32` | 同左 | AC-021 | 一致（非品牌页「共 x 条」） |
| `time_status` vs `status` | 筛选含时间状态 | 计算字段 | AC-010~011 | OpenSpec：`time_status` 服务端计算；`EXPIRED` status 与筛选规则见 D6 |
| SKU 图库 | modal-sku-detail | FR-010 | AC-031~033 | 单弹窗 + jump_type 分支，非 4 独立页面组件 |
| object_key 前缀 | — | MinIO | AC-045 | 采用 `images/default/banners/{uuid}.{ext}`（与 REQ-0012 对齐） |

## Goals / Non-Goals

**Goals:**

- `/admin/banners` 与 list HTML + PNG 在 1440×1024 并排验收 pass。
- 四套 modal HTML + PNG 并排验收 pass（jump_type 条件显隐）。
- CSS Port：`banner-management.css`；Shell 复用 `AdminLayout` + 品牌页 online/offline 确认模式。
- 完整 Banners API + topics 种子 + Orval + 测试。
- Dashboard 快捷「新增 Banner」+ Sidebar path 落地。

**Non-Goals:**

- 店主 Web / 小程序 Banner 轮播消费端。
- 类目页跳转、专题 CRUD、外链白名单/中转页引擎。
- 拖拽排序、复制、批量、导出、过期自动下线 job。
- 弹窗内编辑 status。

## Decisions

### D1：CSS Port + 单弹窗 jump_type 分支（路径 A）

- **决策**：新增 `features/admin/styles/banner-management.css`，自 `banner-management-*.html` port；**一个** `BannerFormModal` 组件，按 `jump_type` 条件渲染字段（非 4 个独立 Modal 组件）。
- **理由**：四套 HTML 差异仅在条件块；单组件避免状态同步重复；与 prototype 标题「新增 Banner · {类型}」一致。
- **备选**：4 独立 Modal — 维护成本高，不采用。

### D2：权限模型

| 角色 | Banner 管理 |
|---|---|
| `admin` | CRUD + online/offline + 条件删除 |
| `employee` | 同上 |
| `store_owner` | 403 |

- API：`require_admin_access`（与 brands 一致）。

### D3：API 设计

```text
GET    /api/v1/admin/banners              # keyword, display_client, status, time_status, page, page_size + summary
GET    /api/v1/admin/banners/{id}
POST   /api/v1/admin/banners              # 创建；默认 DRAFT
PUT    /api/v1/admin/banners/{id}         # 更新；不自动改 status
POST   /api/v1/admin/banners/{id}/online
POST   /api/v1/admin/banners/{id}/offline
DELETE /api/v1/admin/banners/{id}         # status != ONLINE
POST   /api/v1/admin/uploads/banner-images   # 或等价；返回 object_key
GET    /api/v1/admin/topics               # keyword, status=ENABLED；只读
```

- 错误码：`BANNER_TITLE_DUPLICATED`、`BANNER_JUMP_TARGET_INVALID`、`BANNER_DELETE_FORBIDDEN`、`BANNER_NOT_FOUND`、`BANNER_EXTERNAL_URL_INVALID`。

### D4：数据模型

```sql
banners (
  id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  display_client TEXT NOT NULL,  -- WEB_HOME | MINIAPP_HOME | TOPIC
  position TEXT NOT NULL,
  image_object_key TEXT NOT NULL,
  image_source TEXT NOT NULL,      -- sku_main_image | sku_gallery_image | custom_upload | topic_cover
  sku_gallery_asset_id INTEGER REFERENCES tile_images(id),
  jump_type TEXT NOT NULL,         -- SKU_DETAIL | EXTERNAL_LINK | TOPIC_PAGE | NO_JUMP
  sku_id INTEGER REFERENCES tiles(id),
  external_url TEXT,
  topic_id INTEGER REFERENCES topics(id),
  sort_order INTEGER NOT NULL DEFAULT 100,
  valid_from TEXT,
  valid_to TEXT,
  status TEXT NOT NULL CHECK (status IN ('DRAFT','ONLINE','OFFLINE','EXPIRED')),
  remark TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  UNIQUE(display_client, position, title)
)

topics (
  id INTEGER PRIMARY KEY,
  code TEXT NOT NULL UNIQUE,
  title TEXT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('ENABLED','DISABLED')),
  cover_object_key TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
)
```

- migration 种子 ≥2 条 `ENABLED` topics（对齐 prototype 文案）。

### D5：跳转类型与图片

- `SKU_DETAIL`：必选 `sku_id`；默认 `image_source=sku_main_image`；可切换 `tile_images` 或 `custom_upload`。
- `EXTERNAL_LINK`：必选 `https://` `external_url`；`custom_upload` 图。
- `TOPIC_PAGE`：必选 `topic_id`；首期 `custom_upload` 为主。
- `NO_JUMP`：无跳转目标；UI 禁用「无需配置」。
- 切换 `jump_type` MUST 清空不兼容字段；切换 `display_client` MUST 重置 `position` 为合法默认。

### D6：`time_status` 计算（列表 API）

| time_status | 条件 |
|---|---|
| `ACTIVE` | `status=ONLINE` 且（`valid_from` 为空或 ≤now）且（`valid_to` 为空或 ≥now） |
| `PENDING` | `status=ONLINE` 且 `valid_from` > now |
| `EXPIRED` | `valid_to` < now（不论 status；列表 badge 可展示已过期） |

- 筛选 `time_status` 基于计算字段；**不**强制后台 job 写回 `status=EXPIRED`（可选增强）。

### D7：前端结构

```text
AdminLayout
  └─ BannerManagementPage (/admin/banners)
       ├─ page-hero + filter + metric-grid + table + pagination
       ├─ BannerFormModal (640px, jump_type 分支)
       ├─ OnlineOfflineConfirmDialog（对齐 BrandManagementPage）
       └─ DeleteConfirmDialog

DashboardPage
  └─ quick action banner → navigate('/admin/banners?action=create')
```

### D8：与 object-storage-key-layout 协调

- Banner 自定义上传 Key：`images/default/banners/{uuid}.{ext}`。
- 若 `update-object-storage-key-layout` 尚未 apply，实现时 MUST 使用同一 `build_upload_object_key()` 入口，避免 `original/` 新对象。

## Risks / Trade-offs

| 风险 | 缓解 |
|---|---|
| Sprint 容量 29 人天 | 0016 排在 apply 队列末位；可与 0009 后端并行 |
| 消费端不可验 | release note 声明；后续独立 REQ |
| REQ-0012 与 Banner 上传 Key 不一致 | D8 统一 `build_upload_object_key` |

## Open Questions

- 无阻塞项；专题封面复用为可选增强（首期 custom_upload）。
