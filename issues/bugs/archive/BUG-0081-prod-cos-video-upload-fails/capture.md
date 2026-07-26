---
bug_id: BUG-0081-prod-cos-video-upload-fails
title: 生产环境腾讯 COS 视频上传失败
status: done
created_at: 2026-07-23 08:37:33
updated_at: 2026-07-23 10:08:26
severity_hint: high
environment: 生产环境
source: 用户反馈
source_command: /bug-capture
related_requirement:
related_bug:
---

# 现象

生产环境中，使用腾讯 COS 作为对象存储时，视频上传失败；前端上传进度卡在 99%，浏览器返回 `504 Gateway Time-out`，但腾讯 COS 中实际已经出现对应文件。

# 复现步骤

1. 打开生产环境管理端。
2. 进入 SKU 或其他支持视频上传的业务页面。
3. 选择一个允许类型与大小范围内的视频文件上传。
4. 观察上传进度卡在 99%，浏览器请求最终返回 `504 Gateway Time-out`。
5. 检查腾讯 COS Bucket，确认对应对象实际已经写入。
6. 检查 Web Nginx access/error 日志与后端日志。

# 期望 vs 实际

期望：生产环境管理端可通过后端鉴权上传视频，后端将对象写入腾讯 COS 对应 Bucket 与 `videos/` 前缀，并返回 `/media/{object_key}` 受控读取地址。

实际：视频上传失败，前端进度卡在 99%，浏览器显示 `504 Gateway Time-out`；腾讯 COS 中已有对应文件。Nginx 日志显示上传请求体被缓冲到 `/var/cache/nginx/client_temp/...`，随后该请求在约 60 秒后记录为 `499`。该现象倾向说明对象写入已成功或接近成功，但后端成功响应未能在反向代理/客户端超时窗口内返回，优先怀疑上传链路的 `proxy_read_timeout` / `proxy_send_timeout` / 外层网关超时或 COS SDK 写入完成后响应等待过久。

# 附件

- 用户原始反馈：`生产环境，视频上传失败，腾讯COS`
- 用户补充反馈：`上传进度卡在99%`
- 浏览器请求：`POST https://tilesfst.wjoyhappy.site/api/v1/admin/uploads/tile-videos?tile_id=3`，状态 `504 Gateway Time-out`
- 现场证据：腾讯 COS 中已有对应文件
- Nginx 证据：`client request body is buffered to a temporary file /var/cache/nginx/client_temp/0000000005`；同一上传请求约 60 秒后记录 `499`
- 待补充：失败接口 request_id、后端应用日志、视频大小、视频 MIME、当前生产 `OBJECT_STORAGE_*` 非敏感配置摘要、外层网关或宿主机反代超时配置。
