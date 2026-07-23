## 1. 小程序分类页修复

- [x] 1.1 定位 `src/miniapp/pages/category/index` 中二级分类宫格和分类名称展示结构。
- [x] 1.2 移除或调整导致 4 字以上名称被过早省略的单行截断、固定宽度或 `text-overflow` 等样式策略。
- [x] 1.3 设计并实现长名称展示方案，使 5-8 字二级分类名称可完整识别，超过 8 字名称可辨识且不破坏布局。
- [x] 1.4 保持三列宫格、深色视觉、二级分类点击热区和商品列表跳转行为不变。

## 2. 回归测试

- [x] 2.1 补充或更新小程序静态测试，覆盖二级分类长名称展示策略。
- [x] 2.2 回归 4 字以内、5-8 字、超过 8 字二级分类名称，确认不再出现超过 4 字即不可辨识省略的问题。
- [x] 2.3 回归二级分类点击跳转 `pages/product-list/index?categoryId={secondaryCategoryId}&categoryName={encodedName}&categoryLevel=secondary&sourcePage=category` 或等价路径。
- [x] 2.4 回归一级分类切换、右侧滚动到顶部、返回分类页状态恢复、空二级分类状态和网络异常降级。
- [x] 2.5 如仅调整小程序前端展示样式，在实现输出中说明不需要 OpenAPI / Orval；如实际修改 API 字段或响应结构，必须同步 OpenAPI、Orval、`docs/03-api-index.md` 和相关测试。

## 3. 验收与追踪

- [x] 3.1 采集微信开发者工具截图，覆盖 4 字以内、5-8 字、超过 8 字二级分类名称。
- [x] 3.2 采集至少一种真机证据，确认长名称展示和点击入口可用。
- [x] 3.3 更新 `BUG-0077` trace、Change trace 与验收证据。
- [x] 3.4 修复完成后评估是否需要沉淀到 `docs/knowledge-base/incidents/`；若无复用价值，在验收输出中说明不新增知识库条目。
