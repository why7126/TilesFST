---
bug_id: BUG-0020-tile-sku-modal-video-upload-413
title: SKU弹窗视频上传返回413 Request Entity Too Large
severity: high
status: draft
owner: product
discovered_at: 2026-06-27 14:01:38
environment: local|docker
related_requirement: REQ-0006-tile-sku-management
related_change: null
related_bug: BUG-0018-tile-sku-modal-video-upload-display
---

# 缺陷说明

瓷砖 SKU 新增/编辑弹窗（`TileSkuFormModal`，`/admin/tile-skus`）中上传商品视频时，经 Docker Web 入口（`http://localhost:3000`）发起的 `POST /api/v1/admin/uploads/tile-videos` 返回 **413 Request Entity Too Large**，视频无法上传至对象存储。典型 MP4 体积远大于 Nginx 默认 body 上限（约 1MB），导致 REQ-0006 多视频管理（AC-035）在 Docker/演示部署路径下不可用。

> **Scope 说明**：本 BUG 聚焦 **上传请求在 Web/Nginx 反代层被拒绝**（413）及 **图片/视频上传格式与大小须可通过环境变量配置并与代理层对齐**；不包含 BUG-0018 所覆盖的「上传成功但弹窗内无即时回显」。

# 复现步骤

1. 以 admin 登录 Web 管理端（Docker Compose，`http://localhost:3000`）。
2. 进入「瓷砖 SKU」列表页（`/admin/tile-skus`），点击「新增 SKU」或某行「编辑」，打开 SKU 弹窗。
3. 滚动至「商品视频」区块，点击「上传视频」，选择合法 **MP4** 文件（体积通常 > 1MB，例如 2–50MB）。
4. 观察 Network：`POST http://localhost:3000/api/v1/admin/uploads/tile-videos?tile_id=<id>` 返回 **413 Request Entity Too Large**。
5. （对照）同一文件直连 `http://localhost:8000/api/v1/admin/uploads/tile-videos` 通常可到达后端（超限则返回 400 + `FILE_SIZE_EXCEEDED`，非 413）。

# 期望结果

- 在 `MAX_VIDEO_SIZE_MB` 与 `ALLOWED_VIDEO_TYPES` 环境变量配置范围内，合法 MP4 视频经 `localhost:3000` 上传 **MUST 成功**，接口返回 200 及 `object_key` / `url`。
- 图片上传 **MUST** 受 `MAX_IMAGE_SIZE_MB` 与 `ALLOWED_IMAGE_TYPES` 约束；视频上传 **MUST** 受 `MAX_VIDEO_SIZE_MB` 与 `ALLOWED_VIDEO_TYPES` 约束；四类限制 **MUST** 可通过 `.env` 配置。
- Web 容器 Nginx `client_max_body_size` **MUST** ≥ `max(MAX_IMAGE_SIZE_MB, MAX_VIDEO_SIZE_MB)`，避免代理层先于后端拒绝大文件。
- 超限或 MIME 不符时由后端返回 400 及统一错误码（`50002` / `50003`），而非 Nginx 413。

# 实际结果

- 经 `localhost:3000` 上传大于约 1MB 的视频时，请求在 Nginx 反代层被拒绝，返回 **413**。
- 弹窗内显示上传失败（如「视频上传失败」），用户无法完成视频素材维护。
- 修复前：`src/web/nginx.conf` 未配置 `client_max_body_size`；后端曾统一使用 `MAX_UPLOAD_SIZE_MB`，且 `MAX_VIDEO_SIZE_MB` / `ALLOWED_*_TYPES` 未完整接入配置层，前后限制不一致。

# 影响范围

| 范围 | 影响 |
|---|---|
| Web 管理端 / SKU 新增/编辑弹窗 | 视频上传功能在 Docker 演示路径下基本不可用 |
| Web 管理端 / 其他大文件上传 | 同一 Nginx `/api/` 反代下，超过约 1MB 的图片/Logo 等亦可能 413 |
| REQ-0006 验收 | 阻塞 AC-035（多视频上传）在 `localhost:3000` 路径的端到端验收 |
| 后端 / API | 接口逻辑存在但请求可能无法到达 FastAPI |
| Vite 开发（`5173`） | 代理一般无 1MB 硬限，缺陷在 Docker Web 入口更易暴露 |
| 小程序 / 店主端 | 无直接影响 |

**与 BUG-0018 关系**

| BUG | 层级 | 说明 |
|---|---|---|
| BUG-0020（本项） | 基础设施 / 代理 + 上传限制配置 | 上传请求 413 失败 |
| BUG-0018 | 前端 UI | 上传 200 后弹窗内无文件卡片回显 |

二者可叠加：先 413 导致永远看不到成功卡片；仅修 BUG-0018 无法解决本缺陷。

# 严重等级说明

严重程度为 `high`。

理由：

- **阻塞 SKU 视频素材上传**：真实业务 MP4 几乎都超过 Nginx 默认 1MB 限制，Docker 演示与本地 Compose 路径下功能实质不可用。
- 影响 REQ-0006 核心能力 FR-005（多视频上传与管理）及 AC-035 端到端验收。
- 可稳定复现（`localhost:3000` + 常见 MP4 体积）。
- 修复面预计为 `src/web/nginx.conf`（`client_max_body_size`）、`config.py` / 上传校验与环境变量对齐；不涉及数据库 schema 变更。

# 代码线索

| 线索 | 路径 |
|---|---|
| Web Nginx 反代 | `src/web/nginx.conf`（`/api/`、`client_max_body_size`） |
| 上传端点 | `src/backend/app/api/v1/uploads.py`（`upload_tile_video` 等） |
| 大小校验 | `src/backend/app/modules/media/storage.py`（`save_upload_file`） |
| 环境配置 | `src/backend/app/core/config.py`；根目录 `.env.example` |
| SKU 弹窗上传 | `src/web/src/features/admin/components/TileSkuFormModal.tsx`（`handleVideoUpload`） |
| Docker Web | `docker-compose.yml`（`HOST_PORT_WEB` → Nginx 80） |
| 上传规范 | `docs/standards/file-upload.md`、`rules/environment.md` |
| 关联缺陷 | BUG-0018（同链路、不同层） |

# 分类结论

| 判断 | 结论 |
|---|---|
| 需求 vs 缺陷 | 缺陷（部署/代理配置与上传限制未对齐，导致既有视频上传能力不可用） |
| 根因类型 | 基础设施（Nginx body 限制）+ 配置治理（图片/视频格式与大小 env 未统一落地） |
| 建议修复 Change | `fix-tile-sku-modal-video-upload-413` 或 `fix-nginx-upload-body-size-limit` |
