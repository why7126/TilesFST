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

系统 SHALL 通过后端受控接口读取媒体对象，保护对象存储访问边界，并 SHALL 支持图片缓存、列表缩略图、详情展示图、媒体观测、对象存储直出和视频 Range 请求。商品列表缩略图、品牌图片缩略图、Banner 图片缩略图、图片类品牌证书缩略图、用户头像和图片 `display` 派生图 SHALL 与原图位于同一对象目录或等价可追溯对象路径，并 SHALL 通过文件名差异、规格目录或等价稳定规则区分 `thumbnail`、`display` 与 `original`。业务记录保存非空媒体 object key 前 SHOULD 校验对象存在；用户头像等当前身份展示关键媒体写入非空 key 前 MUST 校验对象存在且可受控读取。

系统 SHALL 生成真实轻量缩略图与详情展示图：对于尺寸大于目标尺寸的支持图片，派生图 SHALL 经过后端图片处理生成，像素宽高 SHALL 小于或等于对应规格约定最大宽高，且 SHALL NOT 只是原图 bytes 的复制品。无法达到目标体积时 SHALL NOT 默认阻断原图上传或业务保存，且 SHALL 记录 warning 或可复核失败原因。

对象存储直出 SHALL 作为受控媒体读取形态之一，仅能由后端媒体服务或对象存储适配层生成。系统 SHALL 明确签名 URL、公开 URL、后端 `/media` 代理 URL 的选择条件、过期策略、缓存策略和 fallback。客户端 SHALL NOT 直连未授权对象存储，响应 SHALL NOT 暴露对象存储密钥、bucket 权限细节或内部 endpoint 白名单。

#### Scenario: 用户头像 key 写入前对象可读

- **GIVEN** 用户资料写入链路接收非空头像 `avatar_object_key`
- **WHEN** 该 key 对应对象不存在、权限异常或无法通过后端对象存储适配层读取
- **THEN** 系统 SHALL 拒绝写入该 key
- **AND** 系统 SHALL 返回统一错误响应
- **AND** 错误响应 SHALL NOT 暴露对象存储 endpoint、bucket、access key、secret key 或底层 SDK 堆栈

#### Scenario: 用户头像受控媒体 URL 可读

- **GIVEN** 用户头像 `avatar_object_key` 已成功保存
- **WHEN** 客户端访问 `/media/{avatar_object_key}` 或等价受控 URL
- **THEN** 后端 SHALL 返回可读图片响应
- **AND** 响应 Content-Type SHALL 与对象内容匹配
- **AND** 客户端 SHALL NOT 直连未授权对象存储

### Requirement: 对象 Key 必须使用标准前缀

系统 MUST 使用 `rules/object-storage.md` 定义的单桶标准前缀生成对象 Key。图片类上传 MUST 使用 `images/`，原始视频 MUST 使用 `videos/`，视频封面 MUST 使用 `videos/covers/`，文件类资源 MUST 使用 `files/`，处理后资源 MUST 使用 `processed/` 或更具体标准前缀。系统 MUST NOT 使用用户原始文件名、本机绝对路径、临时路径、对象存储 raw URL 或不可脱敏业务文本作为对象 Key。`original/` 仅允许作为存量兼容前缀，新上传 MUST NOT 使用。

新上传媒体对象 SHOULD 在业务对象 id 已存在时直接写入业务对象 id 目录；业务对象 id 尚未生成时 MUST 写入对应媒体类型的 `pending` 目录，并在业务对象保存成功后 formalize 到正式目录。正式目录矩阵 MUST 至少覆盖：

| 媒体类型 | 业务对象 id | 正式目录 |
|---|---|---|
| 用户头像 | `user_id` | `images/default/user-avatars/{user_id}/{uuid}.{ext}` |
| 品牌 Logo | `brand_id` | `images/default/brand-logos/{brand_id}/{uuid}.{ext}` |
| Banner 图片 | `banner_id` | `images/default/banners/{banner_id}/{uuid}.{ext}` |
| SKU 图片 | `tile_id` | `images/default/tiles/{tile_id}/{uuid}.{ext}` |
| SKU 视频 | `tile_id` | `videos/default/tiles/{tile_id}/{uuid}.{ext}` |
| 品牌证书图片 | `certificate_id` | `images/default/brand-certificates/{certificate_id}/{uuid}.{ext}` |
| 品牌证书 PDF/文档 | `certificate_id` | `files/default/brand-certificates/{certificate_id}/{uuid}.{ext}` |

新生成的图片派生 key MUST 在原图所在业务对象目录或等价可追溯目录中表达规格与 WebP 格式，例如 `{base}.thumb.webp` 与 `{base}.display.webp`。原图 key MUST 保留上传扩展名和 MIME；派生 key 不得使用用户原始文件名，也不得暴露真实 object key 全量值到用户可见错误、请求日志、Task Trace 或维护任务摘要。

系统 MUST 保留旧数据库引用中的完整 key 读取兼容。客户端、管理端、小程序和公开展示端 MUST 消费后端返回的受控 URL 或 key 字段，不得自行拼接对象存储 endpoint、bucket、业务对象 id 目录或 raw URL。旧对象和过渡目录删除或清理 MUST 作为单独高风险动作确认，不得随新 Key 策略、formalize 或派生图补生成默认执行。

针对存量媒体，系统 MUST 支持受控 dry-run、apply、二次审计和幂等迁移，将可迁移对象从旧资源目录或过渡目录迁移到扁平业务媒体类型目录。apply MUST 要求数据库备份和对象存储 bucket/prefix 备份确认；二次审计 MUST 覆盖数据库引用、对象存在性、受控 URL 可读性、端侧 render/Network 证据和幂等复跑结果，并识别 `avartars` 等错误拼写目录。

#### Scenario: 新上传媒体按业务对象 id 归属

- **GIVEN** 管理端上传媒体时已存在对应业务对象 id
- **WHEN** 上传接口经后端授权、MIME、大小和对象 Key 校验后写入对象存储
- **THEN** object key MUST 使用该业务对象 id 的正式目录
- **AND** 上传响应 MUST 返回 `object_key` 与 `/media/{object_key}` 或等价受控读取 URL
- **AND** 响应 MUST NOT 暴露 raw object URL、bucket、内部 endpoint、access key、secret key 或本机路径。

#### Scenario: pending 媒体保存后正式化

- **GIVEN** 管理端在业务对象 id 尚未生成时上传媒体
- **WHEN** 业务对象创建成功并获得稳定 id
- **THEN** 系统 MUST 将 pending 媒体 formalize 到正式业务对象 id 目录
- **AND** 系统 MUST 同步更新业务表中的媒体引用
- **AND** 图片媒体的原图、`.thumb.webp` 与 `.display.webp` MUST 保持同一业务对象目录或等价可追溯目录
- **AND** 重复 formalize MUST 幂等，不得删除源对象或写入指向缺失对象的业务引用。

#### Scenario: 旧 key 继续可通过受控 URL 读取

- **GIVEN** 历史数据库记录保存了旧目录 object key
- **WHEN** 客户端访问后端返回的 `/media/{object_key}` 或等价受控 URL
- **THEN** 后端 MUST 按保存的完整 key 读取对象
- **AND** 客户端 MUST NOT 根据新目录规则推导旧对象路径
- **AND** 若对象缺失、权限异常或派生图缺失，系统 MUST 返回可诊断错误、稳定 fallback 或维护候选摘要。

#### Scenario: 存量迁移默认 dry-run

- **WHEN** 运维执行存量媒体迁移命令且未显式 apply
- **THEN** 迁移 MUST 只读扫描数据库媒体引用和对象存储状态
- **AND** 输出 MUST 包含待迁移数量、跳过数量、失败分类、目标冲突、对象缺失和风险摘要
- **AND** dry-run MUST NOT 写数据库、复制对象或删除对象
- **AND** 输出 MUST 使用脱敏 key 摘要，不得包含完整 object key、密钥、连接串、Authorization header、Cookie、`.env` 原文或本机绝对路径。

#### Scenario: 存量迁移 apply 后可审计回滚

- **GIVEN** 数据库备份和对象存储 bucket/prefix 备份已确认
- **WHEN** 运维显式执行存量媒体迁移 apply
- **THEN** 系统 MUST 分批复制对象并更新数据库引用
- **AND** apply 后 MUST 支持二次审计 key、object、URL、render/Network、失败分类和幂等复跑结果
- **AND** 回滚说明 MUST 以数据库备份和对象存储快照恢复为主
- **AND** 旧对象删除 MUST 等待单独确认，不得在 apply 中默认执行。

#### Scenario: 错误拼写目录被审计暴露

- **GIVEN** 数据库媒体引用中存在错误拼写目录，例如 `avartars`
- **WHEN** 运维执行对象 key 审计或媒体漂移聚合审计
- **THEN** 审计结果 MUST 将该对象标记为非标准 key
- **AND** 失败原因 MUST 使用枚举化分类
- **AND** 审计输出 MUST 使用脱敏 key 摘要，不得输出完整 object key。

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

媒体类 BUG 修复、返修、回归测试、Sprint 验收或发布前检查 SHALL 使用媒体类 BUG 四联验收模板。模板 SHALL 覆盖原 BUG 场景、`key`、`object`、`URL`、`render` 四个维度，并 SHALL 为每个维度记录 `pass`、`fail`、`n/a` 或 `blocked` 状态、证据和失败/阻塞处理。模板 SHALL 遵守对象存储单桶策略、对象 Key 标准前缀、后端受控媒体读取、上传安全和小程序平台限制。模板 SHALL NOT 记录真实客户数据、真实密钥、Authorization header、Cookie、`.env` 内容、本机绝对路径或未脱敏 MinIO 凭证。涉及历史用户头像 key 数据修复时，模板 SHALL 记录 dry-run、apply 和二次幂等复查摘要。

#### Scenario: 用户头像历史对象修复四联验收

- **WHEN** 团队验收用户头像对象缺失类 BUG
- **THEN** key 维度 SHALL 记录头像 key 前缀、业务字段清理或保留原因
- **AND** object 维度 SHALL 记录对象存在性、MIME、大小或缺失原因
- **AND** URL 维度 SHALL 记录 `/media/{object_key}` 或等价受控 URL 的 HTTP 状态与业务错误码
- **AND** render 维度 SHALL 覆盖个人资料页、侧边栏或用户列表中的头像 fallback 表现

### Requirement: 小程序媒体历史对象四联审计

系统 SHALL 支持小程序媒体历史对象四联审计 helper 或等价受控流程，用于 dry-run 检查历史媒体对象的 key、object、URL 和 render 风险。审计 SHALL 默认只读，不得默认写入数据库或对象存储。审计输出 SHALL 脱敏，使用 key hash、标准前缀、资源类型、计数和失败原因枚举，不得输出真实 object key 全量值、密钥、`.env`、Authorization header、Cookie、本机绝对路径或真实客户数据。

#### Scenario: dry-run 审计覆盖媒体风险

- **WHEN** 团队执行小程序媒体历史对象 dry-run 审计
- **THEN** 审计 SHALL 支持按资源类型抽样或批量检查 SKU 图片、SKU 视频 poster、品牌 Logo、Banner、品牌证书或小程序商品卡片图
- **AND** 输出 SHALL 包含 object 存在性、MIME、大小、缩略图是否存在、缩略图是否明显轻量、URL 是否可能 fallback、失败原因枚举和统计摘要
- **AND** dry-run SHALL NOT 写数据库或对象存储。

#### Scenario: 审计结果分类明确

- **WHEN** 审计完成
- **THEN** 结果 SHALL 将对象分类为已闭环、缺缩略图、缩略图无收益、URL fallback、object 缺失、权限异常或证据不足
- **AND** 对缺缩略图或缩略图无收益的历史对象 SHALL 标记是否需要独立回填或重生成
- **AND** 审计摘要 SHALL NOT 替代小程序受影响页面的 render evidence。

#### Scenario: apply 回填显式受控

- **WHEN** 审计结果需要 apply 回填或重生成
- **THEN** 系统 SHALL 要求显式 apply 参数、MySQL 与对象存储 bucket / prefix 备份确认、幂等验证、成功数量、失败数量、跳过数量和失败原因
- **AND** 重复执行 SHALL 保持幂等
- **AND** 任一失败项 SHALL 记录实际结果、期望结果、影响范围和重试条件。

### Requirement: 对象存储影响必须纳入跨版本升级和回滚
对象存储能力 SHALL 为跨版本升级计划提供媒体对象、bucket、prefix、object key、缩略图和维护任务影响证据。

#### Scenario: 跨版本对象存储影响聚合
- **WHEN** 系统生成跨版本升级计划
- **THEN** 计划 SHALL 聚合中间版本涉及对象存储 provider、bucket、prefix、object key、缩略图、历史媒体维护任务和受控读取策略的影响
- **AND** 写入型维护任务 SHALL 要求 dry-run、备份确认和人工授权。

#### Scenario: 对象存储回滚边界明确
- **WHEN** 升级或维护任务可能写入、复制、删除或重生成对象
- **THEN** 回滚计划 SHALL 记录对象存储备份、只读确认或不可逆风险
- **AND** 缺少对象存储恢复证据 SHALL 使升级计划 blocked 或 requires manual review。

