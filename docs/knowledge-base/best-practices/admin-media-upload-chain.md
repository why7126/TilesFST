---
title: 管理端媒体上传全链路最佳实践
purpose: 预防 MinIO 未写入、回显失败、Nginx 413、legacy 双目录类缺陷
content: 提炼自 Sprint 002 BUG-0004~0008、0018、0019、0020
source: /sprint-exps sprint-002
update_method: 上传能力或部署变更时更新
owner: 全栈负责人
status: draft
created_at: 2026-06-27 16:15:00
updated_at: 2026-08-03 23:45:44
note: 个案见 issues/bugs/；本文写链路与检查清单
---

# 管理端媒体上传全链路最佳实践

## 链路概览

```text
浏览器 → Nginx (Web Docker) → FastAPI uploads API → MinIO 单桶
                ↓                                      ↓
         client_max_body_size                   object_key 入库
                ↓                                      ↓
         展示 URL: /media/{object_key} ← 后端代理读取 MinIO
```

## 五层必须同时验收

| 层 | 检查项 | 典型缺陷 |
|----|--------|----------|
| **前端** | 选择文件后立即上传；`idle→uploading→done/failed`；同会话即时回显 | BUG-0004、0018、0019 |
| **后端 API** | MIME 白名单；分类型大小上限；写入 MinIO 非 `UPLOAD_DIR` | BUG-0006 |
| **媒体读取** | `object_key` 与 `/media/` 代理一致；品牌/用户/SKU 列表字段回显 | BUG-0007 |
| **Nginx** | `client_max_body_size` ≥ `max(MAX_IMAGE_SIZE_MB, MAX_VIDEO_SIZE_MB)` | BUG-0020 |
| **环境与文档** | `.env.example`、`src/backend/.env.docker`、`docs/standards/file-upload.md` 同步 | BUG-0020、0008 |

## 环境变量（默认参考）

| 变量 | 用途 |
|------|------|
| `MAX_IMAGE_SIZE_MB` / `MAX_VIDEO_SIZE_MB` | 后端校验上限 |
| `ALLOWED_IMAGE_TYPES` / `ALLOWED_VIDEO_TYPES` | MIME 白名单 |
| `MINIO_BUCKET` / `MINIO_PREFIX_*` | 单桶与前缀 |

## Docker 验证清单（每个含上传的 change MUST）

1. `docker compose build tilesfst-web && docker compose up -d tilesfst-web --force-recreate`
2. 经 **`http://localhost:3000`**（非仅 8000）上传边界文件：
   - 小文件 → 200 + `object_key`
   - 超限文件 → 400 `FILE_SIZE_EXCEEDED`（非 413）
3. 列表/弹窗刷新后 URL 仍可展示

## 前端状态机参考

以 `BrandFormModal` Logo 区为 **Golden Reference**：

- 上传前进度/文案可见
- 成功后缩略图或文件卡片即时更新
- 失败在控件内展示错误，非仅全局 toast

新页面（用户头像、SKU 视频）**MUST** 复用或抽取同一 hook/组件，禁止复制简化版。

## 媒体类 BUG 四联验收映射

媒体类 BUG 修复、返修、回归测试、Sprint 验收和发布前检查 MUST 引用 `docs/standards/media-bug-four-point-acceptance-template.md`。本最佳实践中的链路检查应转化为以下四联 evidence：

| 来源检查 | 四联维度 | evidence 要求 |
|---|---|---|
| 上传状态机 `idle -> uploading -> done/failed` | `render` / `URL` | 记录上传控件状态、失败态位置、成功后的可见媒体入口；失败不能只依赖全局 toast |
| 同会话即时回显 | `render` | 管理端上传、编辑或列表刷新必须记录同一会话内的缩略图、文件卡片或媒体 URL 回显 |
| Docker Web `http://localhost:3000` 边界文件 | `URL` / `render` | 上传大小、Nginx 或 Docker Web 边界相关 BUG 必须从 Web 用户入口验证，不能只打后端 `:8000` |
| `object_key` 与 `/media/` 代理一致 | `key` / `object` / `URL` | 同时记录脱敏 key、对象存在性、HTTP 状态、业务错误码和用户可见表现 |
| MinIO 单桶、legacy 双目录清理 | `key` / `object` | 记录标准前缀、历史 key 兼容或迁移结果；禁止将 `data/uploads/` 作为新上传通过证据 |
| 小程序媒体卡片 | `render` | 记录 DevTools、真机或体验版 evidence；无法补齐时必须标记 `blocked` 或进入 Release 前检查清单 |

Sprint 015/016 媒体链路复盘进一步要求：历史对象、缩略图、回填或审计脚本相关 BUG 必须记录 dry-run、apply、幂等性或统计摘要；缩略图名义存在但尺寸/体积无收益不得写作通过；小程序 evidence 可以作为发布前补证项，但不得在缺证时写作真机通过。

## Legacy 与数据目录

- 新上传 **MUST NOT** 写入 `data/uploads/`
- legacy 清理见 `BUG-0008` 与 `fix-object-storage-legacy-upload-residue`
- `data/minio` vs `data/uploads` 职责见 `rules/data-management.md`

## 关联文档

- `docs/standards/file-upload.md`
- `docs/06-video-asset-management.md`
- `openspec/specs/object-storage/spec.md`
- `docs/knowledge-base/incidents/minio-upload-timeout.md`

## 关联 BUG（个案）

- `BUG-0006` ~ `BUG-0008`、`BUG-0018`、`BUG-0019`、`BUG-0020`
