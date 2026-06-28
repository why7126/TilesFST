---
title: 业务流程
purpose: 描述 Object Key 生成、上传、读取与迁移流程
content: 基于 requirement.md 提炼
source: AI 根据 PRD 生成，项目团队确认
update_method: PRD 变更时同步更新
owner: product
status: draft
created_at: 2026-06-27 22:17:37
updated_at: 2026-06-27 22:17:37
note: REQ-0012-object-storage-key-layout
---

# 业务流程

## 1. 与现有系统的差异

```text
变更前（现网）                              变更后（REQ-0012）
────────────────────────────────────────────────────────────────────────────
图片类前缀: original/                       图片类前缀: images/
Key 形态:  prefix/default/resource/YYYY/MM/uuid.ext   prefix/default/resource/uuid.ext
头像 resource: avatars                       user/avatars
SKU 图 resource: tiles/{id}/images           tiles/{id}  （去掉冗余 /images）
视频 prefix: videos/（不变）                 videos/（不变，仅去 YYYY/MM）
租户段 default/                              default/（保留）
```

**不变**：单桶 `tile-info-platform`、后端授权上传、响应 `{ object_key, url }`、`GET /media/{object_key}` 读取、MIME/大小校验。

## 2. 新 Object Key 生成流程

```text
管理端选择文件 → POST /api/v1/admin/uploads/*
  ↓
后端校验 MIME + 大小（MAX_*_SIZE_MB、ALLOWED_*_TYPES）
  ↓
根据 API 确定 (prefix, resource_type)
  例: brand-logos → (images, brands/logos)
  ↓
build_object_key(prefix, resource_type, ext, tenant=default)
  → images/default/brands/logos/{uuid}.webp
  ↓
MinioMediaStorageClient.put_object(MINIO_BUCKET, object_key)
  ↓
返回 { object_key, url: "/media/{object_key}" }
  ↓
前端写入品牌/SKU/用户表单 → 业务 API 持久化 object_key 至 SQLite
```

## 3. 媒体读取流程（不变）

```text
浏览器 / 前端 <img src="/media/{object_key}">
  ↓
Nginx proxy → FastAPI GET /media/{object_key:path}
  ↓
validate_object_key（防路径穿越）
  ↓
MinIO get_object(MINIO_BUCKET, object_key)
  ↓
返回 bytes + Content-Type
```

## 4. 上传 API → Key 映射（目标态）

| API | prefix | resource_type |
|---|---|---|
| `POST .../uploads` | `images` | `user/avatars` |
| `POST .../uploads/brand-logos` | `images` | `brands/logos` |
| `POST .../uploads/tile-images?tile_id=` | `images` | `tiles/{tile_id}` 或 `tiles/pending` |
| `POST .../uploads/tile-videos?tile_id=` | `videos` | `tiles/{tile_id}` 或 `tiles/pending` |

## 5. 存量迁移流程（本期选定：方案 A）

> `/req-complete` 敲定：**一次性迁移脚本**（非长期双读兼容）。

```text
发版前备份
  ├─ SQLite: data/sqlite/*.db
  └─ MinIO: data/minio/tile-info-platform/（或 mc mirror）
  ↓
python scripts/migrate_object_keys.py --dry-run
  → 输出: 旧 Key → 新 Key 映射表、计数、冲突检测
  ↓
python scripts/migrate_object_keys.py --apply
  ├─ MinIO: copy 对象至新 Key，成功后 delete 旧 Key
  └─ SQLite: UPDATE avatar_object_key / logo_object_key / tile_images / tile_videos
  ↓
冒烟: 品牌 Logo、用户头像、SKU 图/视频列表预览
  ↓
确认无 original/ 前缀新写入；pytest 全绿
```

**映射规则（脚本逻辑）**：

| 旧 Key 模式 | 新 Key 模式 |
|---|---|
| `original/default/avatars/{Y}/{M}/{uuid}.ext` | `images/default/user/avatars/{uuid}.ext` |
| `original/default/brands/logos/{Y}/{M}/{uuid}.ext` | `images/default/brands/logos/{uuid}.ext` |
| `original/default/tiles/{id}/images/{Y}/{M}/{uuid}.ext` | `images/default/tiles/{id}/{uuid}.ext` |
| `original/default/tiles/pending/images/{Y}/{M}/{uuid}.ext` | `images/default/tiles/pending/{uuid}.ext` |
| `videos/default/tiles/{id}/{Y}/{M}/{uuid}.ext` | `videos/default/tiles/{id}/{uuid}.ext` |
| `videos/default/tiles/pending/{Y}/{M}/{uuid}.ext` | `videos/default/tiles/pending/{uuid}.ext` |

## 6. 与父需求 / 关联 REQ 差异

| 关联 | 差异说明 |
|---|---|
| REQ-0006 SKU 管理 | 上传 API 不变；仅 `object_key` 字符串格式变化；前端仍存 API 返回值 |
| REQ-0005 品牌/用户 | Logo、头像 Key 前缀与路径变化；迁移后 URL 路径变短 |
| BUG-0006～0008 | 已完成「写 MinIO 不写 UPLOAD_DIR」；本 REQ 为 Key 命名优化，不重复存储链路改造 |
| `openspec/specs/object-storage` | MODIFIED：Key 前缀与形态条款 |

## 7. 依赖

| 依赖 | 说明 |
|---|---|
| `object_keys.py` | Key 生成核心 |
| `uploads.py` | 四上传入口映射 |
| `storage.py` | MinIO 读写 |
| `scripts/migrate_object_keys.py` | 新建迁移脚本（OpenSpec apply 阶段） |
| `rules/object-storage.md` | 规范同步 |
