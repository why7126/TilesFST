# 对象存储规范

## Purpose
定义对象存储单桶策略、管理端上传写入、媒体受控读取和对象 Key 前缀规则，确保图片、视频与后续媒体资源统一经后端授权写入 MinIO。
## Requirements
### Requirement: 管理端上传必须写入 MinIO 单桶

系统 MUST 将管理端上传的头像、品牌 Logo、SKU 图片、SKU 视频、品牌证书文件和后续媒体对象写入 MinIO/S3 兼容对象存储单桶。上传链路 MUST 经后端授权、MIME 校验、大小校验、对象 Key 校验和对象存储适配层写入；前端、小程序和管理端 MUST NOT 直连未授权对象存储写入。系统 MUST NOT 仅将业务上传对象保存到本地 `UPLOAD_DIR` 后即返回成功。

图片上传大小上限 MUST 由 **effective** 配置 `media.max_image_size_mb` 决定（SQLite `system_settings` 覆盖值 merge 环境变量 `MAX_IMAGE_SIZE_MB` 默认值）；视频上传大小上限 MUST 由 **effective** `media.max_video_size_mb` merge `MAX_VIDEO_SIZE_MB` 决定；文档 / 文件 / 证书类上传大小上限 MUST 由 **effective** `media.max_file_size_mb` 或等价文件类配置 merge 环境变量默认值决定。图片 MIME 白名单 MUST 由 **effective** `media.allowed_image_types` merge `ALLOWED_IMAGE_TYPES` 决定；视频 MIME 白名单 MUST 由 **effective** `media.allowed_video_types` merge `ALLOWED_VIDEO_TYPES` 决定；文档类 MIME 白名单 MUST 与对应业务上传入口显式定义并返回可诊断错误。Effective 值 MUST 在每次上传请求时读取，MUST NOT 仅使用进程启动时的 env snapshot 或不可配置的硬编码大小上限。

超限、MIME 不符或对象存储不可用 MUST 由后端返回统一结构错误响应和明确错误码，MUST NOT 依赖 Nginx 413 作为业务校验手段。Docker / Nginx / 生产代理请求体大小和超时配置 MUST 大于等于后端最大 effective 上传限制。对于 SKU 视频等大文件上传，对象存储写入成功后，上传接口 MUST 在配置的上传超时窗口内返回业务成功响应，避免对象已写入但前端仍判定失败。

#### Scenario: 视频上传受 effective 大小与 MIME 约束

- **GIVEN** 系统设置或环境变量允许 MP4 且视频大小上限不低于 23MB
- **WHEN** 客户端经授权上传接口提交 23MB 合法 MP4
- **THEN** 上传 MUST 成功并写入对象存储
- **AND** 上传响应 MUST 返回 `object_key` 与 `/media/{object_key}` 或等价受控读取 URL。

#### Scenario: 大视频上传响应不因反代默认超时失败

- **GIVEN** Docker Web Nginx 和生产外层反代已配置上传专用超时
- **WHEN** `admin` 上传合法视频且对象已成功写入 S3 兼容对象存储
- **THEN** 上传接口 MUST 在配置的上传超时窗口内返回 200 与 `object_key`
- **AND** 响应 MUST 包含 `/media/{object_key}` 或等价受控读取 URL
- **AND** MUST NOT 在对象已写入后让前端仍视为上传失败。

#### Scenario: 对象写入成功后可追踪孤儿对象风险

- **WHEN** 浏览器上传请求最终失败但对象存储中已出现对应 `videos/...` 对象
- **THEN** 实施或验收记录 MUST 标注该对象可能为孤儿对象
- **AND** 团队 MUST 记录对象 key、上传时间、请求状态码和后续清理或关联策略
- **AND** 系统 MUST NOT 要求通过公开 bucket 或前端直连来绕过失败。

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

### Requirement: 对象 Key 必须使用标准前缀

系统 MUST 使用 `rules/object-storage.md` 定义的单桶标准前缀生成对象 Key。图片类上传 MUST 使用 `images/`，原始视频 MUST 使用 `videos/`，视频封面 MUST 使用 `videos/covers/`，文件类资源 MUST 使用 `files/`，处理后资源 MUST 使用 `processed/` 或更具体标准前缀。系统 MUST NOT 使用用户原始文件名作为对象 Key。`original/` 仅允许作为存量兼容前缀，新上传 MUST NOT 使用。**Banner 运营图** MUST 使用 `images/default/banners/{uuid}.{ext}`（当 `update-object-storage-key-layout` 已生效时 MUST 使用 `images/` 语义前缀；未生效前实现 MUST 与 `build_upload_object_key()` 当前项目约定一致并在 apply 时对齐）。SKU 图片在新建前 MAY 使用 `images/default/tiles/pending/{uuid}.{ext}` 作为暂存 key；一旦绑定到 SKU 或进入公开展示，系统 MUST 使用可追溯到 SKU 的正式商品图片 key。

#### Scenario: 图片对象 Key 生成

- **WHEN** 用户上传头像、品牌 Logo 或 SKU 图片
- **THEN** 对象 Key MUST 使用 `images/` 前缀
- **AND** 对象 Key MUST 包含租户或默认命名空间、资源类型和随机文件名
- **AND** 文件扩展名 MUST 来自后端 MIME 白名单映射
- **AND** 新上传 MUST NOT 使用 `original/` 前缀

#### Scenario: SKU 图片从 pending 正式化

- **GIVEN** SKU 图片对象 key 位于 `images/default/tiles/pending/`
- **WHEN** 后端将该图片绑定到 SKU 或迁移存量公开主图
- **THEN** 目标对象 key MUST 位于 `images/default/tiles/{tile_id}/` 或等价 SKU 正式商品图片目录
- **AND** 目标 key MUST 由后端生成，不得由前端提交
- **AND** 系统 MUST NOT 使用用户原始文件名作为目标 key
- **AND** 对象复制、缩略图复制或生成、数据库引用更新必须通过后端受控逻辑完成。

#### Scenario: Banner 对象 Key 生成

- **WHEN** 用户上传 Banner 运营图
- **THEN** 对象 Key MUST 匹配 `images/default/banners/{uuid}.{ext}`（或与当期 `build_upload_object_key('images', 'banners', ...)` 等价形态）
- **AND** MUST NOT 使用用户原始文件名

#### Scenario: 视频对象 Key 生成

- **WHEN** 用户上传 SKU 视频
- **THEN** 对象 Key MUST 使用 `videos/` 前缀
- **AND** 文件扩展名 MUST 来自后端 MIME 白名单映射

#### Scenario: 不新增业务 Bucket

- **WHEN** 上传头像、品牌 Logo、SKU 图片、SKU 视频或 Banner 运营图
- **THEN** 系统 MUST 使用同一个对象存储 bucket
- **AND** MUST NOT 创建额外业务 Bucket，除非后续 OpenSpec Change 明确要求

### Requirement: 生产 MinIO 必须持久化并保持单桶策略

生产 Docker Compose MUST 继续使用 MinIO 存储媒体对象，MUST 为 MinIO 配置持久化 volume，MUST 通过 `minio-init` 或等价初始化流程创建单桶 `MINIO_BUCKET`，并 MUST 将桶权限设置为最小权限。生产环境 `MINIO_ACCESS_KEY` 与 `MINIO_SECRET_KEY` MUST 使用非默认值。生产环境上传、媒体 URL、`object_key` 前缀和受控读取规则 MUST 与既有 object-storage capability 保持兼容。

#### Scenario: 生产媒体上传和读取可用

- **GIVEN** 生产 backend 已连接外部 MySQL 和 MinIO
- **WHEN** `admin` 完成一次图片或视频上传
- **THEN** 对象 MUST 写入 `MINIO_BUCKET`
- **AND** 上传响应中的 `/media/{object_key}` 或等价 URL MUST 可读取该对象
- **AND** 重启 backend、web、minio 后对象 MUST 仍可访问
- **AND** 小程序视频播放所需的实际 `/media/{object_key}` MUST 返回可播放视频 Content-Type，而不是 Nginx 502 或 SPA HTML。

### Requirement: 外部 MinIO 生产部署必须保持单桶和受控读取策略

当生产环境使用客户已提供的外部 MinIO、自建 S3 兼容服务或云上对象存储（如腾讯云 COS、火山云 TOS）时，系统 MUST 仍使用单桶 `OBJECT_STORAGE_BUCKET` 与既有对象 Key 前缀策略。外部 bucket MUST 由运维提前创建，并设置最小权限；backend MUST 通过授权凭据读写对象，Web MUST 继续通过 backend `/media/{object_key}` 反代受控读取，不得要求前端直连对象存储写入。

#### Scenario: 外部对象存储上传和读取可用

- **GIVEN** backend 已通过对象存储 endpoint 连接外部 MinIO、COS、TOS 或其他 S3 兼容服务
- **AND** 配置的 bucket 已存在且凭据具备最小读写权限
- **WHEN** `admin` 完成一次图片上传
- **THEN** 对象 MUST 写入配置的外部 bucket
- **AND** 上传响应中的 `/media/{object_key}` MUST 可通过 backend 读取

#### Scenario: 前端不暴露云存储连接细节

- **GIVEN** 系统使用云上对象存储承载媒体
- **WHEN** 管理端、店主端或小程序展示上传后的媒体
- **THEN** 客户端 MUST 使用后端返回的受控媒体 URL
- **AND** 客户端 MUST NOT 依赖云厂商 endpoint、bucket 名称、access key、secret key 或 raw object URL

### Requirement: 对象存储配置必须支持云上 S3 兼容服务

系统 MUST 支持通过后端对象存储适配层连接 MinIO、自建 S3 兼容服务、腾讯云 COS、火山云 TOS 等云上对象存储。应用配置 MUST 统一使用 `OBJECT_STORAGE_*` 表达 provider、endpoint、access key、secret key、bucket、secure/TLS、region、path-style/virtual-host 风格、bucket 自动创建策略和对象前缀。后端应用 MUST NOT 同时暴露重复的 `MINIO_*` 应用配置；MinIO 容器自身所需的 `MINIO_ROOT_USER` / `MINIO_ROOT_PASSWORD` 不属于后端应用配置。配置摘要不得在日志、接口响应、文档示例或前端页面中暴露 secret key。

#### Scenario: 腾讯云 COS 使用 S3 兼容配置上传

- **GIVEN** 生产环境已配置腾讯云 COS 的 S3 兼容 endpoint、region、bucket、TLS 和最小权限凭据
- **AND** `OBJECT_STORAGE_AUTO_CREATE_BUCKET=false`
- **WHEN** 管理员通过后端授权上传接口上传品牌 Logo
- **THEN** 对象 MUST 写入配置的 COS bucket
- **AND** 上传响应 MUST 继续返回 `/media/{object_key}` 形式的受控读取 URL
- **AND** 响应 MUST NOT 暴露 COS secret key、bucket 权限细节或 raw signed URL

#### Scenario: 火山云 TOS 使用 S3 兼容配置读取

- **GIVEN** 生产环境已配置火山云 TOS 的 S3 兼容 endpoint、region、bucket、TLS 和最小权限凭据
- **AND** bucket 中存在已上传对象
- **WHEN** 客户端访问 `/media/{object_key}`
- **THEN** 后端 MUST 从 TOS 读取对象并返回媒体内容
- **AND** 前端 MUST NOT 直连 TOS 写入或读取未授权对象

#### Scenario: 云上对象存储不自动创建 bucket

- **GIVEN** provider 配置为云上 S3 兼容对象存储
- **AND** `OBJECT_STORAGE_AUTO_CREATE_BUCKET=false`
- **WHEN** bucket 不存在、region 不匹配或凭据无权访问 bucket
- **THEN** 上传 MUST 返回对象存储不可用错误
- **AND** 系统 MUST NOT 尝试在云上隐式创建业务 bucket
- **AND** 错误响应 MUST NOT 暴露底层凭据、内部 endpoint 白名单或完整 SDK 堆栈

### Requirement: 媒体类 BUG 必须使用四联验收模板

媒体类 BUG 修复、返修、回归测试、Sprint 验收或发布前检查 SHALL 使用媒体类 BUG 四联验收模板。模板 SHALL 覆盖原 BUG 场景、`key`、`object`、`URL`、`render` 四个维度，并 SHALL 为每个维度记录 `pass`、`fail`、`n/a` 或 `blocked` 状态、证据和失败/阻塞处理。模板 SHALL 遵守对象存储单桶策略、对象 Key 标准前缀、后端受控媒体读取、上传安全和小程序平台限制。模板 SHALL NOT 记录真实客户数据、真实密钥、Authorization header、Cookie、`.env` 内容、本机绝对路径或未脱敏 MinIO 凭证。

#### Scenario: 记录原 BUG 场景

- **WHEN** 团队使用四联模板验收媒体类 BUG
- **THEN** 验收记录 SHALL 包含 BUG 编号、标题、严重等级、影响范围、复现入口、受影响端和环境
- **AND** 验收记录 SHALL 包含修复前实际结果和修复后期望结果
- **AND** 涉及特定媒体资源时 SHALL 记录媒体类型、业务资源或等价脱敏标识。

#### Scenario: key 维度验收

- **WHEN** 团队验收媒体类 BUG 的 key 维度
- **THEN** 验收记录 SHALL 确认业务记录中的媒体 key 稳定、可追溯，并符合单 Bucket 标准前缀策略
- **AND** 验收记录 SHALL 禁止用户原始文件名、本机绝对路径、临时路径或未脱敏内部路径作为对象存储 key
- **AND** 若修复涉及历史 key 兼容或迁移，验收记录 SHALL 包含旧 key、新 key 和兼容结果。

#### Scenario: object 维度验收

- **WHEN** 团队验收媒体类 BUG 的 object 维度
- **THEN** 验收记录 SHALL 确认对象存储中真实 object 存在，并与业务记录 key 对应
- **AND** 验收记录 SHALL 覆盖 MIME Type、文件大小、扩展名、权限边界和对象可读性
- **AND** object 验收失败时 SHALL 记录对象不存在、大小为 0、类型不匹配、权限错误或存储环境不可用等失败原因。

#### Scenario: URL 维度验收

- **WHEN** 团队验收媒体类 BUG 的 URL 维度
- **THEN** 验收记录 SHALL 区分相对 URL、公开 URL、签名 URL、代理 URL 或静态资源 URL
- **AND** 验收记录 SHALL 记录页面或接口入口、HTTP 状态、业务错误码和用户可见表现
- **AND** 客户端 SHALL 继续使用后端鉴权、代理或签名 URL 策略读取媒体，SHALL NOT 直连未授权对象存储。

#### Scenario: render 维度验收

- **WHEN** 团队验收媒体类 BUG 的 render 维度
- **THEN** 验收记录 SHALL 覆盖受影响端的媒体展示、占位、失败态和用户可见行为
- **AND** Web 管理端 SHOULD 覆盖上传后预览、列表缩略展示、详情或编辑弹窗展示
- **AND** 店主 Web SHOULD 覆盖公开页面、商品卡片、详情页或媒体预览入口
- **AND** 微信小程序 SHALL 覆盖合法域名、图片/视频组件限制、DevTools/真机/体验版 evidence 或明确的不可用原因
- **AND** 小程序端 SHALL NOT 依赖 Web 浏览器专属 API。

#### Scenario: 不适用、失败和阻塞处理

- **WHEN** 某端、某维度或某 evidence 对当前媒体 BUG 不适用
- **THEN** 验收记录 SHALL 标记 `n/a` 并说明不适用原因和影响判断
- **WHEN** 某维度验收失败
- **THEN** 验收记录 SHALL 标记 `fail`，并包含实际结果、期望结果、复现步骤、影响范围和排查线索
- **WHEN** 验收被环境、数据、域名、MinIO 或小程序体验版阻塞
- **THEN** 验收记录 SHALL 标记 `blocked`，并记录阻塞原因、缺失资源、负责人或下一步补证方式。

#### Scenario: 媒体上传链路横切验收

- **WHEN** 媒体类 BUG 涉及上传、编辑、列表回显、历史对象、缩略图、回填或审计脚本
- **THEN** 四联模板 SHALL 要求记录上传状态机 `idle -> uploading -> done/failed` 或等价状态证据
- **AND** 涉及 Web 管理端上传/编辑/列表刷新时 SHALL 记录同会话即时回显 evidence
- **AND** 涉及上传大小、Nginx 或 Docker Web 边界时 SHALL 通过 `http://localhost:3000` 或等价 Web 入口验证边界文件，或记录 `N/A` 原因
- **AND** 涉及历史对象、缩略图、回填或审计脚本时 SHALL 记录 dry-run/apply/统计摘要，且输出 SHALL NOT 泄露敏感信息。

