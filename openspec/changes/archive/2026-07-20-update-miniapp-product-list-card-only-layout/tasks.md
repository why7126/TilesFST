## 1. 商品列表页布局收敛

- [x] 1.1 调整 `src/miniapp/pages/product-list/index.wxml`，移除搜索框、筛选按钮、排序 tabs、筛选 chips 和筛选抽屉 DOM。
- [x] 1.2 调整 `src/miniapp/pages/product-list/index.wxss`，将商品列表改为一行 2 个的双列 grid，并保证单数商品左侧自然排列。
- [x] 1.3 将商品列表页商品卡片调用改为 `density="grid"` 或等价视觉，复用现有 `product-card` 核心结构。

## 2. 状态与交互逻辑

- [x] 2.1 清理商品列表页 TS/JS 中页面内搜索、筛选、排序、筛选抽屉和筛选 chips 相关事件路径。
- [x] 2.2 保留入口上下文查询参数，包括 `categoryId`、`categoryName`、`categoryLevel`、`brandId`、`section`、`keyword` 和 `sourcePage`。
- [x] 2.3 保留首屏加载、下拉刷新、上拉加载更多、无更多、空状态、错误状态和加载更多失败重试。
- [x] 2.4 调整商品列表页埋点，保留浏览、曝光、点击、刷新、加载更多和加载失败事件，停止触发列表页筛选/排序事件。

## 3. 边界与兼容

- [x] 3.1 确认微信小程序搜索页 `pages/search/index` 的搜索、筛选和结果展示能力不受本 Change 影响。
- [x] 3.2 确认商品列表页仍可承接搜索页传入的 `keyword` 初始结果，但页面内不展示二次搜索控件。
- [x] 3.3 确认不新增或修改后端 API、数据库、对象存储、Web 管理端或 Orval 生成物；若实现发现必须变更 API，停止并回到 OpenSpec 设计更新。
- [x] 3.4 修正一级分类商品列表接口过滤语义，确保 `categoryLevel=primary` 同时返回一级分类直挂 SKU 与启用二级子分类 SKU，不新增 API 参数或响应字段。

## 4. 验收与测试

- [x] 4.1 补充或更新小程序静态测试，断言商品列表页不再包含搜索、筛选、排序和筛选抽屉入口。
- [x] 4.2 补充或更新小程序静态测试，断言商品列表页使用双列商品卡片布局并保留 `product-card` 复用。
- [x] 4.3 补充入口上下文回归测试或等价检查，覆盖分类、首页 `section=hot/new`、品牌和 `keyword` 初始查询。
- [x] 4.4 补充搜索页边界回归检查，确认搜索页自身搜索、筛选和结果能力未被误删。
- [x] 4.5 补充 320 / 375 / 430 pt DevTools 或真机 evidence，确认双列卡片不溢出、不遮挡，且自定义导航、页面标题、底部 TabBar 与列表内容不重叠。
- [x] 4.6 补充后端回归测试，覆盖一级分类直挂 SKU 与启用二级子分类 SKU 聚合返回，且停用二级分类 SKU 不返回。

## 5. 文档与同步

- [x] 5.1 更新 REQ-0056 acceptance 对应实现证据或 Sprint 验收报告。
- [x] 5.2 运行必要测试与 OpenSpec 校验，记录结果。
- [x] 5.3 运行 Workflow Sync，确保 REQ、Change 与 sprint-009 状态一致。
