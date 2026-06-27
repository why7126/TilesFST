## Why

[BUG-0020-tile-sku-modal-video-upload-413](issues/bugs/BUG-0020-tile-sku-modal-video-upload-413/) 已评审通过并纳入 `sprint-002`。瓷砖 SKU 弹窗经 Docker Web 入口（`http://localhost:3000`）上传商品视频时，`POST /api/v1/admin/uploads/tile-videos` 返回 **413 Request Entity Too Large**，典型 MP4 无法到达 FastAPI。根因为 Web 容器 Nginx 未配置 `client_max_body_size`（默认约 1MB），且图片/视频上传大小与 MIME 白名单未通过环境变量统一落地。该缺陷阻塞 REQ-0006 **AC-035** 在 Docker 演示路径下的端到端可上传性，与 BUG-0018（上传成功后的 UI 回显）为不同修复层。

## What Changes

- 在 `src/web/nginx.conf` 设置 `client_max_body_size`，须 ≥ `max(MAX_IMAGE_SIZE_MB, MAX_VIDEO_SIZE_MB)`（默认建议 `512m`）。
- 后端 `Settings` 读取 `MAX_IMAGE_SIZE_MB`、`MAX_VIDEO_SIZE_MB`、`ALLOWED_IMAGE_TYPES`、`ALLOWED_VIDEO_TYPES`；`uploads.py` 与 `save_upload_file` 按图片/视频分别校验。
- 同步根目录 `.env.example`、`src/backend/.env.docker`、`docs/standards/file-upload.md`。
- 补充 pytest：视频/图片超限、可配置 MIME 白名单、配置解析。
- Docker 路径手工验收：2MB～50MB MP4 经 `localhost:3000` 返回 200（非 413）；修改 Nginx 后 **须重建 Web 镜像**。
- **Scope**：代理层 413 + env 上传限制；不包含 BUG-0018 弹窗回显 UI（已独立 change）。

## Capabilities

### New Capabilities

（无 — 本 change 修复既有上传与部署约束，不引入新 capability 域。）

### Modified Capabilities

- `object-storage`：新增/明确图片与视频上传大小、MIME 白名单须由环境变量配置并由后端强制执行。
- `web-client`：Docker Compose Web 入口 Nginx 反代 MUST 允许不小于后端/env 上限的请求 body。

## Impact

| 影响面 | 说明 |
|---|---|
| Web 部署 | `src/web/nginx.conf`；Docker Web 镜像须重建 |
| 后端 | `config.py`、`uploads.py`、`storage.py`；无 API schema 变更 |
| 环境变量 | 根目录 `.env.example`、`src/backend/.env.docker` |
| REQ-0006 | AC-035 Docker 路径可上传多个 MP4 |
| 数据库 / Orval | 不变 |
| 小程序 / 店主端 | 不涉及 |
| 测试 | pytest `test_admin_brands.py`、`test_upload_settings.py` |
| 关联 BUG | BUG-0018（同链路、UI 层）；BUG-0006 MinIO 基线 |

## Rollback Plan

1. 恢复 `nginx.conf` 至无 `client_max_body_size` 或较小值（仅应急）。
2. 恢复 `config.py` / `uploads.py` 至统一 `MAX_UPLOAD_SIZE_MB` 与硬编码 MIME（若曾存在）。
3. 恢复 `.env.example` 与文档。
4. 回滚后重新标记 `BUG-0020` 未修复；**不得**回滚 MinIO 写入链路（BUG-0006）。
