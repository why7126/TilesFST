# miniapp-sku-detail-page Delta

## MODIFIED Requirements

### Requirement: 图片与视频混合媒体浏览

SKU 详情页 SHALL 支持图片和视频混合轮播，并提供图片全屏预览和视频播放控制。视频播放体验 SHALL 适配生产环境受控媒体读取链路，避免用户点击播放后长时间空白或无反馈。SKU 详情页首屏图片展示 SHALL 优先使用真实轻量缩略图，图片预览 SHALL 保留原图清晰度。

#### Scenario: 详情页首屏图片使用缩略图

- **WHEN** 小程序请求 `GET /api/v1/miniapp/skus/{sku_id}` 且 SKU 存在图片媒体
- **THEN** 图片媒体用于首屏展示的 URL SHALL 优先指向同目录 `.thumb` 缩略图
- **AND** 图片媒体的 `preview_url` SHALL 指向原图或等价高清预览 URL
- **AND** 小程序详情页首屏 `<image>` SHALL 使用展示 URL
- **AND** 用户点击图片预览时 SHALL 使用 `preview_url` 或等价原图 URL
- **AND** 响应 SHALL NOT 暴露原始 object key、对象存储 endpoint、bucket 名称或未授权素材路径。

#### Scenario: 视频封面使用缩略图且播放 URL 不变

- **WHEN** SKU 详情页展示视频媒体项
- **THEN** 视频媒体的 `src` SHALL 使用详情接口返回的安全可播放视频 URL
- **AND** 视频媒体的 `cover_url` SHALL 优先使用主图或首张图片的同目录 `.thumb` 缩略图
- **AND** 当 `cover_url` 缺失或不可用时 SHALL 使用商品主图、首张图片或安全兜底图作为等待态展示
- **AND** 修复 SHALL NOT 将视频播放 URL 替换为图片缩略图 URL。

#### Scenario: 缩略图缺失回退不替代性能验收

- **WHEN** 详情页请求同目录 `.thumb` 缩略图且对象缺失
- **THEN** 后端受控 `/media/{object_key}` MAY 回退原图以避免破图
- **AND** 媒体验收 SHALL 记录该回退风险
- **AND** 性能验收 SHALL 检查缩略图对象大小、像素或 bytes 差异，不能只以 URL 可访问作为通过依据。

### Requirement: SKU 详情页接口与测试同步

SKU 详情页涉及的 API、数据库、OpenAPI、Orval、文档和测试 SHALL 保持同步。

#### Scenario: 详情页缩略图修复测试覆盖

- **WHEN** SKU 详情页媒体缩略图修复完成
- **THEN** 后端测试 SHALL 覆盖图片展示 URL 使用 `.thumb`、预览 URL 保留原图、视频 `cover_url` 使用缩略图且视频 `url` 不变
- **AND** 小程序静态测试 SHALL 覆盖详情页首屏图片绑定展示 URL、图片预览绑定原图 URL、视频 poster 兜底
- **AND** API 文档 SHALL 说明 SKU 详情媒体字段的展示、预览、播放和封面语义
- **AND** 媒体类 BUG 四联验收 SHALL 覆盖 key、object、URL、render 和小程序 evidence。
