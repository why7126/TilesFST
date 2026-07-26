## 1. 导航模块与页面接入

- [x] 1.1 盘点 `src/miniapp` 当前首页和非首页顶部导航、页面配置和内容顶部 spacing。
- [x] 1.2 创建或复用统一自定义导航模块，支持首页形态与非首页形态。
- [x] 1.3 首页接入首页形态，保留当前品牌 `brand-header`，确认不显示左侧返回按钮。
- [x] 1.4 search、tile-detail、category、product-list、favorites、certificates、store-info 接入非首页形态。

## 2. 返回、胶囊与状态栏

- [x] 2.1 实现非首页左侧返回按钮，优先页面栈返回上一页。
- [x] 2.2 实现无页面栈时返回首页兜底，并覆盖分享直达场景。
- [x] 2.3 使用微信系统信息和菜单按钮信息计算状态栏高度、胶囊位置和右侧避让区。
- [x] 2.4 确认 WXML / WXSS 未自绘模拟微信分享按钮、关闭按钮或系统胶囊。
- [x] 2.5 保留支持分享页面的页面级原生分享配置，尤其是 tile-detail 当前 SKU 参数。

## 3. 内容避让与视觉稳定

- [x] 3.1 建立统一导航栏高度 offset，页面主体、骨架屏、空态、错误态和下拉刷新共用。
- [x] 3.2 验证 search 搜索框、tile-detail 媒体区、category 双栏、product-list 商品列表、favorites 收藏列表、certificates 证书列表、store-info 内容不被 fixed header 遮挡。
- [ ] 3.3 验证 320、375、430 pt 宽度下返回按钮、标题/品牌信息和右侧胶囊避让区不重叠、不横向滚动。
- [x] 3.4 保持 REQ-0042 / REQ-0043 深色品牌导航视觉，不做整体视觉重设计。

## 4. 测试、文档与验收

- [x] 4.1 补充小程序静态或单元测试，覆盖导航模块形态、返回兜底、覆盖页面接入和禁止硬编码/自绘胶囊的关键约束。
- [ ] 4.2 在微信开发者工具或真机完成返回行为、分享行为、状态栏避让、原生胶囊避让和内容不遮挡验收。
- [x] 4.3 更新 REQ-0048 验收记录或 Sprint 验收摘要，明确 API / DB / Orval / Docker Compose 是否为 N/A。
- [x] 4.4 运行必要测试和 `openspec validate add-miniapp-global-custom-navigation-bar --strict`。
