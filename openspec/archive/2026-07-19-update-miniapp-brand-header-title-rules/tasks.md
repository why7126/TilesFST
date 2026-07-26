## 1. 导航契约与页面接入

- [x] 1.1 梳理 `src/miniapp/components/custom-navigation/` 或等价导航组件的现有属性、事件和 header offset 输出方式。
- [x] 1.2 实现首页 `brand-header` 双行文案规则，固定展示 `菲尚特瓷砖馆` 与 `质感空间，由砖而生`，并确保首页不显示返回按钮。
- [x] 1.3 实现非首页单行标题规则，禁止渲染 `subtitle`、品牌副文案、SKU 编号第二行或其他辅助第二行。
- [x] 1.4 更新 index、search、tile-detail、category、product-list、favorites、certificates、store-info 的导航调用参数或页面配置。
- [x] 1.5 若 find、profile 已接入自定义导航，按非首页单行标题规则处理；若未接入，记录为非本 Change 范围。

## 2. 返回、胶囊避让与内容布局

- [x] 2.1 确认非首页返回按钮热区不小于 44x44 pt，并在加载态、空态、错误态下保持可点击。
- [x] 2.2 实现有页面栈时 `navigateBack`，无页面栈时兜底进入首页的返回逻辑。
- [x] 2.3 保持微信右侧原生分享 / 关闭胶囊避让，不在 WXML / WXSS 中新增自绘分享、关闭或胶囊控件。
- [x] 2.4 统一导航栏实际高度与页面主体 offset，覆盖正常、加载、空态、错误态、骨架屏和下拉刷新状态。
- [x] 2.5 确认 tile-detail 分享标题、分享路径和 SKU 参数不因顶部标题固定为 `商品详情` 而丢失。

## 3. 测试与验收证据

- [x] 3.1 补充小程序静态测试或等价断言，覆盖首页双行文案、首页无返回按钮、非首页无 subtitle。
- [x] 3.2 补充返回按钮逻辑测试或等价验证，覆盖有页面栈返回和无页面栈兜底回首页。
- [x] 3.3 补充胶囊避让和禁止自绘系统按钮的静态检查或人工验收记录。
- [x] 3.4 使用微信开发者工具或真机记录 320、375、430 pt 宽度下返回按钮、标题和右侧胶囊无重叠的 evidence。
- [x] 3.5 逐页验证 search、category、product-list、tile-detail、favorites、certificates、store-info 的非首页单行标题，以及 index 首页双行文案和内容不遮挡。

## 4. 文档与收口

- [x] 4.1 更新必要的小程序实现说明、验收记录或测试说明；不涉及 API / DB / Orval 时明确记录不需要同步。
- [x] 4.2 运行 OpenSpec 校验，确保 delta spec、proposal、design 和 tasks 可通过检查。
- [x] 4.3 执行 `/opsx-apply` 收口时同步 Workflow Sync 和 AI usage hook。
