---
title: 需求验收标准
purpose: 瓷砖规格管理、SKU 联动、迁移与接口验收
content: 基于 requirement.md v2 与 prototype/web/tile-size-management-* 提炼
source: AI 根据 PRD 与原型生成，项目团队确认
update_method: PRD 或原型变更时同步更新
owner: product
status: draft
created_at: 2026-06-27 22:53:26
updated_at: 2026-06-27 22:53:26
note: REQ-0009-tile-spec-management
---

# 验收标准

## 1. 功能验收 — 规格管理页

### 1.1 访问与布局

- [ ] **AC-001** 已登录 `admin`/`employee` 可访问 `/admin/tile-specs`，页面标题「瓷砖规格」。
- [ ] **AC-002** Sidebar OPERATIONS「瓷砖规格」激活；位于「瓷砖类目」与「Banner 管理」之间；继承 AdminLayout（264px Sidebar、内容区 max-width 1080px）。
- [ ] **AC-003** 页头含 eyebrow `MASTER DATA`、说明文案、主按钮「＋ 新增瓷砖规格」。
- [ ] **AC-004** 无导出、无批量操作、无列表 section 标题行。

### 1.2 数据概览

- [ ] **AC-005** 四指标卡：规格总数、启用规格、停用规格、未关联 SKU；与 API `summary` 一致。
- [ ] **AC-006** 指标卡视觉与品牌管理页 metric-card 一致（semantic token，无裸 Hex）。

### 1.3 搜索与筛选

- [ ] **AC-007** 筛选区一行：关键词、状态（全部/启用/停用）、查询、重置。
- [ ] **AC-008** 关键词匹配 `display_name`、宽/长数值、备注（模糊）。
- [ ] **AC-009** 查询重置 page=1；重置清空关键词并恢复「全部状态」。

### 1.4 规格列表

- [ ] **AC-010** 表格列：尺寸名称、宽度(mm)、长度(mm)、厚度(mm)、关联 SKU、排序、状态、更新时间、操作。
- [ ] **AC-011** 状态列 badge：启用 / 停用（样式对齐品牌页）。
- [ ] **AC-012** 操作列：编辑、启用/停用、删除（条件展示）；无其他操作。

### 1.5 启停

- [ ] **AC-013** 启停点击弹出二次确认（文案/按钮对齐 `BrandManagementPage`）。
- [ ] **AC-014** 新建规格默认 `ENABLED`；弹窗不含状态字段。
- [ ] **AC-015** 已关联 SKU 的规格可停用；停用后 SKU 列表仍展示原 `size` 文本。

### 1.6 删除

- [ ] **AC-016** 仅 `sku_count=0` 且 `status=DISABLED` 时删除可点击。
- [ ] **AC-017** 其余情况删除置灰，hover：`仅允许删除未关联SKU且已停用的规格`。
- [ ] **AC-018** 删除前确认弹窗；服务端非法删除返回 `TILE_SPEC_DELETE_FORBIDDEN`。

### 1.7 新增 / 编辑弹窗

- [ ] **AC-019** 弹窗 720px；字段：宽*、长*、尺寸名称(只读)、厚度、排序*、备注。
- [ ] **AC-020** 弹窗不含：单位选择、规格类型、常用尺寸、系统状态、可编辑尺寸名称。
- [ ] **AC-021** 宽长填写后实时显示 `{w}×{l}mm`；冲突提示「该尺寸已存在，请勿重复创建」。
- [ ] **AC-022** 排序为正整数；厚度可选、最多 1 位小数；备注 ≤200 字。
- [ ] **AC-023** 重复 `(width_mm,length_mm,unit)` 返回 `TILE_SPEC_DUPLICATED`。

### 1.8 分页

- [ ] **AC-024** 左侧「共 {total} 条」；右侧页码 + 每页 20/50/100。
- [ ] **AC-025** 无跳页输入框、「当前显示 x-y」文案。

## 2. 功能验收 — SKU 联动

- [ ] **AC-026** SKU 表单「规格尺寸」为下拉，仅 `ENABLED` 规格；按 `sort_order ASC, id ASC`。
- [ ] **AC-027** 创建/更新 SKU 提交 `spec_id`；服务端同步 `tiles.size = display_name`。
- [ ] **AC-028** 新建 SKU 选择 `DISABLED` 规格时服务端拒绝（业务错误码待 OpenSpec 定稿）。
- [ ] **AC-029** 编辑 SKU 保留已停用 `spec_id` 时允许保存非规格字段；换绑时必须选 `ENABLED` 规格。
- [ ] **AC-030** 上架校验：`spec_id` 非空且 `size` 非空；否则阻止发布并提示。
- [ ] **AC-031** `spec_id` 为空且未选手动规格时，保存提示：「请选择规格尺寸」。

## 3. 历史数据迁移

- [ ] **AC-032** Migration 创建 `tile_specs` 表与 `tiles.spec_id` 列（可 NULL）。
- [ ] **AC-033** 迁移脚本匹配 `size` 至 `display_name` 或解析 `(\d+)×(\d+)mm` 回填 `spec_id`。
- [ ] **AC-034** 匹配失败记录保留原 `size`，`spec_id=NULL`；不丢数据。
- [ ] **AC-035** 未匹配 SKU 打开编辑时展示 inline 提示：「当前规格未对齐主数据，请选择规格尺寸以继续保存或上架」。

## 4. 接口验收

| 接口 | 说明 |
|---|---|
| `GET /api/v1/admin/tile-specs` | 分页 + keyword + status + summary |
| `GET /api/v1/admin/tile-specs/{id}` | 详情 |
| `POST /api/v1/admin/tile-specs` | 创建，默认 ENABLED，unit=mm |
| `PUT /api/v1/admin/tile-specs/{id}` | 更新 |
| `POST /api/v1/admin/tile-specs/{id}/enable` | 启用 |
| `POST /api/v1/admin/tile-specs/{id}/disable` | 停用 |
| `DELETE /api/v1/admin/tile-specs/{id}` | 条件删除 |
| `POST/PUT /api/v1/admin/tile-skus` | payload 含 `spec_id`（MODIFIED） |

- [ ] **AC-036** 路径符合 `rules/api.md`；统一 `ApiResponse` 包装。
- [ ] **AC-037** OpenAPI 更新 + `pnpm` Orval 重新生成前端客户端。
- [ ] **AC-038** `store_owner` 调用规格 API 返回 403；`employee` 可 CRUD+启停+条件删除。

### 4.1 建议错误码

| code | 名称 | 场景 |
|---|---|---|
| 待分配 | `TILE_SPEC_DUPLICATED` | 宽长单位重复 |
| 待分配 | `TILE_SPEC_DELETE_FORBIDDEN` | 非法删除 |
| 待分配 | `TILE_SPEC_NOT_FOUND` |  id 不存在 |
| 待分配 | `TILE_SPEC_DISABLED` | 新建 SKU 选了停用规格 |

（数值编号在 OpenSpec / `error-codes.md` 阶段定稿）

## 5. 数据验收

- [ ] **AC-039** `tile_specs` 含 FR 定义字段；`(width_mm,length_mm,unit)` UNIQUE。
- [ ] **AC-040** `tiles.spec_id` FK → `tile_specs.id`；`size` 保留冗余。
- [ ] **AC-041** `sku_count` 在 SKU 增删改 spec 时正确维护；不为负。

## 6. 技术验收

- [ ] **AC-042** 前端 semantic token；复用 AdminLayout、品牌页启停确认与分页模式。
- [ ] **AC-043** 后端 pytest：CRUD、启停、重复、非法删除、sku_count、RBAC。
- [ ] **AC-044** 前端 vitest（可选）：删除按钮 disabled 逻辑、display_name 实时生成。

## 7. 视觉验收 Trace

原型优先级：

```text
1. prototype/web/tile-size-management.html
2. prototype/web/tile-size-management.png（待导出 Golden Reference）
3. prototype/web/tile-size-management-modal.html
4. prototype/web/tile-size-management-modal.png（待导出）
5. prototype/web/tile-size-management-context.md
6. acceptance.md（本文件）
7. rules/ui-design.md
```

- [ ] **AC-045** 列表页与 HTML 并排：指标卡（启用/停用）、状态筛选、状态列、启停操作。
- [ ] **AC-046** 弹窗与 modal HTML 并排：字段网格、只读尺寸名称、无状态字段。
- [ ] **AC-047** SKU 表单规格下拉与 ENABLED 列表一致（实现页验收，prototype 可不单独出 HTML）。

## 8. 不在本期

- 导出、批量、跳页、规格类型弹窗编辑、inch 单位 UI、前台/小程序、readonly 角色。
