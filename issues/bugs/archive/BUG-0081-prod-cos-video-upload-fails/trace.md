---
bug_id: BUG-0081-prod-cos-video-upload-fails
status: done
lifecycle_stage: archive
severity: high
created_at: 2026-07-23 08:37:33
updated_at: 2026-07-23 10:08:59
lifecycle:
  captured: 2026-07-23 08:37:33
  generated: 2026-07-23 08:58:10
  completed: 2026-07-23 09:00:31
  reviewed: 2026-07-23 09:04:56
  approved: 2026-07-23 09:04:56
iteration: sprint-011
related_requirement: null
related_bug: null
related_change: fix-upload-proxy-timeout-config
source_command: /bug-capture
openspec_changes:
  - change_id: fix-upload-proxy-timeout-config
    type: fix
    status: archived
related_bugs: []
---

```yaml
bug_id: BUG-0081-prod-cos-video-upload-fails
status: done
severity: high
lifecycle_stage: archive
created_at: 2026-07-23 08:37:33
updated_at: 2026-07-23 10:08:59
lifecycle:
  captured: 2026-07-23 08:37:33
  generated: 2026-07-23 08:58:10
  completed: 2026-07-23 09:00:31
  reviewed: 2026-07-23 09:04:56
  approved: 2026-07-23 09:04:56
iteration: sprint-011
related_requirement: null
related_bug: null
related_change: fix-upload-proxy-timeout-config
source_command: /bug-capture
openspec_changes:
  - change_id: fix-upload-proxy-timeout-config
    type: fix
    status: archived
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
  bug: done
  root_cause: done
  workaround: done
  acceptance: done
  review: done
  trace: done
  next: opsx-apply
```

## 来源

| 类型 | ID / 路径 | 说明 |
|---|---|---|
| 用户反馈 | /bug-capture | 生产环境腾讯 COS 视频上传失败 |
| 用户补充 | /bug-capture | 前端上传进度卡在 99% |
| 用户补充 | /bug-capture | 浏览器返回 `504 Gateway Time-out`，但腾讯 COS 已有对应文件；Nginx 约 60 秒后记录该上传请求为 `499` |

## 建议复现要点

| 要点 | 说明 |
|---|---|
| 接口请求 | 记录 `/api/v1/admin/uploads/tile-videos` 的 HTTP 状态码、响应错误码和 request_id |
| 进度卡点 | 上传进度卡在 99% 且 COS 已有文件时，优先确认后端写入完成后为何未及时返回成功响应 |
| 超时证据 | 对照 Nginx 记录：请求体在 `00:42:53 +0000` 被缓冲，上传请求在 `00:43:53 +0000` 记录为 `499`，约 60 秒，疑似命中默认反代或外层网关超时 |
| 文件信息 | 记录视频大小、扩展名、浏览器上报 MIME、是否超过 `MAX_VIDEO_SIZE_MB` |
| 代理限制 | 仍需确认 Web Nginx `client_max_body_size` 是否不小于 `MAX_VIDEO_SIZE_MB`，但 99% 卡住时优先级低于 COS 写入链路 |
| 反代超时 | 检查 Web Nginx、宿主机反代、CDN/网关的 `proxy_read_timeout`、`proxy_send_timeout`、`send_timeout` 或等价超时是否默认为 60 秒 |
| 请求缓冲 | 检查是否需要对大文件上传接口配置 `proxy_request_buffering off` 或专用上传 location，避免大文件先落 Nginx 临时文件再转发造成总耗时过长 |
| 存储配置 | 确认 `OBJECT_STORAGE_PROVIDER=tencent-cos` 或 `s3-compatible`、COS endpoint 不带协议、`OBJECT_STORAGE_SECURE=true`、region 与 bucket 匹配 |
| 访问风格 | 腾讯 COS S3 兼容 virtual-host 场景通常应使用 `OBJECT_STORAGE_PATH_STYLE=false` |
| Bucket 权限 | 确认 AccessKey/SecretKey 对目标 Bucket 与 `videos/` 前缀具备写入权限，生产 `OBJECT_STORAGE_AUTO_CREATE_BUCKET=false` |
| 网络链路 | 确认 backend 容器可访问 COS endpoint，安全组、DNS、TLS 证书与出口白名单正常 |
| 后端日志 | 检查 `对象存储不可用`、COS SDK 异常、超时、签名不匹配、AccessDenied、NoSuchBucket 或 region mismatch |

## 建议验收要点

| 验收点 | 说明 |
|---|---|
| 上传成功 | 生产管理端上传合法 MP4 视频成功，返回 `object_key` 与 `/media/{object_key}` |
| 对象写入 | 腾讯 COS 目标 Bucket 下出现符合规范的 `videos/default/tiles/{tile_id|pending}/{uuid}.mp4` 对象 |
| 响应及时 | COS 对象写入后，上传接口在反代超时窗口内稳定返回 200，不再出现浏览器 504 或 Nginx 499 |
| 受控读取 | 上传返回的 `/media/{object_key}` 可经后端读取，前端不直连未授权 COS 写入 |
| 错误可诊断 | COS 不可用、权限不足、配置错误、文件过大或 MIME 不允许时返回明确错误码与日志 |
| 回归覆盖 | 品牌 Logo/SKU 图片上传不受影响，视频上传大小限制与 Nginx body 限制一致 |

## 实施验证

| 时间 | 验证 | 结果 |
|---|---|---|
| 2026-07-23 09:37:50 | Web 容器 Nginx 上传路径 | `src/web/nginx.conf.template` 与默认 `src/web/nginx.conf` 已在通用 `/api/` 前增加 `/api/v1/admin/uploads/` 专用 location |
| 2026-07-23 09:37:50 | 上传反代环境变量 | `.env.example`、本地 Compose、自建 MinIO 生产 Compose、外部 COS/TOS 生产 Compose 已配置 `UPLOAD_*` 默认值：body `512m`、主要超时 `600s`、request buffering `off` |
| 2026-07-23 09:37:50 | 外层 HTTPS 反代文档 | `docs/02-deployment.md` 已补充生产外层 Nginx 上传 location、`nginx -t`、reload 与 Web 容器重建步骤 |
| 2026-07-23 09:37:50 | 自动化测试 | `uv run pytest tests/test_cloud_object_storage_deployment.py tests/test_media_storage.py`：12 passed, 1 warning |
| 2026-07-23 09:40:30 | Web 镜像与 Nginx 配置 | `docker compose build web` 通过；`docker run --rm --add-host backend:127.0.0.1 projecttilesfst-web nginx -t` 通过 |

生产现场同类视频上传 smoke 尚待部署后执行：合法视频返回 200、COS 对象存在且 key 与响应一致、返回 `/media/{object_key}` 可读取、SKU 表单保存闭环、外层与容器 Nginx 日志不再出现同类 504/499。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-23 10:08:30 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-upload-proxy-timeout-config） |
| 2026-07-23 10:08:11 | /opsx-archive | Change `fix-upload-proxy-timeout-config` 已归档，状态同步完成。 |
| 2026-07-23 09:17:23 | /sprint-propose | 纳入 sprint-011 正式范围，关联 Change `fix-upload-proxy-timeout-config` |
| 2026-07-23 09:09:35 | /bug-opsx | 创建 OpenSpec Change `fix-upload-proxy-timeout-config`，状态 proposed |
| 2026-07-23 09:05:43 | lifecycle-stage-migrate | plan → review（/bug-review --approve） |
| 2026-07-23 09:04:56 | /bug-review --approve | 评审通过，状态更新为 approved，准备由 plan 迁入 review 阶段 |
| 2026-07-23 09:00:31 | /bug-complete | 补齐 root-cause、workaround、acceptance；状态更新为 pending_review |
| 2026-07-23 08:58:10 | /bug-generate | 生成 bug.md，状态更新为 draft；记录上传反代超时环境变量化作为后续修复方向 |
| 2026-07-23 08:49:17 | /bug-capture | 补充浏览器 504、COS 已写入对象、Nginx 60 秒后 499 与请求体临时文件缓冲证据，根因方向收敛到上传反代/网关超时与响应链路 |
| 2026-07-23 08:43:24 | /bug-capture | 补充上传进度卡在 99% 的复现证据，排查优先级收敛到后端 COS 写入阶段 |
| 2026-07-23 08:37:33 | /bug-capture | 记录生产环境腾讯 COS 视频上传失败缺陷 |

- 2026-07-23 10:08:11 workflow-sync：状态同步为 done（Change archived）
