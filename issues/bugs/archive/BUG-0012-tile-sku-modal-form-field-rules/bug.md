---
bug_id: BUG-0012-tile-sku-modal-form-field-rules
title: SKU弹窗表面工艺与参考价格字段规则不符合产品预期
severity: medium
status: draft
owner: product
discovered_at: 2026-06-27 08:56:54
environment: local|docker
related_requirement: REQ-0006-tile-sku-management
related_change: add-tile-sku-management
---

# 缺陷说明

瓷砖 SKU 新增/编辑弹窗中，「表面工艺」与「参考价格（元）」的必填规则、默认值与当前产品验收预期不一致：

1. **表面工艺**：实现与 REQ-0006 v4 文档均要求必填（Label 带 `*`、前后端校验拦截）；产品期望改为**非必填**，留空可正常保存。
2. **参考价格（元）**：当前为选填，新建时默认空，未填时存 `null`、列表展示「—」；产品期望改为**必填**，新建默认 **0 元**，不允许空值提交。

> 注：本缺陷记录 UAT 阶段的产品规则调整，与 REQ-0006 v4 `requirement.md` §字段定义及 `acceptance.md` AC-024 原定义存在差异；修复时须同步 acceptance 与 OpenSpec delta。

# 复现步骤

1. 以 admin 登录 Web 管理端（local 或 Docker 均可）。
2. 进入「瓷砖 SKU」列表页（`/admin/tile-skus`），点击「新增 SKU」打开弹窗。
3. 填写 SKU 名称、编码、品牌、类目、规格尺寸等必填项，**不填表面工艺**，点击「创建 SKU」——观察是否被阻止。
4. 同上，**不填参考价格（元）**，点击「创建 SKU」或「保存」——观察是否允许保存。
5. 重新打开「新增 SKU」弹窗，观察「参考价格（元）」初始值是否为空（非 `0`）。
6. 保存成功后查看列表「参考价格」列：未填价格时是否展示「—」而非 `¥ 0.00`。
7. （可选）仅填 SKU 名称后点「保存草稿」、表面工艺留空——观察草稿是否可保存（后端写入 `"-"`）。
8. 对照 `issues/requirements/archive/REQ-0006-tile-sku-management/acceptance.md` AC-024、AC-026、AC-015。

# 期望结果

| 字段 | 期望 |
|---|---|
| 表面工艺 | 非必填；Label 无 `*`；留空可正常创建/编辑保存 |
| 参考价格（元） | 必填；Label 带 `*`；新建弹窗默认 `0`；不允许空值；列表展示 `¥ 0.00` |
| Label 文案 | 仍为「参考价格（元）」；支持两位小数 |

# 实际结果

| 字段 | 实际 |
|---|---|
| 表面工艺 | Label 带 `*`；「创建 SKU」/编辑「保存」时前端校验 `表面工艺不能为空`；后端 create（`save_mode=create`）与 update 同样拦截 |
| 参考价格（元） | 无必填标记与校验；新建默认空字符串；`buildPayload` 空值 → `null`；列表 `formatReferencePrice(null)` →「—」 |
| 草稿路径 | 「保存草稿」可绕过表面工艺前端校验，后端 `_resolve_draft_defaults` 写入 `surface_finish = "-"` |
| 上架 | `publish_sku` 仍拒绝表面工艺为空或 `"-"` 的记录（与「非必填」策略需产品确认） |

# 影响范围

| 范围 | 影响 |
|---|---|
| Web 管理端 / SKU 弹窗 | `TileSkuFormModal.tsx` 校验、`*` 标记、默认值、`buildPayload` |
| Web 管理端 / SKU 列表 | `formatReferencePrice` 对 `null` 展示「—」（`0` 已可格式化为 `¥ 0.00`） |
| 后端 API | `tile_sku_admin_service.py` create/update 校验；`TileSkuCreateRequest.reference_price` 可选 |
| 上架逻辑 | `publish_sku` 对 `surface_finish` 的完整性检查可能需同步调整 |
| 关联需求 | REQ-0006（`acceptance.md` AC-024、AC-015 需 delta） |
| 关联 Change | `add-tile-sku-management`（按旧 spec 实现；建议 fix change `fix-tile-sku-modal-form-field-rules`） |
| 测试 | 前后端 tile SKU 测试假设与旧规则一致，修复时需更新 |

# 严重等级说明

严重程度为 `medium`。

理由：

- 不阻断登录、列表查询或 SKU 草稿保存等核心链路。
- 属于表单业务规则与产品验收预期偏差，影响运营录入体验与 REQ-0006 验收对齐。
- 修复涉及前后端校验、默认值、可能的上架策略及 REQ acceptance 同步，但非紧急 hotfix。

# 代码线索

| 线索 | 路径 |
|---|---|
| 前端表单校验与默认值 | `src/web/src/features/admin/components/TileSkuFormModal.tsx` |
| 列表价格格式化 | `src/web/src/features/admin/api/tile-skus-api.ts`（`formatReferencePrice`） |
| 后端 create/update 校验 | `src/backend/app/services/tile_sku_admin_service.py` |
| 上架 surface_finish 检查 | 同上 `publish_sku` |
| API Schema | `src/backend/app/schemas/tile_sku_admin.py` |
| 需求字段定义 | `issues/requirements/archive/REQ-0006-tile-sku-management/requirement.md` |
| 验收 | `issues/requirements/archive/REQ-0006-tile-sku-management/acceptance.md` |
