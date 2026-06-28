---
bug_id: BUG-0038-tile-sku-modal-spec-hint-styling
status: pending_review
created_at: 2026-06-28 17:02:26
updated_at: 2026-06-28 17:02:26
root_cause_type: code
---

# 根因分析

## 1. 直接原因

- `TileSkuFormModal.tsx` 规格字段下方提示使用 `className="form-hint"`。
- 全项目 CSS 中**不存在** `.form-hint` 规则（`rg form-hint` 仅命中该一处 TSX）。
- 元素继承浏览器默认 `<p>` 样式：字号约 16px（或父级继承）、颜色为 `--admin-text` 主文字色，视觉权重高于字段标签与辅助说明。

## 2. 根本原因

`add-tile-spec-management` 落地 SKU `spec_id` 联动与迁移失败提示（tasks 7.2）时，未复用管理端既有字段辅助文案类名 `form-help`（已在 `UserFormModal`、`BrandFormModal`、`user-management.css` 定义），误用不存在的 `form-hint`，属于 CSS Port / Design System 对齐遗漏。

## 3. 触发条件

须同时满足：

| 条件 | 说明 |
|------|------|
| `mode === 'edit'` | 仅编辑弹窗 |
| `sku.spec_id == null` | 历史 SKU 迁移未匹配规格 |
| `!specId` | 下拉尚未手动选择规格 |

新增 SKU、已有有效 `spec_id` 的 SKU 均不展示该提示。

## 4. 分类结论

| 维度 | 结论 |
|------|------|
| 缺陷分类 | code / frontend-ui |
| 修复面 | Web 管理端 `TileSkuFormModal.tsx` 单行类名 |
| 建议修复 | `form-hint` → `form-help`（无需新增 CSS，`TileSkuManagementPage` 已 import `user-management.css`） |

## 5. 修复方案（建议）

1. 将提示元素 `className` 由 `form-hint` 改为 `form-help`。
2. 在 `TileSkuFormModal.test.tsx` 补充：`spec_id: null` 编辑模式断言提示可见且带 `form-help` 类。
3. **MUST NOT** 新增裸 Hex 或重复定义 `.form-hint` CSS（遵循 `rules/ui-design.md` 与 BUG-0010 共享样式模式）。
