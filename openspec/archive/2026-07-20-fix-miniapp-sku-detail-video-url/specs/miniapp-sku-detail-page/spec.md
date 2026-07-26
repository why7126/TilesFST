## MODIFIED Requirements

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
