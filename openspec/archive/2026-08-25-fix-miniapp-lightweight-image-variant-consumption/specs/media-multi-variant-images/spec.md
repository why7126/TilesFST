## MODIFIED Requirements

### Requirement: 媒体图片必须支持多规格展示图

系统 MUST 支持 `thumbnail`、`display`、`original` 三类媒体图片规格。`thumbnail` MUST 用于列表、卡片、小 Logo、推荐位和轻量预览；`display` MUST 用于小程序 Banner 轮播图、品牌主页顶部 Hero 图、详情普通展示、图册浏览和受控分享图；`original` MUST 保留上传原图或等价高清资源，用于高清预览、下载或需要保真的场景。三类规格 MUST 可追溯到同一媒体记录或业务对象，并 MUST 明确 key、MIME、尺寸、质量、体积上限、生成状态和失败原因的记录方式。`.display` 派生图体积目标 MUST 读取系统设置 media 分组的 display 图体积目标 effective 配置，默认 MUST 为 `768` KB，且 MUST NOT 复用缩略图体积目标配置。

系统 MUST 沉淀 Web 与微信小程序统一的图片三规格消费矩阵。矩阵字段 MUST 至少包括：页面、位置、图对象、是否缩略图、是否 display 图、是否原图、优化方案。矩阵 MUST 覆盖微信小程序真实页面、Web 管理端真实媒体展示位置，并为店主 Web 展示端提供明确的预留规范。矩阵中的每个页面位置 MUST 只表达一个主消费规格；普通展示、高清预览、下载、分享或原文件查看使用不同规格时，MUST 拆成独立行。

非原图目标场景 MUST NOT fallback 到 `original`。当列表、卡片、推荐位、小 Logo 等 `thumbnail` 目标场景，或小程序 Banner 轮播图、品牌主页顶部 Hero 图、详情普通展示、图册浏览、表单大预览、受控分享图等 `display` 目标场景缺少目标规格时，系统 MUST 使用安全占位、补齐派生图或在矩阵优化方案中标记后续修正；验收 MUST NOT 将原图 fallback 写作缩略图或展示图性能通过。

#### Scenario: 统一消费矩阵覆盖小程序页面

- **WHEN** 团队维护图片三规格消费矩阵
- **THEN** 矩阵 MUST 覆盖微信小程序首页、商品列表页、搜索页、商品详情页、品牌列表页、品牌详情页、证书列表页、证书详情页和收藏页
- **AND** 商品卡片、搜索结果、推荐商品、品牌 Logo、证书缩略图和收藏商品卡片 MUST 以 `thumbnail` 或等价轻量字段为目标规格
- **AND** 首页 Banner、品牌列表 Banner、品牌主页顶部 Hero 图、商品详情 Banner 普通展示、证书详情普通展示和受控分享图 MUST 以 `display` 或明确分享轻量字段为目标规格
- **AND** 商品图片预览、证书图片预览、下载或原文件查看 MUST 以 `original` 为目标规格
- **AND** 小程序普通展示入口 SHALL NOT 使用 `original_url`、`preview_url`、旧 `url` 或语义不明的 `image_url` 作为默认冷加载兜底
- **AND** 不使用业务媒体的页面 MAY 标注“不涉及业务图片”。

#### Scenario: 小程序轻量图字段缺失时不回退原图

- **GIVEN** 小程序页面目标规格为 `thumbnail` 或 `display`
- **WHEN** 后端未返回对应轻量 URL、对象不可读或图片加载失败
- **THEN** 页面 SHALL 展示安全占位、品牌首字、默认图或可理解失败态
- **AND** 页面 SHALL NOT 通过 `original_url`、`preview_url`、旧 `url`、`brand_logo_url` 或非轻量 `image_url` 冷加载原图
- **AND** 验收 SHALL 记录小程序 DevTools、真机或体验版 Network/render evidence。

### Requirement: 媒体 API 必须提供多规格 URL 语义

商品、SKU、Banner、品牌、品牌证书或媒体相关 API MUST 提供 `thumbnail_url`、`display_url`、`original_url` 或等价语义字段，使小程序、店主 Web 和管理端可以按场景选择图片规格。证书详情等品牌证书媒体 API 也 MUST 遵守同一语义：图片证书详情普通展示 MUST 使用 `display_url` 或等价展示图，图片预览 MUST 使用 `original_url`、`preview_url` 或等价高清 URL，PDF/文档证书 MUST 使用文件打开或占位策略而不是图片 `display_url`。API MUST 明确 URL 类型、签名、缓存、权限、过期和 fallback 策略，并 MUST 同步 OpenAPI、Orval、API 文档和测试。

#### Scenario: Banner 媒体响应包含轻量 URL

- **WHEN** 小程序请求首页或品牌列表 Banner 数据
- **THEN** 响应 MUST 为每条图片 Banner 提供 `display_url`、`thumbnail_url` 或等价轻量展示 URL
- **AND** 旧 `image_url` 字段如保留 SHALL 明确作为兼容字段，不得作为端侧普通展示唯一契约
- **AND** 小程序端普通展示 SHALL 优先消费 `display_url`，缺失或不可读时降级到 `thumbnail_url`，再降级到安全视图占位
- **AND** 当轻量对象缺失或不可读时，响应 SHALL 返回空轻量字段或安全占位语义，不得伪造不可读派生 URL。

#### Scenario: 分享图响应不默认使用原图

- **WHEN** 小程序请求 SKU、品牌或证书详情且响应包含分享图
- **THEN** 分享图字段 SHOULD 优先使用明确分享轻量字段、`display_url`、`thumbnail_url` 或安全占位
- **AND** 默认分享字段 SHALL NOT 直接退到 `original_url`、`preview_url` 或旧 `url`
- **AND** 如平台限制要求高清分享图，API 文档和验收 SHALL 将其记录为分享入口例外，并证明该例外不会影响普通展示冷加载。
