---
bug_id: BUG-0139-admin-avatar-upload-nginx-redirect-cors
document_status: ready
created_at: 2026-08-25 15:35:15
updated_at: 2026-08-25 15:36:40
---

# 临时规避方案

## 可用规避

在正式修复 Nginx 配置前，可采用以下临时规避方式：

1. 使用后端 API 文档或受控脚本直接调用后端 `POST http://localhost:8000/api/v1/admin/uploads` 上传头像，取得 `object_key` 后再通过用户编辑接口保存。
2. 临时使用宿主机 `80` 端口访问 Web 容器，避免 Nginx 301 生成的 `http://localhost/...` 与页面 Origin 产生端口差异。
3. 临时改用 Vite 本地开发入口并确认 `/api` 代理直接转发到 `localhost:8000`，绕过 Docker Web Nginx 的尾斜杠重定向问题。

## 风险与限制

- 以上规避方式不适合普通管理后台用户，只适合开发或测试人员临时处理。
- 直接调用后端接口仍必须携带合法管理端鉴权，不得绕过后端上传校验。
- 临时端口或开发入口切换不能替代正式修复；Docker Web 默认入口仍会复现该问题。

## 推荐正式修复方向

在 `src/web/nginx.conf` 与 `src/web/nginx.conf.template` 中增加 `location = /api/v1/admin/uploads` 精确匹配，复用上传专用代理参数并反代到后端无尾斜杠接口，同时保留现有 `location /api/v1/admin/uploads/` 以覆盖带子路径上传接口。
