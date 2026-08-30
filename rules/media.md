---
purpose: 图片与视频媒体资产管理规范
content: 瓷砖图片、视频、封面、转码、上传、对象存储、前端展示和安全限制
source: AI自动生成初稿，项目团队确认
update_method: 新增媒体类型、视频转码、封面生成、上传限制、对象存储策略时更新
created_at: 2026-06-13 00:00:00
updated_at: 2026-08-30 12:26:56
note: 适用于Web展示端、微信小程序和管理端的媒体资产处理
---

# 媒体资产管理规范

## 1. 媒体类型

本项目支持：

- 瓷砖主图
- 瓷砖详情图
- 瓷砖铺贴效果图
- 瓷砖介绍视频
- 瓷砖工艺/质检视频
- 视频封面图
- 品牌证书图片与 PDF/文档
- 规格书和检测报告附件

## 2. 存储规则

媒体文件必须通过后端授权上传到对象存储。默认上传链路为前端提交到后端，后端写入 MinIO、S3 兼容对象存储或腾讯云 COS；不允许前端绕过后端直接写入未授权对象存储。

项目默认存储桶：

```text
OBJECT_STORAGE_BUCKET=tilesfst
```

推荐对象前缀：

```text
images/                图片类资源（头像、Logo、SKU 图、Banner、品牌证书图片）
videos/                原始视频
videos/covers/         视频封面
videos/transcoded/     转码后视频
files/                 PDF、规格书、检测报告、证书文档
processed/             处理后资源
thumbnails/            缩略图
original/              Deprecated，仅存量兼容
```

品牌证书必须按媒体类型分流：JPG、PNG、WebP 证书图片使用 `images/default/brand-certificates/` 或等价标准图片前缀，PDF 等证书文档继续使用 `files/default/brand-certificates/`。图片证书缩略图和详情展示图必须与原图保持同一图片资源归属，优先使用同目录 `.thumb.webp` / `.display.webp` key；PDF 不生成 `thumbnail_url` 或 `display_url`。

新上传媒体必须优先落在扁平业务媒体类型目录：用户头像 `images/default/user-avatars/{user_id}/`，品牌 Logo `images/default/brand-logos/{brand_id}/`，Banner 图片 `images/default/banners/{banner_id}/`，SKU 图片 `images/default/tiles/{tile_id}/`，SKU 视频 `videos/default/tiles/{tile_id}/`，品牌证书图片 `images/default/brand-certificates/{certificate_id}/`，品牌证书文件 `files/default/brand-certificates/{certificate_id}/`。业务对象创建前允许进入同类资源 `pending/` 暂存目录，保存后必须由后端 formalize 或维护任务迁入正式 id 目录；端侧不得自行拼接业务 id 目录。

图片上传的原图 MUST 保留上传格式、原始 MIME 与原图 key。首期仅对 JPEG/JPG、PNG、WebP 输入生成 WebP 派生图：列表/卡片缩略图使用 `.thumb.webp`，详情普通展示图使用 `.display.webp`，对象 Content-Type MUST 为 `image/webp`。SVG/PDF 跳过 WebP 派生；GIF、HEIC、TIFF、BMP 首期不转码，上传入口按现有允许类型拒绝或跳过。派生图生成失败不得阻断原图上传，必须记录脱敏 warning、任务 span 或维护任务失败原因。

## 3. 视频规范

- 默认推荐MP4格式。
- 管理端上传视频后，应生成或上传封面图。
- 视频文件大小必须受环境变量控制。
- 小程序端展示视频时必须考虑网络和体积限制。
- 视频转码能力可作为可选能力，不应阻塞基础上传管理流程。
- 管理端上传视频若出现 99% 或“正在保存视频，请稍候”停留较久，必须优先查看后端 `media_upload_timing` 中 `storage_put_done stage_ms`；若该阶段耗时远高于文件读取和校验，瓶颈在后端到对象存储的写入链路。

## 4. 安全规则

- 必须校验MIME Type和扩展名。
- 必须限制文件大小。
- 必须防止路径穿越。
- 必须隔离原始文件名和对象存储Key。
- 对外访问应使用签名URL或受控公开策略。
- 前端直传对象存储必须通过 OpenSpec Change 设计，并使用短期凭证或预签名 URL；禁止把永久 access key / secret key 下发到前端。

## 5. 媒体类 BUG 四联验收

媒体类 BUG 修复、返修、回归测试、Sprint 验收和发布前检查必须使用 `docs/standards/media-bug-four-point-acceptance-template.md`。触发范围包括：

- 上传、编辑、删除、列表回显、详情展示、公开展示或小程序展示中的图片、视频、Logo、证书、缩略图、封面图问题。
- `object_key`、对象存储 object、`/media/{object_key}` 或等价受控 URL、签名 URL、代理 URL、静态资源 URL 不一致问题。
- 历史对象、缩略图、回填、审计脚本、媒体性能回归、小程序域名或组件限制导致的媒体缺陷。

四联验收必须先记录原 BUG 场景，再逐项记录：

| 维度 | 必须确认 |
|---|---|
| `key` | 业务记录中的媒体 key 稳定、可追溯，符合单 Bucket 与标准前缀策略，不使用用户原始文件名、本机绝对路径、临时路径或未脱敏内部路径 |
| `object` | 对象存储中真实 object 存在，MIME、大小、扩展名、权限边界和对象可读性符合预期 |
| `URL` | 相对 URL、公开 URL、签名 URL、代理 URL 或静态资源 URL 可区分、可追溯，端侧通过后端受控读取，不直连未授权对象存储 |
| `render` | 受影响端覆盖展示、预览、播放、占位、失败态和用户可见行为；小程序必须按目标环境记录 DevTools、真机或体验版 evidence，或明确后置补证方式 |

每个维度必须记录 `pass`、`fail`、`n/a` 或 `blocked` 状态、证据和失败/阻塞处理。`n/a` 必须说明不适用原因；`blocked` 不得视为通过；任一 `fail` 必须包含实际结果、期望结果、复现步骤、影响范围和排查线索。

涉及上传链路时，四联验收还必须覆盖上传状态机、同会话即时回显、Docker Web `http://localhost:3000` 边界文件、`object_key` 与受控媒体 URL 一致性。涉及历史对象、缩略图、展示图、WebP 派生图回填或审计脚本时，必须记录 dry-run、apply、幂等性或统计摘要，且不得泄露敏感信息。

小程序媒体相关需求、BUG、Sprint 验收和发布前检查必须优先引用 `docs/knowledge-base/best-practices/miniapp-media-four-part-acceptance-practice.md`。除静态测试外，还应记录 DevTools、真机或体验版 Network evidence，覆盖图片展示 URL、preview URL、视频 URL、poster/cover、fallback、lazy-load 和受控 `/media` URL。测试 helper 只能证明模板绑定与 URL 安全边界；审计 helper 只能证明历史对象和缩略图状态，二者均不得替代小程序 render evidence。

开发阶段无法访问生产环境、体验版入口、真机设备、生产对象存储或生产公开域名时，媒体四联验收不得把这些生产专属证据缺口默认写为开发归档 blocker。应按 `docs/standards/media-bug-four-point-acceptance-template.md` 和 `docs/standards/miniapp-device-evidence-template.md` 记录 `target_environment`、`phase`、`blocking_scope` 与 `classification`，将仅生产可得的证据标记为 `production_only_pending`、`environment_unavailable`、`follow_up` 或 `not_applicable_for_development`。若 Change 目标明确是生产维护执行或生产发布确认，则生产对象、生产 URL、生产 no-fallback 媒体、备份、dry-run/apply 和二次审计证据按范围参与强门禁。

涉及品牌证书时，四联验收必须明确区分图片类证书与 PDF/文档类证书：图片 key 与缩略图 key 使用 `images/`，PDF/文档 key 使用 `files/`；历史图片 key 迁移必须记录 dry-run/apply/幂等摘要。

生产媒体维护作业必须通过后端包内入口或受控兼容脚本执行，默认 dry-run。写入数据库或对象存储的任务 MUST 显式使用 `--apply --confirm-backup`，并在执行前确认 MySQL 与对象存储 bucket/prefix 备份已完成。`migrate-business-id-media-keys` 用于把头像、品牌 Logo、Banner、SKU 图片/视频、品牌证书图片/文件迁移到业务 id 目录；任务不得默认删除旧对象，旧对象清理必须另行评估、备份并通过单独受控流程执行。维护输出 MUST 使用对象 Key hash、标准前缀、统计摘要和枚举化失败原因，不得输出真实 object key 全量值、数据库连接串、access key、secret key、Authorization header、Cookie、真实 `.env` 内容或本机绝对路径。任务结果 MUST 至少提供 key、object、URL、thumbnail benefit、render 维度的验收摘要；只读审计和批处理摘要不能替代受影响端的 Web、小程序或管理端渲染 evidence。

非媒体 BUG 可将本模板标记为 `n/a`，但必须说明“本 BUG 不涉及媒体 key、object、URL 或端侧渲染”的判断依据。通用媒体能力或缩略图收益验收优先引用 `docs/standards/media-five-point-acceptance-template.md`；媒体 BUG 修复闭环优先引用四联模板，必要时同时引用五联模板。

## 6. AI更新规则

AI新增或修改媒体能力时，必须同步更新：

```text
.env.example
data/README.md
docs/06-video-asset-management.md
docs/standards/media-bug-four-point-acceptance-template.md
openspec/specs/media-assets/spec.md
src/backend/app/modules/media/
src/web/src/features/media/
src/miniapp/pages/tile-detail/
tests/integration/media/
```
