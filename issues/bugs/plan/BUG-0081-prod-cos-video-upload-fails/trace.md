---
bug_id: BUG-0081-prod-cos-video-upload-fails
status: captured
lifecycle_stage: plan
severity: high
created_at: 2026-07-23 08:37:33
updated_at: 2026-07-23 08:37:33
lifecycle:
  captured: 2026-07-23 08:37:33
  generated: null
  completed: null
  reviewed: null
  approved: null
iteration: null
related_requirement: null
related_bug: null
related_change: null
source_command: /bug-capture
openspec_changes: []
related_bugs: []
---

```yaml
bug_id: BUG-0081-prod-cos-video-upload-fails
status: captured
severity: high
lifecycle_stage: plan
created_at: 2026-07-23 08:37:33
updated_at: 2026-07-23 08:37:33
lifecycle:
  captured: 2026-07-23 08:37:33
  generated: null
  completed: null
  reviewed: null
  approved: null
iteration: null
related_requirement: null
related_bug: null
related_change: null
source_command: /bug-capture
openspec_changes: []
related_bugs: []
scope:
  terminal: admin-web
  environment: production
  module: media_upload
  storage_provider: tencent-cos
  media_type: video
  issue_type: upload_failed
readiness:
  capture: done
  bug: todo
  root_cause: todo
  workaround: todo
  acceptance: todo
  review: todo
  trace: done
  next: bug-explore
```

## 来源

| 类型 | ID / 路径 | 说明 |
|---|---|---|
| 用户反馈 | /bug-capture | 生产环境腾讯 COS 视频上传失败 |

## 建议复现要点

| 要点 | 说明 |
|---|---|
| 接口请求 | 记录 `/api/v1/admin/uploads/tile-videos` 的 HTTP 状态码、响应错误码和 request_id |
| 文件信息 | 记录视频大小、扩展名、浏览器上报 MIME、是否超过 `MAX_VIDEO_SIZE_MB` |
| 代理限制 | 确认 Web Nginx `client_max_body_size` 是否不小于 `MAX_VIDEO_SIZE_MB` |
| 存储配置 | 确认 `OBJECT_STORAGE_PROVIDER=tencent-cos` 或 `s3-compatible`、COS endpoint 不带协议、`OBJECT_STORAGE_SECURE=true`、region 与 bucket 匹配 |
| 访问风格 | 腾讯 COS S3 兼容 virtual-host 场景通常应使用 `OBJECT_STORAGE_PATH_STYLE=false` |
| Bucket 权限 | 确认 AccessKey/SecretKey 对目标 Bucket 与 `videos/` 前缀具备写入权限，生产 `OBJECT_STORAGE_AUTO_CREATE_BUCKET=false` |
| 网络链路 | 确认 backend 容器可访问 COS endpoint，安全组、DNS、TLS 证书与出口白名单正常 |

## 建议验收要点

| 验收点 | 说明 |
|---|---|
| 上传成功 | 生产管理端上传合法 MP4 视频成功，返回 `object_key` 与 `/media/{object_key}` |
| 对象写入 | 腾讯 COS 目标 Bucket 下出现符合规范的 `videos/default/tiles/{tile_id|pending}/{uuid}.mp4` 对象 |
| 受控读取 | 上传返回的 `/media/{object_key}` 可经后端读取，前端不直连未授权 COS 写入 |
| 错误可诊断 | COS 不可用、权限不足、配置错误、文件过大或 MIME 不允许时返回明确错误码与日志 |
| 回归覆盖 | 品牌 Logo/SKU 图片上传不受影响，视频上传大小限制与 Nginx body 限制一致 |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-23 08:37:33 | /bug-capture | 记录生产环境腾讯 COS 视频上传失败缺陷 |
