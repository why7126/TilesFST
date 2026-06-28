---
title: 需求验收标准
purpose: REQ-0012 对象存储 Key 布局优化验收标准
content: 基于 requirement.md 与 business-flow.md
source: AI 根据 PRD 生成，项目团队确认
update_method: PRD 或实现变更时同步更新
owner: product
status: draft
created_at: 2026-06-27 22:17:37
updated_at: 2026-06-28 12:30:00
note: REQ-0012-object-storage-key-layout；migrate_object_keys.py --apply 已于 2026-06-28 完成（8 条）
---

# 验收标准

## 1. Key 形态与生成（FR-003）

- [x] **AC-001** `build_object_key()` 生成形态 MUST 为 `{prefix}/{tenant}/{resource_type}/{uuid}.{ext}`。
- [x] **AC-002** 生成的 Key MUST NOT 包含 `{YYYY}/{MM}` 四段日期目录。
- [x] **AC-003** `{uuid}` MUST 为 UUID v4；`{ext}` MUST 来自 MIME 白名单映射，非用户文件名。
- [x] **AC-004** 默认 `{tenant}` MUST 为 `default`。

## 2. 标准前缀（FR-001）

- [x] **AC-005** 新上传图片类对象 Key MUST 以 `images/` 开头，MUST NOT 以 `original/` 开头。
- [x] **AC-006** 新上传视频类对象 Key MUST 以 `videos/` 开头。
- [x] **AC-007** 规范与 `.env.example` MUST 声明 `files/`、`audios/` 为预留前缀；本期无实际上传入口。
- [x] **AC-008** `original/` MUST 在 `rules/object-storage.md` 标记为 deprecated。

## 3. resource_type 映射（FR-002、FR-004）

- [x] **AC-009** 头像上传 Key MUST 匹配 `images/default/user/avatars/{uuid}.{ext}`。
- [x] **AC-010** 品牌 Logo 上传 Key MUST 匹配 `images/default/brands/logos/{uuid}.{ext}`。
- [x] **AC-011** SKU 图片（有 tile_id）MUST 匹配 `images/default/tiles/{tile_id}/{uuid}.{ext}`。
- [x] **AC-012** SKU 图片（无 tile_id）MUST 匹配 `images/default/tiles/pending/{uuid}.{ext}`。
- [x] **AC-013** SKU 视频（有/无 tile_id）MUST 匹配 `videos/default/tiles/{tile_id|pending}/{uuid}.{ext}`。
- [x] **AC-014** 四上传 API 响应 MUST 仍为 `{ object_key, url: "/media/{object_key}" }`；MIME/大小校验无回归。

## 4. 读取与安全（不变）

- [x] **AC-015** `GET /media/{object_key}` 对新 Key MUST 返回 200 与正确 Content-Type。
- [x] **AC-016** 非法 Key（`..`、绝对路径、反斜杠）MUST 仍返回 4xx。
- [x] **AC-017** 单桶策略不变；MUST NOT 新增业务 Bucket。

## 5. 存量迁移（FR-006 — 方案 A）

- [x] **AC-018** 存在 `scripts/migrate_object_keys.py`（或等价名），支持 `--dry-run` 与 `--apply`。
- [x] **AC-019** dry-run MUST 列出 `users.avatar_object_key`、`brands.logo_object_key`、`tile_images.object_key`、`tile_videos.object_key` 待迁移条目。
- [x] **AC-020** apply 后 DB 中引用 Key MUST 与 MinIO 实际对象一致；旧 Key 对象 MUST 已移除或不存在重复。
- [x] **AC-021** 迁移后管理端品牌 Logo、用户头像、SKU 图/视频预览 MUST 无 404。
- [x] **AC-022** 迁移脚本 MUST NOT 删除 DB 仍引用但 MinIO 缺失的对象（应报错中止）。

## 6. 文档与配置（FR-005）

- [x] **AC-023** 已更新 `rules/object-storage.md`、`docs/07-object-storage-strategy.md`、根目录 `.env.example`。
- [x] **AC-024** `data/README.md` 媒体排查示例 MUST 使用新 Key 形态。
- [x] **AC-025** 上传入口与 Key 对照表 MUST 与 `docs/07-object-storage-strategy.md` §2 一致。

## 7. 测试与 OpenSpec（FR-007）

- [x] **AC-026** pytest `test_upload_endpoints_store_expected_minio_prefixes` 等 MUST 断言新前缀。
- [x] **AC-027** 单元测试 MUST 断言 Key 不含 `/20` 年月段（或等价正则）。
- [x] **AC-028** `cd src/backend && pytest` MUST 通过。
- [x] **AC-029** Docker Compose 冒烟：上传 Logo + 访问 `/media/...` MUST 通过（`localhost:8010`，2026-06-28）。
- [x] **AC-030** 变更经 OpenSpec `update-object-storage-key-layout`（或等价 change-id）开发并 archive。

## 8. 不回归

- [x] **AC-031** 前端 Web MUST NOT 要求改动（Orval 无 API schema 变更时可不跑）。
- [x] **AC-032** MUST NOT 恢复写入本地 `UPLOAD_DIR` / `data/uploads`。
- [x] **AC-033** Nginx `client_max_body_size` 与上传大小 env MUST 无无意回归。

## 9. UI / 原型

- [x] **AC-034** 本需求无 UI 变更；**无需** HTML/PNG 原型（N/A）。
