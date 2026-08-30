---
purpose: 对象存储使用规范
content: 规定 MinIO/S3兼容对象存储/腾讯 COS 桶、对象Key、目录前缀、权限、生命周期与AI更新要求
source: 人工编写 + AI辅助生成
update_method: 对象存储策略变化时由技术负责人确认后更新
created_at: 2026-06-13 00:00:00
updated_at: 2026-08-29 22:18:26
note: V5 推荐一个项目一个 Bucket，桶内使用目录前缀区分业务资源；支持 MinIO、S3 兼容云对象存储与腾讯 COS
---

# 对象存储规范

## 1. 总原则

本项目使用 MinIO、S3 兼容对象存储或腾讯云 COS 作为媒体对象存储。V5 采用：

```text
一个项目一个 Bucket
桶内按对象前缀区分资源类型
```

默认：

```text
OBJECT_STORAGE_BUCKET=tilesfst
```

不推荐按资源拆成多个桶，例如 `tile-original`、`tile-thumbnail`、`tile-video`。

后端应用统一使用 `OBJECT_STORAGE_*` 环境变量。当 `OBJECT_STORAGE_PROVIDER=tencent-cos` 时，后端 MUST 使用腾讯云 `qcloud_cos` 官方 SDK；当 provider 为 `minio`、`self-hosted-minio`、`s3-compatible`、`volcengine-tos` 等值时，后端使用 S3 兼容适配层。云上对象存储由运维提前创建 bucket、配置 region、TLS、访问风格和最小权限。

## 2. 标准对象前缀

```text
images/                图片类上传（头像、Logo、SKU 图、Banner 等）
videos/                原始视频
files/                 文档类（预留）
audios/                音频类（预留）
thumbnails/            图片缩略图
processed/             处理后的图片或文件
tmp/                   临时文件
imports/               批量导入文件
exports/               导出文件
videos/covers/         视频封面
videos/transcoded/     转码后视频
original/              Deprecated — 仅存量对象；新上传 MUST NOT 使用
```

## 2.1 Object Key 形态

新上传对象 Key MUST 符合：

```text
{prefix}/{tenant}/{business_media_type}/{business_object_id}/{uuid}.{ext}
```

示例：

```text
images/default/user-avatars/{user_id}/<uuid>.jpg
images/default/brand-logos/{brand_id}/<uuid>.webp
images/default/banners/{banner_id}/<uuid>.webp
images/default/tiles/{tile_id}/<uuid>.jpg
videos/default/tiles/{tile_id}/<uuid>.mp4
images/default/brand-certificates/{certificate_id}/<uuid>.webp
files/default/brand-certificates/{certificate_id}/<uuid>.pdf
```

MUST NOT 在新 Key 中插入 `{YYYY}/{MM}` 日期分片。MUST NOT 把用户原始文件名、本机路径、raw URL、未脱敏业务文本或对象存储 endpoint/bucket 拼入 key。业务对象尚未创建、没有稳定 id 时，上传入口 MAY 暂存到 `{prefix}/{tenant}/{business_media_type}/pending/{uuid}.{ext}`；业务保存后必须通过后端受控 formalize 或维护任务复制到正式业务 id 目录并同步数据库引用。存量 `original/.../{YYYY}/{MM}/...`、历史语义目录和已短暂生成的过渡目录继续通过受控读取与迁移任务兼容，但不得作为新写入最终目录。

标准目录矩阵：

| 媒体对象 | 正式对象 Key 目录 | 创建前暂存目录 |
|---|---|---|
| 用户头像 | `images/default/user-avatars/{user_id}/` | 不适用，当前用户 id 已存在 |
| 品牌 Logo | `images/default/brand-logos/{brand_id}/` | `images/default/brand-logos/pending/` |
| Banner 图片 | `images/default/banners/{banner_id}/` | `images/default/banners/pending/` |
| SKU 图片 | `images/default/tiles/{tile_id}/` | `images/default/tiles/pending/` |
| SKU 视频 | `videos/default/tiles/{tile_id}/` | `videos/default/tiles/pending/` |
| 品牌证书图片 | `images/default/brand-certificates/{certificate_id}/` | `images/default/brand-certificates/pending/` |
| 品牌证书文件 | `files/default/brand-certificates/{certificate_id}/` | `files/default/brand-certificates/pending/` |

SKU 图片新建前 MAY 使用 `images/default/tiles/pending/<uuid>.<ext>` 作为暂存对象，历史 `images/default/tiles/pending/images/<uuid>.<ext>` 和 `images/default/tiles/pending/<uuid>.<ext>` 继续作为 pending 兼容来源。图片一旦绑定到 SKU、保存为 SKU 图片或进入公开商品响应，后端 MUST 将原图与同目录缩略图正式化到 `images/default/tiles/{tile_id}/`，并同步数据库引用。发布流程 MUST 兜底阻止公开主图继续引用 `images/default/tiles/pending/`。历史公开 SKU pending 主图迁移使用 `scripts/migrate-pending-tile-images.py` 或 `python -m app.modules.media.maintenance formalize-pending-tile-images`，默认 dry-run，`--apply --confirm-backup` 才可写对象存储和数据库。

图片原图 key MUST 保留上传格式扩展名，图片派生 key MUST 使用同目录 `.thumb.webp` / `.display.webp`，且对象 Content-Type 为 `image/webp`。JPEG/JPG、PNG、WebP 首期生成 WebP 派生图；SVG/PDF 跳过；GIF、HEIC、TIFF、BMP 首期不转码，按上传入口允许类型拒绝或在维护任务中记录跳过/失败原因。历史 `.thumb.jpg`、`.thumb.png`、`.display.jpg`、`.display.png` 等 key 仅作为读取 fallback 或迁移来源，新生成对象不得继续使用。

品牌证书按媒体类型分流：JPG、PNG、WebP 证书图片 MUST 使用 `images/default/brand-certificates/{certificate_id}/` 或 pending 等价标准图片前缀；PDF 或其他文档类证书 MUST 使用 `files/default/brand-certificates/{certificate_id}/` 或 pending 等价文件前缀。证书图片缩略图和详情展示图 MUST 与原图保持同一图片资源归属，优先使用同目录 `.thumb.webp` / `.display.webp` key。历史 `files/default/brand-certificates/*.{jpg,jpeg,png,webp}` 图片 key 通过 `python -m app.modules.media.maintenance migrate-certificate-image-keys` dry-run/apply 迁移；所有历史媒体业务 id 目录迁移通过 `python -m app.modules.media.maintenance migrate-business-id-media-keys` 执行。PDF 不得迁入 `images/`，也不得返回图片 `thumbnail_url` 或 `display_url`。

生产对象存储维护任务 MUST 默认 dry-run，并优先通过 `python -m app.modules.media.maintenance <task>` 在后端镜像或生产等价环境执行。只读审计任务 MUST 拒绝 apply；写入对象存储或数据库的任务 MUST 同时要求 `--apply --confirm-backup`，确认 MySQL 与对象存储 bucket/prefix 已备份。维护任务输出 MUST 使用 object key hash、标准前缀、统计摘要、幂等状态和失败原因枚举，不得输出 access key、secret key、数据库连接串、Authorization header、Cookie、真实 `.env` 内容、本机绝对路径或未脱敏 object key。

## 3. 媒体类 BUG 对象存储验收

媒体类 BUG 的修复验收 MUST 引用 `docs/standards/media-bug-four-point-acceptance-template.md`，并在 `key`、`object`、`URL`、`render` 四个维度中至少覆盖以下对象存储事实：

- `key`：业务记录中的 `object_key` 或等价脱敏标识符合单 Bucket、标准前缀和 `{prefix}/{tenant}/{resource_type}/{uuid}.{ext}` 形态；不得记录用户原始文件名、本机绝对路径、临时路径或未脱敏内部路径作为通过证据。
- `object`：对象存储中真实 object 存在，且 MIME Type、文件大小、扩展名、权限边界、缩略图或封面关系与业务记录一致；对象不存在、0 字节、类型不匹配、权限错误或存储环境不可用 MUST 标记 `fail` 或 `blocked`。
- `URL`：端侧访问 MUST 通过后端鉴权、代理或签名 URL 策略读取媒体，继续禁止直连未授权对象存储；验收记录必须区分相对 URL、公开 URL、签名 URL、代理 URL 或静态资源 URL，并记录 HTTP 状态、业务错误码和用户可见表现。
- `render`：对象存储验收不能替代端侧验收；Web 管理端、店主 Web 或小程序受影响时，必须记录对应页面/组件的展示、占位、失败态、小程序合法域名或设备 evidence。

涉及历史对象、缩略图、回填或审计脚本时，验收记录 MUST 包含 dry-run、apply、幂等性或统计摘要，并遵守敏感信息脱敏要求。涉及上传大小、Nginx 或 Docker Web 边界时，MUST 经 `http://localhost:3000` 或等价 Web 入口验证边界文件，或记录明确的 `n/a` 原因。

小程序历史媒体对象审计 MUST 按 `docs/knowledge-base/best-practices/miniapp-media-four-part-acceptance-practice.md` 输出四联分类与脱敏摘要。审计 helper 默认 dry-run，只读输出 `missing_key`、`object_missing`、`thumbnail_missing`、`thumbnail_no_benefit`、`url_fallback_risk`、`closed` 等分类统计；默认 CLI 不得输出 raw object key 或业务 label。任何 apply / backfill 写入 MUST 显式参数触发，执行前确认数据库与 bucket/prefix 备份，执行后记录幂等复跑、失败重试和失败原因枚举。

## 4. AI必须遵守

AI 在新增文件上传、视频上传、图片处理、导入导出能力时：

1. 不允许新增多个业务 Bucket，除非 OpenSpec 明确要求；
2. 必须复用 `.env.example` 中的 `OBJECT_STORAGE_BUCKET`；
3. 必须使用标准前缀；
4. 必须更新媒体资源相关 OpenSpec 和文档；
5. 必须补充对象Key生成逻辑和测试。

## 5. 云上对象存储部署要求

- 云上对象存储 provider 可使用 `s3-compatible`、`tencent-cos`、`volcengine-tos` 等枚举值表达。
- `OBJECT_STORAGE_ENDPOINT` MUST 使用后端容器可访问的 endpoint，且不得包含 access key、secret key 或真实不可公开域名截图；`tencent-cos` 使用腾讯云 COS endpoint，例如 `cos.ap-guangzhou.myqcloud.com`。
- `OBJECT_STORAGE_REGION` 在云厂商要求时 MUST 显式配置。
- `OBJECT_STORAGE_AUTO_CREATE_BUCKET` 在云上生产环境 MUST 为 `false`，bucket 由运维提前创建。
- 默认情况下，前端、管理端和小程序 MUST 继续通过后端上传与 `/media/{object_key}` 受控读取，不得直连云对象存储写入。
- 若要引入前端直传云对象存储，MUST 先创建 OpenSpec Change，并满足：后端鉴权、短期凭证或预签名 URL、后端生成受控对象 Key、限制 MIME/大小/前缀、禁止前端持有永久密钥、上传完成后由后端确认并保存业务引用。
