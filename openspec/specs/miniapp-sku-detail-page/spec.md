# miniapp-sku-detail-page Specification

## Purpose
定义微信小程序 SKU 详情页的公开数据、媒体浏览、收藏分享、品牌入口、相关推荐、异常状态、安全边界和测试同步要求，确保用户可从多入口稳定查看单个瓷砖 SKU 的完整公开信息。
## Requirements
### Requirement: SKU 详情页入口与公开数据

系统 SHALL 提供微信小程序 SKU 详情页，用于从首页、分类、搜索、品牌页、收藏页和微信分享卡片进入单个瓷砖 SKU 的公开详情。

#### Scenario: 多入口进入 SKU 详情

- **WHEN** 用户从首页商品卡片、分类列表、搜索结果、品牌页、收藏页或微信分享卡片点击 SKU
- **THEN** 小程序 SHALL 携带 `skuId` 进入 SKU 详情页
- **AND** 页面 SHALL 记录可用的来源参数
- **AND** 缺少或非法 `skuId` 时 SHALL 展示可恢复错误状态，而不是白屏或路由错误。

#### Scenario: 详情接口返回公开数据

- **WHEN** 小程序请求 SKU 详情数据
- **THEN** 后端 SHALL 返回 SKU 主体、媒体、品牌、收藏状态、同系列推荐和同品牌推荐所需公开字段
- **AND** 响应 SHALL NOT 暴露后台内部字段、库存管理、内部备注、未授权素材、原始 object key、Authorization header、Cookie 或敏感配置
- **AND** 响应 MAY 保留 `sku_code` 作为兼容字段，但小程序 SHALL NOT 直接渲染该字段。

#### Scenario: SKU 不存在或不可公开

- **WHEN** SKU 不存在、已下架或不允许公开展示
- **THEN** 小程序 SHALL 展示“商品暂不可查看”或等价空状态
- **AND** 页面 SHALL 提供返回首页或返回上一页入口。

### Requirement: SKU 详情信息展示

SKU 详情页 SHALL 完整展示用户选砖所需的品牌、商品名称、价格、参数、类目和备注信息。SKU 编码 SHALL 作为系统内部识别字段，不在小程序/店主端详情页标题、参数区或推荐卡中展示。备注说明 SHALL 使用 SKU 详情接口返回的公开备注字段端到端展示，非空时可见，空值时按安全空态处理。

#### Scenario: 展示 SKU 核心字段

- **WHEN** SKU 详情加载成功
- **THEN** 页面 SHALL 展示品牌名称、商品名称、参考价格、计价单位、规格、表面工艺、主色系、完整类目路径和备注说明
- **AND** 备注说明非空时 SHALL 在详情信息区或等价公开信息区展示，内容 SHALL 与 SKU 详情接口返回的公开备注说明字段一致
- **AND** 品牌信息 SHALL 位于商品名称上方并提供品牌入口
- **AND** 页面 SHALL NOT 展示 SKU 编码、`sku_code` 字段名或“SKU 编码：xxx”参数行。

#### Scenario: 空字段安全展示

- **WHEN** 表面工艺、主色系、备注或可选媒体字段为空
- **THEN** 页面 SHALL 按字段规则展示 “—”、隐藏对应模块或展示安全占位
- **AND** 备注说明为空时 SHALL NOT 展示 `null`、`undefined`、接口字段名、异常空白卡片或布局错位
- **AND** 页面 SHALL NOT 展示 `null`、`undefined`、接口字段名或空白异常卡片
- **AND** 商品名称缺失 SHALL 作为异常数据处理，不得用 SKU 编码作为正常公开兜底。

#### Scenario: 备注说明公开字段边界

- **WHEN** SKU 详情接口和小程序页面处理备注说明
- **THEN** 小程序 SHALL 只展示允许公开的商品/SKU 备注说明字段
- **AND** 响应和页面 SHALL NOT 暴露后台内部备注、库存管理、内部审核信息、原始 object key、Authorization header、Cookie 或敏感配置
- **AND** 小程序端字段映射 SHALL 与接口返回字段保持一致，避免接口已返回但页面未绑定展示。

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

### Requirement: SKU 收藏与分享

SKU 详情页 SHALL 支持 SKU 粒度收藏、取消收藏和微信原生分享。公开分享文案 SHALL 使用品牌名称与商品名称，不展示 SKU 编码。

#### Scenario: 收藏和取消收藏成功

- **WHEN** 用户点击收藏或取消收藏当前 SKU 且请求成功
- **THEN** 页面 SHALL 更新按钮状态
- **AND** 页面 SHALL 展示成功 Toast
- **AND** 收藏页或等价收藏数据 SHALL 与当前 SKU 收藏事实保持一致。

#### Scenario: 收藏失败回滚

- **WHEN** 收藏或取消收藏请求失败、超时或授权失败
- **THEN** 页面 SHALL 回滚到请求前状态
- **AND** 页面 SHALL 展示可理解失败提示
- **AND** 失败 SHALL NOT 阻断用户继续浏览详情。

#### Scenario: 收藏接口幂等

- **WHEN** 客户端重复提交收藏或取消收藏请求
- **THEN** 后端 SHALL 返回与目标状态一致的结果
- **AND** 不得产生重复收藏记录或错误取消状态。

#### Scenario: 分享 SKU

- **WHEN** 用户点击 SKU 详情页分享入口
- **THEN** 小程序 SHALL 调起微信原生分享或等价分享能力
- **AND** 分享标题 SHALL 包含商品名称和品牌名称
- **AND** 分享卡片 SHALL 包含主图、商品名称、品牌和参考价格
- **AND** 分享路径 SHALL 携带 `skuId` 和来源参数
- **AND** 分享标题、摘要和卡片展示 SHALL NOT 拼接 SKU 编码。

### Requirement: 品牌入口与相关推荐

SKU 详情页 SHALL 支持进入品牌主页、同系列商品和同品牌推荐，使用户可以继续浏览相关瓷砖；SKU 详情页品牌卡 SHALL 使用微信小程序品牌卡片组件承载单品牌展示、Logo fallback、入口提示和点击跳转。SKU 详情接口返回的品牌入口路径 SHALL 指向对应品牌详情页，品牌卡片不得在存在有效品牌详情页入口时误跳搜索页。SKU 详情接口返回的品牌对象 SHALL 包含 `brand_logo_thumbnail_url` 或等价轻量 Logo URL，使商品详情页品牌卡普通展示可以优先使用缩略图。

#### Scenario: SKU 详情接口返回品牌详情页入口

- **WHEN** 小程序请求 `GET /api/v1/miniapp/skus/{sku_id}` 且当前 SKU 关联启用品牌
- **THEN** 后端 SHALL 在 `data.brand.brand_entry_path` 返回 `/pages/brand-detail/index?brandId=<brand_id>`
- **AND** `brand_id` SHALL 与当前 SKU 关联品牌一致
- **AND** 响应 SHALL NOT 将可访问品牌入口返回为 `/pages/search/index` 或搜索结果页路径
- **AND** 后端 SHALL 在 `data.brand.brand_logo_thumbnail_url` 返回品牌 Logo 缩略图或等价轻量 URL，缺少可用缩略图时 SHALL 返回空值而不是伪造不可读 URL。

#### Scenario: SKU 详情页使用品牌卡片组件

- **WHEN** SKU 详情页展示品牌卡
- **THEN** 页面 SHALL 使用微信小程序品牌卡片组件替换重复的内联品牌卡片结构
- **AND** 页面 SHALL 从 SKU 详情数据中提取品牌展示对象、`skuId` 和来源上下文传入组件
- **AND** 页面 SHALL 保留并传递 `brand_logo_thumbnail_url`
- **AND** 组件 SHALL 负责 Logo 缺失/失败、长品牌名、入口不可用和点击防重复等卡片级行为。

#### Scenario: SKU 详情页品牌卡 Logo 缩略图优先

- **WHEN** SKU 详情页品牌对象同时包含 `brand_logo_thumbnail_url` 与 `brand_logo_url`
- **THEN** 品牌卡普通展示 SHALL 优先请求 `brand_logo_thumbnail_url`
- **AND** `brand_logo_url` SHALL 仅作为兼容字段或高清语义引用，不得作为缩略图可用时的首选展示资源
- **AND** 验收 SHALL 记录小程序 DevTools、真机或体验版 Network evidence，覆盖品牌 Logo URL 类型、HTTP 状态、资源大小、耗时和渲染结果。

### Requirement: SKU 详情页视觉与可用性

SKU 详情页 SHALL 延续微信小程序首页 v6 深色企业轻奢风，并在主流小程序视口内保持可用。顶部媒体区 SHALL 比旧固定 `680rpx` 更适合瓷砖详情展示，同时 SHALL 保持首屏商品名称或关键商品信息可见。

#### Scenario: 深色视觉和大媒体区

- **WHEN** 用户查看 SKU 详情页
- **THEN** 页面 SHALL 使用与小程序首页 v6 一致的深色背景、卡片层、主文字、辅助文字和品牌金语义
- **AND** 顶部媒体区 SHALL 采用大图布局
- **AND** 媒体区高度 SHALL 基于视口宽度、安全区和上限约束计算，避免固定 `680rpx` 无法适配主流设备
- **AND** 首屏 SHALL 露出商品名称或关键商品信息
- **AND** 页面 SHALL NOT 使用电商红主按钮、纯白大背景或购物导向视觉。

#### Scenario: 移动视口可用

- **WHEN** 团队在 320 到 430px 逻辑宽度和常见底部安全区验收页面
- **THEN** 页面 SHALL 无横向滚动、内容重叠、按钮遮挡或关键文字截断
- **AND** 主要点击目标 SHALL 不小于 44x44px 或小程序等效尺寸
- **AND** 顶部媒体区变高后 SHALL NOT 将商品名称或关键商品信息完全挤出首屏。

### Requirement: SKU 详情页范围控制与安全

SKU 详情页 SHALL 明确不做购物交易能力，并保证富文本、媒体和埋点安全。

#### Scenario: 安全媒体 URL

- **WHEN** 详情响应包含图片、视频或分享图
- **THEN** URL SHALL 来自后端授权、公开安全 URL 或对象存储适配层生成结果
- **AND** 小程序 SHALL NOT 直接使用未授权 object key 拼接对象存储地址
- **AND** 视频媒体 URL SHALL NOT 使用 `tile_videos.file_name` 原始上传文件名作为播放地址
- **AND** 当视频记录包含 `tile_videos.object_key` 时，详情接口 SHALL 基于该对象 key 返回 `/media/{object_key}` 或完整公开安全 URL
- **AND** 实际反馈 SKU 的视频 `media[].url` MUST 在生产 smoke 中确认不为空且可通过同域受控链路读取。

### Requirement: SKU 详情页接口与测试同步

SKU 详情页涉及的 API、数据库、OpenAPI、Orval、文档和测试 SHALL 保持同步。

#### Scenario: 详情页高清展示图修复测试覆盖

- **WHEN** SKU 详情页媒体清晰度与高度修复完成
- **THEN** 后端测试 SHALL 覆盖图片展示 URL 使用原图或详情级高清展示图、预览 URL 保留原图、视频 `cover_url` 使用缩略图且视频 `url` 不变
- **AND** 后端测试 SHALL 覆盖商品列表、商品卡片、推荐位和 Banner 仍保留 `.thumb` 或等价轻量图片 URL
- **AND** 小程序静态测试 SHALL 覆盖详情页首屏图片绑定高清展示 URL、图片预览绑定原图 URL、视频 poster 兜底和轮播高度约束
- **AND** API 文档 SHALL 说明 SKU 详情媒体字段的展示、预览、播放和封面语义
- **AND** 媒体类 BUG 四联验收 SHALL 覆盖 key、object、URL、render 和小程序 evidence。

### Requirement: 商品列表进入 SKU 详情
SKU 详情页 SHALL 支持从小程序商品列表页商品卡片进入，并保持公开字段、安全媒体 URL、来源参数和不可公开状态边界。

#### Scenario: 商品列表卡片进入详情页
- **WHEN** 用户在商品列表页、搜索结果、首页推荐、品牌商品列表或收藏列表点击商品卡片
- **THEN** 小程序 SHALL 携带 `skuId` 和可用来源参数进入 SKU 详情页
- **AND** SKU 详情页 SHALL 按既有公开数据契约加载详情。

#### Scenario: 商品列表来源参数
- **WHEN** SKU 详情页由商品卡片打开
- **THEN** 页面 SHALL 记录可用来源参数
- **AND** 可用来源参数 MAY 包含 `sourcePage`、`sourceModule`、`categoryId`、`brandId`、`keyword`、`listContext`、`index` 和 `requestId`
- **AND** 来源参数 SHALL NOT 包含 Authorization header、Cookie、手机号、raw payload、raw object key、未授权素材路径或其他敏感信息。

#### Scenario: 不可公开 SKU
- **WHEN** 商品卡片进入的 SKU 不存在、已下架或不允许公开展示
- **THEN** SKU 详情页 SHALL 展示“商品暂不可查看”或等价空状态
- **AND** 页面 SHALL 提供返回商品列表或返回上一页入口。

### Requirement: SKU 详情页微信分享

SKU 详情页 SHALL 支持分享给微信朋友和分享到微信朋友圈，并 SHALL 保留当前 SKU 参数、分享图兜底和分享直达异常态。分享图字段 SHALL 与详情普通展示字段解耦，默认 SHALL 优先使用明确分享轻量字段、`display_url`、`thumbnail_url` 或安全兜底图；不得因兼容旧字段而默认下发原图。

#### Scenario: SKU 详情分享给微信朋友

- **WHEN** 用户在 SKU 详情页触发微信朋友分享
- **THEN** 小程序 SHALL 返回微信原生分享对象
- **AND** 分享路径 SHALL 指向当前 SKU 详情页并携带有效 `skuId` 和 `source=share` 或等价来源参数
- **AND** 分享标题 SHALL 优先使用商品分享标题，未配置时 SHALL 使用 SKU 名称与品牌名称组合
- **AND** 分享图 SHALL 优先使用明确分享轻量字段、商品主图 `display_url`、`thumbnail_url` 或安全兜底图
- **AND** 分享图 SHALL NOT 默认回退到 `original_url`、`preview_url` 或原始 `media[].url`
- **AND** 若平台限制要求高清分享图，验收 SHALL 将该行为记录为分享入口例外，并证明普通展示未受影响。

#### Scenario: SKU 分享图原图 fallback 回归测试

- **GIVEN** SKU 主图同时存在 `.jpg` 原图和 `.thumb.webp` 或 `.display.webp` 派生图
- **WHEN** 小程序加载 SKU 详情并生成分享对象
- **THEN** `share.image_url` SHALL 优先指向轻量分享图、`display_url`、`thumbnail_url` 或安全兜底图
- **AND** `share.image_url` SHALL NOT 在默认路径中指向原图 `.jpg`
- **AND** AppData、Network 或等价 evidence SHALL 记录分享图 URL 类型与页面渲染结果。

### Requirement: SKU 详情页视频全屏操作

SKU 详情页 SHALL 为视频媒体提供明确可感知的全屏播放入口，并在微信小程序平台能力允许范围内支持全屏态操作菜单或等价交互。全屏态操作 SHALL 覆盖转发给朋友、保存视频和取消三个用户意图，并 SHALL 保持既有图片预览、视频播放、分享、安全媒体 URL 和页面隐藏暂停能力不回归。对于已在内嵌区域开始播放的视频，点击全屏入口 SHALL 优先复用当前视频组件上下文或等价能力进入全屏播放态，避免重新进入长时间加载。

#### Scenario: 视频全屏入口

- **WHEN** SKU 详情页存在可播放视频媒体
- **THEN** 小程序 SHALL 在视频媒体项展示明确可感知的全屏播放入口，或使用微信原生视频控制条中可见的全屏入口
- **AND** 全屏入口 SHALL NOT 遮挡媒体计数、播放控制、轮播滑动、原生胶囊 reserve、返回按钮或底部操作栏
- **AND** 无视频媒体、视频 URL 为空或视频加载失败时 SHALL NOT 展示误导性的可用全屏入口，或 SHALL 展示明确错误提示。

#### Scenario: 进入与退出全屏播放

- **WHEN** 用户点击视频全屏入口
- **THEN** 当前视频 SHALL 进入微信小程序支持的视频全屏播放态
- **AND** 全屏播放 SHALL 由用户主动触发，不得默认自动全屏或默认自动播放
- **AND** 用户退出全屏后 SHALL 回到当前 SKU 详情页和当前媒体上下文
- **AND** 页面隐藏、锁屏、跳转、返回上一页或切换媒体时 SHALL 暂停当前视频或保持既有暂停策略不回归。

#### Scenario: 已播放视频切换全屏不重新长时间加载

- **WHEN** 用户先在 SKU 详情页内嵌轮播区域播放视频并已看到视频起播
- **AND** 用户点击当前视频的全屏入口
- **THEN** 小程序 SHALL 优先复用当前视频组件上下文或平台等价能力进入全屏播放态
- **AND** 全屏态 SHALL 在可接受时间内出现首帧或可播放反馈
- **AND** 小程序 SHOULD NOT 将已播放视频的主全屏入口实现为会重新长时间加载同一视频的独立媒体预览链路
- **AND** 若平台限制导致必须使用独立预览或重新加载，页面 SHALL 提供明确加载反馈或失败提示，并在验收材料中记录平台限制。

#### Scenario: 全屏态长按操作菜单

- **WHEN** 用户在视频全屏播放态长按当前视频
- **THEN** 小程序 SHOULD 展示包含“转发给朋友”“保存视频”“取消”的操作菜单，或微信平台允许的等价交互入口
- **AND** 点击“取消” SHALL 关闭菜单且不触发分享、保存、页面跳转或异常退出
- **AND** 若微信原生全屏态不支持自定义长按菜单，验收材料 SHALL 记录平台限制、降级方案和用户可达路径
- **AND** 系统 SHALL NOT 在验收材料中将不可自定义的原生能力宣称为已完全支持自定义长按菜单。

#### Scenario: 全屏态转发给朋友

- **WHEN** 用户从视频全屏态操作入口选择“转发给朋友”
- **THEN** 小程序 SHALL 复用 SKU 详情页既有微信分享能力或等价分享路径构造
- **AND** 分享路径 SHALL 指向当前 SKU 详情页并保留 `skuId` 与 `source=share` 或等价来源参数
- **AND** 分享标题和分享图 SHALL 使用当前 SKU 商品名称、品牌名称、商品分享图、主图或安全兜底图
- **AND** 分享埋点失败 SHALL NOT 阻断微信分享。

#### Scenario: 全屏态保存视频

- **WHEN** 用户从视频全屏态操作入口选择“保存视频”
- **THEN** 小程序 SHOULD 尝试按微信平台能力将当前视频保存到用户相册
- **AND** 视频 URL SHALL 来自详情接口返回的安全可播放 URL，不得使用原始 object key 拼接对象存储地址
- **AND** 保存流程 SHALL 遵守微信授权、远程文件下载、临时文件和相册保存限制
- **AND** 保存成功时 SHALL 展示明确成功提示
- **AND** 保存失败时 SHALL 展示权限拒绝、网络异常、视频暂不可保存、格式不支持或平台不支持等可理解提示
- **AND** 保存失败 SHALL NOT 阻断视频继续播放或商品详情继续浏览。

#### Scenario: 平台、安全与测试验收

- **WHEN** 团队实现或验收视频全屏操作能力
- **THEN** OpenSpec apply 记录 SHALL 明确微信 `video` 组件全屏、长按、自定义菜单、下载和保存到相册的实际能力边界
- **AND** 小程序静态测试 SHALL 覆盖视频全屏入口属性、分享路径、保存视频降级提示或等价关键逻辑
- **AND** 小程序静态测试 SHALL 覆盖已播放视频切换全屏时使用当前视频上下文或等价主路径的关键逻辑
- **AND** `src/miniapp/pages/tile-detail/index.ts` 与运行时 `index.js` 的视频全屏、菜单、分享和保存逻辑 SHALL 保持同步
- **AND** DevTools evidence SHALL 覆盖 320 / 375 / 430 pt 视口下视频全屏入口不遮挡关键 UI
- **AND** 至少一台真机 evidence SHALL 覆盖全屏入口、全屏播放、长按菜单或降级入口、转发、保存成功或失败提示、退出全屏回到详情页
- **AND** 真机 evidence SHALL 记录同一 SKU 视频的内嵌播放首帧耗时与点击全屏到全屏首帧耗时
- **AND** 若真机暂不可用，验收状态 SHALL 标记 `real_device_follow_up` 或 `blocked`，不得把静态测试或 DevTools 截图写成真机通过。

