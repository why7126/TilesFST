# REQ-0008 启停确认弹窗 — 原型上下文

## 1. 参考

- 删除确认：已实现 `BrandManagementPage` 删除弹窗（标题「删除品牌」）
- 同类交互：`REQ-0007-tile-category-management-refine` → `tile-category-status-confirm-context.md`
- 本弹窗 MUST 复用相同 modal 样式类（`modal-backdrop`、`modal-card`、`modal-head`、`modal-body`、`modal-footer`）

## 2. 停用

| 元素 | 内容 |
|------|------|
| 标题 | 停用品牌 |
| 正文 | 确认停用品牌「{name}」？停用后前台将不再展示该品牌。 |
| 取消 | 取消 |
| 确认 | 确认停用（主按钮） |

## 3. 启用

| 元素 | 内容 |
|------|------|
| 标题 | 启用品牌 |
| 正文 | 确认启用品牌「{name}」？ |
| 取消 | 取消 |
| 确认 | 确认启用（主按钮） |

## 4. 交互

- 打开弹窗时不调用 API
- 确认后调用 `POST /admin/brands/{brand_id}/disable` 或 `POST /admin/brands/{brand_id}/enable`
- ESC / 遮罩 / × 等同「取消」
- 与删除弹窗 MUST NOT 共用同一 state；启停与删除可同时存在独立 target state

## 5. 验收说明

- 列表页基线沿用 `REQ-0005-brand-management/prototype/web/brand-management.html`；本需求仅增量描述启停确认弹窗。
- PNG Golden Reference：可选待导出（非阻塞 req-opsx / opsx-apply）。
