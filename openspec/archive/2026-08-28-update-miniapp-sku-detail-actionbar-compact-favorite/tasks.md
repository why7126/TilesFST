## 1. 商品详情底部操作栏

- [x] 1.1 调整 `src/miniapp/pages/tile-detail/index.wxml`，移除收藏按钮下方“收藏 / 已收藏”可见文字，保留收藏按钮事件、状态和必要语义说明。
- [x] 1.2 调整 `src/miniapp/pages/tile-detail/index.wxss`，压缩底部 actionbar 高度、收藏按钮尺寸、间距和页面底部留白，并保持触控热区不小于 44x44 pt 或等效尺寸。
- [x] 1.3 验证收藏、取消收藏、请求中和失败回滚状态不会导致底部 actionbar 高度跳变，toast 反馈和状态切换保持不变。

## 2. 分享按钮与返回首页悬浮按钮

- [x] 2.1 确认“分享给客户”按钮保留主视觉权重、点击热区和微信 `open-type="share"` 能力。
- [x] 2.2 调整 `src/miniapp/components/home-floating-button` 在 actionbar 场景下的 offset，使其匹配压缩后的底部栏和安全区避让。
- [x] 2.3 确认返回首页悬浮按钮不遮挡收藏按钮、分享按钮、推荐商品卡片或底部安全区。

## 3. 测试与验收证据

- [x] 3.1 补充或更新小程序静态测试，覆盖商品详情页收藏按钮无可见第二行文字、分享按钮能力保留、底部 actionbar 紧凑样式和首页悬浮按钮 actionbar offset。
- [x] 3.2 运行小程序相关聚焦测试，至少覆盖 `tests/test_miniapp_static.py` 中商品详情页和首页悬浮按钮契约。
- [x] 3.3 记录 320 pt、375 pt、430 pt 小程序视口视觉证据或人工摘要；若微信开发者工具 / 真机不可用，在 trace 中标记 `blocked` 或 `follow_up` 并说明剩余风险。
- [x] 3.4 通过实现 diff 复核未修改收藏 API、SKU 详情 API、分享 `open-type`、请求封装、track 事件名、数据模型、OpenAPI 或 Orval。
