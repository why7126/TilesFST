---
title: Change 追溯
purpose: fix-object-storage-upload-not-minio 追溯记录
change_id: fix-object-storage-upload-not-minio
bug_id: BUG-0006-object-storage-upload-not-minio
status: archived
created_at: 2026-06-26 13:47:54
---

# Change 追溯

## 1. 来源

| 项 | 内容 |
|---|---|
| BUG | `issues/bugs/BUG-0006-object-storage-upload-not-minio` |
| 严重等级 | high |
| Sprint | sprint-002 |
| 评审 | `issues/bugs/BUG-0006-object-storage-upload-not-minio/review.md` |
| 临时规避 | 仅可验证本地 `/media` 或 `data/uploads`，不能视为 MinIO 验收通过 |

## 2. Bug Analysis Report

| 判断 | 结论 |
|---|---|
| 现象 | MinIO 桶已初始化，但业务上传对象未进入 MinIO |
| 直接原因 | `save_upload_file()` 写入 `settings.upload_dir` 本地路径 |
| 根本原因 | 媒体存储适配层仍是本地文件系统实现，未接入 MinIO client |
| 影响范围 | 头像、品牌 Logo、SKU 图片、SKU 视频、Docker 演示环境 |
| 修复类型 | fix |

## 3. Spec 映射

| BUG AC | OpenSpec |
|---|---|
| AC-001 MinIO 单桶写入 | `object-storage/spec.md` 管理端上传必须写入 MinIO 单桶 |
| AC-002 标准前缀 | `object-storage/spec.md` 对象 Key 必须使用标准前缀 |
| AC-003 后端授权与校验 | `object-storage/spec.md` 管理端上传必须写入 MinIO 单桶 |
| AC-004 API 兼容 | `proposal.md` / `design.md` API 与 Orval 策略 |
| AC-005 受控读取 | `object-storage/spec.md` 媒体对象必须可受控读取 |
| AC-006 Docker 验证 | `tasks.md` 5.7 |
| AC-007 测试 | `tasks.md` §5 |
| AC-008 不破坏既有上传 | `tasks.md` 3.5 / 5.6 |
| AC-009 文档同步 | `tasks.md` §4 |

## 4. 状态

- [x] `/bug-capture BUG-0006-object-storage-upload-not-minio`
- [x] `/bug-generate BUG-0006-object-storage-upload-not-minio`
- [x] `/bug-complete BUG-0006-object-storage-upload-not-minio`
- [x] `/bug-review BUG-0006-object-storage-upload-not-minio`
- [x] 纳入 `sprint-002`
- [x] `/bug-opsx BUG-0006-object-storage-upload-not-minio`
- [x] `/opsx-apply fix-object-storage-upload-not-minio`
- [x] `/opsx-archive fix-object-storage-upload-not-minio`

## 5. 变更记录

| 时间 | 动作 | 说明 |
|---|---|---|
| 2026-06-26 13:47:54 | `/bug-opsx` | 创建 `fix-object-storage-upload-not-minio` OpenSpec Change |
| 2026-06-26 14:06:45 | `/opsx-apply` | 后端上传写入 MinIO 单桶，`/media/{object_key}` 从 MinIO 受控读取；上传响应 schema 保持 `{ object_key, url }`，无需 Orval |
| 2026-06-26 14:20:50 | `/opsx-archive` | 已同步 `brand-management` 与新增 `object-storage` 正式 spec，并归档到 `openspec/changes/archive/2026-06-26-fix-object-storage-upload-not-minio/` |

## 6. 实现与验证

| 项 | 结果 |
|---|---|
| 存储适配 | `save_upload_file()` 改为通过 `MinioMediaStorageClient` 写入 `MINIO_BUCKET` |
| 读取策略 | `/media/{object_key}` 保持 URL 兼容，由后端从 MinIO 读取并返回媒体响应 |
| 对象前缀 | 头像、品牌 Logo、SKU 图片、SKU 视频分别使用 `original/` 与 `videos/` 标准前缀 |
| 错误映射 | MinIO 不可用映射为 `50001 STORAGE_UNAVAILABLE`；非法 MIME 为 `50002`；文件大小超限为 `50003` |
| Orval | 未执行；上传成功响应字段与 URL 语义保持兼容，未改变前端生成客户端依赖的 schema |
| Docker Compose | 已重建 backend；实际上传品牌 Logo 后在 `tile-info-platform` 桶 stat 到对象，`/media/{object_key}` 读取字节数一致 |
| 后端 pytest | `cd src/backend && uv run pytest tests/test_admin_brands.py tests/test_admin_tile_skus.py tests/test_auth.py`：35 passed |
| incident 沉淀 | 不新增 `docs/knowledge-base/incidents/`；本缺陷影响范围与复盘已在 BUG 文档和本 trace 覆盖，未形成线上事故 |
| Spec 同步 | 已同步 `openspec/specs/brand-management/spec.md` 与 `openspec/specs/object-storage/spec.md` |
