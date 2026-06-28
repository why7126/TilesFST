## Context

- **BUG**: BUG-0038-tile-sku-modal-spec-hint-styling
- **Severity**: low
- **Root cause**: code / frontend-ui — 误用未定义 `form-hint`，应复用 `form-help`
- **Related REQ**: REQ-0006-tile-sku-management、REQ-0009-tile-spec-management（历史 SKU 迁移失败场景）
- **Reference**: `UserFormModal`、`BrandFormModal` 字段辅助文案；BUG-0010 共享样式模式

## Design Decisions

### D1：复用 `.form-help`，不新增 CSS

`TileSkuManagementPage` 已 import `user-management.css`。字段级辅助提示 MUST 使用：

```css
.admin-shell .form-help {
  margin-top: 7px;
  color: var(--admin-weak);
  font-size: 11px;
}
```

单行修改：`className="form-hint"` → `className="form-help"`。

### D2：行为与文案不变

显隐条件保持：

```tsx
{!specId && mode === 'edit' && sku && !sku.spec_id ? ( ... ) : null}
```

文案保持：「历史 SKU 未匹配规格，请手动选择后保存」。

### D3：不回退同弹窗既有修复

不修改 `modal-desc`（BUG-0010）、弹窗 body 滚动（BUG-0011）、字段校验规则（BUG-0012）。

## Test Strategy

- Vitest：`TileSkuFormModal.test.tsx` — `spec_id: null` 编辑模式断言提示存在、`form-help` 类名、文案片段
- 人工：与 BUG-0038 截图并排对比；可选对比用户管理弹窗 `form-help` Typography
