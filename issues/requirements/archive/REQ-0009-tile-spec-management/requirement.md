---
requirement_id: REQ-0009-tile-spec-management
title: 管理后台 - 瓷砖规格管理
terminal: web-admin
version: v2
status: in_sprint
owner: product
source: capture.md
priority: P1
parent_requirement:
---

# REQ-0009 管理后台 - 瓷砖规格管理

## 1. 需求背景

瓷砖规格是 SKU 建档、列表展示、筛选检索与前台规格说明的基础主数据。当前 `TileSkuFormModal` 中「规格尺寸」为自由文本（`tiles.size`），运营手写易产生重复、拼写不一致；且系统尚无独立规格主数据管理能力。

本需求交付：

1. 管理后台 **瓷砖规格** 主数据页（CRUD、检索、启停、条件删除）；
2. 左侧 OPERATIONS 导航在「瓷砖类目」之后新增同级入口「瓷砖规格」；
3. SKU 表单「规格尺寸」改为 **下拉选择已启用规格主数据**，并通过 `spec_id` 与主数据关联。

关联能力：瓷砖类目（`REQ-0005-tile-category-management`）、瓷砖 SKU（`REQ-0006-tile-sku-management`）、品牌启停确认模式（`REQ-0008-brand-status-confirm`）。

## 2. 目标用户

- **后台管理员 / 后台运营**（`admin`、`employee`）：维护规格主数据；在 SKU 表单中选择规格。
- **店主**（`store_owner`）：不得访问管理端规格 API 与页面（与现有管理端 RBAC 一致）。

## 3. 范围

### 3.1 本期包含

- 管理端路由与页面：瓷砖规格列表页 + 新增/编辑弹窗。
- 左侧导航：OPERATIONS 区「瓷砖类目」与「Banner 管理」之间新增同级菜单「瓷砖规格」。
- 规格主数据：宽/长（必填）、厚度（可选）、**单位**（库表字段，默认 `mm`）、排序、备注；**尺寸名称系统生成**；**启停状态**（列表维护，弹窗不含状态字段）。
- 列表交互 **对齐瓷砖品牌管理**：关键词 + 状态筛选、查询/重置、启停二次确认、条件删除、分页。
- 后端 API、SQLite 表 `tile_specs`、`tiles.spec_id` 外键、`sku_count` 维护、`size` 冗余同步。
- **SKU 表单改造**：规格由自由文本改为下拉（仅 `ENABLED` 规格）；创建/更新/发布校验联动。
- **历史 SKU 迁移**：按 `display_name` 或宽长匹配回填 `spec_id`（无法匹配项在 acceptance 定义处理策略）。
- OpenAPI 变更 + Orval 客户端 regeneration。

### 3.2 本期不包含

- 导出、批量操作、跳页输入框。
- 弹窗内编辑「规格类型」「常用尺寸」「系统状态」；规格类型若展示仅为系统分类/统计，不可在弹窗维护。
- 前台店主端 / 小程序规格展示改造。
- 多语言、拖拽排序、inch 等非 mm 单位的 UI 切换（单位字段预留，首期 UI 固定 mm）。
- 新增 `readonly` 角色或变更全局 RBAC 模型。

## 4. 信息架构与导航

```text
admin-shell
├── sidebar（264px sticky）
│   └── OPERATIONS
│       ├── 首页
│       ├── 瓷砖 SKU
│       ├── 瓷砖品牌
│       ├── 瓷砖类目
│       ├── 瓷砖规格  ← 新增，active 时高亮
│       └── Banner 管理
└── main-content
    ├── page-header（眉标 MASTER DATA、标题、说明、＋ 新增瓷砖规格）
    ├── metric-grid（四指标卡，对齐品牌页）
    ├── filter-card（关键词、状态、查询、重置）
    ├── table-card（规格列表，无额外 section 标题行）
    └── pagination（左「共 x 条」+ 右页码与每页条数）
```

- 路由建议：`/admin/tile-specs`；API 前缀 `/api/v1/admin/tile-specs`。
- 页面标题：**瓷砖规格**（req-complete 阶段统一 prototype 中「瓷砖尺寸」文案）。

## 5. 数据模型

### 5.1 表 `tile_specs`（逻辑字段）

| 字段 | 类型/约束 | 说明 |
|---|---|---|
| id | INTEGER PK | 主键 |
| width_mm | INTEGER NOT NULL | 1–9999 |
| length_mm | INTEGER NOT NULL | 1–9999 |
| thickness_mm | REAL NULL | 可选，1 位小数，1–99.9 |
| unit | TEXT NOT NULL DEFAULT `'mm'` | 首期固定 `mm`；参与 `display_name` 生成 |
| display_name | TEXT NOT NULL | 系统生成，如 `800×800mm` |
| sort_order | INTEGER NOT NULL | 默认 100；越小越靠前 |
| status | TEXT NOT NULL | `ENABLED` \| `DISABLED`；新建默认 `ENABLED` |
| sku_count | INTEGER NOT NULL DEFAULT 0 | 只读计数 |
| remark | TEXT NULL | 0–200 字 |
| spec_type | TEXT NULL | 可选；系统分类（标准/大板/异形等），列表只读，弹窗不可编辑 |
| created_at / updated_at | TEXT NOT NULL | ISO 时间 |

**业务唯一键**：`(width_mm, length_mm, unit)`。厚度、排序、备注、状态不参与唯一性。

**display_name 生成**：

```text
display_name = width_mm + "×" + length_mm + unit
```

示例：800、800、`mm` → `800×800mm`。

### 5.2 表 `tiles`（SKU）变更

| 字段 | 变更 |
|---|---|
| spec_id | 新增 INTEGER NULL → FK `tile_specs.id` |
| size | 保留；创建/更新 SKU 时 MUST 同步为所选规格的 `display_name`（冗余展示字段） |

### 5.3 启停与 SKU 引用规则

- **新建 SKU**：下拉 MUST 仅展示 `status = ENABLED` 的规格。
- **已绑定 SKU 的规格**：允许 **停用**；停用后已关联 SKU 仍保留 `spec_id` 与 `size` 展示，不要求自动改绑。
- **删除**：仅当 `sku_count = 0` **且** `status = DISABLED`（与品牌/类目一致）。

## 6. 功能要求

### FR-001 导航与路由

- OPERATIONS 导航 MUST 在「瓷砖类目」之后、「Banner 管理」之前新增同级菜单「瓷砖规格」。
- 进入 `/admin/tile-specs` 时对应 Sidebar 项 MUST 高亮；沿用 `AdminLayout` 与 `admin-nav.ts` 扩展模式。

### FR-002 数据概览（指标卡）

- 四列只读指标卡，对齐品牌页语义：
  - 规格总数
  - 启用规格（`ENABLED`）
  - 停用规格（`DISABLED`）
  - 未关联 SKU（`sku_count = 0`）

### FR-003 检索与筛选

- 筛选区 MUST 包含：关键词、状态（全部 / 启用 / 停用）、**查询**、**重置**。
- 关键词 MUST 支持对 `display_name`、宽/长数值、备注模糊匹配。
- 「查询」MUST 重置页码为 1；「重置」MUST 清空关键词并恢复状态为「全部」。
- MUST NOT 出现导出、批量操作。

### FR-004 规格列表

- 表格列 MUST 包含：尺寸名称、宽度(mm)、长度(mm)、厚度(mm)、关联 SKU、排序、**状态**、更新时间、操作。
- 操作列 MUST 包含：**编辑**、**启用/停用**、**删除**（条件展示）。
- 状态列 MUST 使用与品牌页一致的 badge 样式。
- 表格卡片 MUST NOT 展示额外「规格列表」标题行。

### FR-005 启停操作

- 列表行「启用/停用」MUST 二次确认（文案与交互对齐 `BrandManagementPage` / `REQ-0008-brand-status-confirm`）。
- 提供 `POST /api/v1/admin/tile-specs/{id}/enable` 与 `.../disable`。
- 弹窗内 MUST NOT 包含状态字段；新建记录默认 `ENABLED`。

### FR-006 新增 / 编辑弹窗

- 「＋ 新增瓷砖规格」与行内「编辑」打开同一结构居中弹窗。
- 弹窗字段：
  - 宽度(mm)*、长度(mm)*
  - 尺寸名称（系统生成，只读，跨列）
  - 厚度(mm)、排序*
  - 备注（跨列）
- 弹窗 MUST NOT 包含：单位选择（首期固定 mm）、规格类型、常用尺寸、系统状态、可编辑尺寸名称。
- 宽、长填写后 MUST 实时生成 `display_name`；若 `(width_mm, length_mm, unit)` 冲突 MUST 提示「该尺寸已存在，请勿重复创建」并禁止提交。
- 保存成功后关闭弹窗并刷新列表与指标卡。

### FR-007 删除规则

- 允许删除条件：`sku_count = 0` **AND** `status = DISABLED`。
- 不满足条件时删除入口 MUST 置灰；hover 提示：`仅允许删除未关联SKU且已停用的规格`。
- 删除前 MUST 二次确认；服务端 MUST 二次校验，失败返回业务错误码（建议 `TILE_SPEC_DELETE_FORBIDDEN`）。

### FR-008 分页

- 左侧：`共 {total} 条`。
- 右侧：上一页、页码、下一页、每页条数（20 / 50 / 100）。
- MUST NOT 展示跳页输入框、「当前显示 x-y」等文案。

### FR-009 后端 API

- MUST 提供：`GET` 列表（分页+keyword+status）、`GET` 详情、`POST` 创建、`PUT` 更新、`POST` enable/disable、`DELETE` 删除。
- 可选：`GET` 精简列表（仅 `ENABLED`，供 SKU 下拉，可与列表 API 复用 `status=ENABLED` 参数）。
- 创建/更新时服务端 MUST 生成 `display_name`、固定 `unit='mm'`（首期）、执行唯一性校验。
- SKU 创建/更新/删除/变更 `spec_id` 时 MUST 维护对应规格的 `sku_count`（与 `brands.sku_count` 同模式）。
- API MUST 使用 `require_admin_access`（`admin` | `employee`）；`store_owner` MUST 403。

### FR-010 SKU 表单联动

- `TileSkuFormModal`「规格尺寸」MUST 由 `<input>` 改为 `<select>`，数据源为 **已启用** 规格列表，按 `sort_order ASC, id ASC` 排序。
- 选项展示：`display_name`（可副行展示厚度，若有）。
- 创建/更新 SKU MUST 提交 `spec_id`；服务端 MUST 校验规格存在且为 `ENABLED`（编辑已绑定停用规格的历史 SKU 时，允许保留原 `spec_id` 仅更新非规格字段，或强制换绑——实现取「允许保留原 spec_id」以降低运营阻塞）。
- 服务端 MUST 将 `tiles.size` 同步为所选规格 `display_name`。
- 上架校验（现有「规格尺寸不完整」）MUST 改为：`spec_id` 有效且 `size` 非空。

### FR-011 历史数据迁移

- 上线迁移脚本或一次性任务 MUST 尝试将现有 `tiles.size` 匹配到 `tile_specs.display_name`（或解析 `宽×长mm` 匹配 `(width_mm, length_mm, unit)`）。
- 无法自动匹配的 SKU MUST 在管理端仍可打开编辑，但保存/上架前 MUST 要求运营手动选择规格（acceptance 中定义提示文案）。
- 迁移 MUST NOT 删除或覆盖原有 `size` 文本直至成功绑定 `spec_id`。

### FR-012 权限

- 与现有管理端主数据一致：`admin`、`employee` 可查看、新增、编辑、启停、删除（满足 FR-007 条件）。
- MUST NOT 引入 `readonly` 角色；权限实现沿用 `require_admin_access`，不新增 `require_system_admin` 除非产品另行决策。

## 7. UI / UE 约束

- MUST 继承 TILESFST 管理后台暗色旗舰风：semantic token、禁止裸 Hex；组件优先 `AdminListPage` + 既有 shared/ui / shadcn。
- 列表/启停/删除/分页 MUST 与 `BrandManagementPage` 行为一致；启停确认弹窗对齐品牌页。
- prototype（`tile-size-management*.html`）在 req-complete 阶段 MUST 补充 **状态列、启停操作、状态筛选**，并将文案统一为「瓷砖规格」。
- OpenSpec 视觉验收以更新后 prototype 为准（HTML > PNG > acceptance）。

## 8. 关联需求

| 需求 | 关系 |
|---|---|
| REQ-0005-tile-category-management | 同级主数据；导航位于其下 |
| REQ-0006-tile-sku-management | MODIFIED：SKU 规格由文本改为 spec 下拉 |
| REQ-0005-brand-management | 列表/启停/删除/分页/指标卡模式参考 |
| REQ-0008-brand-status-confirm | 启停二次确认交互参考 |

## 9. 文档与 OpenSpec

- 六件套已齐（见 `trace.md` documents）；PNG Golden Reference **待导出**。
- 预期 OpenSpec change：`add-tile-spec-management`。

## 10. 状态

```yaml
requirement_id: REQ-0009-tile-spec-management
title: 管理后台 - 瓷砖规格管理
terminal: web-admin
version: v2
status: in_sprint
owner: product
priority: P1
parent_requirement:
iteration: null
openspec_change: null
```
