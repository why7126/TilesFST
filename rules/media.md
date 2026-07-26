---
purpose: 图片与视频媒体资产管理规范
content: 瓷砖图片、视频、封面、转码、上传、对象存储、前端展示和安全限制
source: AI自动生成初稿，项目团队确认
update_method: 新增媒体类型、视频转码、封面生成、上传限制、对象存储策略时更新
created_at: 2026-06-13 00:00:00
updated_at: 2026-07-26 15:19:59
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
- 规格书和检测报告附件

## 2. 存储规则

媒体文件必须通过后端授权上传到对象存储。默认上传链路为前端提交到后端，后端写入 MinIO、S3 兼容对象存储或腾讯云 COS；不允许前端绕过后端直接写入未授权对象存储。

项目默认存储桶：

```text
OBJECT_STORAGE_BUCKET=tilesfst
```

推荐对象前缀：

```text
original/              原始图片、文件
videos/                原始视频
videos/covers/         视频封面
videos/transcoded/     转码后视频
processed/             处理后资源
thumbnails/            缩略图
```

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

## 5. AI更新规则

AI新增或修改媒体能力时，必须同步更新：

```text
.env.example
data/README.md
docs/06-video-asset-management.md
openspec/specs/media-assets/spec.md
src/backend/app/modules/media/
src/web/src/features/media/
src/miniapp/pages/tile-detail/
tests/integration/media/
```
