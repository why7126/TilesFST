---
created_at: '2026-09-08 08:31:48'
updated_at: '2026-09-08 08:31:48'
---

## MODIFIED Requirements

### Requirement: 管理端上传必须写入 MinIO 单桶

系统 MUST 将管理端上传的头像、品牌 Logo、SKU 图片、SKU 视频、品牌证书文件和后续媒体对象写入 MinIO/S3 兼容对象存储单桶。上传链路 MUST 经后端授权、MIME 校验、大小校验、对象 Key 校验和对象存储适配层控制写入；前端、小程序和管理端 MUST NOT 直连未授权对象存储写入。系统 MUST NOT 仅将业务上传对象保存到本地 `UPLOAD_DIR` 后即返回成功。

图片上传大小上限 MUST 由 **effective** 配置 `media.max_image_size_mb` 决定（SQLite `system_settings` 覆盖值 merge 环境变量 `MAX_IMAGE_SIZE_MB` 默认值）；视频上传大小上限 MUST 由 **effective** `media.max_video_size_mb` merge `MAX_VIDEO_SIZE_MB` 决定；文档 / 文件 / 证书类上传大小上限 MUST 由 **effective** `media.max_file_size_mb` 或等价文件类配置 merge 环境变量默认值决定。图片 MIME 白名单 MUST 由 **effective** `media.allowed_image_types` merge `ALLOWED_IMAGE_TYPES` 决定；视频 MIME 白名单 MUST 由 **effective** `media.allowed_video_types` merge `ALLOWED_VIDEO_TYPES` 决定；文档类 MIME 白名单 MUST 与对应业务上传入口显式定义并返回可诊断错误。Effective 值 MUST 在每次上传请求时读取，MUST NOT 仅使用进程启动时的 env snapshot 或不可配置的硬编码大小上限。

超限、MIME 不符或对象存储不可用 MUST 由后端返回统一结构错误响应和明确错误码，MUST NOT 依赖 Nginx 413 作为业务校验手段。代理模式的 Docker / Nginx / 生产代理请求体大小和超时配置 MUST 大于等于后端最大 effective 上传限制；授权直传文件主体不经该代理，控制请求仍经后端。对于 SKU 视频等大文件上传，对象存储写入成功后，上传接口 MUST 在配置的上传超时窗口内返回业务成功响应，避免对象已写入但前端仍判定失败。

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
- **AND** 系统 MUST NOT 要求通过公开 bucket 或未授权前端直连来绕过失败。

授权直传 MUST 由后端适配层发放临时对象授权，文件主体可由浏览器写入COS；传输完成只代表待确认，后端验证与稳定副本就绪后才返回可关联媒体，不能把授权申请成功或COS写入成功等同业务保存成功。上述单次上传超时场景仅约束代理上传；直传控制接口返回可信异步状态。

#### Scenario: 直传完成仍待后端确认

- **WHEN** 浏览器已写入临时对象但尚未校验
- **THEN** 系统 MUST 返回待确认/校验状态且禁止业务绑定。

### Requirement: 媒体对象必须可受控读取

系统 SHALL 通过后端受控接口读取媒体对象，保护对象存储访问边界，并 SHALL 支持图片缓存、列表缩略图、详情展示图、媒体观测、对象存储直出和视频 Range 请求。商品列表缩略图、品牌图片缩略图、Banner 图片缩略图、图片类品牌证书缩略图、用户头像和图片 `display` 派生图 SHALL 与原图位于同一对象目录或等价可追溯对象路径，并 SHALL 通过文件名差异、规格目录或等价稳定规则区分 `thumbnail`、`display` 与 `original`。业务记录保存非空媒体 object key 前 SHOULD 校验对象存在；用户头像等当前身份展示关键媒体写入非空 key 前 MUST 校验对象存在且可受控读取。

系统 SHALL 生成真实轻量缩略图与详情展示图：对于尺寸大于目标尺寸的支持图片，派生图 SHALL 经过后端调度的受控图片处理器生成，像素宽高 SHALL 小于或等于对应规格约定最大宽高，且 SHALL NOT 只是原图 bytes 的复制品。有效派生已生成但无法达到目标体积时 SHALL NOT 默认阻断原图上传或业务保存，且 SHALL 记录 warning 或可复核失败原因；授权直传必要派生缺失或校验失败时 SHALL 阻止该新媒体绑定，原图保留供处理重试。

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

代理上传媒体对象 SHOULD 在业务对象 id 已存在时直接写入业务对象 id 目录；授权直传 MUST 先写受控临时目录，确认后再由服务端形成业务目录的稳定副本；业务对象 id 尚未生成时 MUST 写入对应媒体类型的 `pending` 目录，并在业务对象保存成功后 formalize 到正式目录。正式目录矩阵 MUST 至少覆盖：

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
- **THEN** 可关联 object key MUST 使用该业务对象 id 的正式目录；直传临时对象在确认前 MUST 隔离且不可作为正式引用
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

直传会话临时对象 MUST 使用媒体标准前缀下独立pending/session命名空间与随机标识；清理仅针对本功能新建未引用残留，历史对象删除仍按原单独确认规则。

#### Scenario: 正式副本拒绝客户端覆盖

- **WHEN** 客户端持旧上传授权请求写入正式对象
- **THEN** 存储权限 MUST 拒绝该写入，绑定内容 MUST 与已验证稳定副本一致。
