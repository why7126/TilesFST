---
purpose: 视频资产管理说明
content: 瓷砖视频上传、存储、封面、转码、预览、前端展示、小程序适配和测试规则
source: AI自动生成初稿，项目团队确认
update_method: 视频上传、转码、封面、播放、存储策略变化时更新
created_at: 2026-06-13 00:00:00
updated_at: 2026-08-04 11:32:00
note: 本文档用于指导视频相关需求、开发、测试和验收
---

# 视频资产管理说明

## 1. 业务场景

瓷砖信息管理平台可能需要通过视频展示：

- 瓷砖铺贴效果
- 产品细节纹理
- 生产工艺
- 防滑、耐磨等测试过程
- 门店营销素材

## 2. 使用端

| 端 | 视频能力 |
|---|---|
| Web展示端 | 查看瓷砖介绍视频 |
| 微信小程序 | 查看轻量化视频、封面预览 |
| 管理端Web | 上传、维护、排序、删除视频 |

## 3. 存储设计

视频原文件存储在 MinIO：

```text
bucket: tilesfst
key: videos/default/tiles/{tile_id}/<object_id>.mp4
```

视频封面存储在：

```text
bucket: tilesfst
key: videos/covers/default/tiles/{tile_id}/<object_id>.jpg
```

项目采用一个 Bucket + 标准前缀策略，图片、视频、封面、转码产物均通过 `MINIO_BUCKET` 与 `MINIO_PREFIX_*` 环境变量管理。

## 4. 数据库元数据

视频应作为 `tile_media` 的一种类型记录：

```text
media_type = video
duration
cover_object_key
mime_type
file_size
sort_order
```

## 5. 初始化阶段建议

V4模板默认只提供视频管理目录和规范，不强制接入真实转码服务。

推荐阶段：

1. V1：支持视频上传、封面上传、播放。
2. V2：支持自动截帧生成封面。
3. V3：支持转码、压缩、多清晰度。

## 6. 生产媒体维护

生产媒体维护任务统一通过后端包内入口执行：

```bash
uv run --no-sync python -m app.modules.media.maintenance <task> --limit 100
```

当前任务包括 `object-key-audit`、`backfill-brand-certificate-thumbnails`、`formalize-pending-tile-images`、`migrate-certificate-image-keys` 和 `bug-0116-media-drift`。涉及写入对象存储或数据库的任务默认 dry-run；执行写入必须追加 `--apply --confirm-backup`，并先完成数据库与对象存储备份。

视频、封面、SKU 图片、品牌 Logo 和证书图片的维护结果应按媒体 key、object、URL、thumbnail benefit、render 维度记录摘要。只读审计或后端批处理不能替代端侧渲染验收；影响小程序、Web 展示端或管理端时，apply 后仍需补充实际端侧 evidence。

维护任务输出不得包含真实对象存储密钥、数据库连接串、Authorization header、Cookie、`.env` 内容、本机绝对路径或未脱敏 object key。需要定位对象时使用 hash、标准前缀、业务 ID 与统计摘要。

## 7. AI更新要求

视频需求进入开发时，AI必须创建或更新：

```text
openspec/changes/<change-id>/
openspec/specs/media-assets/spec.md
rules/media.md
.env.example
data/README.md
src/backend/app/modules/media/
src/web/src/features/media/
tests/integration/media/
```
