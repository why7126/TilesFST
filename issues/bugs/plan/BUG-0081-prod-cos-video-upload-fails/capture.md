---
bug_id: BUG-0081-prod-cos-video-upload-fails
title: 生产环境腾讯 COS 视频上传失败
status: captured
created_at: 2026-07-23 08:37:33
updated_at: 2026-07-23 08:37:33
severity_hint: high
environment: 生产环境
source: 用户反馈
source_command: /bug-capture
related_requirement:
related_bug:
---

# 现象

生产环境中，使用腾讯 COS 作为对象存储时，视频上传失败。

# 复现步骤

1. 打开生产环境管理端。
2. 进入 SKU 或其他支持视频上传的业务页面。
3. 选择一个允许类型与大小范围内的视频文件上传。
4. 观察上传请求、前端提示、后端日志与腾讯 COS 对象写入结果。

# 期望 vs 实际

期望：生产环境管理端可通过后端鉴权上传视频，后端将对象写入腾讯 COS 对应 Bucket 与 `videos/` 前缀，并返回 `/media/{object_key}` 受控读取地址。

实际：视频上传失败。暂未确认失败发生在 Web Nginx 请求体限制、后端 MIME/大小校验、FastAPI 到 COS 的 S3 兼容 `put_object`、COS endpoint/region/TLS/path-style 配置、Bucket 权限或网络白名单环节。

# 附件

- 用户原始反馈：`生产环境，视频上传失败，腾讯COS`
- 待补充：失败接口状态码、响应错误码、request_id、后端日志、COS 错误码、视频大小、视频 MIME、当前生产 `OBJECT_STORAGE_*` 非敏感配置摘要。
