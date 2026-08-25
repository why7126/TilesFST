---
change_id: fix-miniapp-certificate-detail-display-url
type: fix
status: applied
source_bug: BUG-0134-miniapp-certificate-detail-display-url
source_requirement: REQ-0115-media-multi-variant-images
sprint: sprint-025
created_at: 2026-08-22 21:26:55
updated_at: 2026-08-24 14:30:46
---

# Change Trace

```yaml
change_id: fix-miniapp-certificate-detail-display-url
type: fix
status: applied
source_bug: BUG-0134-miniapp-certificate-detail-display-url
source_requirement: REQ-0115-media-multi-variant-images
sprint: sprint-025
created_at: 2026-08-22 21:26:55
updated_at: 2026-08-24 13:08:11
```

## 验收返修记录

| 时间 | 反馈 | 根因状态 | 调整 | 验证 |
|---|---|---|---|---|
| 2026-08-23 08:30:02 | 本地 `sqlite-tencent-cos` dry-run 在 `backfill-brand-certificate-thumbnails` 的 `variant_info` 阶段报告 `object_storage_unreachable`，阻断 `.display` object 补证 | confirmed：脱敏只读诊断显示 COS 原图 HEAD 成功，缺失 `.thumb.webp` HEAD 返回 SDK 错误码 `NoSuchResource`，当前适配层未将其识别为媒体对象缺失 | 将 Tencent COS / S3 兼容适配层缺失对象判断统一为 `NoSuchKey`、`NoSuchObject`、`NoSuchResource`，并读取 SDK `get_error_code()` / `get_code()` | 聚焦 pytest 13 项通过；当前源码加载 `sqlite-tencent-cos.env` dry-run 结果 `failed=0`、`retry_candidates=99`、`thumbnail_candidates=99`、`non_standard_keys_after_audit=0` |
| 2026-08-23 09:09:12 | 用户补充小程序 DevTools Network 截图，选中 `/media/images/default/tiles/143/...thumb.jpg` 请求 | confirmed：维护 apply 与幂等 dry-run 后，缩略图受控 URL 可 200 读取且 `x-media-fallback: 0`，页面正常渲染证书详情 | 记录为 render / URL 验收证据；`.display` object 仍需单独补证 | apply 后幂等 dry-run `failed=0`、`retry_candidates=0`、`thumbnail_candidates=0`、`non_standard_keys_after_audit=0`；截图显示 HTTP `200 OK`、`content-length: 25159`、`content-type: image/jpeg` |
| 2026-08-24 13:08:11 | 用户反馈小程序首页商品卡仍空图；补充接口样本显示同一批商品仅 `original_url` 有值，`cover_image`、`thumbnail_url`、`display_url` 均为空 | confirmed：`backfill-image-variants --limit 100/500` 只覆盖前段候选；全量 dry-run 才暴露仍有 186 个图片缺 `.thumb/.display` | 执行全量 `backfill-image-variants --apply --confirm-backup`，并记录接口字段恢复与小程序首页商品卡 render evidence；本次不新增源码改动 | 全量 apply 成功 370 个写入；幂等 dry-run 收敛为 `skipped=682`、`thumbnail_missing=1`、`display_missing=1`、`estimated_writes=3`、`retry_candidates=2`；刷新后 `/products` 已返回 `.thumb.webp` 与 `.display.webp`，截图 `codex-clipboard-77f20599-cb4c-4c6c-b85e-c070c03d10b0.png` 显示新品/热销商品卡图片恢复 |
| 2026-08-24 14:30:46 | 用户反馈证书详情 `media[]` 仍使用 `files/default/brand-certificates` 历史 URL，`display_url/thumbnail_url` 为空且轮播占位 | confirmed：本地 `brand_certificate_images.media_id=40` 已完成 `file_key` 迁移，但 `file_url` 仍是旧 `/media/files/default/...`；详情接口此前只用 `file_url` 派生变体 | 后端仓库带出 `brand_certificate_images.file_key`，服务层优先使用 canonical 证书图片 key 派生 display/thumb/original，主证书查询也用 canonical key 兜正 URL | `tests/test_miniapp_home.py` 44 项通过；`migrate-certificate-image-keys` dry-run `image_candidates=0`、`document_skipped=5`；运行时 `/api/v1/miniapp/certificates/4` 返回 `media_id=40.display_url=/media/images/default/brand-certificates/...display.webp`，display/thumb HEAD 均 `200 OK`、`image/webp`、`x-media-fallback=0` |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-23 09:09:12 | evidence-update | 补充小程序 DevTools Network 截图作为受控 `/media` URL 与 render 证据；`.display` object 仍待补证。 |
| 2026-08-24 13:08:11 | `/opsx-modify` | 补充全量 `backfill-image-variants` 验证、小程序首页商品卡 render evidence 与 limit 覆盖不足根因记录。 |
| 2026-08-24 14:30:46 | `/opsx-modify` | 修复证书详情 `brand_certificate_images` 半迁移记录仍用旧 `file_url` 派生变体的问题，并补齐证书图片 key 迁移与 display/thumb object 证据。 |
| 2026-08-23 08:30:02 | `/opsx-modify` | 修复 Tencent COS `NoSuchResource` 缺失对象错误码误判为对象存储不可达，维护任务可继续识别缺失 `.thumb/.display` 变体。 |
| 2026-08-22 21:26:55 | `/bug-opsx` | 基于 BUG-0134 创建证书详情 display_url 修复 Change。 |
