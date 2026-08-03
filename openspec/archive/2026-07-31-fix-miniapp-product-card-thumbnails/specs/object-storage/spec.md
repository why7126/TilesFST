## MODIFIED Requirements

### Requirement: 媒体对象必须可受控读取

系统 SHALL 通过后端受控接口读取媒体对象，保护对象存储访问边界，并 SHALL 支持图片缓存、列表缩略图、媒体观测和视频 Range 请求。商品列表缩略图 SHALL 与原图位于同一对象目录，并 SHALL 通过文件名差异区分缩略图与原图；历史 `thumbnails/` 前缀 MAY 作为兼容读取或迁移来源，但新生成的商品列表缩略图 SHALL NOT 依赖 `thumbnails/default/tiles/pending/` 作为最终存储位置。

#### Scenario: 通过后端读取媒体对象
- **WHEN** Web、小程序或管理端需要展示已授权媒体对象
- **THEN** 客户端 SHALL 通过后端公开或授权媒体 URL 读取媒体
- **AND** 客户端 SHALL NOT 直连未授权对象存储 endpoint、泄露 MinIO 凭据或绕过后端访问控制。

#### Scenario: 图片响应缓存
- **WHEN** 客户端通过 `/media/{object_key}` 或等价受控 URL 读取图片对象
- **THEN** 后端 SHOULD 返回合理的 `Cache-Control`、`ETag`、`Last-Modified` 或对象版本信息
- **AND** 同一版本图片重复读取 SHOULD 支持客户端或中间层缓存
- **AND** 图片替换或对象版本变化 SHALL 有明确失效策略，避免长期展示旧图。

#### Scenario: 列表缩略图读取
- **WHEN** 小程序商品卡片、搜索结果、首页推荐或品牌详情商品 Tab 读取商品列表图片
- **THEN** 后端 SHOULD 优先返回与原图同目录且文件名差异化的缩略图或等价轻量优化图片 URL
- **AND** 缩略图缺失时 SHALL 安全回退到原图、占位图或可观测的失败状态
- **AND** 缩略图读取 SHALL 遵守单 Bucket + 前缀策略和既有鉴权边界。

#### Scenario: pending 主图缩略图命名
- **GIVEN** 原图对象 key 为 `images/default/tiles/pending/<uuid>.<ext>`
- **WHEN** 系统为商品列表生成或回填缩略图
- **THEN** 缩略图对象 key SHALL 保持在 `images/default/tiles/pending/` 同目录
- **AND** 缩略图文件名 SHALL 与原图文件名有明确差异
- **AND** 系统 SHALL NOT 机械生成 `/media/thumbnails/default/tiles/pending/<uuid>.<ext>` 作为最终列表缩略图 URL。

#### Scenario: 媒体读取观测
- **WHEN** 后端处理媒体读取请求
- **THEN** 系统 SHOULD 记录状态码、耗时、对象是否存在、媒体类型和请求入口中的可用脱敏字段
