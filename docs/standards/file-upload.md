---
purpose: 文件上传规范
content: 图片/视频/附件上传流程与返回结构
source: rules/media.md / build-api-standard
update_method: 上传能力变更时同步更新
created_at: 2026-06-13 00:00:00
updated_at: 2026-08-04 09:05:00
---

# 文件上传规范

## 原则

- 前端 **禁止** 直连未授权 MinIO
- 上传 MUST 经后端 `multipart/form-data` 接口
- 存储：单桶 `tilesfst` + 前缀（见 `project.yaml`）

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
    "object_key": "images/default/...",
    "url": "/media/images/default/...",
    "thumbnail_key": "images/default/...thumb.jpg",
    "thumbnail_url": "/media/images/default/...thumb.jpg",
    "task_trace_id": "task_upload_image_abcdef1234567890",
    "task_type": "upload_image",
    "mime_type": "image/jpeg",
    "size": 102400
  }
}
```

视频上传额外可含 `duration`、`cover_url`（若已实现）。图片类上传成功时应返回同目录 `.thumb` 缩略图 `thumbnail_key`、`thumbnail_url`；不生成缩略图的文件类型返回 `null`。缩略图内容读取 `media.thumbnail_max_size_kb` effective 策略，`0` 表示不限制，正整数表示尽量不超过目标 KB；该策略不得改变 `.thumb` Key / URL 命名规则。

图片、视频、文件上传首批接入 Task Trace。成功响应 MUST 返回后端生成或确认的 `task_trace_id` 与 `task_type`，前端后续行为事件可携带该 ID 继续串联同一次上传任务。

## 限制

- 图片 MIME 白名单：见 `ALLOWED_IMAGE_TYPES`；大小上限：`MAX_IMAGE_SIZE_MB`
- 视频 MIME 白名单：见 `ALLOWED_VIDEO_TYPES`；大小上限：`MAX_VIDEO_SIZE_MB`
- 品牌证书 MIME 白名单：JPG、PNG、WebP、PDF；证书多图图片保存仅接受 JPG、PNG、WebP；图片类证书上传生成同目录 `.thumb` 缩略图，PDF 不生成缩略图并由前端展示占位；大小上限：`MAX_FILE_SIZE_MB` / `media.max_file_size_mb` effective 值；对象前缀按媒体类型分流：图片证书使用 `images/default/brand-certificates/`，PDF/文档证书使用 `files/default/brand-certificates/`
- Docker Web（Nginx）`client_max_body_size` 须 >= `max(MAX_IMAGE_SIZE_MB, MAX_VIDEO_SIZE_MB, MAX_FILE_SIZE_MB)`（见 `src/web/nginx.conf.template` 与 `src/web/nginx.conf`）
- Docker Web 上传路径 `/api/v1/admin/uploads/` 使用专用反代超时：`UPLOAD_CLIENT_BODY_TIMEOUT_SECONDS`、`UPLOAD_PROXY_SEND_TIMEOUT_SECONDS`、`UPLOAD_PROXY_READ_TIMEOUT_SECONDS`、`UPLOAD_SEND_TIMEOUT_SECONDS` 默认均为 `600` 秒，`UPLOAD_CLIENT_MAX_BODY_SIZE` 默认 `512m`
- 大文件上传路径默认 `UPLOAD_PROXY_REQUEST_BUFFERING=off`，减少请求先落 Web Nginx `client_temp` 后再转发导致的总耗时；如生产网关策略必须开启，应同步提高外层与容器内反代超时
- 修改 `src/web/nginx.conf.template`、`src/web/nginx.conf` 或上传反代环境变量后须 **重建 Web Docker 镜像并重启 `web` 服务**，否则 `localhost:3000` 仍可能使用旧 Nginx 配置
- 错误码：`50002`、`50003`、`50004`、`50005`、`50001`
- Task Trace metadata MUST 脱敏，不保存 Authorization、Cookie、AccessKey、SecretKey、数据库 DSN、`.env`、真实客户数据、内部绝对路径、完整敏感请求体或原始本地路径。

## 99% / 504 诊断

当浏览器上传进度卡在 99%，接口返回外层 `504 Gateway Time-out`，但 COS/TOS/MinIO 中已经出现对象时，优先按“对象写入成功、响应链路超时”排查，而不是按对象存储写入失败处理：

- 外层 HTTPS Nginx 必须对 `/api/v1/admin/uploads/` 单独设置 `proxy_send_timeout`、`proxy_read_timeout`、`send_timeout`，建议生产不低于 `600s`
- 容器内 Web Nginx 也必须同步设置上传路径专用超时；只改外层反代可能继续命中容器内默认 60 秒
- 同时检查外层 access/error log 与容器内 Nginx log：出现请求体写入 `client_temp`、约 60 秒后 `499`/`504` 时，通常说明上传响应链路被代理层截断
- 验收必须包含合法视频上传返回 200、对象存在、返回 `/media/{object_key}` 可读取，以及管理端 SKU 保存闭环
- 管理端日志审计可按 `task_trace_id` 查询上传任务，并在详情 Task Trace 时间线中查看 `frontend_upload_body_done` 到 `api_response` 的耗时；若最慢节点为 `storage_put_object`、`db_create_media`、`post_process` 或 `api_response`，按对应层继续排查。

## 相关

- `rules/object-storage.md`
- `rules/media.md`
- `docs/06-video-asset-management.md`
