## Context

当前 `build_object_key()`（`src/backend/app/modules/media/object_keys.py`）生成：

```text
{prefix}/{tenant}/{resource_type}/{YYYY}/{MM}/{uuid}.{ext}
```

四上传 API（`uploads.py`）映射：

| API | prefix | resource_type |
|---|---|---|
| `POST .../uploads` | `original` | `avatars` |
| `POST .../uploads/brand-logos` | `original` | `brands/logos` |
| `POST .../uploads/tile-images` | `original` | `tiles/{id\|pending}/images` |
| `POST .../uploads/tile-videos` | `videos` | `tiles/{id\|pending}` |

REQ-0012 `/req-complete` 已敲定：**方案 A** 一次性迁移脚本（非长期双读）。无 UI 原型（N/A）。

## Goals / Non-Goals

**Goals:**

- 新上传 Key 符合 `{prefix}/{tenant}/{resource_type}/{uuid}.{ext}`。
- 图片类使用 `images/`；视频 `videos/`；禁止新对象使用 `original/`。
- 四 API 映射与 acceptance AC-009～AC-013 一致。
- 迁移脚本 dry-run + apply；迁移后媒体无 404。
- 规范文档与 OpenSpec delta 同步。

**Non-Goals:**

- `files/`、`audios/` 实际上传 API（仅 env + 文档预留）。
- 缩略图、转码、封面自动生成流水线。
- 多 Bucket、前端直连 MinIO、签名 URL 分级。
- 微信小程序变更。

## Decisions

### D1 — 迁移策略：方案 A 一次性脚本

**选择**：`scripts/migrate_object_keys.py` 支持 `--dry-run` 与 `--apply`。

**理由**：REQ-0012 已评审确认；避免长期双读增加 `/media` 与测试复杂度。

**替代**：方案 B 读取层双格式兼容 — 拒绝（退役窗口难治理）。

### D2 — Key 生成：移除日期分片

**选择**：`build_object_key()` 不再插入 `{YYYY}/{MM}`。

**理由**：业务检索依赖 SQLite `object_key`；Console 按目录浏览无需按月分片。

### D3 — 前缀来源：settings.minio_prefix_*

**选择**：`build_upload_object_key()` 从 `settings.minio_prefix_images` / `minio_prefix_videos` 读取；新增 `MINIO_PREFIX_IMAGES`（默认 `images/`），保留 `MINIO_PREFIX_ORIGINAL` 仅作 deprecated 文档说明。

**理由**：消除 uploads 硬编码 `"original"`。

### D4 — resource_type 规范化

| 场景 | 新 resource_type |
|---|---|
| 头像 | `user/avatars` |
| Logo | `brands/logos`（不变） |
| SKU 图 | `tiles/{id}` 或 `tiles/pending`（去掉 `/images` 后缀） |
| SKU 视频 | `tiles/{id}` 或 `tiles/pending`（不变） |

### D5 — 迁移 Key 映射规则

旧 Key → 新 Key 转换逻辑（脚本内）：

```text
original/default/avatars/{YYYY}/{MM}/{uuid}.{ext}
  → images/default/user/avatars/{uuid}.{ext}

original/default/brands/logos/{YYYY}/{MM}/{uuid}.{ext}
  → images/default/brands/logos/{uuid}.{ext}

original/default/tiles/{id|pending}/images/{YYYY}/{MM}/{uuid}.{ext}
  → images/default/tiles/{id|pending}/{uuid}.{ext}

videos/default/tiles/{id|pending}/{YYYY}/{MM}/{uuid}.{ext}
  → videos/default/tiles/{id|pending}/{uuid}.{ext}
```

MinIO：copy 至新 Key → 验证 → delete 旧 Key；DB 四表批量 UPDATE；任一步失败 MUST 中止并报告。

### D6 — 无 UI / 无 Conflict Resolution

本 change 无 `prototype/`；**跳过** UI Explore Gate。acceptance.md 与 requirement.md 一致，无冲突。

## Risks / Trade-offs

| 风险 | 缓解 |
|---|---|
| 迁移误删导致 404 | dry-run 先行；AC-022 缺失对象报错中止；发版前 backup SQLite + MinIO |
| 进行中 Sprint 上传混用旧 Key | apply 后立即生效新规则；迁移脚本在部署窗口执行 |
| pytest 大量前缀断言变更 | 集中更新 `test_admin_brands.py` 等；CI 门禁 |
| `MINIO_PREFIX_ORIGINAL` 残留引用 | grep 清理；文档标记 deprecated |

## Migration Plan

1. 部署新后端（新 Key 生成逻辑）。
2. 维护窗口：`python scripts/migrate_object_keys.py --dry-run` 审阅映射。
3. `python scripts/migrate_object_keys.py --apply`。
4. 冒烟：品牌 Logo、用户头像、SKU 图/视频 `/media/...` 200。
5. 回滚：自 backup 恢复 SQLite + MinIO（runbook 写入脚本 docstring）。

## Open Questions

_无 — REQ-0012 已 approved，迁移策略与 Key 形态已在 acceptance 敲定。_
