## MODIFIED Requirements

### Requirement: 图片与视频混合媒体浏览

SKU 详情页 SHALL 支持图片和视频混合轮播，并提供图片全屏预览和视频播放控制。视频播放体验 SHALL 适配生产环境受控媒体读取链路，避免用户点击播放后长时间空白或无反馈。

#### Scenario: 视频播放控制

- **WHEN** 用户点击视频媒体
- **THEN** 视频 SHALL 由用户主动播放
- **AND** 页面 SHALL NOT 默认自动播放视频
- **AND** 视频播放期间轮播 SHALL NOT 自动切换
- **AND** 页面隐藏、锁屏或跳转时 SHALL 暂停当前视频
- **AND** 视频媒体的 `src` SHALL 使用详情接口返回的安全可播放 URL
- **AND** 生产验收 SHALL 使用实际反馈 SKU 的视频 URL 完成真机播放验证。

#### Scenario: 视频首帧与封面兜底

- **WHEN** SKU 详情页展示视频媒体项
- **THEN** 页面 SHALL 优先使用视频媒体项的 `cover_url` 作为 `poster`
- **AND** 当 `cover_url` 缺失或不可用时 SHALL 使用商品主图、首张图片或安全兜底图作为等待态展示
- **AND** 页面 SHALL NOT 在视频未起播前长期展示空白或黑屏
- **AND** 页面 SHALL NOT 暴露原始 object key、对象存储 endpoint、bucket 名称或未授权素材路径。

#### Scenario: 生产视频首播验收

- **WHEN** 修复生产视频播放启动慢问题
- **THEN** 验收 SHALL 记录至少一个实际 SKU 的视频文件大小、格式、编码、时长、机型、网络类型和点击播放到首帧耗时
- **AND** 首播等待期间 SHALL 有封面、加载状态或等价可理解反馈
- **AND** 验收 SHALL 附实际 `/media/{object_key}` Range 响应证据或生产等价证据。

#### Scenario: 单项媒体失败

- **WHEN** 单张图片或单个视频加载失败
- **THEN** 页面 SHALL 展示该媒体项的失败占位或重试入口
- **AND** 其他媒体和 SKU 文本信息 SHALL 继续可浏览
- **AND** 视频 URL 无效时 SHALL 不阻断图片媒体展示和 SKU 文本信息浏览
- **AND** 若生产域名、`/api/v1/health` 或 `/media/{object_key}` 返回 Nginx 502，验收记录 MUST 将该失败归入生产入口或反代链路，而不是仅归因于小程序播放器。

### Requirement: SKU 详情页接口与测试同步

SKU 详情页涉及的 API、数据库、OpenAPI、Orval、文档和测试 SHALL 保持同步。

#### Scenario: 测试覆盖

- **WHEN** SKU 详情页实现完成或生产视频播放缺陷修复完成
- **THEN** 后端测试 SHALL 覆盖公开字段过滤、详情成功、不可公开状态、收藏幂等、推荐排除和安全媒体 URL
- **AND** 小程序或静态测试 SHALL 覆盖页面入口、媒体状态、收藏分享交互、异常状态和范围外能力未出现
- **AND** 后端测试 SHALL 覆盖 `tile_videos.object_key` 与 `tile_videos.file_name` 语义不同的场景，确保视频 `media[].url` 使用对象 key 生成安全媒体 URL
- **AND** 后端测试 SHALL 覆盖视频 `/media/{object_key}` Range/206 响应
- **AND** 小程序测试 SHALL 覆盖视频封面或兜底 poster 展示
- **AND** 生产修复验收 SHALL 附实际 SKU 接口、实际 `/media/{object_key}` 与微信真机播放证据。
