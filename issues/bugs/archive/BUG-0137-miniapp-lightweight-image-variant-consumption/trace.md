---
bug_id: BUG-0137-miniapp-lightweight-image-variant-consumption
status: done
severity: high
created_at: 2026-08-24 14:54:45
updated_at: 2026-08-25 09:46:40
lifecycle_stage: archive
lifecycle:
  captured: 2026-08-24 14:54:45
  generated: 2026-08-24 14:59:14
  completed: 2026-08-24 17:48:19
  reviewed: 2026-08-24 17:59:18
  approved: 2026-08-24 17:59:18
iteration: sprint-025
openspec_changes:
  - change_id: fix-miniapp-lightweight-image-variant-consumption
    type: fix
    status: archived
related_requirement: REQ-0115-media-multi-variant-images
related_bug: BUG-0126-miniapp-brand-media-slow-load
related_change: fix-miniapp-lightweight-image-variant-consumption
---

# BUG Trace

```yaml
bug_id: BUG-0137-miniapp-lightweight-image-variant-consumption
status: done
severity: high
created_at: 2026-08-24 14:54:45
updated_at: 2026-08-25 08:40:18
lifecycle_stage: review
lifecycle:
  captured: 2026-08-24 14:54:45
  generated: 2026-08-24 14:59:14
  completed: 2026-08-24 17:48:19
  reviewed: 2026-08-24 17:59:18
  approved: 2026-08-24 17:59:18
iteration: sprint-025
openspec_changes:
  - change_id: fix-miniapp-lightweight-image-variant-consumption
    type: fix
    status: archived
related_requirement: REQ-0115-media-multi-variant-images
related_bug: BUG-0126-miniapp-brand-media-slow-load
related_change: fix-miniapp-lightweight-image-variant-consumption
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-25 09:43:46 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-miniapp-lightweight-image-variant-consumption） |
| 2026-08-25 09:43:38 | /opsx-archive | Change `fix-miniapp-lightweight-image-variant-consumption` 已归档，状态同步完成。 |
| 2026-08-25 08:40:18 | evidence-update | 用户补充首页与品牌列表 Banner display 优先策略 DevTools Network/render evidence；`.webp` 过滤下可见 `*.display.webp` 200 请求，商品卡片和品牌 Logo 继续使用 `*.thumb.webp`，页面渲染正常，未见原图或不存在静态占位图请求；BUG acceptance 更新为 accepted。 |
| 2026-08-25 08:29:38 | `/opsx-modify` | 验收策略升级：小程序 Banner 轮播图属于首屏大图展示位，目标规格调整为 `display`；首页与品牌列表 Banner 普通展示改为 `display_url -> thumbnail_url -> 安全视图占位`，BUG acceptance 进入补充复核，并于后续补齐 Network/render 证据。 |
| 2026-08-25 08:17:05 | workflow-sync-dry-run | `sync-workflow-status.py --event opsx.modify --dry-run` 通过且 Errors=0，但会将 BUG acceptance 计算为补充复核状态；为避免覆盖用户已补齐首页返修回归证据后的 accepted 结论，未执行写入同步。 |
| 2026-08-25 08:17:05 | evidence-update | 用户补充首页返修后 DevTools Network/render evidence：Network 过滤 `place` 未出现 `tile-placeholder.png` 请求，首页视图占位与商品卡片渲染可见；BUG acceptance 更新为 accepted，Change tasks 25/25。 |
| 2026-08-25 08:13:32 | /opsx-modify | Change `fix-miniapp-lightweight-image-variant-consumption` 验收返修已同步，并进入复验归档链路。 |
| 2026-08-25 08:07:55 | `/opsx-modify` | 验收返修：首页 fallback 请求 `/assets/tile-placeholder.png`，DevTools Network 显示 307 后 500；已改为不依赖本地占位图片的视图占位/空字段策略，并于后续补齐首页 Network/render 回归证据。 |
| 2026-08-24 20:59:27 | workflow-sync-dry-run | `sync-workflow-status.py --event opsx.apply --dry-run` 通过且 Errors=0，但会将 BUG acceptance 计算为补充复核状态；为避免覆盖用户已补齐证据后的 accepted 结论，未执行写入同步。 |
| 2026-08-24 20:54:30 | evidence-update | 用户补充修复后小程序 DevTools Network/render evidence，BUG acceptance 更新为 accepted，Change tasks 23/23。 |
| 2026-08-24 18:46:10 | /opsx-apply | Change `fix-miniapp-lightweight-image-variant-consumption` 实现推进并补齐剩余验收。 |
| 2026-08-24 18:42:54 | `/opsx-apply` | Change 实现已完成；已完成代码修复、OpenAPI/Orval 同步、API 文档和自动化验证。BUG 验收进入补充复核，后续已回填小程序 DevTools Network/render evidence。 |
| 2026-08-24 18:03:50 | `/sprint-propose` | 纳入 sprint-025 正式范围，完成迭代范围登记。 |
| 2026-08-24 18:00:29 | `/bug-review` | confirmed 根因门禁通过，评审结果 approved，等待纳入 Sprint。 |
| 2026-08-24 17:59:38 | lifecycle-stage-migrate | plan → review（/bug-review） |
| 2026-08-24 17:48:19 | `/bug-complete` | 根据小程序 DevTools Network/render 与 AppData 用户补证，补齐修复前 evidence，并将根因状态升级为 confirmed。 |
| 2026-08-24 15:02:18 | `/bug-complete` | 补齐 root-cause、workaround、acceptance，状态进入 pending_review。 |
| 2026-08-24 14:59:14 | `/bug-generate` | 根据 capture 生成正式 `bug.md`，状态更新为 draft。 |
| 2026-08-24 14:54:45 | `/capture` | 记录小程序 Banner、品牌 Logo、分享图普通展示仍可能未统一消费轻量图字段并冷加载原图的问题。 |

- 2026-08-25 09:43:38 workflow-sync：状态同步为 done（Change archived）
