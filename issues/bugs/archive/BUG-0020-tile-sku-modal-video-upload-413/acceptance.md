---
bug_id: BUG-0020-tile-sku-modal-video-upload-413
status: pending_review
created_at: 2026-06-27 15:23:29
updated_at: 2026-06-27 15:23:29
related_requirement: REQ-0006-tile-sku-management
---

# 回归验收标准

> 修复本缺陷 MUST 满足 REQ-0006 **AC-035** 在 Docker Web 入口下的 **可上传性**，并落实 **图片/视频格式与大小四类 env 可配置**。  
> **Scope**：代理层 413 + 后端/env 上传限制对齐；**不包含** BUG-0018 上传成功后的弹窗回显（另验）。

## AC-001 Docker 路径大体积 MP4 MUST 上传成功

**Given** Docker Compose 已启动，admin 访问 `http://localhost:3000`  
**And** `.env` 中 `MAX_VIDEO_SIZE_MB` 为默认值（500）或项目约定值  
**When** 在 SKU 弹窗「商品视频」上传 **2MB～50MB** 合法 MP4（`ALLOWED_VIDEO_TYPES` 内 MIME）  
**Then** `POST /api/v1/admin/uploads/tile-videos` MUST 返回 **200**  
**And** 响应 `data` MUST 含有效 `object_key` 与 `url`  
**And** MUST NOT 返回 **413 Request Entity Too Large**

## AC-002 Nginx body 限制 MUST 与 env 对齐

**Given** `src/web/nginx.conf` 已随修复部署  
**When** 检查 Web 容器 Nginx 配置  
**Then** `client_max_body_size` MUST ≥ `max(MAX_IMAGE_SIZE_MB, MAX_VIDEO_SIZE_MB)`（默认配置下 ≥ 500MB，如 `512m`）  
**And** `docs/standards/file-upload.md` MUST 说明该对齐关系

## AC-003 图片上传大小与格式 MUST 由 env 控制

**Given** 后端读取 `.env` 中 `MAX_IMAGE_SIZE_MB` 与 `ALLOWED_IMAGE_TYPES`  
**When** 经 `localhost:3000` 上传品牌 Logo 或 SKU 图片  
**Then** MIME 不在白名单 MUST 返回 **400** + `FILE_TYPE_NOT_ALLOWED`（50002）  
**And** 超过 `MAX_IMAGE_SIZE_MB` MUST 返回 **400** + `FILE_SIZE_EXCEEDED`（50003）  
**And** 合法图片在限制内 MUST 返回 **200**（经 Nginx 反代，非 413）

## AC-004 视频上传大小与格式 MUST 由 env 控制

**Given** 后端读取 `.env` 中 `MAX_VIDEO_SIZE_MB` 与 `ALLOWED_VIDEO_TYPES`  
**When** 经 `localhost:3000` 上传 SKU 视频  
**Then** MIME 不在白名单 MUST 返回 **400** + `50002`  
**And** 超过 `MAX_VIDEO_SIZE_MB` MUST 返回 **400** + `50003`（非 Nginx 413）  
**And** 修改 env 中 `ALLOWED_VIDEO_TYPES`（如仅 `video/quicktime`）后，对应 MIME MUST 按新白名单生效（需重启 backend）

## AC-005 env 示例与 Docker 后端配置 MUST 同步

**Given** 修复已合并  
**When** 检查配置文件  
**Then** 根目录 `.env.example` MUST 含 `MAX_IMAGE_SIZE_MB`、`MAX_VIDEO_SIZE_MB`、`ALLOWED_IMAGE_TYPES`、`ALLOWED_VIDEO_TYPES`  
**And** `src/backend/.env.docker` MUST 与上述变量一致或子集说明  
**And** MUST NOT 保留未接入代码的误导项（如孤立的 `MAX_UPLOAD_SIZE_MB` 作为唯一上限）

## AC-006 回归：小文件与其它上传端点

**Given** 缺陷修复已合并  
**When** 经 `localhost:3000` 上传小 MP4（< 1MB）、SKU 图片、品牌 Logo  
**Then** 原有上传成功路径 MUST 无回归  
**And** BUG-0011 弹窗滚动、SKU 图片主图逻辑 MUST 无回归

## AC-007 测试与 Change 记录

**Given** 进入 `fix-tile-sku-modal-video-upload-413`（或等价 fix-* Change）  
**When** 完成 `/opsx-apply`  
**Then** MUST 补充后端测试：视频/图片超限、`ALLOWED_*_TYPES` 可配置  
**And** MUST 在 Change `trace.md` 记录 Docker 路径大 MP4 手工验收（文件大小、Network 状态码）  
**And** 修改 `nginx.conf` 后验收说明 MUST 注明 **重建 Web 镜像**

## AC-008 REQ-0006 AC-035 可上传性对齐

**Given** BUG-0020 修复完成  
**When** 对照 REQ-0006 AC-035「支持上传多个视频」  
**Then** 在 **Docker Web 入口** 下上传多个合法 MP4 MUST 均可成功到达后端并返回 `object_key`  
**And** 即时回显与上传状态仍由 BUG-0018 / 既有前端能力验收（本 BUG 不重复判 UI）
