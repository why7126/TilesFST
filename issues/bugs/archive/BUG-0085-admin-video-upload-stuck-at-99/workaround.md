---
bug_id: BUG-0085-admin-video-upload-stuck-at-99
title: 管理后台视频上传长时间卡在 99% 临时规避方案
status: done
created_at: 2026-07-24 20:36:23
updated_at: 2026-07-26 15:25:45
severity: high
related_requirement:
related_bug: BUG-0081-prod-cos-video-upload-fails
related_change:
---

# Workaround - BUG-0085 管理后台视频上传长时间卡在 99%

## 临时处理原则

在正式修复前，不建议让前端绕过后端鉴权直传未授权对象存储，也不建议手工把 COS/TOS/MinIO 原始地址写入业务数据。所有临时处理仍应保持“管理端鉴权上传 → 后端对象存储适配层 → 返回 `/media/{object_key}`”的受控链路。

## 现场临时排查

1. 上传同一视频时打开浏览器 Network，记录 `POST /api/v1/admin/uploads/tile-videos` 的最终状态码、耗时和响应体。
2. 在对象存储控制台检查是否已经出现对应 `videos/...` 对象。
3. 查看外层 HTTPS Nginx、容器内 Web Nginx、backend 日志，重点关注 `504`、`499`、`client_temp`、对象存储超时、`对象存储不可用`。
4. 若对象已写入但浏览器失败，先不要重复多次上传，避免产生孤儿对象；记录对象 key 后等待正式修复或人工清理策略。

## 反代超时临时缓解

若确认最终是约 60 秒 `504/499`，可先按 `BUG-0081` 的经验检查并补齐生产外层 HTTPS Nginx 上传专用配置：

```nginx
location /api/v1/admin/uploads/ {
    proxy_pass http://127.0.0.1:<web-or-backend-port>/api/v1/admin/uploads/;
    proxy_request_buffering off;
    proxy_connect_timeout 60s;
    proxy_send_timeout 600s;
    proxy_read_timeout 600s;
    client_max_body_size 512m;
    client_body_timeout 600s;
    send_timeout 600s;
}
```

执行前必须先 `nginx -t`，通过后 reload。若生产部署经由 Web 容器反代到 backend，还需要确认容器内 Web Nginx 当前运行配置也包含 `/api/v1/admin/uploads/` 专用 location。

## 运维侧临时缓解

- 优先使用网络稳定、文件大小较小且符合编码规范的 MP4 做验证。
- 避免在同一视频 99% 等待期间反复刷新或重复提交。
- 若对象已写入但页面失败，记录对象 key、上传时间、文件名和请求 ID，后续用于孤儿对象清理或手工关联评估。
- 若对象存储返回权限、region 或 bucket 错误，先修正 `OBJECT_STORAGE_*` 配置与 bucket 权限，再重试。

## 不建议的绕行

- 不建议把对象存储 Bucket 改为公开写入。
- 不建议让管理端前端直接持有对象存储写入密钥。
- 不建议跳过 `/media/{object_key}` 受控读取策略。
- 不建议在未确认对象是否已写入时多次重复上传同一大视频。

## 回滚注意

若临时调整 Nginx 上传 location 后出现异常，可回滚该 location 或恢复原超时配置，但需保留 `client_max_body_size` 不低于业务上传上限。回滚后重新执行 `nginx -t` 与 reload，并记录 BUG-0085 是否复现。
