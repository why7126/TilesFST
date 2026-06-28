---
title: 业务流程
purpose: 瓷砖规格管理、启停删除与 SKU 联动主流程
content: 基于 requirement.md v2 与 prototype/web/tile-size-management-* 提炼
source: AI 根据 PRD 与原型生成，项目团队确认
update_method: PRD 或原型变更时同步更新
owner: product
status: draft
created_at: 2026-06-27 22:53:26
updated_at: 2026-06-27 22:53:26
note: REQ-0009-tile-spec-management
---

# 业务流程

## 1. 流程总览

```text
后台用户登录（admin / employee）
  ↓
┌─────────────────────────────────────────────────────────┐
│ 路径 A：规格主数据                                       │
│   /admin/tile-specs → 列表 / 筛选 / 指标卡               │
│   ├─ 新增/编辑规格 → 弹窗 → POST/PUT → 刷新              │
│   ├─ 启用/停用 → 确认 → POST enable/disable → 刷新       │
│   └─ 删除（sku_count=0 且 DISABLED）→ 确认 → DELETE      │
└─────────────────────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────────────────────┐
│ 路径 B：SKU 建档（REQ-0006 MODIFIED）                    │
│   /admin/tile-skus → 新增/编辑 SKU                       │
│   └─ 规格下拉（仅 ENABLED）→ spec_id + size 同步 → 保存  │
└─────────────────────────────────────────────────────────┘
```

## 2. 与关联 REQ 差异

| 对比项 | REQ-0005 品牌 | REQ-0009 规格 |
|---|---|---|
| 唯一键 | name | (width_mm, length_mm, unit) |
| 展示名 | 用户输入 | 系统生成 display_name |
| SKU 关联 | brand_id | spec_id + size 冗余 |
| 弹窗状态 | 无 | 无（列表启停） |
| 删除条件 | sku_count=0 且 DISABLED | 同左 |

## 3. 访问与权限

```text
JWT → require_admin_access
  ├─ role ∈ {admin, employee} → 允许
  └─ role = store_owner → 403 AuthForbidden
```

| 产品角色 | 后端 role | 规格菜单 | SKU 规格下拉 |
|---|---|---|---|
| 后台运营 | employee | ✓ | ✓ |
| 后台管理员 | admin | ✓ | ✓ |
| 店主 | store_owner | ✗ | ✗ |

## 4. 规格列表查询

```text
GET /api/v1/admin/tile-specs?page=1&page_size=20&keyword=&status=
  ↓
响应：items[] + pagination + summary
  summary: total_count, enabled_count, disabled_count, unlinked_count
  ↓
渲染 metric-grid + filter + table + pagination
```

### 4.1 筛选

```text
用户输入 keyword / 选择 status（全部|启用|停用）
  ↓
点击「查询」→ page=1 重新请求
  ↓
点击「重置」→ 清空 keyword，status=全部 → 重新请求
```

## 5. 新增 / 编辑规格

```text
点击「＋ 新增瓷砖规格」或行内「编辑」
  ↓
弹窗：width_mm*, length_mm*, display_name(只读), thickness, sort_order*, remark
  ↓
客户端：宽长变化 → 实时 display_name = {w}×{l}mm
  ↓
唯一性预检：与已有 (width,length,unit) 冲突 → 错误提示，禁止提交
  ↓
POST（新增）/ PUT（编辑）
  ↓
服务端：unit='mm'，生成 display_name，唯一性校验
  ↓
成功 → Toast → 关弹窗 → 刷新列表 + summary
失败 → TILE_SPEC_DUPLICATED 等
```

## 6. 启停流程

```text
列表行点击「停用」或「启用」
  ↓
二次确认弹窗（对齐 BrandManagementPage）
  ↓
POST .../disable 或 .../enable
  ↓
成功 → Toast → 刷新行/列表
```

**规则**：

- 已关联 SKU 的规格 **允许停用**；停用后 SKU 仍保留 spec_id。
- 新建 SKU 下拉 **不展示** DISABLED 规格。

## 7. 删除流程

```text
判断 deletable = (sku_count == 0 AND status == DISABLED)
  ├─ false → 删除置灰，hover「仅允许删除未关联SKU且已停用的规格」
  └─ true → 点击删除
        ↓
     确认弹窗「删除规格」
        ↓
     DELETE /api/v1/admin/tile-specs/{id}
        ↓
     服务端二次校验 → 成功 200 / 失败 TILE_SPEC_DELETE_FORBIDDEN
```

## 8. SKU 规格选择流程

```text
打开 TileSkuFormModal
  ↓
GET /api/v1/admin/tile-specs?status=ENABLED&page_size=100（或专用 options）
  ↓
<select> 展示 display_name（可选副行厚度）
  ↓
用户选择 spec_id
  ↓
POST/PUT SKU payload 含 spec_id
  ↓
服务端：
  ├─ 新建：spec 必须 ENABLED
  ├─ 编辑：若 spec_id 变更 → 旧 spec sku_count-1，新 spec sku_count+1
  ├─ 编辑：若保留已停用 spec_id → 允许（不强制换绑）
  └─ tiles.size = tile_specs.display_name
  ↓
上架 publish：spec_id 非空且 size 非空
```

## 9. 历史数据迁移流程

```text
部署 migration：创建 tile_specs + tiles.spec_id
  ↓
对每个 tiles 记录：
  ├─ 解析 size 文本（如 900×1800mm）→ 匹配 display_name 或 (w,l,unit)
  ├─ 匹配成功 → 写入 spec_id，保留 size
  └─ 匹配失败 → spec_id=NULL，保留原 size
  ↓
运营打开未匹配 SKU：
  ├─ 下拉无选中，展示提示「请选择规格尺寸以完成主数据对齐」
  └─ 保存/上架前必须选择 ENABLED 规格
```

## 10. sku_count 维护

```text
SKU 创建且 spec_id=S     → specs[S].sku_count += 1
SKU 删除且 spec_id=S     → specs[S].sku_count -= 1
SKU 更新 spec_id S→T     → S-=1, T+=1
规格删除（物理删）         → 仅 sku_count=0 时允许
```
