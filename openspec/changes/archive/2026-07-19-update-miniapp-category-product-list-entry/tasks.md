## 1. Miniapp Category Entry

- [x] 1.1 在分类页右侧当前一级分类标题区或等价区域增加一级分类商品列表入口，保持左侧一级分类点击只用于切换。
- [x] 1.2 统一一级/二级分类跳转参数为 `categoryId`、`categoryName`、`categoryLevel` 和 `sourcePage`。
- [x] 1.3 为一级/二级入口补充 300ms 防重复触发、跳转失败提示和分类页状态保留。
- [x] 1.4 验证分类页在 320 到 430px 小程序宽度下无横向滚动、重叠、底部 TabBar 遮挡或入口热区不足。

## 2. Product List Context

- [x] 2.1 商品列表页解析并持久化 `categoryLevel=primary|secondary` 分类上下文。
- [x] 2.2 实现一级分类聚合查询：展开启用二级分类并返回其公开 SKU 聚合结果，不只查询一级分类直挂 SKU。
- [x] 2.3 保持二级分类精确查询只返回当前二级分类公开 SKU。
- [x] 2.4 筛选、排序、分页、下拉刷新、上拉加载更多和重试请求持续携带 `categoryId` 与 `categoryLevel`。
- [x] 2.5 商品列表页标题、搜索提示、空状态和错误状态按一级/二级分类上下文展示。

## 3. Tracking / API / Docs

- [x] 3.1 补充分类入口点击和商品列表分类浏览 usage event 字典、客户端上报与服务端校验。
- [x] 3.2 若商品列表公开接口新增或调整 `categoryLevel` 参数，同步 OpenAPI、Orval、API 文档和错误码说明。
- [x] 3.3 确认埋点字段不包含手机号、Authorization、Cookie、raw payload、raw object key 或无关个人敏感信息。

## 4. Tests / Validation

- [x] 4.1 补充小程序分类页交互测试，覆盖一级入口、二级入口、防重复点击、跳转失败和返回状态恢复。
- [x] 4.2 补充商品列表查询测试，覆盖一级分类聚合、二级分类精确、无启用二级分类、无商品、分类下架和非法 `categoryLevel`。
- [x] 4.3 补充埋点测试，覆盖一级入口、二级入口、商品列表浏览事件和敏感字段拦截。
- [x] 4.4 运行相关后端测试、小程序/前端测试和 `openspec validate update-miniapp-category-product-list-entry --strict`。
