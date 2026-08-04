## 1. 实现

- [x] 1.1 复核 `src/miniapp/pages/brand-list/index.wxml` 与 `index.wxss` 中品牌类目胶囊的容器结构和现有点击绑定。
- [x] 1.2 将 `.brand-categories` 调整为固定两列布局或等效列约束，确保左列和右列分别左对齐。
- [x] 1.3 将 `.category-pill` 调整为受列宽约束的单行胶囊，长文本使用省略号，不换行、不撑破边框、不横向溢出。
- [x] 1.4 确认 `category_items`、`data-brand-index`、`data-category-index`、`onCategoryTap` 和 `brand_list_category_click` 埋点不变。
- [x] 1.5 如结构或逻辑涉及 `.ts`，同步运行时 `.js` 文件，避免微信开发者工具加载旧逻辑。

## 2. 测试

- [x] 2.1 更新 `tests/test_miniapp_static.py`，将品牌列表页旧的“不得使用两列 grid”断言改为两列固定布局或等效列约束断言。
- [x] 2.2 补充 `.category-pill` 单行省略号样式断言，覆盖 `overflow`、`text-overflow`、`white-space`、`min-width` 或等效约束。
- [x] 2.3 保留类目点击跳转参数断言，确认完整 `brandId`、`categoryId`、`categoryLevel=secondary`、`categoryName` 和 `sourcePage=brand-list-category` 不变。
- [x] 2.4 运行 `uv run pytest tests/test_miniapp_static.py` 或实现阶段新增的最小相关测试。

## 3. 验收与文档

- [x] 3.1 使用短、中、长类目名称数据验证品牌列表页类目区两列各自左对齐。
- [x] 3.2 验证长类目名称单行省略号展示，不换行、不撑破胶囊、不横向溢出。
- [x] 3.3 验证无类目品牌仍展示 `暂无类目` 且布局不异常。
- [x] 3.4 回填 `BUG-0114` AC-001 至 AC-008 验收 evidence。
- [x] 3.5 若实现过程中发现可复用的小程序胶囊网格布局经验，更新 `docs/knowledge-base/incidents/` 或 best-practice。
- [x] 3.6 运行 `openspec validate fix-miniapp-brand-list-category-column-alignment --strict` 和 `python scripts/validate-openspec-language.py`。
