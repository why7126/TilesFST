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
- **AND** 响应 SHALL NOT 暴露后台内部字段、库存管理、内部备注、未授权素材、原始 object key、Authorization header、Cookie 或敏感配置。

#### Scenario: SKU 不存在或不可公开
- **WHEN** SKU 不存在、已下架或不允许公开展示
- **THEN** 小程序 SHALL 展示“商品暂不可查看”或等价空状态
- **AND** 页面 SHALL 提供返回首页或返回上一页入口。

### Requirement: SKU 详情信息展示
SKU 详情页 SHALL 完整展示用户选砖所需的品牌、SKU、价格、参数、类目和备注信息。

#### Scenario: 展示 SKU 核心字段
- **WHEN** SKU 详情加载成功
- **THEN** 页面 SHALL 展示品牌名称、SKU 名称、SKU 编码、参考价格、计价单位、规格、表面工艺、主色系、完整类目路径和备注说明
- **AND** 品牌信息 SHALL 位于 SKU 名称上方并提供品牌入口。

#### Scenario: 空字段安全展示
- **WHEN** 表面工艺、主色系、备注或可选媒体字段为空
- **THEN** 页面 SHALL 按字段规则展示 “—”、隐藏对应模块或展示安全占位
- **AND** 页面 SHALL NOT 展示 `null`、`undefined`、接口字段名或空白异常卡片。

#### Scenario: 价格展示为参考价
- **WHEN** 详情页展示价格
- **THEN** 页面 SHALL 使用“参考价格”文案和计价单位
- **AND** 价格为 0 或空值时 SHALL 展示“暂无参考价”或等价状态
- **AND** 页面 SHALL 提示实际价格以门店最终确认为准。

### Requirement: 图片与视频混合媒体浏览
SKU 详情页 SHALL 支持图片和视频混合轮播，并提供图片全屏预览和视频播放控制。

#### Scenario: 视频播放控制
- **WHEN** 用户点击视频媒体
- **THEN** 视频 SHALL 由用户主动播放
- **AND** 页面 SHALL NOT 默认自动播放视频
- **AND** 视频播放期间轮播 SHALL NOT 自动切换
- **AND** 页面隐藏、锁屏或跳转时 SHALL 暂停当前视频
- **AND** 视频媒体的 `src` SHALL 使用详情接口返回的安全可播放 URL。

#### Scenario: 单项媒体失败
- **WHEN** 单张图片或单个视频加载失败
- **THEN** 页面 SHALL 展示该媒体项的失败占位或重试入口
- **AND** 其他媒体和 SKU 文本信息 SHALL 继续可浏览
- **AND** 视频 URL 无效时 SHALL 不阻断图片媒体展示和 SKU 文本信息浏览。

### Requirement: SKU 收藏与分享
SKU 详情页 SHALL 支持 SKU 粒度收藏、取消收藏和微信原生分享。

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
- **AND** 分享标题 SHALL 包含 SKU 名称和品牌名称
- **AND** 分享卡片 SHALL 包含主图、SKU 名称、品牌和参考价格
- **AND** 分享路径 SHALL 携带 `skuId` 和来源参数。

### Requirement: 品牌入口与相关推荐
SKU 详情页 SHALL 支持进入品牌主页、同系列商品和同品牌推荐，使用户可以继续浏览相关瓷砖；SKU 详情页品牌卡 SHALL 使用微信小程序品牌卡片组件承载单品牌展示、Logo fallback、入口提示和点击跳转。

#### Scenario: 品牌入口
- **WHEN** 用户点击品牌卡或底部品牌按钮
- **THEN** 小程序 SHALL 使用 `brandId` 进入对应品牌主页或可用品牌承接页
- **AND** 目标不可用时 SHALL 安全降级到可返回提示或搜索筛选结果。

#### Scenario: SKU 详情页使用品牌卡片组件
- **WHEN** SKU 详情页展示品牌卡
- **THEN** 页面 SHALL 使用微信小程序品牌卡片组件替换重复的内联品牌卡片结构
- **AND** 页面 SHALL 从 SKU 详情数据中提取品牌展示对象、`skuId` 和来源上下文传入组件
- **AND** 组件 SHALL 负责 Logo 缺失/失败、长品牌名、入口不可用和点击防重复等卡片级行为。

#### Scenario: 品牌入口 fallback
- **WHEN** SKU 详情页品牌卡缺少 `brand_entry_path` 但品牌名称可用
- **THEN** 小程序 SHALL fallback 到品牌关键词搜索页或等价品牌承接页
- **AND** 小程序 SHALL 对品牌名称进行 URL 编码
- **AND** 品牌名称不可用或入口不可用时 SHALL 提示“品牌内容暂不可查看”或等价文案并阻止无效跳转。

#### Scenario: 同系列推荐
- **WHEN** SKU 存在同系列其他公开 SKU
- **THEN** 页面 SHALL 展示同系列商品推荐
- **AND** 推荐 SHALL NOT 包含当前 SKU
- **AND** 用户点击推荐卡 SHALL 进入新的 SKU 详情页并重置滚动位置。

### Requirement: SKU 详情页视觉与可用性
SKU 详情页 SHALL 延续微信小程序首页 v6 深色企业轻奢风，并在主流小程序视口内保持可用。

#### Scenario: 深色视觉和大媒体区
- **WHEN** 用户查看 SKU 详情页
- **THEN** 页面 SHALL 使用与小程序首页 v6 一致的深色背景、卡片层、主文字、辅助文字和品牌金语义
- **AND** 顶部媒体区 SHALL 采用大图布局
- **AND** 页面 SHALL NOT 使用电商红主按钮、纯白大背景或购物导向视觉。

#### Scenario: 移动视口可用
- **WHEN** 团队在 320 到 430px 逻辑宽度和常见底部安全区验收页面
- **THEN** 页面 SHALL 无横向滚动、内容重叠、按钮遮挡或关键文字截断
- **AND** 主要点击目标 SHALL 不小于 44x44px 或小程序等效尺寸。

#### Scenario: 底部操作栏
- **WHEN** SKU 详情页正常展示
- **THEN** 底部固定操作栏 SHALL 包含收藏、品牌和分享
- **AND** 分享 SHALL 为主按钮
- **AND** 操作栏 SHALL 避让底部安全区。

### Requirement: SKU 详情页范围控制与安全
SKU 详情页 SHALL 明确不做购物交易能力，并保证富文本、媒体和埋点安全。

#### Scenario: 安全媒体 URL
- **WHEN** 详情响应包含图片、视频或分享图
- **THEN** URL SHALL 来自后端授权、公开安全 URL 或对象存储适配层生成结果
- **AND** 小程序 SHALL NOT 直接使用未授权 object key 拼接对象存储地址
- **AND** 视频媒体 URL SHALL NOT 使用 `tile_videos.file_name` 原始上传文件名作为播放地址
- **AND** 当视频记录包含 `tile_videos.object_key` 时，详情接口 SHALL 基于该对象 key 返回 `/media/{object_key}` 或完整公开安全 URL。

### Requirement: SKU 详情页接口与测试同步
SKU 详情页涉及的 API、数据库、OpenAPI、Orval、文档和测试 SHALL 保持同步。

#### Scenario: 测试覆盖
- **WHEN** SKU 详情页实现完成
- **THEN** 后端测试 SHALL 覆盖公开字段过滤、详情成功、不可公开状态、收藏幂等、推荐排除和安全媒体 URL
- **AND** 小程序或静态测试 SHALL 覆盖页面入口、媒体状态、收藏分享交互、异常状态和范围外能力未出现
- **AND** 后端测试 SHALL 覆盖 `tile_videos.object_key` 与 `tile_videos.file_name` 语义不同的场景，确保视频 `media[].url` 使用对象 key 生成安全媒体 URL。

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

