---
purpose: 对象存储策略说明
content: 说明 MinIO 单桶策略、目录前缀、资源类型、迁移与维护规范
source: AI自动生成，人工确认
update_method: 对象存储策略或媒体资源类型变化时更新
note: V5 从多桶策略调整为单桶 + 前缀策略
---

# 对象存储策略

## 1. 当前策略

本项目使用 MinIO，采用：

```text
一个项目一个 Bucket
桶内使用二级目录/前缀区分资源类型
```

默认：

```text
MINIO_BUCKET=tile-info-platform
```

## 2. 目录前缀

| 前缀 | 用途 |
|---|---|
| `original/` | 原始图片、文件 |
| `thumbnails/` | 缩略图 |
| `processed/` | 处理后的资源 |
| `tmp/` | 临时文件 |
| `imports/` | 批量导入文件 |
| `exports/` | 导出文件 |
| `videos/` | 原始视频 |
| `videos/covers/` | 视频封面 |
| `videos/transcoded/` | 转码后视频 |

当前后端上传入口使用以下业务前缀：

| 上传入口 | 对象前缀 |
|---|---|
| 头像 | `original/default/avatars/` |
| 品牌 Logo | `original/default/brands/logos/` |
| SKU 图片 | `original/default/tiles/{tile_id|pending}/images/` |
| SKU 视频 | `videos/default/tiles/{tile_id|pending}/` |

上传响应保持 `{ object_key, url }`，其中 `url` 为后端受控读取地址 `/media/{object_key}`。

## 3. 本地持久化与 legacy 清理

| 路径 | 职责 |
|---|---|
| `data/minio/tile-info-platform/` | 本地 Docker 下 MinIO 桶物理存储；对象增长属预期 |
| `data/uploads/` | BUG-0006 前本地上传历史目录；迁移后新上传 **不得** 写入 |

对象存储从本地 `UPLOAD_DIR` 迁移至 MinIO 后，应清理 `data/uploads` 中与数据库 `object_key` 无关联的孤儿文件：

```bash
python scripts/clean_legacy_uploads.py          # dry-run
python scripts/clean_legacy_uploads.py --apply
python scripts/clean_legacy_uploads.py --check-only
```

详见 `data/README.md`。

## 4. 适用原因

瓷砖信息管理平台的媒体资源主要围绕同一个业务域，单桶便于部署、迁移、备份和权限管理。

## 4. 何时考虑多桶

只有在生命周期策略、权限隔离、合规要求或资源规模明确要求时，才通过 OpenSpec Change 引入多桶。
