## MODIFIED Requirements

### Requirement: 图片与视频混合媒体浏览

SKU 详情页 SHALL 支持图片和视频混合轮播，并提供图片全屏预览和视频播放控制。视频播放体验 SHALL 适配生产环境受控媒体读取链路，避免用户点击播放后长时间空白或无反馈。SKU 详情页首屏图片展示 SHALL 使用 `display_url`、原图或详情级高清展示图以支持瓷砖纹理、花色、表面质感和规格细节查看；图片预览 SHALL 使用 `original_url`、原图或等价高清预览 URL。商品列表、推荐卡和轻量卡片 SHALL 使用 `thumbnail_url` 或等价轻量图片 URL。

#### Scenario: 详情页普通展示使用 display 图

- **WHEN** 小程序请求 `GET /api/v1/miniapp/skus/{sku_id}` 且 SKU 存在图片媒体
- **THEN** 图片媒体用于详情页普通展示的 URL SHALL 优先使用 `display_url` 或等价详情展示 URL
- **AND** 图片媒体的 `preview_url` 或等价字段 SHALL 指向 `original_url`、原图或等价高清预览 URL
- **AND** 小程序详情页首屏 `<image>` SHALL 使用详情展示 URL
- **AND** 用户点击图片预览时 SHALL 基于被点击媒体在 `media` 中的下标生成 `current` 和 `urls`
- **AND** `current` 和 `urls` SHALL 统一按 `original_url || preview_url || url` 的优先级选择高清预览 URL
- **AND** 响应 SHALL NOT 暴露原始 object key、对象存储 endpoint、bucket 名称或未授权素材路径。

#### Scenario: 详情页首屏外图片 lazy-load

- **WHEN** SKU 详情页存在多张图片媒体
- **THEN** 首屏外图片 SHALL 启用 `lazy-load` 或等价延迟加载策略
- **AND** 首屏基础信息 SHALL 不被非关键图片请求阻塞
- **AND** 小程序静态测试、DevTools、体验版或真机 evidence SHALL 覆盖该行为。

#### Scenario: 小程序媒体 Network evidence 覆盖三类 URL

- **WHEN** 团队验收 SKU 详情页媒体多规格图
- **THEN** 验收 SHALL 分别记录列表 `thumbnail_url`、详情 `display_url`、预览 `original_url` 的页面路径、URL 类型、HTTP 状态、资源大小和耗时
- **AND** render evidence SHALL 覆盖页面展示、预览、fallback 或失败态
- **AND** 缺少体验版或真机 evidence 时 SHALL 标记 `blocked` 或 `follow_up`，不得写作已通过。
