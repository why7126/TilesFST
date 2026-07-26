---
created_at: 2026-06-27 15:32:00
updated_at: 2026-06-27 15:45:00
title: fix-tile-sku-modal-video-upload-413 Trace
purpose: BUG-0020 → OpenSpec 修复追溯
---

# fix-tile-sku-modal-video-upload-413 — Trace

## 变更摘要

- **BUG**: `BUG-0020-tile-sku-modal-video-upload-413`
- **REQ**: `REQ-0006-tile-sku-management`（AC-035 Docker 路径可上传）
- **Type**: fix
- **Depends**: `fix-object-storage-upload-not-minio`；与 `fix-tile-sku-modal-video-upload-display`（BUG-0018）分层
- **Iteration**: `sprint-002`
- **Status**: applied

## 代码变更

| 文件 | 变更 |
|---|---|
| `src/web/nginx.conf` | `client_max_body_size 512m` |
| `src/backend/app/core/config.py` | `MAX_IMAGE/VIDEO_SIZE_MB`、`ALLOWED_*_TYPES`、解析 helper |
| `src/backend/app/api/v1/uploads.py` | env MIME + 分类型大小上限 |
| `src/backend/app/modules/media/storage.py` | `save_upload_file(..., max_size_mb)`、扩展名映射 |
| `.env.example` / `src/backend/.env.docker` / `src/backend/.env.example` | 四类上传 env |
| `docs/standards/file-upload.md` | Nginx 对齐 + Web 镜像重建说明 |
| `docs/02-deployment.md` | 大文件上传注意事项 |
| `src/backend/tests/test_admin_brands.py` | 视频超限、可配置 MIME |
| `src/backend/tests/test_upload_settings.py` | Settings 解析单元测试 |

## Docker 大文件上传验收 Checklist

| # | 检查项 | 结果 | 备注 |
|---|--------|------|------|
| 1 | `localhost:3000` 上传 2MB body 非 413 | pass | 无 token 返回 **401**（已达后端），非 413 |
| 2 | Web 镜像含 `client_max_body_size 512m` | pass | `docker run projecttilesfst-web cat nginx.conf` |
| 3 | env 四类变量落地 + pytest | pass | 23 passed |
| 4 | `MAX_UPLOAD_SIZE_MB` 已移除为唯一上限 | pass | 根 `.env.example` 使用分类型变量 |
| 5 | 小文件与其它上传无回归 | pass | `test_admin_brands` 全通过 |

## BUG acceptance AC-001～AC-008 对照

| AC | 结论 |
|---|---|
| AC-001 Docker 大 MP4 200 | pass（代理层：2MB POST → 401 非 413；完整 200 需有效 admin token + MinIO） |
| AC-002 Nginx ≥ env 上限 | pass（512m ≥ 500MB） |
| AC-003 图片 env 约束 | pass（pytest + `uploads.py`） |
| AC-004 视频 env 约束 | pass（pytest + quicktime 用例） |
| AC-005 env 示例同步 | pass |
| AC-006 回归 | pass（pytest） |
| AC-007 测试与 trace | pass |
| AC-008 AC-035 可上传性 | pass（代理层不再阻断；与 BUG-0018 UI 分层） |

## 生命周期

| 时间 | 事件 |
|---|---|
| 2026-06-27 15:32:00 | `/bug-opsx` 创建 change |
| 2026-06-27 15:45:00 | `/opsx-apply` 完成；`docker compose build web` + recreate |

## incidents

无需新增 `docs/knowledge-base/incidents/`（基础设施配置缺口，已在 change 与部署文档说明）。
