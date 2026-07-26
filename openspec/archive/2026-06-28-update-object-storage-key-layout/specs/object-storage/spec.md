## MODIFIED Requirements

### Requirement: 对象 Key 必须使用标准前缀

系统 MUST 使用 `rules/object-storage.md` 定义的语义前缀生成对象 Key。原始图片 MUST 使用 `images/`；原始视频 MUST 使用 `videos/`；通用原始文件 MUST 使用 `files/`（规范预留）；原始音频 MUST 使用 `audios/`（规范预留）；视频封面 MUST 使用 `videos/covers/`；处理后资源 MUST 使用 `processed/` 或更具体标准前缀。`original/` MUST 标记为 **deprecated**，新上传对象 MUST NOT 使用 `original/` 前缀。系统 MUST NOT 使用用户原始文件名作为对象 Key。

Object Key 生成形态 MUST 为：

```text
{prefix}/{tenant}/{resource_type}/{uuid}.{ext}
```

其中 `{tenant}` 默认 MUST 为 `default`；`{uuid}` MUST 为 UUID v4；`{ext}` MUST 来自后端 MIME 白名单映射。系统 MUST NOT 在 Key 中包含 `{YYYY}/{MM}` 日期目录片段。

`resource_type` MUST 使用小写领域路径（可含 `/`），且 MUST NOT 以 `/` 开头或结尾。标准映射 MUST 为：

| 业务场景 | prefix | resource_type |
|---|---|---|
| 用户头像 | `images` | `user/avatars` |
| 品牌 Logo | `images` | `brands/logos` |
| SKU 图片（有关联 tile_id） | `images` | `tiles/{tile_id}` |
| SKU 图片（新建暂存） | `images` | `tiles/pending` |
| SKU 视频 | `videos` | `tiles/{tile_id}` 或 `tiles/pending` |

代码生成 Key 时 SHOULD 优先读取 `settings.minio_prefix_*`（如 `MINIO_PREFIX_IMAGES`、`MINIO_PREFIX_VIDEOS`），MUST NOT 硬编码已废弃的 `original/` 作为新上传前缀。

存量 `object_key` MUST 通过一次性迁移脚本（支持 `--dry-run` 与 `--apply`）将 SQLite 中 `users.avatar_object_key`、`brands.logo_object_key`、`tile_images.object_key`、`tile_videos.object_key` 与 MinIO 对象同步至新 Key 规则；迁移 MUST NOT 删除仍被数据库引用但 MinIO 缺失的对象。

#### Scenario: 图片对象 Key 生成

- **WHEN** 用户上传头像、品牌 Logo 或 SKU 图片
- **THEN** 对象 Key MUST 使用 `images/` 前缀
- **AND** 对象 Key MUST 匹配 `{prefix}/default/{resource_type}/{uuid}.{ext}` 形态
- **AND** 对象 Key MUST NOT 包含 `{YYYY}/{MM}` 日期目录
- **AND** 对象 Key MUST NOT 使用 `original/` 前缀
- **AND** 文件扩展名 MUST 来自后端 MIME 白名单映射

#### Scenario: 头像 Key 领域路径

- **WHEN** 用户经 `POST /api/v1/admin/uploads` 上传头像
- **THEN** 生成的 object_key MUST 匹配 `images/default/user/avatars/{uuid}.{ext}`

#### Scenario: 品牌 Logo Key 领域路径

- **WHEN** 用户经 `POST /api/v1/admin/uploads/brand-logos` 上传 Logo
- **THEN** 生成的 object_key MUST 匹配 `images/default/brands/logos/{uuid}.{ext}`

#### Scenario: SKU 图片 Key 领域路径

- **WHEN** 用户经 `POST /api/v1/admin/uploads/tile-images` 上传 SKU 图片
- **THEN** 有 `tile_id` 时 object_key MUST 匹配 `images/default/tiles/{tile_id}/{uuid}.{ext}`
- **AND** 无 `tile_id` 时 object_key MUST 匹配 `images/default/tiles/pending/{uuid}.{ext}`

#### Scenario: 视频对象 Key 生成

- **WHEN** 用户上传 SKU 视频
- **THEN** 对象 Key MUST 使用 `videos/` 前缀
- **AND** 对象 Key MUST NOT 包含 `{YYYY}/{MM}` 日期目录
- **AND** 文件扩展名 MUST 来自后端 MIME 白名单映射

#### Scenario: 不新增业务 Bucket

- **WHEN** 上传头像、品牌 Logo、SKU 图片或 SKU 视频
- **THEN** 系统 MUST 使用同一个 `MINIO_BUCKET`
- **AND** MUST NOT 创建 `tile-images`、`tile-videos`、`tile-documents` 等额外业务 Bucket，除非后续 OpenSpec Change 明确要求

#### Scenario: 存量 object_key 迁移

- **GIVEN** SQLite 中存在 `original/` 前缀或含 `{YYYY}/{MM}` 的旧 object_key
- **WHEN** 运维执行迁移脚本 `--dry-run`
- **THEN** 脚本 MUST 列出待迁移条目数与旧 Key → 新 Key 映射示例
- **WHEN** 运维执行 `--apply`
- **THEN** 数据库四处 object_key 引用 MUST 与 MinIO 实际对象一致
- **AND** 管理端品牌 Logo、用户头像、SKU 图/视频预览 MUST 可访问（无 404）
