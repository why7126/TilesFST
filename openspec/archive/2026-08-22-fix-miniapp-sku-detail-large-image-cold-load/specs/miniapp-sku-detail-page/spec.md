## MODIFIED Requirements

### Requirement: 图片与视频混合媒体浏览

SKU 详情页 SHALL 支持图片和视频混合轮播，并提供图片全屏预览和视频播放控制。视频播放体验 SHALL 适配生产环境受控媒体读取链路，避免用户点击播放后长时间空白或无反馈。SKU 详情页首屏图片展示 SHALL 使用详情级展示图或受控压缩图以支持瓷砖纹理、花色、表面质感和规格细节查看，且 SHALL NOT 在默认冷加载普通展示链路中加载 `>1 MB` 原图。图片预览 SHALL 使用 `original_url`、原图或等价高清预览 URL。商品列表、推荐卡和轻量卡片 SHALL 使用 `thumbnail_url` 或等价轻量图片 URL。

#### Scenario: 详情页冷加载限制大图资源

- **WHEN** 小程序请求 `GET /api/v1/miniapp/skus/{sku_id}` 且 SKU 存在图片媒体
- **THEN** 详情页普通展示 URL SHALL 优先使用 `display_url`、详情展示图、压缩图或等价安全展示 URL
- **AND** 后端 SHALL only return `display_url` and `thumbnail_url` when the corresponding derived media object exists and is readable
- **AND** 当 `.display.*` 或 `.thumb.*` 派生对象缺失或不可读时，响应 SHALL leave the corresponding display or thumbnail field empty and SHALL NOT synthesize a broken derived URL
- **AND** 默认冷加载普通展示链路 SHALL NOT 加载 `>1 MB` 原图
- **AND** 首屏关键图片目标体积 SHOULD 控制在 `100-300 kB`
- **AND** 普通详情展示图片目标体积 SHOULD 控制在 `150-500 kB`
- **AND** 图片媒体的 `preview_url`、`original_url` 或等价字段 SHALL 指向原图、高清图或等价高清预览 URL
- **AND** 详情页普通展示 fallback SHALL use `thumbnail_url` or a local placeholder when `display_url` is empty and SHALL NOT use `original_url`、`preview_url` or original `media[].url`
- **AND** 用户点击图片预览前 SHALL NOT 请求高清原图
- **AND** 响应 SHALL NOT 暴露原始 object key、对象存储 endpoint、bucket 名称、未授权素材路径或内部文件系统路径。

#### Scenario: PNG 大图提供展示版替代

- **WHEN** SKU 图片媒体原始文件为 PNG 且体积超过详情普通展示目标范围
- **THEN** 系统 SHALL 提供展示版替代资源用于详情页普通展示
- **AND** 非透明 PNG MAY 转换为 JPG、WebP 或等价压缩展示格式
- **AND** 透明 PNG SHALL 保留透明语义或使用等价可接受的透明展示格式
- **AND** 原始 PNG SHALL 仅在点击预览、下载或等价高清查看场景加载。

#### Scenario: 详情页首屏外图片 lazy-load

- **WHEN** SKU 详情页存在多张图片媒体
- **THEN** 首屏外图片 SHALL 启用 `lazy-load` 或等价延迟加载策略
- **AND** 首屏基础信息 SHALL 不被非关键图片请求阻塞
- **AND** 小程序静态测试、DevTools、体验版或真机 evidence SHALL 覆盖该行为。

#### Scenario: 冷加载大图修复验收 evidence

- **WHEN** 团队验收 `BUG-0132` 修复结果
- **THEN** 验收 SHALL 记录小程序商品详情页 Network evidence，至少包含首屏关键图、普通详情图和点击预览原图的 URL 类型、HTTP 状态、资源大小、耗时、Waterfall 和缓存状态
- **AND** 首屏关键图 evidence SHOULD 满足 `100-300 kB` 目标范围
- **AND** 普通详情展示图 evidence SHOULD 满足 `150-500 kB` 目标范围
- **AND** 默认冷加载普通展示链路 SHALL NOT 出现 `>1 MB` 原图
- **AND** media evidence SHALL 覆盖 key、object、URL、render 四点
- **AND** 缺少体验版、真机或等价 DevTools evidence 时 SHALL 标记 `blocked` 或 `follow_up`，不得写作已通过。
