---
bug_id: BUG-0012-tile-sku-modal-form-field-rules
status: pending_review
created_at: 2026-06-27 11:35:29
updated_at: 2026-06-27 11:35:29
root_cause_type: product-rule
---

# 根因分析

## 1. 直接原因

### 1.1 前端表单按 REQ-0006 v4 将表面工艺设为必填

`TileSkuFormModal.tsx` 中：

- Label 渲染 `表面工艺 <span className="req">*</span>`。
- `validateCreateFields()` 在 `save_mode=create` 及编辑「保存」路径校验 `!surfaceFinish.trim()`，报错「表面工艺不能为空」。

### 1.2 前端未对参考价格做必填校验且默认值为空

同文件新建弹窗初始化：

```text
setReferencePrice('');
```

`buildPayload()` 将空字符串解析为 `reference_price: null`，无前端拦截。

### 1.3 后端 create/update 校验与 schema 沿用旧规则

`tile_sku_admin_service.py`：

- `_validate_create_fields()`：`surface_finish` 为空 → `AuthInvalidRequestError("表面工艺不能为空")`。
- `update_sku()`：同样拒绝空 `surface_finish`。
- `TileSkuCreateRequest.reference_price` 为 `float | None = None`，无必填校验。

### 1.4 上架逻辑仍要求表面工艺完整

`publish_sku()` 拒绝 `surface_finish` 为空或 `"-"` 的记录，与 UAT 提出的「表面工艺非必填」策略不一致。

### 1.5 列表展示与 null 语义绑定

`formatReferencePrice(null)` 返回「—」，与「参考价格必填、默认 0」的产品预期不一致（`0` 已可正确格式化为 `¥ 0.00`）。

## 2. 根本原因

### 2.1 实现严格对齐 REQ-0006 v4 文档，未吸收 UAT 产品规则变更

`requirement.md` §字段定义与 `acceptance.md` AC-024 原定义为：

- 表面工艺（必填）
- 参考价格（元）（选填）

`add-tile-sku-management` 按上述 spec 实现前后端校验与 OpenSpec。UAT 阶段产品方提出规则调整（表面工艺改非必填、参考价格改必填且默认 0），但尚未回写 REQ acceptance / OpenSpec delta，导致实现与最新验收预期脱节。

### 2.2 前后端双重校验未建立「产品规则变更」同步机制

表面工艺必填在前端 `validateCreateFields` 与后端 `_validate_create_fields` / `update_sku` 三处重复；参考价格选填在 schema、service、表单默认值三处一致但均基于旧 spec。缺少单一业务规则源（如 shared validation 或已更新的 acceptance）使 UAT 变更无法自动传导。

### 2.3 草稿与正式保存路径行为不对称（表面工艺）

草稿保存走 `_resolve_draft_defaults`，空表面工艺写入 `"-"` 且不触发 create 校验；正式「创建 SKU」仍拦截。运营易误以为「草稿能存、正式也能存」，加剧验收困惑。

## 3. 触发条件

满足以下条件时可稳定复现：

1. 以 admin 登录 Web 管理端（local 或 Docker）。
2. 进入 `/admin/tile-skus`，打开「新增 SKU」或「编辑 SKU」弹窗。
3. **表面工艺**：填齐其他必填项、留空表面工艺，点击「创建 SKU」或编辑「保存」→ 被拦截。
4. **参考价格**：留空参考价格提交 → 允许保存，`reference_price=null`，列表显示「—」。
5. **默认值**：新建弹窗打开时参考价格输入框为空，非 `0`。

## 4. 分类结论

| 维度 | 结论 |
|---|---|
| 缺陷分类 | product-rule / validation（前后端业务规则） |
| 是否接口缺陷 | 是（校验规则与产品预期不符） |
| 是否数据库缺陷 | 否（`surface_finish NOT NULL`、`reference_price` 可空 schema 可承载新规则） |
| 是否权限缺陷 | 否 |
| 主要修复面 | Web SKU 弹窗、Admin Tile SKU API 校验、上架策略、REQ-0006 acceptance delta |
| 关联需求 AC | AC-024（必填标记）、AC-015（价格展示）、AC-026（价格 Label）、AC-027（校验失败 UX） |

## 5. 产品决策（complete 阶段确认）

| 决策项 | 结论 |
|---|---|
| 表面工艺 | **非必填**；创建/编辑保存允许留空；存储空值时使用 `"-"`（与草稿路径一致） |
| 参考价格 | **必填**；新建默认 `0`；不允许 `null`/空提交；≥0，两位小数 |
| 上架与表面工艺 | 留空表面工艺的 SKU **允许上架**（移除 `publish_sku` 对 surface_finish 的完整性拦截） |
| REQ-0006 同步 | fix change MUST 更新 `requirement.md` 字段定义与 `acceptance.md` AC-024、AC-015 |

## 6. 后续修复建议

1. 建议 Change 命名：`fix-tile-sku-modal-form-field-rules`。
2. 前端：去掉表面工艺 `*` 与校验；参考价格加 `*`、默认 `"0"`、提交前校验。
3. 后端：移除 surface_finish 必填校验；增加 reference_price 必填（含 `0.0`）；调整 `publish_sku`。
4. 测试：更新 `TileSkuFormModal`、`test_admin_tile_skus`、价格格式化边界用例。
5. OpenSpec / REQ acceptance delta 与代码同批合并。
