## 1. 实现

- [x] 1.1 定位小程序返回首页悬浮按钮组件，以及页面级重复返回首页处理器。
- [x] 1.2 统一或对齐返回首页导航状态，确保 `success`、`fail`、`complete` 和页面重新进入路径都会释放导航锁。
- [x] 1.3 确保快速重复点击最多触发一次有效返回首页导航，且不会让按钮永久禁用。
- [x] 1.4 验证搜索结果、分类/商品列表、品牌列表/详情、证书列表/详情、收藏、SKU 详情等覆盖页面使用一致且可重复的返回首页行为。
- [x] 1.5 修复范围保持在小程序前端代码内；不新增 API、数据库、管理端、Web、对象存储或分析埋点变更。

## 2. 验证

- [x] 2.1 新增或更新小程序导航组件/工具测试，或等价静态检查，覆盖锁释放和重试行为。
- [x] 2.2 运行本仓库使用的小程序静态、类型或 lint 测试命令。
- [x] 2.3 在微信开发者工具或体验版中手工验证：同页重复进入、跨页重复进入和快速重复点击均能可靠返回首页。
- [x] 2.4 记录 BUG-0109 AC-001 至 AC-005 的验收 evidence。
- [x] 2.5 运行 `openspec validate fix-miniapp-home-navigation-repeat-click --strict`。
- [x] 2.6 评估本次问题是否有可复用经验；只有实现确认存在通用导航状态陷阱时，才更新 `docs/knowledge-base/incidents/`。

## 归档验证摘要

- 验证命令：`uv run pytest tests/test_miniapp_static.py`，验证结果：31 passed。
- 验证命令：`openspec validate fix-miniapp-home-navigation-repeat-click --strict`，验证结果：通过。
- 验收结论：BUG-0109 AC-001 至 AC-005 通过；小程序返回首页按钮支持同页重复进入、跨页重复进入、快速重复点击和导航失败后的状态恢复。
- Issue/Sprint 状态：来源 BUG 为 `BUG-0109-miniapp-home-button-one-time-failure`，Sprint 为 `sprint-018`，归档后由 Workflow Sync 和 promote 脚本闭环。
- 归档路径：`openspec/archive/2026-08-03-fix-miniapp-home-navigation-repeat-click`。
