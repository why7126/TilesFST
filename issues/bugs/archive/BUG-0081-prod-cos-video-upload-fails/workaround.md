---
bug_id: BUG-0081-prod-cos-video-upload-fails
status: done
created_at: 2026-07-23 09:00:31
updated_at: 2026-07-23 10:08:26
workaround_available: true
related_requirement:
related_change: fix-upload-proxy-timeout-config
---

# Workaround - BUG-0081 生产环境腾讯 COS 视频上传 99% 后返回 504

## 临时规避方案

当前可用的临时规避是先在生产外层 HTTPS Nginx 与容器内 Web Nginx 同时放宽上传路径的反代超时。

### 外层 HTTPS Nginx

在 `tilesfst.wjoyhappy.site` 的 443 server 中，将 `client_max_body_size` 调整到不小于项目视频上传上限，并在通用 `location /` 前增加上传专用 location：

```nginx
client_max_body_size 512m;
client_body_timeout 600s;
send_timeout 600s;

location /api/v1/admin/uploads/ {
    proxy_pass http://127.0.0.1:3000/api/v1/admin/uploads/;

    client_max_body_size 512m;
    client_body_timeout 600s;
    proxy_connect_timeout 60s;
    proxy_send_timeout 600s;
    proxy_read_timeout 600s;
    send_timeout 600s;

    proxy_request_buffering off;

    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto https;
    proxy_set_header X-Forwarded-Host $host;
}
```

改完后执行：

```bash
nginx -t
systemctl reload nginx
```

### 容器内 Web Nginx

在 `src/web/nginx.conf` 的通用 `location /api/` 前增加上传专用 location，生产镜像重建前也可以先在容器或挂载配置中进行等价热修：

```nginx
location /api/v1/admin/uploads/ {
    proxy_pass http://backend:8000/api/v1/admin/uploads/;

    client_max_body_size 512m;
    client_body_timeout 600s;
    proxy_connect_timeout 60s;
    proxy_send_timeout 600s;
    proxy_read_timeout 600s;
    send_timeout 600s;

    proxy_request_buffering off;

    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

正式重建方式：

```bash
docker compose -f docker-compose.prod.external.yml build web
docker compose -f docker-compose.prod.external.yml up -d web
```

若生产使用的不是 `docker-compose.prod.external.yml`，需替换为实际 Compose 文件。

## 孤儿对象临时处理

在修复前，若前端已返回 504 但 COS 中出现对象：

1. 不建议管理员反复上传同一个大视频。
2. 记录本次对象 key、上传时间、文件大小和操作者。
3. 若 SKU 页面没有保存该视频，后续可通过对象 key 与数据库引用关系清理未引用视频对象。
4. 暂不建议直接把 COS 原始地址手工写入业务数据，避免绕过 `/media/{object_key}` 受控读取策略。

## 不建议的规避

- 不建议把腾讯 COS Bucket 改成公开写入或让前端直传未授权 COS。
- 不建议降低视频大小上限来掩盖超时问题，除非作为非常短期的运维止血。
- 不建议只改外层 Nginx 而不改容器内 Web Nginx；外层放宽后仍可能被内层默认 60 秒截断。
- 不建议只修改 `.env.example` 期望 Nginx 自动读取环境变量；Nginx 配置需要模板渲染或启动脚本。

## 回滚策略

若调整超时后出现异常，可回滚上传专用 location 或移除 `proxy_request_buffering off`，保留 `client_max_body_size` 与基础反代配置。回滚后需重新执行 `nginx -t` 与 reload，并记录是否再次出现 504/499。
