## 1. 小程序分类页布局修复

- [x] 1.1 定位 `src/miniapp/pages/category/index.wxss` 中 `.secondary-grid`、`.secondary-card`、`.secondary-name` 和 `.skeleton-grid` 的现有样式。
- [x] 1.2 将二级类目卡片实际网格调整为每行 2 个。
- [x] 1.3 将二级类目加载态 skeleton 网格同步调整为每行 2 个。
- [x] 1.4 调整二级类目名称文本规则，确保名称完整显示，不使用省略号、行数 clamp 或隐藏溢出省略名称。
- [x] 1.5 保持二级类目卡片点击热区、按压反馈、`data-id`、`data-name` 和 `aria-label` 不退化。

## 2. 边界与非影响范围确认

- [x] 2.1 确认不修改分类树接口响应结构、缓存版本、排序和状态过滤逻辑。
- [x] 2.2 确认不修改 `openSecondary` 跳转参数语义，继续携带 `categoryId`、`categoryName`、`categoryLevel=secondary` 和 `sourcePage=category`。
- [x] 2.3 确认不影响品牌页、搜索页、首页商品卡片布局和管理端类目维护。
- [x] 2.4 若实现阶段发现必须调整 API 或数据结构，停止并补充 API、Orval、docs 与测试任务。

## 3. 回归测试与验收

- [x] 3.1 补充或更新小程序分类页样式/静态检查，覆盖 `.secondary-grid` 和 `.skeleton-grid` 两列布局。
- [x] 3.2 使用包含 4 字以内、5-8 字、超过 8 字、数字规格和中文组合的二级类目数据验证名称完整显示。
- [x] 3.3 验证长名称换行后不遮挡相邻卡片、一级类目、标题、“查看全部商品”入口、底部 TabBar 或页面滚动。
- [x] 3.4 验证点击二级类目仍进入对应商品列表页，路由参数保持一致。
- [x] 3.5 在微信开发者工具记录 320 pt、375 pt、390 pt、430 pt 或等价视口 evidence；真机不可用时标记 blocked/follow_up。

## 4. 文档与追溯

- [x] 4.1 更新 `BUG-0093` trace 与 Change trace，记录实现、测试和验收结论。
- [x] 4.2 归档前运行 OpenSpec 校验、目录结构校验和相关小程序检查。
- [x] 4.3 评估该回归是否有可复用经验；如有，补充 `docs/knowledge-base/incidents/` 或对应 Sprint 复盘。

## 验收返修记录

| 时间 | 反馈 | 调整 | 验证 |
|---|---|---|---|
| 2026-07-30 23:48:19 | 二级类目名称没有垂直居中显示，偏靠上 | `.secondary-name` 增加 flex 垂直/水平居中与 border-box，保持完整换行和不截断 | 已通过 `uv run pytest tests/test_miniapp_static.py`（31 passed） |
