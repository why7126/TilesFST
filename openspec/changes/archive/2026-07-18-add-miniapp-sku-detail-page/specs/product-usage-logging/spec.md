## ADDED Requirements

### Requirement: 小程序 SKU 详情页行为事件
系统 SHALL 支持微信小程序 SKU 详情页行为事件，用于记录详情浏览、媒体交互、收藏、分享、品牌入口、推荐点击和加载失败，同时遵守统一 usage event 脱敏策略。

#### Scenario: SKU 详情页浏览事件
- **WHEN** 微信小程序 SKU 详情页成功展示
- **THEN** 系统 SHALL 接受已登记或等价预留的 `sku_detail_view` 事件
- **AND** 事件 SHALL 仅携带必要的 SKU ID、页面标识、来源参数、client type 和时间上下文
- **AND** 埋点失败 SHALL NOT 阻断详情页展示。

#### Scenario: SKU 媒体交互事件
- **WHEN** 用户切换媒体、打开图片预览或播放视频
- **THEN** 系统 SHALL 接受已登记或等价预留的 `sku_media_swipe`、`sku_image_preview` 和 `sku_video_play` 事件
- **AND** 事件 SHALL NOT 包含原始 object key、未授权媒体 URL、Authorization header、Cookie 或用户敏感信息。

#### Scenario: SKU 收藏和分享事件
- **WHEN** 用户成功收藏、取消收藏或点击分享 SKU
- **THEN** 系统 SHALL 接受已登记或等价预留的 `sku_favorite`、`sku_unfavorite` 和 `sku_share_click` 事件
- **AND** 收藏事件 SHALL 仅记录 SKU 粒度业务事实和必要上下文
- **AND** 分享事件 SHALL NOT 存储聊天内容、联系人、群信息或原始手机号。

#### Scenario: SKU 品牌和推荐点击事件
- **WHEN** 用户点击品牌入口、同系列推荐或同品牌推荐
- **THEN** 系统 SHALL 接受已登记或等价预留的 `sku_brand_click` 和 `sku_recommend_click` 事件
- **AND** 推荐点击事件 SHALL 携带当前 SKU ID、目标 SKU ID、推荐类型和必要页面上下文。

#### Scenario: SKU 详情加载失败事件
- **WHEN** SKU 详情加载失败、SKU 不存在或网络失败
- **THEN** 系统 SHALL 接受已登记或等价预留的 `sku_load_error` 事件
- **AND** 事件 metadata SHALL 只包含脱敏错误码、失败阶段和必要页面上下文
- **AND** SHALL NOT 持久化原始响应体、token、Cookie、Authorization header 或内部路径。
