---
bug_id: BUG-0030-banner-list-ui-inconsistency
status: pending_review
created_at: 2026-06-28 16:16:51
updated_at: 2026-06-28 16:16:51
---

# 临时规避方案

## 1. 可用性规避

该缺陷不阻断 Banner 管理功能，当前可继续使用：

1. Banner 列表分页仍可通过 ‹ / › 按钮、页码按钮与每页条数下拉完成翻页。
2. 筛选（关键词、展示端、状态、时间状态）、新增、编辑、上下线、删除等操作均不受影响。
3. 多余标题与统计行不影响数据阅读与行内操作。

## 2. 验收规避

在正式修复前，验收时应明确标注：

- Banner 列表上方「Banner 列表」标题与「当前显示 …」行 **暂不作为 UI 一致性通过项**。
- 底部分页与用户管理页存在 DOM/视觉差异，**暂不满足 `admin-list-page-consistency.md` 基准**。
- 仅验证 Banner 列表查询、分页、CRUD、上下线、删除规则等功能本身是否可用。

## 3. 运营规避

内部管理员可继续按现有路径维护 Banner：

1. 进入「Banner 管理」列表页。
2. 使用现有筛选与分页控件定位目标 Banner。
3. 通过「＋ 新增 Banner」或行内「编辑」维护运营内容。

## 4. 风险说明

该规避方案只能保证功能可用，不能消除以下问题：

- 管理端列表页视觉一致性不足（与用户管理、品牌、规格、SKU 分页不对齐）。
- REQ-0016 列表验收与 Design System 列表 gate 可能因结构差异无法完全通过。
- 与 BUG-0031–0036 同属 Banner 页实现，建议合并 fix change 一次性对齐。

因此仍建议进入 `/bug-review`，评审通过后通过 `fix-banner-admin-ui` 或等价 OpenSpec Change 修复。
