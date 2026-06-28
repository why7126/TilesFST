---
title: 用户故事
purpose: REQ-0009-tile-spec-management 瓷砖规格管理各角色用户故事
content: 基于 requirement.md v2 与 prototype/web/tile-size-management-* 提炼
source: AI 根据 PRD 与原型生成，项目团队确认
update_method: PRD 或原型变更时同步更新
owner: product
status: draft
created_at: 2026-06-27 22:53:26
updated_at: 2026-06-27 22:53:26
note: REQ-0009-tile-spec-management
---

# 用户故事

## 故事索引

| 编号 | 角色 | 优先级 | 本期范围 |
|---|---|---|---|
| US-001 | 后台运营 | P0 | 是 |
| US-002 | 后台管理员 | P0 | 是 |
| US-003 | 后台运营（SKU 建档） | P0 | 是 |
| US-004 | 店主 | P2 | 否（不得访问管理端） |

---

## US-001 后台运营维护瓷砖规格主数据

**作为** 后台运营人员，  
**我希望** 在管理后台维护标准瓷砖规格（宽、长、厚度、排序）并控制启停，  
**以便** SKU 建档与列表展示使用一致的规格主数据，避免手写重复。

### 验收要点

- 可访问 `/admin/tile-specs`，Sidebar OPERATIONS 下「瓷砖规格」高亮（位于「瓷砖类目」之后）。
- 展示规格总数、启用规格、停用规格、未关联 SKU 四个指标卡。
- 支持关键词 + 状态筛选；查询/重置；分页左「共 x 条」、右页码 + 每页 20/50/100。
- 列表含尺寸名称、宽/长/厚、关联 SKU、排序、状态、更新时间；操作：编辑、启用/停用、条件删除。
- 新增/编辑弹窗：宽/长/厚度/排序/备注；尺寸名称系统生成且只读；无状态/规格类型字段。
- 启停需二次确认；删除仅当 `sku_count=0` 且已停用时可用。
- 无导出、无批量操作。

### 关联功能

- FR-001 ~ FR-009

---

## US-002 后台管理员监管规格主数据

**作为** 后台管理员，  
**我希望** 与运营人员一样访问规格 API 并受统一 RBAC 约束，  
**以便** 主数据质量可控、误删可防范。

### 验收要点

- `admin`、`employee` 可 CRUD + 启停；`store_owner` 访问规格 API 返回 403。
- 宽长单位唯一性、删除条件、启停规则前后端双重校验。
- 非法删除返回 `TILE_SPEC_DELETE_FORBIDDEN`；重复规格返回 `TILE_SPEC_DUPLICATED`。

### 关联功能

- FR-007、FR-009、FR-012

---

## US-003 后台运营在 SKU 表单选择规格

**作为** 后台运营人员，  
**我希望** 在 SKU 新增/编辑弹窗通过下拉选择已启用规格，  
**以便** 规格与主数据一致且上架校验可靠。

### 验收要点

- `TileSkuFormModal`「规格尺寸」为 `<select>`，选项来自 `status=ENABLED` 规格，按 `sort_order` 排序。
- 保存 SKU 提交 `spec_id`；`tiles.size` 同步为规格 `display_name`。
- 新建 SKU 必须选择已启用规格；编辑已绑定停用规格的 SKU 可保留原 `spec_id`。
- 上架前 `spec_id` 有效且 `size` 非空；无 `spec_id` 时提示「请选择规格尺寸」。
- 历史 SKU 迁移失败项打开编辑时，下拉为空选中，保存/上架前必须手动选规格。

### 关联功能

- FR-010、FR-011

---

## US-004 店主不得访问规格管理（边界）

**作为** 店主，  
**我希望** 无法进入管理端规格页面，  
**以便** 权限边界清晰。

### 验收要点

- `store_owner` 无法访问 `/admin/tile-specs` 与 `/api/v1/admin/tile-specs`。

### 关联功能

- FR-012

---

## 与父需求差异

本需求为独立主数据能力，非某 REQ 子需求；对 `REQ-0006-tile-sku-management` 为 **MODIFIED**（SKU 规格录入方式）。
