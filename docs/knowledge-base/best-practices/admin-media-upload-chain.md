---
title: 管理端媒体上传全链路最佳实践
purpose: 预防 MinIO 未写入、回显失败、Nginx 413、legacy 双目录类缺陷
content: 提炼自 Sprint 002 BUG-0004~0008、0018、0019、0020
source: /sprint-exps sprint-002
update_method: 上传能力或部署变更时更新
owner: 全栈负责人
status: draft
created_at: 2026-06-27 16:15:00
updated_at: 2026-06-27 16:15:00
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

1. `docker compose build web && docker compose up -d web --force-recreate`
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
