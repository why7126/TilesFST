---
change_id: fix-public-sku-main-image-pending-path
type: fix
status: archived
created_at: 2026-08-01 07:35:40
updated_at: 2026-08-01 08:06:04
source_bug: BUG-0099-public-sku-main-image-key-pending-path
source_requirement: null
iteration: sprint-016
archived_at: 2026-08-01 08:06:04
archive_path: openspec/archive/2026-08-01-fix-public-sku-main-image-pending-path/
---

# Change Trace

## 来源

- BUG: `BUG-0099-public-sku-main-image-key-pending-path`
- 标题：公开商品主图对象 key 仍停留在 pending 暂存路径
- 严重等级：high
- 根因分类：code-design

## 状态

```yaml
change_id: fix-public-sku-main-image-pending-path
type: fix
status: archived
source_bug: BUG-0099-public-sku-main-image-key-pending-path
iteration: sprint-016
archive_path: openspec/archive/2026-08-01-fix-public-sku-main-image-pending-path/
archived_at: 2026-08-01 08:06:04
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-01 08:06:04 | `/opsx-archive fix-public-sku-main-image-pending-path` | Change 已归档到 `openspec/archive/2026-08-01-fix-public-sku-main-image-pending-path/`，关联 BUG-0099 已 promote 至 archive。 |
| 2026-08-01 07:43:29 | `/sprint-propose sprint-016` | 纳入 sprint-016 正式范围，满足后续 `/opsx-apply` 迭代门禁。 |
| 2026-08-01 07:35:40 | `/bug-opsx BUG-0099` | 基于已评审 BUG 创建 OpenSpec fix Change。 |

## 实现记录

- 来源 BUG 已纳入 `sprint-016`，并已通过 `/opsx-apply` 迭代纳入门禁。
- `/opsx-apply` 实现补充媒体 helper、SKU 创建/编辑/发布正式化、存量 pending 主图迁移脚本和聚焦测试；未新增 API 字段、接口参数、数据库字段、错误码或环境变量，因此 OpenAPI / Orval / DB schema / `.env.example` 不适用。
- 本 Change 仅涉及图片对象生命周期和对象存储策略；`docs/06-video-asset-management.md` 不适用，已同步 `docs/07-object-storage-strategy.md` 与 `rules/object-storage.md`。本次沿用 `admin-media-upload-chain` best-practice，不新增 incident 文档。

## 归档验证摘要

- 验证命令与结果：49 个相关 pytest 通过；迁移 dry-run total=0；`openspec validate fix-public-sku-main-image-pending-path --strict` 通过。
- 验收结论：BUG-0099 公开商品主图 pending 路径问题已修复，新建、编辑与发布 SKU 图片路径正式化达到验收要求。
- Issue 状态：`BUG-0099-public-sku-main-image-key-pending-path` 已同步为 `done`，物理路径为 `issues/bugs/archive/BUG-0099-public-sku-main-image-key-pending-path/`。
- Sprint 状态：`sprint-016` 范围内该 Change 已 archived，Sprint 已 completed/archive。
- 归档证据：Change 已归档到 `openspec/archive/2026-08-01-fix-public-sku-main-image-pending-path/`，归档时间 `2026-08-01 08:06:04`。
