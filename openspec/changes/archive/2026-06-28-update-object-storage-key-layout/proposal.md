## Why

REQ-0012 要求优化 MinIO 单桶下的 Object Key 生成规则。当前实现使用 `original/` 作为图片类前缀、Key 含 `{YYYY}/{MM}` 日期分片，且 `resource_type` 命名（如 `avatars`、`tiles/{id}/images`）与领域路径不一致；`MINIO_PREFIX_*` 已在 `.env.example` 定义但上传代码仍硬编码 `"original"` / `"videos"`。这增加 Console 浏览与运维排查成本，且与 `rules/object-storage.md` 目标规范脱节。BUG-0006～0008 已完成 MinIO 迁移，本 change 在稳定存储基座上统一 Key 布局并迁移存量对象。

## What Changes

- **MODIFIED** `build_object_key()`：形态 `{prefix}/{tenant}/{resource_type}/{uuid}.{ext}`，移除 `{YYYY}/{MM}`。
- **MODIFIED** 标准前缀：图片类 `original/` → `images/`；视频保持 `videos/`；`files/`、`audios/` 规范预留；`original/` 标记 deprecated。
- **MODIFIED** 四上传 API 的 prefix / `resource_type` 映射（头像、Logo、SKU 图/视频）。
- **ADDED** 一次性迁移脚本 `scripts/migrate_object_keys.py`（`--dry-run` + `--apply`），更新 SQLite 四处 `object_key` 并同步 MinIO 对象。
- 同步 `rules/object-storage.md`、`docs/07-object-storage-strategy.md`、`.env.example`、`data/README.md`。
- 更新 pytest 前缀断言与 Key 形态回归测试。
- **无 API schema 变更**；响应仍为 `{ object_key, url: "/media/{object_key}" }`；前端 **无需** Orval 重生成。

## Capabilities

### New Capabilities

_无（基础设施优化，不引入新 spec 域）_

### Modified Capabilities

- `object-storage`：MODIFIED「对象 Key 必须使用标准前缀」— 语义前缀 `images`/`videos`/`files`/`audios`、简化 Key 形态、resource_type 领域路径、deprecated `original/`、迁移策略。

## Impact

| 影响面 | 说明 |
|---|---|
| 后端 | `object_keys.py`、`uploads.py`、`config.py`（`MINIO_PREFIX_*` 读取）；迁移脚本 |
| 前端 Web | **无** UI 变更；继续存储 API 返回的 `object_key` |
| 小程序 | 不涉及 |
| 数据库 | 迁移更新 `users.avatar_object_key`、`brands.logo_object_key`、`tile_images.object_key`、`tile_videos.object_key` |
| MinIO | 存量对象 copy/rename 至新 Key；单桶策略不变 |
| API / Orval | 无 schema 变更 |
| 测试 | pytest 上传前缀断言、Key 形态单元测试、Docker 冒烟 |
| 文档 | `rules/object-storage.md`、`docs/07-object-storage-strategy.md`、`.env.example` |
| 关联 REQ | REQ-0005 品牌/用户、REQ-0006 SKU 图视频 object_key 受影响 |
| Sprint | sprint-003；建议优先 apply 于 profile/规格开发前 |
