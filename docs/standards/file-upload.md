---
purpose: 文件上传规范
content: 图片/视频/附件上传流程与返回结构
source: rules/media.md / build-api-standard
update_method: 上传能力变更时同步更新
created_at: 2026-06-13 00:00:00
updated_at: 2026-07-15 09:08:17
---

# 文件上传规范

## 原则

- 前端 **禁止** 直连未授权 MinIO
- 上传 MUST 经后端 `multipart/form-data` 接口
- 存储：单桶 `tile-info-platform` + 前缀（见 `project.yaml`）

## 请求

```http
POST /api/v1/uploads/images
Authorization: Bearer <token>
Content-Type: multipart/form-data

file: <binary>
```

## 成功响应

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "media_id": "uuid",
    "object_key": "original/...",
    "url": "https://...",
    "mime_type": "image/jpeg",
    "size": 102400
  }
}
```

视频上传额外可含 `duration`、`cover_url`（若已实现）。

## 限制

- 图片 MIME 白名单：见 `ALLOWED_IMAGE_TYPES`；大小上限：`MAX_IMAGE_SIZE_MB`
- 视频 MIME 白名单：见 `ALLOWED_VIDEO_TYPES`；大小上限：`MAX_VIDEO_SIZE_MB`
- 品牌证书 MIME 白名单：JPG、PNG、WebP、PDF；大小上限：20MB；对象前缀：`files/default/brand-certificates/`
- Docker Web（Nginx）`client_max_body_size` 须 ≥ `max(MAX_IMAGE_SIZE_MB, MAX_VIDEO_SIZE_MB)`（见 `src/web/nginx.conf`）
- 修改 `src/web/nginx.conf` 后须 **重建 Web Docker 镜像** 并重启 `web` 服务，否则 `localhost:3000` 仍可能返回 413
- 错误码：`50002`、`50003`、`50004`、`50005`、`50001`

## 相关

- `rules/object-storage.md`
- `rules/media.md`
- `docs/06-video-asset-management.md`
