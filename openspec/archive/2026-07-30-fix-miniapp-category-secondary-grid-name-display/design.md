## Background

`BUG-0093` 指向微信小程序分类页右侧二级类目卡片的展示问题。现有正式 spec 中“二级分类宫格”要求二级分类按三列宫格展示，并要求长名称保持可辨识；但实际业务类目名称包含 `600X1200 仿古精雕...` 等较长规格和工艺描述，三列布局下卡片宽度不足，名称仍被截断。

## Root Cause

- `src/miniapp/pages/category/index.wxss` 的 `.secondary-grid` 使用 `grid-template-columns: repeat(3, minmax(0, 1fr))`。
- `.secondary-name` 使用 `overflow: hidden`、`display: -webkit-box` 和 `-webkit-line-clamp: 2`。
- `.skeleton-grid` 也使用 3 列，加载态与目标两列布局要求不一致。
- 历史修复聚焦“超过 4 字不应过早省略”，但正式 spec 仍保留三列宫格，未把“所有类目名称完整显示”作为硬验收。

## Fix Design

1. 小程序分类页二级类目卡片布局改为两列：
   - `.secondary-grid` 使用 2 列网格。
   - `.skeleton-grid` 同步使用 2 列网格。
2. 二级类目名称完整展示：
   - 移除或放宽 `.secondary-name` 的截断限制。
   - 允许名称自然换行。
   - 通过卡片 `min-height`、内边距、对齐和 `word-break` 保证长名称仍在卡片内。
3. 保持页面行为边界：
   - 不改 `openSecondary` 跳转逻辑。
   - 不改 `data-id`、`data-name`、`categoryLevel=secondary`、`sourcePage=category` 参数语义。
   - 不改分类树接口、缓存、排序、状态过滤和埋点字段。

## Test Strategy

- 静态检查：
  - 确认二级类目实际网格和 skeleton 网格均为 2 列。
  - 确认 `.secondary-name` 不再通过省略号、行数 clamp 或隐藏溢出省略名称。
- 小程序页面回归：
  - 覆盖 4 字以内、5-8 字、超过 8 字、数字规格和中文描述组合的二级类目名称。
  - 验证长名称不遮挡相邻卡片、一级类目、标题、“查看全部商品”入口和底部 TabBar。
  - 验证点击二级类目仍进入对应商品列表。
- 设备 evidence：
  - 微信开发者工具覆盖 320 pt、375 pt、390 pt、430 pt 或项目等价视口。
  - 真机不可用时在验收报告中明确标记 blocked 或 follow_up，不把 DevTools 结论表述为真机通过。

## Risk

- 两列布局会减少单屏可见二级类目数量，可能增加纵向滚动。
- 移除截断后极长名称可能拉高卡片高度，需要通过网格自适应和最小高度控制避免视觉跳动。
- 若实现阶段误改分类树接口或路由参数，会扩大影响面；本 Change 明确不包含该类改动。
