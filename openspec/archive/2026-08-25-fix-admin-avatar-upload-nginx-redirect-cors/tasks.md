---
change_id: fix-admin-avatar-upload-nginx-redirect-cors
source_bug: BUG-0139-admin-avatar-upload-nginx-redirect-cors
sprint: sprint-026
created_at: 2026-08-25 16:35:00
updated_at: 2026-08-25 17:17:46
---

# 任务

- [x] 梳理 `src/web/nginx.conf` 与 `src/web/nginx.conf.template` 当前上传代理 location 命中顺序，确认无尾斜杠请求的 301 来源。
- [x] 为 `/api/v1/admin/uploads` 增加精确匹配代理，直接转发到后端同路径，不返回 301 或 rewrite。
- [x] 确保精确匹配块复用上传专用 `client_max_body_size`、`proxy_send_timeout`、`proxy_read_timeout`、`client_body_timeout`、`send_timeout` 与请求缓冲策略。
- [x] 保留 `/api/v1/admin/uploads/` 子路径代理，确认品牌 Logo、Banner、SKU 图片和视频上传路径不回退。
- [x] 补充 Nginx 配置回归测试，覆盖 `nginx.conf` 与 `nginx.conf.template` 中无尾斜杠精确匹配和尾斜杠子路径代理。
- [x] 运行聚焦测试，至少覆盖新增 Nginx 配置测试；若测试框架已有 Docker/Web smoke，补充头像上传 smoke。
- [x] 执行 Docker Compose 或生产等价 Web 上传 smoke，确认 `POST /api/v1/admin/uploads` 首个响应不为 301/302/307/308，且没有跳转到丢失端口的 `http://localhost/...`。
- [x] 上传成功后回填媒体四联验收证据：`object_key`、对象存在性、`/media/{object_key}` 读取、管理端头像上传渲染。
- [x] 确认 API、数据库、OpenAPI、Orval 均不需要变更；若实现发现实际需要变更，先同步相关文档和测试。
- [x] 评估是否需要更新 `docs/knowledge-base/best-practices/admin-media-upload-chain.md`；若无新增可复用经验，记录不沉淀原因。
