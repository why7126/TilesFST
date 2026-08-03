## MODIFIED Requirements

### Requirement: 媒体对象必须可受控读取
系统 SHALL 通过后端受控接口读取媒体对象，保护对象存储访问边界，并 SHALL 支持图片缓存、列表缩略图、媒体观测和视频 Range 请求。商品列表缩略图、品牌图片缩略图和图片类品牌证书缩略图 SHALL 与原图位于同一对象目录或等价可追溯对象路径，并 SHALL 通过文件名差异区分缩略图与原图；历史 `thumbnails/` 前缀 MAY 作为兼容读取或迁移来源，但新生成的列表缩略图 SHALL NOT 依赖 `thumbnails/default/tiles/pending/` 作为最终存储位置。系统 SHALL 生成真实轻量缩略图：对于尺寸大于缩略图目标尺寸的支持图片，缩略图 SHALL 经过后端图片处理生成，像素宽高 SHALL 小于或等于约定最大宽高，且 SHALL NOT 只是原图 bytes 的复制品。

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

#### Scenario: 品牌与证书小图缩略图读取
- **WHEN** 管理端品牌列表、品牌编辑小预览、品牌证书列表、证书卡片、小程序品牌/证书展示或店主 Web 品牌/证书展示读取品牌图片或图片类证书
- **THEN** 后端 SHOULD 优先返回或提供与原图可追溯的真实缩略图 URL
- **AND** 原图预览、证书预览、下载或大图查看 SHALL 继续使用原图或原文件
- **AND** 缩略图缺失、损坏或读取失败时 SHALL 安全回退到原图、占位图或文件类型占位
- **AND** 客户端 SHALL NOT 直连未授权对象存储地址。

#### Scenario: 真实缩略图生成
- **GIVEN** 原图为后端支持的 JPG、PNG 或 WebP 图片且像素尺寸大于缩略图目标尺寸
- **WHEN** 系统生成同目录 `.thumb` 缩略图
- **THEN** 缩略图 SHALL 保持原图比例并限制在约定最大宽高内
- **AND** 缩略图 bytes SHALL NOT 与原图 bytes 完全一致
- **AND** 缩略图文件体积 SHOULD 小于原图文件体积
- **AND** 系统 SHALL 记录或返回可用于测试验证的缩略图处理结果。

#### Scenario: 小图和透明图边界
- **GIVEN** 原图小于或等于缩略图目标尺寸，或原图包含透明通道
- **WHEN** 系统生成同目录 `.thumb` 缩略图
- **THEN** 系统 SHALL NOT 放大原图
- **AND** 透明 PNG/WebP SHALL 按约定保持透明度或使用明确背景策略
- **AND** 小图重编码后若体积异常增大，系统 SHALL 按约定跳过重写、回退或记录告警。

#### Scenario: 历史品牌与证书缩略图审计与重生成
- **GIVEN** 存量品牌图片或图片类品牌证书已存在原图对象
- **WHEN** 运维执行历史缩略图审计 dry-run
- **THEN** 输出 SHALL 包含原图存在、缩略图存在、疑似同 size、疑似同 bytes、需要生成或重生成、跳过、失败原因等摘要
- **AND** dry-run SHALL NOT 写数据库或对象存储
- **WHEN** 运维执行重生成 apply
- **THEN** 系统 SHALL 只生成或重生成需要处理的缩略图对象
- **AND** 重复执行 SHALL 保持幂等，不破坏已合格缩略图
- **AND** 输出 SHALL NOT 泄露密钥、Authorization header、Cookie、`.env` 内容、真实客户数据或本机绝对路径。

#### Scenario: 媒体读取观测
- **WHEN** 后端处理媒体读取请求
- **THEN** 系统 SHOULD 记录状态码、耗时、对象是否存在、媒体类型和请求入口中的可用脱敏字段
- **AND** 缩略图回退到原图或占位时 SHOULD 记录可定位的脱敏失败原因。
