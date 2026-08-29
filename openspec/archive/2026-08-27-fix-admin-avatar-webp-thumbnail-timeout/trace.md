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
| `issues/bugs/archive/BUG-0142-admin-avatar-upload-storage-put-slow/root-cause.md` | 根因状态为 `confirmed`，慢点归属头像 WebP thumbnail 生成。 |

## 实现证据

| 证据 | 结论 |
|---|---|
| `src/backend/app/modules/media/storage.py` | WebP 派生图编码改为低延迟 `WEBP_DERIVATIVE_ENCODER_METHOD=1`，避免使用 Pillow 最慢 `method=6` 阻塞头像 thumbnail 生成。 |
| `tests/test_media_storage.py::test_webp_derivatives_use_low_latency_encoder_method` | 校验 WebP 派生图使用低延迟编码参数。 |
| `tests/test_media_storage.py::test_save_upload_file_generates_webp_avatar_variants_and_stage_spans` | 校验 WebP 头像上传生成原图、thumbnail、display，并记录六个上传阶段 spans。 |
| `localhost:3000` smoke | 159938 bytes WebP 头像上传返回 200，用时 1274.2ms；`task_trace_id=task_upload_image_55a0044030624bd2`，`thumbnail_generate=760ms`。 |

## 产品数据采集与链路观测

product_data_collection_observability: applicable

affected_layers: backend_api, request_logs, task_traces, task_trace_spans, web_admin_smoke

validation:

- 本次修复复用既有 `POST /api/v1/admin/uploads` 上传链路与 Task Trace spans，不新增 usage event、请求头、请求日志 schema、`task_traces` / `task_trace_spans` 表结构或 API 响应字段。
- 后端测试覆盖 `file_read`、`original_put_object`、`thumbnail_generate`、`thumbnail_put_object`、`display_generate`、`display_put_object` 六个阶段 spans，并验证 WebP 头像上传生成原图、thumbnail、display。
- `localhost:3000` smoke 证据中 `task_trace_id=task_upload_image_55a0044030624bd2`，`thumbnail_generate=760ms`，接口返回 200 且三类 `/media/{key}` 均可读，满足阶段级耗时追踪与修复验收。

n/a_reason:

- API Contract / OpenAPI / Orval：未修改请求、响应、错误码或 Pydantic Schema。
- DB / migration：未修改持久化表结构、索引或保留周期。
- Web / 小程序 / App 请求封装：未修改端侧请求封装、链路 ID 透传或离线重试策略。
- usage_events：本修复不新增用户行为埋点，仅消费上传链路已有 request log 与 Task Trace 证据。

## 文档同步

- API 文档 / Orval：N/A，上传接口契约未变。
- DB 设计 / schema / migration：N/A，未修改数据库结构。
- 对象存储策略文档：N/A，bucket、key 前缀、ACL、MinIO / S3 适配层和 `/media/{object_key}` 受控读取策略未变。
- `.env.example` / Docker / 部署文档：N/A，未新增环境变量或部署参数。
- 长期产品规格：通过本 Change 的 OpenSpec delta 合并到 `admin-profile-page` 与 `media-multi-variant-images` specs 承载。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-25 22:35:18 | `/opsx-apply` | 将 WebP 派生图编码切换为低延迟参数，补充 WebP 头像上传 spans 测试与 localhost:3000 smoke 证据。 |
| 2026-08-25 22:25:47 | `/bug-opsx` | 创建修复 Change，聚焦管理端 WebP 头像 thumbnail 生成长尾。 |
