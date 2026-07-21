## Why

REQ-0048 已把小程序自定义导航栏抽成全局能力，但首页与非首页的 `brand-header` 文案边界仍不够收敛，容易出现非首页继续展示副标题、SKU 编号第二行或品牌副文案的体验不一致。REQ-0050 已评审并纳入 sprint-009，需要把首页双行品牌文案、非首页单行标题、返回与微信原生胶囊避让规则固化到 OpenSpec。

## What Changes

- 首页 `brand-header` 固定展示两行品牌文案：`菲尚特瓷砖馆` 与 `质感空间，由砖而生`。
- 非首页 `brand-header` 只展示一行页面标题，禁止 `subtitle`、品牌副文案、SKU 编号第二行或其他辅助第二行。
- 非首页保留左侧返回按钮；有页面栈时返回上一页，无页面栈时兜底回首页。
- 所有覆盖页面继续避让顶部状态栏和微信右侧原生分享 / 关闭胶囊，不自绘分享、关闭或胶囊控件。
- 页面主体、加载态、空态、错误态和骨架屏继续通过统一 header offset 避让 fixed header。
- 本变更不新增业务页面、后台文案配置、API、数据库、底部 TabBar 或 Web / 管理端能力。

## Capabilities

### New Capabilities

- 无。

### Modified Capabilities

- `miniapp-global-custom-navigation-bar`: 收束首页 / 非首页 `brand-header` 文案规则，补充固定首页双行、非首页单行标题、返回兜底、胶囊避让和内容避让验收。

## Impact

- **Miniapp:** 预计影响 `src/miniapp/components/custom-navigation/` 或等价导航组件，以及 index、search、tile-detail、category、product-list、favorites、certificates、store-info 等已接入页面的标题参数和样式。
- **API:** 不新增或修改接口。
- **Database:** 不新增表或字段。
- **Web/Admin:** 不涉及 Web 展示端或管理端。
- **Orval:** 不需要。
- **Docker Compose:** 不需要。
- **Tests:** 后续实现需补充小程序静态测试或等价验证，覆盖首页双行、非首页单行、返回兜底、胶囊避让、内容不遮挡和 320/375/430 pt 宽度证据。
