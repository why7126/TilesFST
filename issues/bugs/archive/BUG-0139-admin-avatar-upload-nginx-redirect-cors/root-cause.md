---
bug_id: BUG-0139-admin-avatar-upload-nginx-redirect-cors
document_status: ready
root_cause_status: confirmed
created_at: 2026-08-25 15:35:15
updated_at: 2026-08-25 15:36:40
---

# 根因分析

## 根因状态

`confirmed`

该 BUG 的根因已由浏览器截图、前端生成客户端、后端路由、Web Nginx 模板和 Docker 端口映射共同闭环确认。

## 直接原因

Web Nginx 上传专用代理只配置了带尾斜杠的 `location /api/v1/admin/uploads/`，而前端头像上传实际请求无尾斜杠路径 `POST /api/v1/admin/uploads`。在 Docker Web 入口下，Nginx 对无尾斜杠请求返回 `301 Moved Permanently` 补齐尾斜杠，重定向目标变成 `http://localhost/api/v1/admin/uploads/`，丢失宿主机端口 `3000`。

浏览器随后将 `http://localhost:3000` 到 `http://localhost` 识别为跨源访问，触发 CORS 预检并拦截上传链路。

## 根本原因

上传专用 Nginx location 只覆盖了带子路径或带尾斜杠的上传入口，没有覆盖头像上传的无尾斜杠根路径。该配置与 OpenAPI / Orval 生成客户端和 FastAPI 路由的路径形态不一致。

同时 Docker Web 使用宿主机端口映射 `3000 -> 80`，Nginx 生成绝对重定向 URL 时无法保留外部访问端口，放大为跨源 CORS 问题。

## 触发条件

- 通过 Docker Web 入口访问管理后台，例如 `http://localhost:3000/admin/users`。
- 在用户创建或编辑弹窗中上传头像。
- 前端调用 `POST /api/v1/admin/uploads`。
- Web Nginx 未配置 `location = /api/v1/admin/uploads` 精确匹配。
- 宿主机 Web 端口不是 `80`，例如默认 `HOST_PORT_WEB=3000`。

## 分类

- 类型：deployment / proxy-config / media-upload
- 影响端：Web 管理端、Docker Web Nginx
- 影响接口：`POST /api/v1/admin/uploads`
- 不涉及：数据库结构、后端业务路由定义、小程序运行时、对象存储 provider 变更

## 证据链

| 证据入口 | 类型 | 结论 |
|---|---|---|
| 用户截图 | 浏览器 Network 证据 | `POST http://localhost:3000/api/v1/admin/uploads` 返回 `301 Moved Permanently`，后续跳转到 `http://localhost/api/v1/admin/uploads/` 并触发 CORS 拦截。 |
| `src/web/src/shared/api/generated.ts` | 代码定位 | Orval 生成客户端调用 `POST /api/v1/admin/uploads`，无尾斜杠。 |
| `src/backend/app/api/v1/uploads.py` | 代码定位 | 后端头像上传路由为 `@router.post("")`，挂载到 `/api/v1/admin/uploads`。 |
| `src/web/nginx.conf.template` | 配置定位 | 上传专用 Nginx location 只声明 `location /api/v1/admin/uploads/`，缺少无尾斜杠精确匹配。 |
| `docker-compose.yml` | 部署配置定位 | Web 容器端口映射为 `${HOST_PORT_WEB:-3000}:80`，默认外部访问端口为 `3000`，容器内 Nginx 监听 `80`。 |

## 验证方式

修复前验证：

1. 通过 `http://localhost:3000/admin/users` 打开管理后台用户弹窗。
2. 选择头像文件上传。
3. 在浏览器 Network 中确认 `POST /api/v1/admin/uploads` 返回 `301`。
4. 查看重定向目标，确认 Location 或后续请求为 `http://localhost/api/v1/admin/uploads/` 且丢失 `:3000`。
5. 确认后续请求被浏览器 CORS 拦截。

修复后验证：

1. 通过相同 Docker Web 入口上传头像。
2. 确认 `POST /api/v1/admin/uploads` 不再返回 `301`。
3. 确认请求保持同源 `localhost:3000`，无 CORS 预检拦截。
4. 确认响应返回头像 `object_key` 与 `/media/...` URL，管理后台即时预览成功。
5. 运行 Nginx 配置测试，确认无尾斜杠路径进入上传专用代理并优先于通用 `/api/` location。

## 人工补证

当前根因已 confirmed，无必需人工补证。后续实现阶段仍建议补充修复后的 Network 截图或测试摘要作为验收证据。
