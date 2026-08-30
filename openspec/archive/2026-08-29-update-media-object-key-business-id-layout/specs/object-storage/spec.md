## MODIFIED Requirements

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
