---
bug_id: BUG-0038-tile-sku-modal-spec-hint-styling
title: SKU弹窗规格字段下方提示字号过大且颜色不当
severity: low
status: draft
owner: product
discovered_at: 2026-06-28 16:59:15
environment: local|docker
related_requirement: REQ-0006-tile-sku-management
related_change: null
---

# 缺陷说明

Web 管理端 SKU **编辑**弹窗中，当历史 SKU 的 `spec_id` 为空（规格迁移未匹配）时，「瓷砖规格 *」下拉框下方展示提示「历史 SKU 未匹配规格，请手动选择后保存」。该提示使用了未定义样式的 `form-hint` 类名，继承浏览器默认 `<p>` 样式，导致字号接近正文/输入框文字、颜色接近主文字白色，视觉层级高于管理端表单辅助说明规范，在暗色弹窗中过于抢眼。

# 复现步骤

1. 以 admin 登录 Web 管理端，进入「瓷砖 SKU」列表页（`/admin/tile-skus`）。
2. 打开一条 **`spec_id` 为 NULL** 的历史 SKU 的「编辑 SKU」弹窗（迁移失败或未执行 `migrate_tile_spec_ids.py --apply` 的环境均可）。
3. 观察「瓷砖规格 *」下拉框下方提示文案的字号与颜色。
4. （可选）对比用户管理/品牌弹窗同位置 `form-help` 辅助文案（如「4–32 位，小写字母开头…」）。

# 期望结果

- 字段级辅助提示 MUST 复用管理端既有 `form-help` 样式（`11px`、`var(--admin-weak)`、`margin-top: 7px`），与用户管理、品牌弹窗一致。
- 提示文案语义不变（仍引导运营手动选择规格后保存）。
- 选择规格后提示 MUST 消失（现有逻辑保留）。
- 符合 `rules/ui-design.md` 辅助文字 11–12px、次要色规范；满足 `web-client/spec.md` SKU 无 `spec_id` 时展示提示的 Scenario（行为已满足，样式对齐）。

# 实际结果

- 提示使用 `className="form-hint"`，全项目无对应 CSS 定义。
- 呈现浏览器默认段落样式：字号偏大、颜色偏亮，与标签（12px `--admin-muted`）及同弹窗 `modal-desc`（12px `--admin-weak`）层级不一致。

# 影响范围

| 范围 | 影响 |
|---|---|
| Web 管理端 | 仅 SKU 编辑弹窗、仅 `spec_id` 为空的历史 SKU 场景 |
| API / DB | 无 |
| 小程序 / 店主端 | 无 |
| REQ-0006 | SKU 弹窗字段与提示 UX |
| REQ-0009 | 历史 SKU 迁移失败后的运营补选引导 |

# 严重等级说明

`low` — 纯视觉/样式问题，不阻断保存、上架或数据正确性；提示内容正确，仅辅助信息视觉层级不当。随迁移完成，触发频率逐步降低。

# 代码线索

| 线索 | 路径 |
|---|---|
| 问题元素 | `src/web/src/features/admin/components/TileSkuFormModal.tsx` L438–440 |
| 正确类名参考 | `UserFormModal.tsx`、`BrandFormModal.tsx` → `form-help` |
| 样式定义 | `src/web/src/features/admin/styles/user-management.css` `.form-help` |
| 页面已 import | `TileSkuManagementPage.tsx` 已引入 `user-management.css` |
| 引入 Change | `add-tile-spec-management` tasks 7.2（迁移失败 SKU 提示） |
