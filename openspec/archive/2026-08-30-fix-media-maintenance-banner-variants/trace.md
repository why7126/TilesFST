---
change_id: fix-media-maintenance-banner-variants
type: fix
status: in_progress
created_at: 2026-08-29 19:31:20
updated_at: 2026-08-30 08:22:53
source_bug: BUG-0146-batch-media-maintenance-banner-variants
source_requirement: REQ-0115-media-multi-variant-images
sprint: sprint-027
---

# Change Trace

```yaml
change_id: fix-media-maintenance-banner-variants
type: fix
status: in_progress
created_at: 2026-08-29 19:31:20
updated_at: 2026-08-30 08:22:53
source_bug: BUG-0146-batch-media-maintenance-banner-variants
source_requirement: REQ-0115-media-multi-variant-images
sprint: sprint-027
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-29 19:31:20 | `/bug-opsx` | 基于 BUG-0146 创建 Banner 历史派生图维护修复 Change。 |
| 2026-08-29 21:13:47 | `/opsx-modify` | 验收返修：本地 `media-drift-reconcile` 暴露 `tile_videos.mime_type` 不存在；已改为 `NULL AS mime_type` 并用真实 SQLite schema 夹具回归。 |
| 2026-08-29 23:23:55 | `/opsx-modify` | 回填 BUG-0146 验收证据：本地等价环境 dry-run、curl headers、小程序 API 响应和用户补充的生产管理端 Banner Network 截图；生产 apply JSON 与生产端 render/no-fallback 仍待补齐。 |
| 2026-08-30 07:39:12 | `/opsx-modify` | 回填生产 `backfill-image-variants` apply JSON：生产扫描 6 条 `banner_image`，Banner 维度失败数为 0；整批任务仍有非 Banner `sku_image` 失败，生产端 render/no-fallback 待补齐。 |
| 2026-08-30 07:46:42 | `/opsx-modify` | 回填生产小程序首页 DevTools 截图：页面渲染和 Network 中存在 `.thumb.webp` / `.display.webp` 200/webp；同时复核生产历史无 id URL 仍 fallback 到 PNG，生产公开 API curl 与截图证据存在冲突，暂不 archive。 |
| 2026-08-30 08:10:01 | `/opsx-modify` | 处理生产历史无 id Banner URL fallback：确认旧无 id URL 仍需兼容，在 `backfill-image-variants` 中补充业务 id Banner 的旧无 id `.thumb.webp` / `.display.webp` alias 审计与生成；生产公开 API URL 为空问题按“旧路径派生对象缺失导致存在性校验置空”纳入同一闭环，部署后用 dry-run/apply、公开 API 和 curl 复核。 |
| 2026-08-30 08:22:53 | 验收补证 | 用户补充本地 alias apply JSON 和本地小程序 DevTools no-fallback 截图；解析确认 JSON 为 `development/sqlite/tencent-cos`，可证明 alias 逻辑可执行但不能替代生产 MySQL apply。公网生产历史无 id thumb/display URL 复核仍为 PNG fallback，继续保持 pending。 |
