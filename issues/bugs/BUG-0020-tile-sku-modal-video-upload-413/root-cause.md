---
bug_id: BUG-0020-tile-sku-modal-video-upload-413
status: pending_review
created_at: 2026-06-27 15:23:29
updated_at: 2026-06-27 15:23:29
root_cause_type: infrastructure
---

# 根因分析

## 1. 分类

| 项 | 值 |
|---|---|
| 缺陷类型 | **infrastructure**（Docker Web Nginx 反代 body 限制）+ **config**（图片/视频上传限制未统一 env 落地） |
| 引入阶段 | 项目 Docker Compose 初建（`src/web/nginx.conf` 仅配置 `/api/` 反代，未设 `client_max_body_size`） |
| 责任模块 | `src/web/nginx.conf`、`src/backend/app/core/config.py`、`uploads.py`、`storage.py` |
| 关联前端 | `TileSkuFormModal` 仅发起上传；413 发生在代理层，前端无法修复 |

## 2. 直接原因

### 2.1 Nginx 默认 body 上限约 1MB，先于后端拒绝大文件

Docker Web 容器（`localhost:3000` → Nginx 80）将所有 `/api/` 请求反代至 `backend:8000`。修复前 `nginx.conf` **未配置** `client_max_body_size`，Nginx 默认约 **1m**。

典型 SKU 商品视频 MP4 体积通常 **数 MB～数百 MB**，请求在到达 FastAPI 之前被 Nginx 拒绝，返回 **413 Request Entity Too Large**（响应体常为 Nginx 默认 HTML，非项目 JSON 错误格式）。

对照路径：

| 入口 | 行为 |
|---|---|
| `localhost:3000`（Nginx） | > ~1MB → **413** |
| `localhost:8000`（直连后端） | 可达 FastAPI；超限 → **400** + `FILE_SIZE_EXCEEDED`（50003） |
| `localhost:5173`（Vite dev proxy） | 一般无 1MB 硬限，缺陷在 Docker 演示路径更易暴露 |

### 2.2 后端上传限制与 env 文档不一致（修复前）

修复前存在多层不一致：

| 层级 | 修复前状态 |
|---|---|
| `config.py` | 仅 `MAX_UPLOAD_SIZE_MB`（默认 50），图片/视频共用 |
| `.env.example` | 存在 `MAX_VIDEO_SIZE_MB`、`ALLOWED_*_TYPES` 等，**未接入** `Settings` |
| `uploads.py` | MIME 白名单 **硬编码**（图片 JPG/PNG/WebP；视频仅 `video/mp4`） |
| Nginx | 默认 1MB，**低于** 后端 50MB 与文档 500MB 视频上限 |

运营按文档理解「可上传大视频」，实际在代理层即失败，形成「接口存在但不可用」的假象。

### 2.3 与 BUG-0018 的叠加

BUG-0018 聚焦上传 **200 后** 弹窗无回显。本 BUG 在更底层：**请求未达后端**。用户侧可能同时看到「视频上传失败」，若仅修 0018 无法消除 413。

## 3. 根本原因

1. **部署规范缺口**：`docs/02-deployment.md` / Docker 交付未要求 Nginx `client_max_body_size` 与上传业务上限对齐；`build-*` 与 `add-tile-sku-management` 实现上传 API 时未在 Web 镜像侧同步大 body 策略。
2. **配置治理未闭环**：`rules/environment.md` 列出 `MAX_VIDEO_SIZE_MB`，但代码层长期未读取；上传校验分散在硬编码与单一 `MAX_UPLOAD_SIZE_MB`，与 `rules/media.md`「大小须受环境变量控制」不一致。
3. **测试盲区**：`test_admin_brands.py` 上传用例 payload 极小（`b"tile-video"`），未覆盖 Docker 路径下 Nginx 大 body；E2E 未在 `localhost:3000` 验证真实体积 MP4。

## 4. 触发条件

1. 使用 **Docker Compose** 或等价部署，浏览器访问 **`http://localhost:3000`**（或映射的 Web 宿主机端口）。
2. admin 登录，打开 SKU 弹窗「商品视频」，选择 **MP4** 且 **Content-Length > Nginx client_max_body_size**（默认约 1MB）。
3. 请求 `POST /api/v1/admin/uploads/tile-videos` 经 Web 反代 → **413**。

## 5. 非根因（排除）

| 假设 | 结论 |
|---|---|
| MinIO 不可用 | 否；413 出现在代理层，非 502 |
| 后端 `upload_tile_video` 逻辑错误 | 否；小文件直连 8000 可 200 |
| 前端未调用上传 API | 否；Network 可见 POST 与 413 |
| BUG-0018 回显问题 | 独立缺陷；不解释 413 |
| SQLite / SKU CRUD | 无关；上传阶段不涉及 |

## 6. 修复方向

建议 Change：`fix-tile-sku-modal-video-upload-413`（`fix-*`，关联 REQ-0006）。

1. **Nginx**：在 `server` 或 `location /api/` 设置 `client_max_body_size`，须 ≥ `max(MAX_IMAGE_SIZE_MB, MAX_VIDEO_SIZE_MB)`（默认建议 512m 覆盖 500MB 视频上限）。
2. **后端配置**：`Settings` 读取 `MAX_IMAGE_SIZE_MB`、`MAX_VIDEO_SIZE_MB`、`ALLOWED_IMAGE_TYPES`、`ALLOWED_VIDEO_TYPES`；`uploads.py` 与 `save_upload_file` 按图片/视频分别校验。
3. **文档**：同步根目录 `.env.example`、`src/backend/.env.docker`、`docs/standards/file-upload.md`；说明调大 env 上限时须同步 Nginx。
4. **测试**：补充视频超限 400（`max_video_size_mb`）、可配置 MIME、与配置解析单元测试。
5. **部署**：修改 `nginx.conf` 后须 **重建 Web 镜像**（非仅重启 backend）。

**预期修复后状态（代码线索，待 `/opsx-apply` 验收）**：`nginx.conf` 已含 `client_max_body_size 512m`；`config.py` 与四类 env 已落地——须在 Change 中归档并手工验证 Docker 路径大文件上传。
