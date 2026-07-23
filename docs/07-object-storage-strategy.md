---
purpose: 对象存储策略说明
content: 说明 MinIO/S3兼容对象存储单桶策略、目录前缀、资源类型、迁移与维护规范
source: AI自动生成，人工确认
update_method: 对象存储策略或媒体资源类型变化时更新
created_at: 2026-06-13 00:00:00
updated_at: 2026-07-21 13:44:26
note: V5 从多桶策略调整为单桶 + 前缀策略；支持 MinIO 与 S3 兼容云对象存储
---

# 对象存储策略

## 1. 当前策略

本项目使用 MinIO 或 S3 兼容对象存储，采用：

```text
一个项目一个 Bucket
桶内使用二级目录/前缀区分资源类型
```

默认：

```text
OBJECT_STORAGE_BUCKET=tilesfst
```

后端应用统一使用 `OBJECT_STORAGE_BUCKET`。腾讯云 COS、火山云 TOS 等云上对象存储通过 S3 兼容 endpoint 接入，仍使用同一 bucket 和相同对象 Key 前缀。

## 2. 目录前缀

| 前缀 | 用途 |
|---|---|
| `images/` | 图片类上传（头像、Logo、SKU 图等） |
| `videos/` | 原始视频 |
| `files/` | 文档类（预留） |
| `audios/` | 音频类（预留） |
| `thumbnails/` | 缩略图 |
| `processed/` | 处理后的资源 |
| `tmp/` | 临时文件 |
| `imports/` | 批量导入文件 |
| `exports/` | 导出文件 |
| `videos/covers/` | 视频封面 |
| `videos/transcoded/` | 转码后视频 |
| `original/` | **Deprecated** — 存量迁移前遗留；新上传不得使用 |

当前后端上传入口使用以下 Key 前缀（`resource_type` 见 `rules/object-storage.md`）：

| 上传入口 | 对象 Key 前缀 |
|---|---|
| 头像 | `images/default/user/avatars/` |
| 品牌 Logo | `images/default/brands/logos/` |
| SKU 图片 | `images/default/tiles/{tile_id\|pending}/` |
| SKU 视频 | `videos/default/tiles/{tile_id\|pending}/` |

上传响应保持 `{ object_key, url }`，其中 `url` 为后端受控读取地址 `/media/{object_key}`。

## 3. 本地持久化与 legacy 清理

| 路径 | 职责 |
|---|---|
| `data/minio/tilesfst/` | 本地 Docker 下 MinIO 桶物理存储；对象增长属预期 |
| `data/uploads/` | BUG-0006 前本地上传历史目录；迁移后新上传 **不得** 写入 |

对象存储从本地 `UPLOAD_DIR` 迁移至 MinIO 后，应清理 `data/uploads` 中与数据库 `object_key` 无关联的孤儿文件：

```bash
python scripts/clean_legacy_uploads.py          # dry-run
python scripts/clean_legacy_uploads.py --apply
python scripts/clean_legacy_uploads.py --check-only
```

详见 `data/README.md`。

## 4. 适用原因

瓷砖信息管理平台的媒体资源主要围绕同一个业务域，单桶便于部署、迁移、备份和权限管理。云上对象存储部署时，bucket、region、TLS、访问风格和最小权限由运维前置准备，应用不在生产环境隐式创建云 bucket。

## 4. 何时考虑多桶

只有在生命周期策略、权限隔离、合规要求或资源规模明确要求时，才通过 OpenSpec Change 引入多桶。
