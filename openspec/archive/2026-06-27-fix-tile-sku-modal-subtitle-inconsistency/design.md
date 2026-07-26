## Context

- **BUG**: BUG-0010-tile-sku-modal-subtitle-inconsistency
- **Severity**: medium
- **Root cause**: design / frontend-ui — 未共享 modal 副标题样式
- **Related REQ**: REQ-0006-tile-sku-management
- **Reference**: BrandFormModal 副标题模式

## Design Decisions

### D1：共享 `.modal-desc` 于 user-management.css

管理端列表页均已 import `user-management.css`；副标题样式 MUST 使用 semantic token：

```css
color: var(--admin-weak);
font-size: 12px;
line-height: 1.5;
margin: 8px 0 0;
```

### D2：弹窗头部自适应

SKU / 品牌 modal-card 内 `.modal-head`：

- `height: auto`
- `min-height: 64px`
- `padding: 16px 20px`
- `align-items: flex-start`

### D3：SKU 副标题文案

```text
维护 SKU 基础资料、参考价格、图片与视频素材；弹窗内不提供状态选择。
```

保留 AC-023；句式对齐品牌「维护…、…与…。」

### D4：不回退 BUG-0011 / BUG-0012

不修改弹窗 body 滚动与表单校验逻辑。

## Test Strategy

- Vitest：`TileSkuFormModal.test.tsx` 断言 `.modal-desc` 与文案片段
- 人工：SKU / 品牌弹窗并排对比副标题 Typography
