---
change_id: fix-admin-avatar-webp-thumbnail-timeout
source_bug: BUG-0142-admin-avatar-upload-storage-put-slow
sprint: sprint-026
status: proposed
created_at: 2026-08-25 22:25:47
updated_at: 2026-08-25 22:35:18
---

# 追溯

## 来源

| 类型 | 编号 | 说明 |
|---|---|---|
| BUG | BUG-0142-admin-avatar-upload-storage-put-slow | 管理端头像上传 127KB 级 WebP 文件返回 200 但等待约 31.74 秒。 |
| Sprint | sprint-026 | 已纳入正式范围，估算 S / 1 人天。 |

## 根因证据

| 证据 | 结论 |
|---|---|
| `screenshots/network-upload-31s.png` | 浏览器 Network 显示 `POST uploads` 返回 200，但等待 `31.74 秒`。 |
| `screenshots/log-detail-stage-timing-thumbnail-generate-28s.png` | 阶段级日志显示 `thumbnail_generate=28464ms`，对象写入阶段仅百毫秒级。 |
| `issues/bugs/review/BUG-0142-admin-avatar-upload-storage-put-slow/root-cause.md` | 根因状态为 `confirmed`，慢点归属头像 WebP thumbnail 生成。 |

## 实现证据

| 证据 | 结论 |
|---|---|
| `src/backend/app/modules/media/storage.py` | WebP 派生图编码改为低延迟 `WEBP_DERIVATIVE_ENCODER_METHOD=1`，避免使用 Pillow 最慢 `method=6` 阻塞头像 thumbnail 生成。 |
| `tests/test_media_storage.py::test_webp_derivatives_use_low_latency_encoder_method` | 校验 WebP 派生图使用低延迟编码参数。 |
| `tests/test_media_storage.py::test_save_upload_file_generates_webp_avatar_variants_and_stage_spans` | 校验 WebP 头像上传生成原图、thumbnail、display，并记录六个上传阶段 spans。 |
| `localhost:3000` smoke | 159938 bytes WebP 头像上传返回 200，用时 1274.2ms；`task_trace_id=task_upload_image_55a0044030624bd2`，`thumbnail_generate=760ms`。 |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-25 22:35:18 | `/opsx-apply` | 将 WebP 派生图编码切换为低延迟参数，补充 WebP 头像上传 spans 测试与 localhost:3000 smoke 证据。 |
| 2026-08-25 22:25:47 | `/bug-opsx` | 创建修复 Change，聚焦管理端 WebP 头像 thumbnail 生成长尾。 |
