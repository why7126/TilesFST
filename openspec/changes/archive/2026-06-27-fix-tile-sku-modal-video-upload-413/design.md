## Context

- **BUG**: `BUG-0020-tile-sku-modal-video-upload-413`
- **Severity**: high
- **Root cause type**: infrastructure + config
- **Related REQ**: `REQ-0006-tile-sku-management`（AC-035 可上传性）
- **Related BUG**: `BUG-0018-tile-sku-modal-video-upload-display`（上传成功后的 UI；分层修复）
- **Parent baseline**: `fix-object-storage-upload-not-minio`（MinIO 写入）
- **Target**: `src/web/nginx.conf`、`config.py`、`uploads.py`、`storage.py`、`.env.example`

## Bug Analysis Report

### 现象

经 `localhost:3000` 上传 SKU 商品视频（典型 MP4 > 1MB）返回 **413 Request Entity Too Large**；直连 `localhost:8000` 可达后端（超限则 400 + `FILE_SIZE_EXCEEDED`）。

### 复现路径

1. Docker Compose 启动，admin 访问 `http://localhost:3000`。
2. SKU 弹窗「商品视频」选择 2MB+ MP4。
3. Network：`POST /api/v1/admin/uploads/tile-videos` → **413**（Nginx 响应）。

### 影响

- 阻塞 REQ-0006 多视频上传在 Docker/演示路径验收。
- 同一 Nginx `/api/` 反代下大图（>1MB）亦可能 413。

## Root Cause

### RC-001：Nginx 默认 body 上限约 1MB

`src/web/nginx.conf` 反代 `/api/` 时未设置 `client_max_body_size`，先于 FastAPI 拒绝大文件。

### RC-002：env 与代码不一致

`MAX_VIDEO_SIZE_MB`、`ALLOWED_*_TYPES` 在 `.env.example` 存在但未接入 `Settings`；后端曾统一 `MAX_UPLOAD_SIZE_MB`；MIME 硬编码于 `uploads.py`。

## Goals / Non-Goals

**Goals**

- Docker Web 路径下合法大体积 MP4 上传返回 200。
- 四类 env 可配置：`MAX_IMAGE_SIZE_MB`、`MAX_VIDEO_SIZE_MB`、`ALLOWED_IMAGE_TYPES`、`ALLOWED_VIDEO_TYPES`。
- Nginx body 限制与 env 上限对齐；文档说明调大 env 时须同步 Nginx 并重建 Web 镜像。

**Non-Goals**

- BUG-0018 视频区 UI 状态机（已由 `fix-tile-sku-modal-video-upload-display` 覆盖）。
- 视频转码、多清晰度、前端直连 MinIO。
- SQLite schema / SKU CRUD API 契约变更。

## Decisions

### D1：Nginx 静态 `client_max_body_size 512m`

**选择**：在 `server` 块设置 `512m`，覆盖默认 `MAX_VIDEO_SIZE_MB=500` 并留缓冲。

**备选**：运行时 envsubst 注入 — 增加 Docker 构建复杂度；本期采用静态值 + 文档说明。

### D2：分离图片/视频 env 上限与白名单

**选择**：`max_image_size_mb` / `max_video_size_mb` + 逗号分隔 MIME 字符串解析为 frozenset。

**备选**：保留单一 `MAX_UPLOAD_SIZE_MB` — 无法满足产品对视频更大上限的需求。

### D3：超限由后端返回 400，非 Nginx 413

代理层 MUST 足够大；业务超限 MUST 返回 `FILE_SIZE_EXCEEDED`（50003）与 `FILE_TYPE_NOT_ALLOWED`（50002）。

### D4：扩展名映射

`build_upload_object_key` 支持 `video/quicktime` 等 env 允许类型；未知 MIME 回退 `mimetypes.guess_extension`。

## Risks / Trade-offs

| 风险 | 缓解 |
|---|---|
| 调大 `MAX_VIDEO_SIZE_MB` 但未改 Nginx | `file-upload.md` 与 design 明确对齐关系；acceptance AC-002 |
| 修改 nginx.conf 未重建 Web 镜像 | tasks 与 release 注明 `docker compose build web` |
| 与 BUG-0018 混淆 | 分层验收：0020 验 Network 200/非 413；0018 验 UI 卡片 |

## Migration Plan

1. 合并 `nginx.conf`、`backend` 配置与 `.env.example`。
2. 运行 pytest。
3. **重建并重启 Web 容器**；backend 仅需重启（若 env 变更）。
4. 手工：Docker 路径上传 2–50MB MP4。

## Open Questions

- 无 — env 默认值与 Nginx `512m` 已在 proposal 定稿。
