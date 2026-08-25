---
bug_id: BUG-0139-admin-avatar-upload-nginx-redirect-cors
status: captured
created_at: 2026-08-25 14:36:24
updated_at: 2026-08-25 14:36:24
severity_hint: high
environment: docker
related_requirement:
related_bug:
lifecycle_stage: plan
---

# 现象

管理后台上传用户头像时，浏览器发起 `POST http://localhost:3000/api/v1/admin/uploads` 后收到 `301 Moved Permanently`，随后跳转到 `http://localhost/api/v1/admin/uploads/`。重定向后的 URL 丢失宿主机端口 `3000`，浏览器将后续请求判定为跨源并拦截，控制台显示 CORS 预检失败。

# 复现步骤

1. 在 Docker Web 入口访问管理后台，例如 `http://localhost:3000/admin/users`。
2. 打开用户创建或编辑弹窗。
3. 选择头像文件并触发上传。
4. 在浏览器 Network 中观察 `POST /api/v1/admin/uploads` 与后续 `OPTIONS /api/v1/admin/uploads/` 请求。

# 期望 vs 实际

- 期望：头像上传请求应由 Web Nginx 同源反代到后端，不发生端口丢失的跨源跳转；上传成功后返回头像对象 key 与 `/media/...` URL。
- 实际：`POST /api/v1/admin/uploads` 被 Nginx 301 重定向到 `http://localhost/api/v1/admin/uploads/`，端口从 `3000` 丢失为默认 `80`，导致浏览器 CORS 拦截，头像上传失败。

# 影响范围

- 管理后台用户创建 / 编辑弹窗头像上传。
- `src/web/nginx.conf` 与 `src/web/nginx.conf.template` 中上传专用反向代理路径。
- Docker Web 入口 `HOST_PORT_WEB=3000` 或其他非 80 宿主机端口场景。

# 初步线索

- 前端 Orval 生成客户端调用无尾斜杠路径：`POST /api/v1/admin/uploads`。
- 后端头像上传路由定义为 `/api/v1/admin/uploads`。
- Web Nginx 上传专用代理当前只显式匹配 `/api/v1/admin/uploads/`，疑似触发 Nginx 自动补尾斜杠重定向。
- 用户截图显示重定向前请求为 `http://localhost:3000/api/v1/admin/uploads`，重定向后为 `http://localhost/api/v1/admin/uploads/`。

# 建议验收或复现要点

- [ ] 修复前确认 Network 中 `POST /api/v1/admin/uploads` 返回 `301`，且 `Location` 丢失 `:3000`。
- [ ] 修复后确认 `POST /api/v1/admin/uploads` 不再返回 301，也不触发跨源 `OPTIONS` 拦截。
- [ ] 通过管理后台用户创建或编辑弹窗上传 JPG / PNG / WebP 头像，确认返回对象 key 与预览 URL。
- [ ] 覆盖 Docker Web Nginx 配置测试，确保无尾斜杠上传路径也进入专用上传代理。

# 附件

- 用户提供截图：浏览器 Network 显示 `POST http://localhost:3000/api/v1/admin/uploads` 返回 `301 Moved Permanently`，后续跳转到 `http://localhost/api/v1/admin/uploads/` 并触发 CORS 拦截。
