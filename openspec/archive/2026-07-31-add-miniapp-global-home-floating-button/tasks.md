## 1. 路由与页面清单

- [x] 1.1 确认小程序首页路径和 TabBar 配置，决定返回首页使用 `wx.switchTab`、`wx.reLaunch` 或项目确认等价策略。
- [x] 1.2 梳理首期覆盖页面路径，至少包含搜索结果页、分类商品列表页、品牌详情页和商品详情页。
- [x] 1.3 梳理特殊页面和例外页面清单，至少包含首页、登录页、授权页、错误页、全屏视频页、图片预览页和原生预览页，并记录展示或豁免理由。
- [x] 1.4 梳理覆盖页面是否存在底部固定操作区、TabBar、客服、分享、咨询或其他悬浮入口，记录避让策略。

## 2. 小程序实现

- [x] 2.1 新增或复用统一返回首页悬浮按钮组件、behavior/mixin 或等价统一接入策略。
- [x] 2.2 实现首页隐藏、主要非首页展示、特殊页面按清单展示或豁免的判定逻辑。
- [x] 2.3 实现点击返回首页逻辑，覆盖 TabBar 首页、非 TabBar 首页、导航失败和连续点击防重复触发。
- [x] 2.4 实现悬浮按钮视觉、图标/短文案、触控热区、按压反馈和统一样式。
- [x] 2.5 实现底部安全区、TabBar、固定操作栏和其他悬浮入口的偏移或避让策略。
- [x] 2.6 确保接入页面 `.ts` 与微信开发者工具实际加载的 `.js` 逻辑一致。

## 3. 页面接入与回归

- [x] 3.1 在搜索结果页接入返回首页悬浮按钮，并确认不遮挡搜索结果、空态、错误态、重试和列表滚动。
- [x] 3.2 在分类商品列表页接入返回首页悬浮按钮，并确认不遮挡筛选、列表、加载更多和底部安全区。
- [x] 3.3 在品牌详情页接入返回首页悬浮按钮，并确认不遮挡品牌信息、Tab、商品列表、证书区域和页面主要入口。
- [x] 3.4 在商品详情页接入返回首页悬浮按钮，并确认上移避让收藏、分享、咨询、询价或其他底部固定操作区。
- [x] 3.5 确认首页、登录/授权、全屏视频、图片预览等例外页面未误展示按钮或已按设计说明处理。

## 4. 测试与设备 evidence

- [x] 4.1 补充小程序静态/页面测试或等价校验，覆盖首页隐藏、非首页展示、点击回首页、导航失败和连续点击防重复触发。
- [x] 4.2 补充小程序布局测试或人工 evidence，覆盖 320、375、430 pt 下按钮不遮挡主要内容、底部操作区、TabBar 和安全区。
- [x] 4.3 按 `docs/knowledge-base/best-practices/miniapp-custom-navigation.md` 记录 DevTools 320、375、430 pt evidence。
- [x] 4.4 记录真机 evidence；真机不可用时在验收材料中标记 `blocked` 或 `follow_up`，不得写作真机通过。
- [x] 4.5 确认 evidence 不包含本机绝对路径、token、Cookie、Authorization header、`.env` 内容、真实密钥、数据库 DSN、MinIO 凭据或真实客户数据。

## 5. 文档与追溯

- [x] 5.1 在 Change trace 中记录页面覆盖清单、例外清单、导航策略、测试和设备 evidence 摘要。
- [x] 5.2 同步 REQ trace、Sprint 验收材料和必要的长期文档引用，不修改 `openspec/specs/` 正式规格。
- [x] 5.3 归档前运行 OpenSpec 校验、目录结构校验和相关测试，确认 `miniapp-global-custom-navigation-bar` delta 可合并且无路径残留。

## 验收返修记录

| 时间 | 反馈 | 调整 | 验证 |
|---|---|---|---|
| 2026-07-31 00:03:10 | 分类列表页、品牌列表页、证书列表页、收藏列表页没有返回首页悬浮按钮。 | 将 `pages/category/index`、`pages/brand-list/index`、`pages/certificates/index`、`pages/favorites/index` 纳入覆盖清单，接入统一 `home-floating-button` 并使用 `offset="tabbar"` 避让自定义 TabBar；同步 Change design/spec、REQ acceptance、Change trace、Sprint 验收和发布说明。 | `uv run pytest tests/test_miniapp_static.py` 31 passed；`openspec validate add-miniapp-global-home-floating-button --strict` valid；`python scripts/validate-directory-structure.py` 通过；`git diff --check` 通过。 |
