---
requirement_id: REQ-0016-banner-management
title: 管理后台 - Banner 管理
terminal: web-admin
version: v1
status: in_sprint
owner: product
source: capture.md
priority: P1
parent_requirement: REQ-0004-admin-home
---

# REQ-0016 管理后台 - Banner 管理

## 1. 需求背景

管理后台首页（`REQ-0004-admin-home`）已在 OPERATIONS 导航预留「Banner 管理」入口，Dashboard 快捷操作含「新增 Banner」，但当前无列表、表单与后端能力。运营需维护店主 Web 首页、小程序首页与专题运营位的 Banner 素材、排序、跳转目标与生效时间。

本需求交付：

1. 管理端 **Banner 列表页**（检索、指标卡、分页、上线/下线/删除）；
2. **新增/编辑弹窗**，按跳转类型分化交互：`SKU 详情`、`外部链接`、`专题页`、`无跳转`；
3. 后端 API、SQLite 数据模型、MinIO Banner 图片存储；
4. 侧栏与 Dashboard 快捷入口接入真实路由 `/admin/banners`。

关联：`REQ-0006-tile-sku-management`（SKU 图库与详情跳转）、`REQ-0005-brand-management`（列表/启停/删除模式参考）。

## 2. 目标用户

- **后台管理员 / 后台运营**（`admin`、`employee`）：维护 Banner 全生命周期。
- **店主**（`store_owner`）：不得访问 Banner 管理 API 与页面。
- **店主 Web / 小程序消费者**：本期不交付前台 Banner 展示接口与页面（数据模型须预留消费端读取字段）。

## 3. 范围

### 3.1 本期包含

- 路由 `/admin/banners`；`admin-nav.ts` 为「Banner 管理」配置 `path`。
- 列表页：关键词、展示端、状态、时间状态筛选；四指标卡；表格与分页（对齐用户管理/品牌管理）。
- 弹窗：公共字段 + 按 `jump_type` 条件字段；**弹窗内不含状态字段与状态策略说明块**。
- 列表操作：**编辑**、**上线/下线**（二次确认）、**删除**（条件限制 + 二次确认）。
- 跳转类型弹窗变体（4 套，见 §5.3）：
  - `SKU_DETAIL`：关联 SKU、SKU 图库选图或自定义上传，记录 `image_source`。
  - `EXTERNAL_LINK`：HTTPS 外链校验；表单提示小程序白名单/中转规则。
  - `TOPIC_PAGE`：关联专题（最小专题主数据，见 §5.2）。
  - `NO_JUMP`：无跳转目标字段；禁用态提示「无需配置」。
- SQLite 表 `banners`、最小 `topics` 种子表（仅供专题跳转关联与检索）。
- Banner 图片上传走后端授权 + MinIO（`rules/media.md`、单桶前缀策略）。
- OpenAPI 变更 + Orval 客户端 regeneration。
- Dashboard「新增 Banner」快捷操作导航至 `/admin/banners` 并打开新增弹窗（或导航至列表页，实现取「导航 + 自动打开新增」以降低断点）。

### 3.2 本期不包含

- **类目页**跳转类型（列表样例数据可出现 badge，但本期不提供创建/编辑能力；无对应弹窗原型）。
- 店主 Web / 小程序 Banner **消费端**展示、轮播组件、点击跳转实现。
- 小程序外链白名单引擎、中转页完整实现（本期仅管理端 URL 校验 + 文案提示 + 数据落库）。
- 专题内容编辑、专题前台页（仅最小 `topics` 主数据供 Banner 关联）。
- 拖拽排序、复制 Banner、批量操作、导出。
- 弹窗内编辑状态；过期自动下线定时任务（`EXPIRED` 可由列表「时间状态」计算展示，后台 job 后续迭代）。
- 多图轮播、A/B 实验、点击统计。

## 4. 信息架构与导航

```text
admin-shell
├── sidebar（264px sticky）
│   └── OPERATIONS
│       ├── …
│       ├── 瓷砖类目
│       ├── 瓷砖规格（若 REQ-0009 已上线）
│       └── Banner 管理  ← active on /admin/banners
└── main-content
    ├── page-hero（眉标 OPERATIONS / BANNER MANAGEMENT、标题、说明、＋ 新增 Banner）
    ├── filter-card（关键词、展示端、状态、时间状态、查询、重置）
    ├── summary-grid（四指标卡）
    ├── table-section（Banner 列表）
    └── pagination
```

- API 前缀：`/api/v1/admin/banners`；专题检索：`/api/v1/admin/topics`（只读列表，供下拉）。

## 5. 数据模型

### 5.1 表 `banners`

| 字段 | 类型/约束 | 说明 |
|---|---|---|
| id | INTEGER PK | 主键 |
| title | TEXT NOT NULL | 2–30 字；同 `display_client` + `position` 下唯一 |
| display_client | TEXT NOT NULL | `WEB_HOME` \| `MINIAPP_HOME` \| `TOPIC` |
| position | TEXT NOT NULL | `HOME_TOP_CAROUSEL` \| `HOME_MID_SLOT` \| `TOPIC_TOP_BANNER` \| `MINIAPP_HOME_CAROUSEL` |
| image_object_key | TEXT NOT NULL | MinIO object key |
| image_source | TEXT NOT NULL | `sku_main_image` \| `sku_gallery_image` \| `custom_upload` \| `topic_cover`（专题可选，首期可统一 `custom_upload`） |
| sku_gallery_asset_id | INTEGER NULL | 当 `image_source=sku_gallery_image` 时关联 SKU 媒体资产 |
| jump_type | TEXT NOT NULL | `SKU_DETAIL` \| `EXTERNAL_LINK` \| `TOPIC_PAGE` \| `NO_JUMP` |
| sku_id | INTEGER NULL FK | `jump_type=SKU_DETAIL` 时必填 |
| external_url | TEXT NULL | `jump_type=EXTERNAL_LINK` 时必填；须 `https://` |
| topic_id | INTEGER NULL FK | `jump_type=TOPIC_PAGE` 时必填 |
| sort_order | INTEGER NOT NULL | 默认 100；越小越靠前 |
| valid_from | TEXT NULL | ISO 时间；空表示立即生效（受状态约束） |
| valid_to | TEXT NULL | ISO 时间；空表示长期有效 |
| status | TEXT NOT NULL | `DRAFT` \| `ONLINE` \| `OFFLINE` \| `EXPIRED` |
| remark | TEXT NULL | 运营备注，0–200 字 |
| created_at / updated_at | TEXT NOT NULL | ISO 时间 |

**业务唯一键**：`(display_client, position, title)` 在未删除记录间唯一。

**状态规则**：

- 新建默认 `DRAFT`（弹窗保存不展示状态字段）。
- `ONLINE` 仅能通过列表「上线」操作设置；须校验必填项与跳转目标完整性。
- `OFFLINE` 通过列表「下线」。
- `EXPIRED`：当 `valid_to` 早于当前时间且曾为 `ONLINE` 时，列表时间状态展示「已过期」；服务端列表 API MAY 计算 `time_status` 字段，不强制写回 `status`（实现二选一，acceptance 定稿）。

**时间状态**（列表筛选/展示，计算字段 `time_status`）：

- `ACTIVE`：当前生效（已上线且在有效期内）
- `PENDING`：待生效（已上线但 `valid_from` 在未来）
- `EXPIRED`：已过期（`valid_to` 已过）

### 5.2 表 `topics`（最小主数据）

| 字段 | 说明 |
|---|---|
| id | PK |
| code | 唯一编码，如 `TOPIC-202606` |
| title | 专题名称 |
| status | `ENABLED` \| `DISABLED`；Banner 下拉仅 `ENABLED` |
| cover_object_key | 可选封面，供专题 Banner 复用图 |

本期通过 migration **种子数据** 提供 ≥2 条专题；不提供专题管理 CRUD 页面。

### 5.3 展示端与展示位置组合（首期）

| display_client | 允许 position |
|---|---|
| `WEB_HOME` | `HOME_TOP_CAROUSEL`、`HOME_MID_SLOT` |
| `MINIAPP_HOME` | `MINIAPP_HOME_CAROUSEL` |
| `TOPIC` | `TOPIC_TOP_BANNER` |

切换 `display_client` 时 `position` MUST 重置为该端第一个合法选项。

## 6. 功能要求

### FR-001 导航与路由

- `admin-nav.ts`「Banner 管理」MUST 配置 `path: '/admin/banners'`。
- 进入该路由时 Sidebar 项 MUST 高亮；沿用 `AdminLayout`。
- Dashboard 快捷「新增 Banner」MUST 导航至 Banner 管理（见 §3.1）。

### FR-002 列表页 — 页面标题区

- 眉标：`OPERATIONS / BANNER MANAGEMENT`
- 标题：`Banner 管理`
- 说明：`维护前台首页、小程序首页与专题运营位的 Banner 内容、排序、跳转与生效时间。`
- 主按钮：`＋ 新增 Banner`

### FR-003 列表页 — 指标卡

四列只读指标卡（对齐用户管理页视觉）：

- Banner 总数
- 当前筛选结果数
- 已上线（`status=ONLINE`）
- 待生效（`time_status=PENDING`）

### FR-004 列表页 — 检索筛选

- 关键词：匹配 `title`、关联 SKU 名称/编码、专题名称/编码。
- 展示端：全部 / Web 首页 / 小程序首页 / 专题页。
- 状态：全部 / 草稿 / 已上线 / 已下线 / 已过期。
- 时间状态：全部 / 当前生效 / 待生效 / 已过期。
- 「查询」重置页码为 1；「重置」清空条件。
- 控件高度 40px。

### FR-005 列表页 — 表格

列 MUST 包含：Banner（缩略图 86×38）、展示端、跳转类型、状态、有效期、排序、更新时间、操作。

- 跳转类型 Badge：`SKU 详情`、`外部链接`、`专题页`、`无跳转`（样例数据可出现「类目页」badge 但本期不可创建）。
- 操作：**编辑**；**上线/下线**（依状态切换）；**删除**（条件展示）。
- 已上线 Banner 删除前 MUST 先下线（列表提示：`已上线 Banner 需先下线后删除`）。

### FR-006 列表 — 上线/下线

- MUST 二次确认（对齐 `BrandManagementPage` / `REQ-0008-brand-status-confirm`）。
- API：`POST /api/v1/admin/banners/{id}/online`、`POST .../offline`。
- 上线前 MUST 校验：图片、跳转目标、排序、有效期逻辑完整。

### FR-007 列表 — 删除

- 仅当 `status` 为 `DRAFT`、`OFFLINE` 或 `EXPIRED` 时允许删除；`ONLINE` MUST 禁止。
- 删除前二次确认；服务端二次校验。

### FR-008 列表 — 分页

- 左侧：每页条数（10 / 20 / 50）+ `1-10 / 32` 式范围文案（与原型一致）。
- 右侧：上一页、页码、下一页。
- MUST NOT 跳页输入框。

### FR-009 弹窗 — 公共结构与约束

- 居中弹窗：宽 640px、最大高度 92vh、内容区可滚动。
- 标题：`新增 Banner · {跳转类型中文}` / `编辑 Banner · {跳转类型中文}`。
- MUST NOT 展示「状态策略信息」块或状态编辑控件。
- 主按钮「保存 Banner」品牌金实底；次按钮「取消」。
- 公共字段：
  - Banner 标题*（hint：同一展示端 + 展示位置下标题不可重复，建议 2–30 个字符）
  - 展示端*
  - 展示位置*
  - Banner 图片*
  - 跳转类型*（切换时清空不兼容的跳转目标字段）
  - 排序*
  - 有效期（开始/结束，可选；空结束=长期）
  - 运营备注

### FR-010 弹窗 — `SKU_DETAIL`

- MUST 展示关联 SKU 选择器（可搜索 SKU 名称/编码）。
- 选择 SKU 后 MUST 默认 Banner 图来自 SKU **主图**（`image_source=sku_main_image`）。
- MUST 支持从 SKU 图库切换：主图 / 空间图 / 细节图等（`sku_gallery_image` + `sku_gallery_asset_id`）。
- MUST 支持「自定义上传」（`custom_upload`）。
- 保存时 MUST 记录 `image_source`；提示：`选择 SKU 后自动回填 SKU 详情跳转地址`。

### FR-011 弹窗 — `EXTERNAL_LINK`

- MUST 展示外部链接输入框；须 `https://` 开头。
- 保存时 MUST URL 格式与安全校验（禁止 `javascript:` 等）。
- 表单说明：`保存时校验 URL 合法性；小程序端外链需走业务白名单或中转页。`
- Banner 图 MUST 用户上传（与 SKU 无绑定）。

### FR-012 弹窗 — `TOPIC_PAGE`

- MUST 展示关联专题选择器；支持按专题名称 / 编码搜索。
- 说明：`选择专题后，前台点击 Banner 进入专题详情页。`
- Banner 图：用户上传或从专题封面复用（首期实现上传为主；封面复用可选增强）。

### FR-013 弹窗 — `NO_JUMP`

- MUST NOT 展示可编辑跳转目标字段。
- MUST 展示禁用态「跳转目标：无需配置」。
- 说明：`选择无跳转时，前台 Banner 仅展示图片与文案，不响应点击跳转。`

### FR-014 后端 API

- `GET /api/v1/admin/banners` — 分页 + keyword + display_client + status + time_status
- `GET /api/v1/admin/banners/{id}`
- `POST /api/v1/admin/banners` — 创建，默认 `DRAFT`
- `PUT /api/v1/admin/banners/{id}` — 更新（`ONLINE` 状态 MAY 限制部分字段，实现取「允许编辑但保存不自动改状态」）
- `POST /api/v1/admin/banners/{id}/online` / `offline`
- `DELETE /api/v1/admin/banners/{id}`
- `POST /api/v1/admin/banners/upload-image` — 授权上传（或复用通用 media API，OpenSpec 定稿）
- `GET /api/v1/admin/topics` — 只读，`status=ENABLED`，供专题下拉

权限：`require_admin_access`（`admin` | `employee`）。

### FR-015 媒体与 MinIO

- Banner 自定义上传 MUST 走后端授权 + MinIO；前缀遵循 `rules/object-storage.md`（如 `MINIO_PREFIX_BANNERS`）。
- SKU 图库引用 MUST NOT 重复上传文件；存储引用 SKU 已有 `object_key`。

## 7. UI / UE 约束

- TILESFST 暗色旗舰风；Sidebar、标题区、筛选卡、指标卡、表格、弹窗、按钮、输入框 **对齐用户管理列表页**。
- semantic token；禁止裸 Hex；优先 `AdminListPage` + shared/ui + shadcn。
- 主 CTA 品牌金；圆角 2px（`rounded-industrial`）；输入/选择器高度 40px。
- 弹窗 640px / 92vh 可滚动（与原型一致）。
- 视觉验收优先级：`prototype/web/*.html` > `*.png` > `prototype/web/*-context.md` > 本文 > `rules/ui-design.md`。

## 8. 关联需求

| 需求 | 关系 |
|---|---|
| REQ-0004-admin-home | 父需求；导航占位与 Dashboard 快捷入口 |
| REQ-0006-tile-sku-management | SKU 图库、详情跳转数据源 |
| REQ-0005-brand-management | 列表/启停/删除/分页/指标卡模式参考 |
| REQ-0008-brand-status-confirm | 上线/下线二次确认交互参考 |
| REQ-0009-tile-spec-management | 同级 OPERATIONS 导航；侧栏顺序在其之后 |

## 9. 文档与 OpenSpec

- 原型已落盘：`prototype/web/`（列表 + 4 弹窗 HTML/PNG/context）。
- 预期 OpenSpec change：`add-banner-management`。
- `/req-complete` 补齐 user-stories、business-flow、acceptance。

## 10. 状态

```yaml
requirement_id: REQ-0016-banner-management
title: 管理后台 - Banner 管理
terminal: web-admin
version: v1
status: in_sprint
owner: product
priority: P1
parent_requirement: REQ-0004-admin-home
iteration: null
openspec_change: null
```
