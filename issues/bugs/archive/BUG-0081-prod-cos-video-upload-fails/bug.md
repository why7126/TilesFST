---
bug_id: BUG-0081-prod-cos-video-upload-fails
title: 生产环境腾讯 COS 视频上传 99% 后返回 504
severity: high
status: done
owner:
discovered_at: 2026-07-23 08:37:33
created_at: 2026-07-23 08:58:10
updated_at: 2026-07-23 10:08:26
environment: 生产环境管理端，腾讯 COS 外部对象存储
related_requirement:
related_change: fix-upload-proxy-timeout-config
related_bug:
---

# 现象

生产环境管理端上传 SKU 视频时，浏览器请求：

```text
POST https://tilesfst.wjoyhappy.site/api/v1/admin/uploads/tile-videos?tile_id=3
```

前端上传进度卡在 99%，最终返回 `504 Gateway Time-out`。但腾讯 COS Bucket 中已经出现对应视频对象，说明对象写入已经成功或接近成功，失败发生在上传接口响应返回给浏览器的链路上。

# 复现步骤

1. 打开生产环境管理端。
2. 进入 SKU 管理或其他支持视频上传的页面。
3. 选择一个合法视频文件上传，例如符合 `ALLOWED_VIDEO_TYPES` 且未超过 `MAX_VIDEO_SIZE_MB` 的视频。
4. 观察前端上传进度停留在 99%。
5. 浏览器 Network 中查看上传请求状态，确认返回 `504 Gateway Time-out`。
6. 登录腾讯 COS 控制台，检查目标 Bucket 下是否已出现 `videos/default/tiles/{tile_id|pending}/{uuid}.{ext}` 对象。
7. 检查外层 HTTPS Nginx、容器内 Web Nginx、backend 与 COS SDK 日志。

# 期望结果

- 生产管理端上传合法视频后，接口应稳定返回 `200`。
- 响应体应包含 `object_key` 与 `/media/{object_key}`，前端可把该视频加入 SKU 表单。
- COS 写入成功后，反代链路不应因默认 60 秒超时返回 `504` 或产生 Nginx `499`。
- 大文件上传相关超时时间应可按部署环境配置，避免生产环境只能修改硬编码 Nginx 配置。
- 上传失败时不应留下大量无法被业务引用的 COS 孤儿对象。

# 实际结果

- 浏览器上传请求返回 `504 Gateway Time-out`。
- 腾讯 COS 中实际已有对应文件。
- Nginx 日志显示请求体被缓冲到临时文件：

```text
client request body is buffered to a temporary file /var/cache/nginx/client_temp/0000000005
```

- 同一上传请求约 60 秒后记录为 `499`：

```text
POST /api/v1/admin/uploads/tile-videos?tile_id=3 HTTP/1.0" 499
```

该时间特征与 Nginx、外层 HTTPS 反代、CDN 或负载均衡默认 60 秒 upstream 超时高度一致。

# 影响范围

- 影响端：管理端 Web。
- 影响环境：生产环境。
- 影响能力：SKU 视频上传、COS 对象存储写入后的上传结果确认。
- 影响用户：管理员无法在页面上确认视频上传成功，无法把已上传视频加入 SKU 表单并保存。
- 潜在副作用：用户重复上传会在 COS 中留下多个孤儿视频对象；这些对象已占用存储空间，但没有被 SKU 业务数据引用。
- 横向风险：如果图片、证书等文件上传耗时超过反代超时，也可能出现类似“对象已写入但前端失败”的问题；视频文件更容易触发。

# 严重等级说明

严重等级为 `high`。该问题发生在生产环境，直接影响管理端视频上传闭环。虽然 COS 写入成功意味着数据没有完全丢失，但前端无法拿到返回结果，业务上等价于上传失败，并会造成孤儿对象堆积。视频是 SKU 展示的重要媒体资产，应优先修复。

# 初步分析

当前上传链路为：

```text
浏览器 HTTPS 请求
→ 外层 HTTPS Nginx
→ 容器内 Web Nginx
→ FastAPI backend
→ 腾讯 COS S3 兼容 put_object
→ backend 返回 { object_key, url }
→ Nginx 返回浏览器
```

已知证据显示 COS 中已有文件，因此更可能的问题不是 COS 写入失败，而是写入 COS 的总耗时或响应返回耗时超过反代超时。容器内 `src/web/nginx.conf` 目前仅配置 `client_max_body_size 512m`，`/api/` 反代没有显式 `proxy_read_timeout`、`proxy_send_timeout` 或上传专用 location。用户提供的外层 HTTPS Nginx 配置中，443 server 仅有 `client_max_body_size 100m` 和通用 `location /`，也没有上传专用超时。

本次修复方向应包括：

1. 外层 HTTPS 反代对 `/api/v1/admin/uploads/` 配置更长的上传/上游响应超时，例如 300s 或 600s。
2. 容器内 Web Nginx 同步对 `/api/v1/admin/uploads/` 配置专用超时，避免外层放宽后又被内层默认超时截断。
3. 评估是否为上传路径配置 `proxy_request_buffering off`，降低大文件先落 Nginx 临时文件再转发 backend 的串行耗时。
4. 将上传超时时间做成环境变量或部署参数，便于不同生产环境按网络与对象存储性能调整。

# 关于超时时间环境变量化

可以做成环境变量配置，而且建议在正式修复中纳入。原因是不同部署环境的外层 Nginx、网络带宽、COS 区域、文件大小上限和磁盘性能不同，固定写死 `600s` 不利于运维调整。

建议后续 OpenSpec 修复中明确：

- `.env.example` 增加上传反代超时变量，例如 `UPLOAD_PROXY_READ_TIMEOUT_SECONDS`、`UPLOAD_PROXY_SEND_TIMEOUT_SECONDS`、`UPLOAD_CLIENT_BODY_TIMEOUT_SECONDS`。
- 生产 Compose 或 Web 容器启动流程支持把环境变量渲染进 Nginx 配置。
- 文档同步说明外层 HTTPS 反代也必须配置相同或更长的超时。
- 默认值可设为 `600` 秒，且不得小于大文件上传实际需要的生产超时。

需要注意：Nginx 原生配置文件不能直接读取普通 Docker 环境变量，通常需要使用模板渲染、`envsubst`、入口脚本或镜像构建时生成配置。因此这不是只改 `.env.example` 就能生效的变更，需要后续通过 OpenSpec Change 设计与实现。

# 建议后续验证

1. 在外层 HTTPS Nginx 为 `/api/v1/admin/uploads/` 增加 600 秒级别超时后，上传同一视频验证是否仍返回 504。
2. 在容器内 Web Nginx 增加相同上传专用 location 后，重建并重启 Web 镜像。
3. 验证浏览器 Network 返回 `200`，响应体包含 `object_key`、`url`。
4. 验证 SKU 表单中新增视频可见，并能保存到 SKU 数据。
5. 验证上传返回的 `/media/{object_key}` 可读取。
6. 检查 COS 是否不再产生重复孤儿对象。
