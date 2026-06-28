---
bug_id: BUG-0020-tile-sku-modal-video-upload-413
status: captured
created_at: 2026-06-27 14:01:38
updated_at: 2026-06-27 14:01:38
severity_hint: high
environment: local|docker
related_requirement: REQ-0006-tile-sku-management
related_bug: BUG-0018-tile-sku-modal-video-upload-display
---

# 现象

瓷砖 SKU 新增/编辑弹窗（`/admin/tile-skus`）中上传商品视频时请求失败，浏览器 Network 显示 `413 Request Entity Too Large`，视频无法上传。

# 复现步骤

1. 以 admin 登录 Web 管理端（`http://localhost:3000`）。
2. 进入瓷砖 SKU 列表页，点击「新增 SKU」或某行「编辑」，打开 SKU 弹窗。
3. 滚动至「商品视频」区块，点击「上传视频」，选择 MP4 文件（体积超过 Nginx/代理默认 body 限制，常见为 >1MB）。
4. 观察 Network：`POST http://localhost:3000/api/v1/admin/uploads/tile-videos?tile_id=2` 返回 **413 Request Entity Too Large**。

# 期望 vs 实际

| | 说明 |
|---|---|
| **期望** | 合法 MP4 视频（在后端 `MAX_VIDEO_SIZE_MB` 等业务限制内）应成功上传至对象存储，接口返回 200 及视频元数据。 |
| **实际** | 请求在 Web 入口（`localhost:3000` 经 Nginx 反代）被拒绝，返回 413，上传失败。 |

# 初步线索

- 请求 URL 为 `localhost:3000`（Web/Nginx），非直连后端 `8000`。
- `src/web/nginx.conf` 的 `/api/` 反代未配置 `client_max_body_size`（Nginx 默认约 1MB）。
- 后端 `MAX_VIDEO_SIZE_MB=500`（`src/backend/.env.example`），前后限制不一致可能导致大文件在代理层被拒。

# 附件

- 暂无截图；用户已提供 Network 413 与请求 URL。
