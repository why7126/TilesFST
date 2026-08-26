---
bug_id: BUG-0139-admin-avatar-upload-nginx-redirect-cors
title: 管理后台头像上传被 Nginx 301 重定向丢端口导致 CORS 拦截
severity: high
status: done
owner:
discovered_at: 2026-08-25 14:36:24
created_at: 2026-08-25 15:25:49
updated_at: 2026-08-25 17:43:45
environment: docker
related_requirement:
related_change: fix-admin-avatar-upload-nginx-redirect-cors
---

# 现象

管理后台上传用户头像时，前端发起 `POST http://localhost:3000/api/v1/admin/uploads`。请求没有进入预期的同源上传代理链路，而是先收到 `301 Moved Permanently`，随后浏览器跳转到 `http://localhost/api/v1/admin/uploads/`。

重定向后的地址丢失宿主机端口 `3000`，浏览器将 `localhost:3000` 到 `localhost:80` 判定为跨源访问，后续预检请求被 CORS 策略拦截，头像上传失败。

# 复现步骤

1. 使用 Docker Web 入口访问管理后台，例如 `http://localhost:3000/admin/users`。
2. 打开用户创建或编辑弹窗。
3. 选择 JPG / PNG / WebP 头像文件并触发上传。
4. 在浏览器 Network 中查看 `POST /api/v1/admin/uploads` 请求。
5. 观察该请求返回 `301 Moved Permanently`，并继续跳转到 `http://localhost/api/v1/admin/uploads/`。
6. 观察后续 `OPTIONS /api/v1/admin/uploads/` 或相关请求被浏览器以 CORS 原因拦截。

# 期望结果

- `POST /api/v1/admin/uploads` 应由 Web Nginx 在同源下直接反代到后端头像上传接口。
- 上传链路不应发生丢失宿主机端口的 301 重定向。
- 管理后台应成功获得头像对象 key 与 `/media/...` 访问 URL，并刷新头像预览。

# 实际结果

- `POST /api/v1/admin/uploads` 返回 `301 Moved Permanently`。
- 重定向目标变为 `http://localhost/api/v1/admin/uploads/`，端口从 `3000` 丢失为默认 `80`。
- 浏览器判定跨源请求，CORS 预检失败，用户头像上传失败。

# 影响范围

- 管理后台用户创建弹窗的头像上传。
- 管理后台用户编辑弹窗的头像上传。
- 使用 Docker Web 入口且宿主机 Web 端口不是 `80` 的本地 / 演示环境。
- 依赖 `/api/v1/admin/uploads` 无尾斜杠路径的头像上传链路。

品牌 Logo、Banner、瓷砖图片、瓷砖视频等带子路径的上传接口不一定受同一问题影响，但需要在修复验证时确认上传专用 Nginx 代理顺序没有回归。

# 严重等级说明

严重等级为 `high`。该问题阻断管理后台用户头像上传的核心操作，且表现为浏览器层 CORS 拦截，普通用户无法通过重试解决。影响范围集中在 Docker Web 入口和头像上传路径，不直接影响后端头像接口定义、数据库结构或其他业务数据读写。

# 已知证据

- 用户截图显示 `POST http://localhost:3000/api/v1/admin/uploads` 返回 `301 Moved Permanently`。
- 用户截图显示后续请求跳转到 `http://localhost/api/v1/admin/uploads/`，丢失 `:3000`。
- 前端生成客户端调用无尾斜杠路径：`POST /api/v1/admin/uploads`。
- 后端头像上传路由挂载后为 `/api/v1/admin/uploads`。
- Web Nginx 上传专用代理当前只显式匹配带尾斜杠的 `/api/v1/admin/uploads/`。

# 验收要点

- [ ] 修复前可稳定复现 `POST /api/v1/admin/uploads` 返回 `301` 且 Location 丢失宿主机端口。
- [ ] 修复后 `POST /api/v1/admin/uploads` 不再返回 `301`。
- [ ] 修复后头像上传不触发跨源 CORS 拦截。
- [ ] 修复后管理后台创建 / 编辑用户时可上传头像并看到预览。
- [ ] Nginx 配置测试覆盖无尾斜杠上传路径，确认该路径优先于通用 `/api/` 代理并复用上传专用超时 / body 限制配置。
openspec_changes:
  - change_id: fix-admin-avatar-upload-nginx-redirect-cors
    type: update
    status: archived
