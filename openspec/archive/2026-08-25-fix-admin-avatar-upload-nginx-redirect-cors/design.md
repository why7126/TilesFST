---
change_id: fix-admin-avatar-upload-nginx-redirect-cors
source_bug: BUG-0139-admin-avatar-upload-nginx-redirect-cors
sprint: sprint-026
created_at: 2026-08-25 16:35:00
updated_at: 2026-08-25 16:35:00
---

# 设计

## 根因摘要

当前根因状态为 `confirmed`。后端上传接口注册在 `/api/v1/admin/uploads`，前端生成客户端也调用同一路径；但 Docker Web Nginx 仅对 `/api/v1/admin/uploads/` 配置上传专用代理。无尾斜杠请求在 Web 层被规范化为带尾斜杠地址并返回 301，重定向 Location 丢失宿主机端口 `3000`，浏览器随后访问 `http://localhost/api/v1/admin/uploads/` 并触发 CORS 拦截。

根本问题是 Web/Nginx 上传代理配置的 path matching 没有覆盖 API 实际无尾斜杠入口，导致上传请求在到达后端前就被重定向。

## 修复方案

1. Nginx 路径匹配
   - 在 `src/web/nginx.conf` 与 `src/web/nginx.conf.template` 增加 `/api/v1/admin/uploads` 精确匹配。
   - 精确匹配必须直接代理到后端 `/api/v1/admin/uploads`，不得通过 `return 301`、`rewrite` 或尾斜杠 location 间接跳转。
   - 精确匹配与现有 `/api/v1/admin/uploads/` location 必须共享上传专用限制和超时策略，避免头像上传修复后大文件上传能力回退。
2. 子路径保持
   - 保留 `/api/v1/admin/uploads/` location 处理品牌 Logo、Banner、SKU 图片和视频等子上传路径。
   - 子路径代理不得被更宽泛的 `/api/` location 或 SPA fallback 捕获。
3. 测试与验收
   - 用静态配置测试确认两个 Nginx 文件均包含无尾斜杠精确匹配和尾斜杠子路径匹配。
   - 用 Docker Web 或等价 Nginx smoke 确认 `POST /api/v1/admin/uploads` 首个响应不是 301，且请求不会跳转到丢失端口的 `http://localhost/...`。
   - 上传成功后继续按媒体四联模板验证对象 key、对象存在、URL 可读和管理端渲染。

## 测试设计

- Nginx 配置测试：
  - `src/web/nginx.conf` 存在 `location = /api/v1/admin/uploads`。
  - `src/web/nginx.conf.template` 存在 `location = /api/v1/admin/uploads`。
  - 两个精确匹配块包含上传专用 `client_max_body_size`、`proxy_send_timeout`、`proxy_read_timeout`、`client_body_timeout` 与 `send_timeout`。
  - 两个文件仍保留 `/api/v1/admin/uploads/` 子路径代理。
- Docker/Web smoke：
  - 登录管理员后提交头像文件到 `http://localhost:3000/api/v1/admin/uploads`。
  - 首个响应状态不为 301、302、307 或 308。
  - 浏览器 Network 或 HTTP 客户端记录中不存在 `http://localhost/api/v1/admin/uploads/`。
  - 上传响应返回的 `/media/{object_key}` 可读取。
- 回归范围：
  - 品牌 Logo、Banner、SKU 图片/视频等 `/api/v1/admin/uploads/*` 子路径继续命中上传专用代理。
  - `/media/` 代理、`/api/` 通用代理和 SPA fallback 不回退。

## 安全边界

- 前端仍通过后端鉴权上传，不能直连未授权对象存储。
- Nginx 配置和测试输出不得包含真实 `.env`、Authorization header、Cookie、对象存储 access key、secret key 或生产私有域名。
- 若 smoke 记录 object key，应按 BUG acceptance 的脱敏策略记录，避免输出真实客户数据。

## 验收方式

- 使用 BUG-0139 `acceptance.md` 中的媒体四联验收项回填 key、object、URL、render 证据。
- 运行 Nginx 配置测试与 Docker Web 上传 smoke。
- 若实现中没有 API、Schema 或错误码变化，在 trace 中明确记录不需要 OpenAPI/Orval。
