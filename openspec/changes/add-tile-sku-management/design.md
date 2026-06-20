## Context

- **现状**：`admin-nav.ts` 中「瓷砖SKU」无 `path`；`tiles` 表仅有 name/model/category/color/size/description/status；`tile_images` 已有 `is_main`；无视频表与 SKU Admin API；Dashboard「新增 SKU」为占位 toast。
- **依赖**：`add-admin-home`（`AdminLayout`）；`add-brand-management`（品牌下拉）；`add-tile-category-management`（类目下拉）；参考 `add-brand-management` 列表/弹窗 CSS Port 模式。
- **原型来源**（优先级，不可省略）：
  1. `issues/requirements/REQ-0006-tile-sku-management/prototype/web/tile-sku-management-list.html`
  2. `issues/requirements/REQ-0006-tile-sku-management/prototype/web/tile-sku-create-modal.html`
  3. `issues/requirements/REQ-0006-tile-sku-management/prototype/images/*.png`（待导出）
  4. `issues/requirements/REQ-0006-tile-sku-management/prototype/web/*-context.md`
  5. `issues/requirements/REQ-0006-tile-sku-management/acceptance.md`
  6. `rules/ui-design.md`
  7. `openspec/specs/`

## Conflict Resolution

| 检查项 | HTML | PNG | acceptance / PRD | 决议 |
|--------|------|-----|------------------|------|
| 内容区 max-width | 1120px | — | context §3 | **以 HTML 为准**（SKU 页宽于品牌 1080px） |
| 弹窗宽度 | 880px | 待 PNG | AC-022 | 以 HTML 为准 |
| 弹窗状态字段 | 无 | — | AC-025 | 一致；创建默认 DRAFT |
| 价格 Label | 「参考价格（元）」 | — | AC-026 | 以 HTML 为准 |
| 保存草稿 vs 创建SKU | 两按钮 | — | review 条件项 | **见 D8** |
| 每页默认条数 | 20 | — | AC-020 | 默认 page_size=20 |
| 筛选触发 | 查询按钮 | — | AC-012 | 以 PRD/HTML 为准（点击查询/回车，非自动防抖） |
| PNG Golden Reference | — | 可选 | trace Ready | HTML 为 gate；PNG 有则增强，无则不阻塞 |
| `model` vs `sku_code` | SKU编码字段 | — | trace schema 差距 | **新增 `sku_code`**，保留 `model` 迁移期 MAY 同步或弃用 |

## Goals / Non-Goals

**Goals:**

- `/admin/tile-skus` 列表 + 弹窗与 v4 HTML 在 1440×1024（验收 MAY 用 1280×1024）并排 pass。
- CSS Port：`tile-sku-management.css`；Shell 复用 `AdminLayout` + `admin-home.css`。
- 完整 Admin Tile SKU API + schema 扩展 + Orval + 测试。
- 多图主图、多视频、参考价格、素材完整度筛选、上下架。
- ≥20 项 HTML checklist 写入 change `trace.md`。

**Non-Goals:**

- SKU 批量导入/导出、复制、审批流、库存、促销价、店主端详情页、视频转码多清晰度。
- 细粒度只读 RBAC（本期文档化 `tile_sku:*` 权限点，后端 `require_admin_user` 即可）。

## Decisions

### D1：CSS Port（路径 A，与 add-admin-home / add-brand-management 一致）

- **决策**：新增 `src/web/src/features/admin/styles/tile-sku-management.css`，自 list/modal HTML v4 port；Shell 复用 `AdminLayout`。
- **理由**：v4 HTML 含完整 metric-grid、五维筛选、素材列 badge、880px 双列弹窗与 upload-grid；Tailwind 拼装 fidelity 风险高。
- **备选**：DS Primitives + `AdminListPage` — 与原型像素差风险大，不采用。

### D2：权限模型

| 角色 | SKU 管理 |
|---|---|
| `admin` | 全部 CRUD + publish/unpublish/delete |
| `employee` | 同上（OPERATIONS 主数据维护） |
| `store_owner` | 不可访问管理端 |

- API 依赖：`require_admin_user`（admin + employee）。
- 只读账号：后续 RBAC；本期 MAY 全员写权限，UI 只读模式留扩展点。

### D3：API 设计

```text
GET    /api/v1/admin/tile-skus              # keyword, brand_id, category_id, status, material_completeness, page, page_size + summary
POST   /api/v1/admin/tile-skus              # 创建；save_mode=draft|create；默认 status=DRAFT
GET    /api/v1/admin/tile-skus/{id}
PUT    /api/v1/admin/tile-skus/{id}
POST   /api/v1/admin/tile-skus/{id}/publish
POST   /api/v1/admin/tile-skus/{id}/unpublish
DELETE /api/v1/admin/tile-skus/{id}         # 非 PUBLISHED 且无 business_reference
POST   /api/v1/admin/uploads                # 扩展 tiles/images、tiles/videos 前缀
```

- 错误码：`TILE_SKU_CODE_DUPLICATED`、`TILE_SKU_DELETE_FORBIDDEN`、`TILE_SKU_PUBLISH_FORBIDDEN` 等。
- 列表默认排序：`updated_at DESC`。

### D4：数据模型

```sql
-- 扩展 tiles（SKU 主表）
tiles (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,                    -- SKU 名称
  sku_code TEXT NOT NULL UNIQUE,         -- SKU 编码（原 model 字段迁移或并存）
  brand_id INTEGER NOT NULL REFERENCES brands(id),
  category_id INTEGER NOT NULL REFERENCES tile_categories(id),
  size TEXT NOT NULL,                    -- 规格尺寸
  surface_finish TEXT NOT NULL,          -- 表面工艺
  color_family TEXT,                     -- 主色系
  reference_price REAL,                  -- 参考价格（元），两位小数
  remark TEXT,                           -- 备注（原 description 可映射）
  status TEXT NOT NULL CHECK (status IN ('PUBLISHED','DRAFT','NEEDS_COMPLETION','DISABLED')),
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
)

tile_images (已有，保留 is_main, sort_order)

tile_videos (
  id INTEGER PRIMARY KEY,
  tile_id INTEGER NOT NULL REFERENCES tiles(id),
  object_key TEXT NOT NULL,
  file_name TEXT NOT NULL,
  file_size_bytes INTEGER,
  duration_seconds REAL,
  sort_order INTEGER NOT NULL DEFAULT 0,
  created_at TEXT NOT NULL
)
```

- **素材完整度**（计算字段）：`complete` | `missing_main_image` | `missing_images` | `missing_videos`。
- **NEEDS_COMPLETION**：必填齐全但缺主图或关键素材时由服务端或创建逻辑设置。

### D5：媒体存储

- 图片：`tiles/{tile_id}/images/{image_id}.{ext}`；`tile_images.is_main=1` 标记主图。
- 视频：`tiles/{tile_id}/videos/{video_id}/source.{ext}`；封面 MAY 后续扩展。
- MIME/大小：见 `rules/media.md` 与 `.env.example`。

### D6：前端结构

```text
AdminLayout
  └─ TileSkuManagementPage  (/admin/tile-skus)
       ├─ page-head（OPERATIONS / SKU + 新增SKU）
       ├─ metric-grid（SKU总数/已上架/待完善/草稿）
       ├─ filter-card（5 筛选项 + 查询/重置）
       ├─ table-card + pagination（10/20/50/100）
       └─ TileSkuFormModal（add/edit，880px）
       └─ ConfirmDialog（删除/上下架）
```

- `admin-nav.ts`：`tile-sku` 项 `path: '/admin/tile-skus'`。
- Dashboard「新增 SKU」：`navigate('/admin/tile-skus?action=create')` MAY 打开弹窗。

### D7：价格展示

- 表单 Label：「参考价格（元）」；输入 number，两位小数。
- 列表：`¥ {price.toFixed(2)}`；空值显示「—」。

### D8：「保存草稿」vs「创建SKU」

| 按钮 | 客户端校验 | 服务端 save_mode | 结果 status | Toast |
|------|-----------|------------------|-------------|-------|
| 保存草稿 | 仅 SKU 名称必填（MAY 允许全空仅创建壳，实现取名称必填） | `draft` | `DRAFT` | 「草稿已保存」 |
| 创建SKU | 全部必填项（名称、编码、品牌、类目、规格、工艺） | `create` | `DRAFT`（缺主图时 MAY 设 `NEEDS_COMPLETION`） | 「SKU创建成功，已保存为草稿」 |

- 两者均不在弹窗选择 status；上架通过列表「上架」操作（publish）。
- 缺主图：两种模式均允许保存；列表素材列显示「缺主图」。

## Risks / Trade-offs

| 风险 | 缓解 |
|------|------|
| 品牌/类目 change 未 apply | SKU change 依赖其 API；sprint 排序 brand → category → sku |
| PNG 缺失 | HTML 并排即可验收；PNG 为可选 golden reference |
| `tiles` 扩展 vs 新表 | 扩展现表减少迁移成本；`model`→`sku_code` 数据迁移脚本 |
| 视频上传体积 | 环境变量限制 + 前端进度/错误提示 |

## Migration Plan

1. ALTER `tiles` 添加新列；迁移 `model`→`sku_code`；创建 `tile_videos`。
2. 部署 API → Orval → 前端。
3. 回滚：禁用路由；表结构保留。

## Open Questions

- [ ] PNG 导出（**可选**）— `prototype/images/*.png` 有则用于 golden reference
- [x] 保存草稿 vs 创建SKU — **D8 已决**

## 验收 Gate

- 视口：**1440×1024**（MAY 1280×1024 回归）
- 对比源：**HTML 原型**（主 gate）；PNG 为可选 golden reference
- Checklist：见 `openspec/changes/add-tile-sku-management/trace.md`
