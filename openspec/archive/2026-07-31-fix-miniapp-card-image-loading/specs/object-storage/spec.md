## MODIFIED Requirements

### Requirement: 媒体对象必须可受控读取
系统 SHALL 通过后端受控接口读取媒体对象，保护对象存储访问边界，并 SHALL 支持图片缓存、列表缩略图、媒体观测和视频 Range 请求。

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
- **THEN** 后端 SHOULD 优先返回 `thumbnails/` 前缀下的缩略图或等价轻量优化图片
- **AND** 缩略图缺失时 SHALL 安全回退到原图、占位图或可观测的失败状态
- **AND** 缩略图读取 SHALL 遵守单 Bucket + 前缀策略和既有鉴权边界。

#### Scenario: 媒体读取观测
- **WHEN** 后端处理媒体读取请求
- **THEN** 系统 SHOULD 记录状态码、耗时、对象是否存在、媒体类型和请求入口中的可用脱敏字段
- **AND** 系统 SHALL NOT 记录 Authorization header、Cookie、真实客户敏感信息或对象内容
- **AND** 媒体慢请求和对象不存在 SHOULD 能被用于定位小程序图片加载异常。

#### Scenario: 视频 Range 请求不退化
- **WHEN** 客户端请求视频对象并携带 Range header
- **THEN** 后端 SHALL 继续返回符合 Range 语义的响应
- **AND** 本次图片缓存或缩略图策略 SHALL NOT 破坏已有视频播放、拖动和分段加载能力。
