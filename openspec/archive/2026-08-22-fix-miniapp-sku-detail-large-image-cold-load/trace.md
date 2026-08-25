---
change_id: fix-miniapp-sku-detail-large-image-cold-load
status: applied
created_at: 2026-08-22 14:15:10
updated_at: 2026-08-22 19:56:51
source_bug: BUG-0132-miniapp-sku-detail-large-image-cold-load
source_requirement: REQ-0044-miniapp-sku-detail-page
source_sprint: sprint-025
change_type: fix
owner: product
impact:
  backend: true
  web: false
  miniapp: true
  admin: possible
  database: possible
  storage: true
  api: possible
related_changes:
  - add-media-multi-variant-images
related_bugs:
  - BUG-0125-miniapp-sku-detail-media-original-load
---

# Change 追踪

## 来源

- BUG：`issues/bugs/archive/BUG-0132-miniapp-sku-detail-large-image-cold-load/`
- 关联需求：`issues/requirements/archive/REQ-0044-miniapp-sku-detail-page/`
- Sprint：`iterations/archive/sprint-025/`
- 评审结论：缺陷已 approved 并纳入 `sprint-025`，允许创建 `fix-*` Change。

## Readiness

```yaml
bug_readiness: Ready
review_gate: pass
sprint_inclusion_gate: pass
change_created_by_cli: true
root_cause_status: probable
reason: BUG 记录、根因分析、workaround、acceptance 和 trace 齐全；已有小程序 DevTools Network 截图作为性能证据；最终 confirmed 需在 apply 阶段绑定代码定位和复测证据。
```

## Conflict Report

```yaml
conflict_status: no_blocking_conflict
related_change: add-media-multi-variant-images
notes:
  - 本 Change 聚焦 BUG-0132 的详情页冷加载修复。
  - REQ-0115 的通用媒体多规格能力可作为实现基础，但不阻塞本 BUG 的最小修复。
  - 实现阶段若复用 REQ-0115 字段，必须保持 thumbnail/display/original 语义一致。
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-22 19:56:51 | `/opsx-archive` | 归档前验收补证：SKU 362 缺失 display 时冷加载使用 15KB thumb；SKU 377 display 存在时冷加载不请求 1.13MB 原图；BUG acceptance 更新为 passed，准备归档。 |
| 2026-08-22 16:54:48 | `/opsx-modify` | 验收返修：确认 `.display.jpg` 派生对象不存在或不可读会导致详情页图片加载失败；后端改为只返回存在且可读的 `display_url` / `thumbnail_url`，缺失时不回退原图冷加载；小程序详情页占位图改用现有资源 `/assets/logos/product-logo.png`；补充缺失派生图回归测试。 |
| 2026-08-22 14:33:44 | `/opsx-apply` | 完成根因 confirmed、UI Contract 补齐、小程序详情页展示 URL fallback 修复、README 同步和聚焦回归；媒体 fixture 测试因当前环境缺 `PIL` 待补。 |
| 2026-08-22 14:15:10 | `/bug-opsx` | 通过 OpenSpec CLI 创建 `fix-*` Change，生成 proposal、design、delta spec、tasks 和 trace。 |
