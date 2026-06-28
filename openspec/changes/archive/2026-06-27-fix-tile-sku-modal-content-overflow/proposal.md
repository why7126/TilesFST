## Why

[BUG-0011-tile-sku-modal-content-overflow](issues/bugs/archive/BUG-0011-tile-sku-modal-content-overflow/) 已评审通过并纳入 `sprint-002`。瓷砖 SKU 新增/编辑弹窗（`TileSkuFormModal`）在常见视口下内容超出可视区域，且弹窗内无有效垂直滚动，底部字段（图片/视频/备注）与操作按钮不可达，阻塞 SKU 主数据创建与编辑。

当前 `add-tile-sku-management` 尚未归档；REQ-0006 **AC-022** 与 add change 的 web-client spec 均要求「头尾固定、主体可滚动」，但实现遗漏 `.modal-body` 的 flex 滚动配置。根据项目规则，验收后发现的可用性缺陷 MUST 使用新的 `fix-*` change 修复。

## What Changes

- 修复 `.sku-modal-card` flex 列布局：固定 `modal-head` / `modal-footer`，`.modal-body` 启用 `flex: 1; min-height: 0; overflow-y: auto`（或等价实现）。
- 确保矮视口（≤900px 高、1080p 非全屏）下新增/编辑弹窗全部字段与 footer 按钮可访问。
- 补充 Vitest 覆盖弹窗 scroll 布局（class 或结构断言）。
- 更新 change `trace.md` 矮视口滚动验收记录。

## Impact

| 影响面 | 说明 |
|---|---|
| Web 管理端 | `/admin/tile-skus` 新增/编辑弹窗布局 |
| REQ-0006 | 满足 AC-022；不修改 AC-024～036 业务逻辑 |
| API | 不变 |
| 数据库 | 不变 |
| Orval | 不需要 |
| MinIO | 不变 |

## Rollback Plan

若修复引起弹窗布局异常，可回滚本 change 的 CSS/TSX 改动：

1. 恢复 `tile-sku-management.css` 中 `.sku-modal-card` / `.modal-body` 相关规则。
2. 恢复 `TileSkuFormModal.tsx` 结构（若有 wrapper 变更）。
3. 保留 BUG 与 OpenSpec 记录，重新评估替代方案。

回滚不涉及 API、数据库或对象存储。
