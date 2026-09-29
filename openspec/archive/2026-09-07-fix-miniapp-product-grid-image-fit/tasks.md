## 1. 小程序商品卡片修复

- [x] 1.1 调整 `src/miniapp/components/product-card/index.wxml` 中 grid 商品图展示模式，使 `density="grid"` 优先完整显示整张商品图。
- [x] 1.2 调整 `src/miniapp/components/product-card/index.wxss` 中 grid 图片区域比例、高度和占位背景，确保卡片高度更适合完整展示方形瓷砖图。
- [x] 1.3 保持 `density="compact"` 与 `density="list"` 场景现有布局不因本 BUG 被强制改动。
- [x] 1.4 确认图片加载失败、无图占位和骨架屏与新的 grid 图片比例一致，不产生布局跳动。

## 2. 复用场景检查

- [x] 2.1 检查 `src/miniapp/pages/product-list/` 商品列表页 grid 商品卡片完整显示整图。
- [x] 2.2 检查 `src/miniapp/pages/brand-detail/` 商品 Tab grid 商品卡片与商品列表页表现一致。
- [x] 2.3 检查 `src/miniapp/pages/index/` 首页全部产品 grid 商品卡片与商品列表页表现一致。

## 3. 测试与验收

- [x] 3.1 更新 `tests/test_miniapp_static.py` 中 grid 图片比例、图片展示模式和骨架屏稳定性相关断言。
- [x] 3.2 运行聚焦小程序静态测试，确认新的 grid 契约通过。
- [x] 3.3 使用小程序 DevTools 或等价截图覆盖 320、375、430 pt 逻辑宽度，记录商品列表页、品牌详情商品 Tab 和首页全部产品 grid 渲染证据。
- [x] 3.4 回填 `issues/bugs/archive/BUG-0148-miniapp-product-list-card-image-fit/acceptance.md` 的 render evidence；key/object/URL 维度保持 n/a。

## 4. 文档与闭环

- [x] 4.1 确认本 Change 不涉及 API、DB、Orval、对象存储、Docker Compose 和产品数据采集链路；如实现阶段发现范围扩大，先更新 proposal/design/spec/tasks。
- [x] 4.2 运行 `openspec validate fix-miniapp-product-grid-image-fit --strict`、`python scripts/validate-openspec-language.py`、目录结构校验、Workflow Sync 和 AI Usage hook。
- [x] 4.3 评估是否需要沉淀到 `docs/knowledge-base/incidents/`；若只是单点样式契约修复，可在归档验收中记录不适用原因。
