## Context

- **BUG**: `BUG-0012-tile-sku-modal-form-field-rules`
- **Severity**: medium
- **Root cause type**: product-rule / validation
- **Related REQ**: `REQ-0006-tile-sku-management`
- **Parent change**: `add-tile-sku-management`（in-progress，34/35 tasks）
- **Sprint**: sprint-002
- **Target**: `TileSkuFormModal.tsx`、`tile_sku_admin_service.py`、`tile_sku_admin.py` schemas

## Bug Analysis Report

### 现象

1. 表面工艺 Label 带 `*`，create/edit 路径拦截空值。
2. 参考价格无必填标记，新建默认空，未填存 `null`，列表显示「—」。
3. 上架拒绝 `surface_finish` 为空或 `"-"`。

### 复现路径

1. admin 登录，打开 `/admin/tile-skus` 新增 SKU 弹窗。
2. 留空表面工艺 → 「创建 SKU」报错。
3. 留空参考价格 → 可保存，`reference_price=null`。

### 影响

- 不阻断列表/草稿（名称-only 草稿仍可用）。
- 阻塞 UAT 产品规则验收与 REQ-0006 字段规则对齐。
- 涉及 API 校验与 Orval，不涉及 DB schema migration。

## Root Cause

### RC-001：实现严格对齐 REQ-0006 v4 旧文档

`requirement.md` 与 AC-024 原定义表面工艺必填、参考价格选填；`add-tile-sku-management` 按此实现。

### RC-002：UAT 规则变更未回写 acceptance/OpenSpec

产品方在验收阶段提出规则调整，未同步到 spec，导致前后端仍执行旧规则。

### RC-003：publish 与 save 策略不一致

草稿路径可将空工艺写 `"-"`，但 publish 仍拒绝 `"-"`，与「非必填」预期冲突。

## Design Decisions

### D1：表面工艺 — 非必填

- 前端：移除 `*` 与 `validateCreateFields` / edit 路径中的工艺必填校验。
- 后端 create（`save_mode=create`）与 update：移除「表面工艺不能为空」。
- 空值存储：沿用 `_resolve_draft_defaults` 语义，空 → `"-"`（DB `NOT NULL` 兼容）。
- `publish_sku`：**移除** surface_finish 完整性检查（BUG-0012 AC-007）。

### D2：参考价格 — 必填，默认 0

- 新建弹窗：`setReferencePrice('0')`。
- Label 带 `*`；create/edit 提交前校验非空且 ≥0。
- `buildPayload`：空值 MUST NOT 发送 `null`；默认提交 `0`。
- 后端：create/update MUST 拒绝 `reference_price is None`；允许 `0.0`。
- 列表：`formatReferencePrice(0)` → `¥ 0.00`（已有逻辑）。

### D3：save_mode=draft

- 仍仅校验 SKU 名称。
- 参考价格：若用户未改默认值，随 payload 写入 `0`；不放宽为 null。

### D4：REQ-0006 文档同步（apply 阶段）

- `requirement.md` §字段：表面工艺（选填）、参考价格（元）（必填，默认 0）。
- `acceptance.md` AC-024：去掉表面工艺 `*`；AC-015：价格为 0 时 `¥ 0.00`。

### D5：不回退 BUG-0011 / BUG-0009

- 不修改弹窗 flex 滚动 CSS 与列表分页 DOM。

## Test Strategy

- Vitest：`TileSkuFormModal` 默认值、必填标记、校验错误文案。
- pytest：`test_admin_tile_skus` create/update/publish 矩阵（空工艺 OK、null 价格拒绝、0 价格 OK、publish 空工艺 OK）。
- Orval：`./scripts/generate-openapi-client.sh` 后前端 build。
- 人工：BUG-0012 acceptance AC-001～AC-012 checklist。

## Risks

| 风险 | 缓解 |
|---|---|
| 历史 SKU `reference_price=null` | 编辑回填默认 `0`；不要求 bulk migration |
| OpenAPI 破坏性变更 | 仅收紧 create/update；响应仍可含 null（旧数据） |
| add-tile-sku-management 未 archive | delta spec MODIFIED 标题对齐 add change；fix 先 apply |

## 原型优先级

1. BUG-0012 `acceptance.md`
2. `issues/requirements/archive/REQ-0006-tile-sku-management/requirement.md`（更新后）
3. `tile-sku-create-modal.html`（字段顺序不变；必填标记以产品规则为准）
