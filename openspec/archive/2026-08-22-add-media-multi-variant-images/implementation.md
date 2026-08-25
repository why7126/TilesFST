---
change_id: add-media-multi-variant-images
status: applied
created_at: 2026-08-22 14:33:52
updated_at: 2026-08-22 14:33:52
source_requirement: REQ-0115-media-multi-variant-images
source_sprint: sprint-025
---

# 实现记录

## 媒体模型

本 Change 采用可派生 key 规则，不新增 SQLite/MySQL 字段：

| 规格 | Key 规则 | 典型用途 |
|---|---|---|
| `original` | 原始 `object_key` | 高清预览、下载语义、兜底读取 |
| `thumbnail` | 同目录 `<stem>.thumb<suffix>` | 列表、卡片、轻量回显 |
| `display` | 同目录 `<stem>.display<suffix>` | 详情普通展示、管理端预览 |

生成策略保留原图格式，不把用户文件名写入对象 key。JPG、PNG、WebP 使用 Pillow 等比缩小且不放大小图；透明 PNG/WebP 尽量保留透明度。`display` 最大宽高为 1600x1600，JPG/WebP 质量为 86，目标体积为 768KB。生成失败只记录脱敏 key hash 和失败类型，原图上传不被阻断，读取 `.thumb` / `.display` 时可回退同目录原图。

## API 与端侧

上传响应、管理端 SKU 图片字段和小程序商品/SKU 媒体字段均扩展 `thumbnail_url`、`display_url`、`original_url`。管理端列表优先使用缩略图，编辑/预览优先使用 display；小程序列表和推荐卡片使用 thumbnail，SKU 详情展示使用 display，图片预览使用 original，首屏外图片启用 lazy-load。

对象存储直出通过后端 storage adapter 生成短期读取 URL。默认 `OBJECT_STORAGE_DIRECT_READ_ENABLED=false`，接口返回 `/media/{object_key}`；开启后由后端返回签名 URL，过期时间由 `OBJECT_STORAGE_DIRECT_READ_EXPIRES_SECONDS` 控制并限制在 60-3600 秒。前端和小程序不得拼接对象存储 endpoint、bucket 或持有永久密钥。

## 存量生成

新增生产维护任务 `backfill-image-variants`，覆盖 SKU 图片、品牌 Logo 和品牌证书图片的 `.thumb` / `.display` 缺失审计与补生成。默认 dry-run，写入对象存储必须显式 `--apply --confirm-backup`，输出只包含统计、hash、标准前缀、失败分类和重试建议。

## 文档同步

已同步 `.env.example`、API 索引、数据库设计、部署文档、视频/媒体维护文档、对象存储策略、data 目录说明和媒体验收模板。
