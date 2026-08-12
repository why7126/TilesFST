---
bug_id: BUG-0126-miniapp-brand-media-slow-load
status: done
lifecycle_stage: archive
created_at: 2026-08-10 22:57:12
updated_at: 2026-08-11 23:25:26
severity: high
related_requirement:
related_bug: BUG-0110-miniapp-card-banner-thumbnail-usage
iteration: sprint-022
openspec_changes:
  - change_id: fix-miniapp-brand-media-performance
    type: fix
    status: archived
---

```yaml
bug_id: BUG-0126-miniapp-brand-media-slow-load
status: done
lifecycle_stage: review
severity: high
related_requirement:
related_bug: BUG-0110-miniapp-card-banner-thumbnail-usage
iteration: sprint-022
openspec_changes:
  - change_id: fix-miniapp-brand-media-performance
    type: fix
    status: archived
```

# Trace

## 摘要

微信小程序品牌列表页、品牌分类商品列表页、品牌详情页图片加载速度慢，初步定位为品牌链路媒体性能问题。

## 线索

- 品牌 Logo、Banner、商品卡片、证书图片均应优先使用缩略图。
- 系统配置 `media.thumbnail_max_size_kb` 默认可能未限制缩略图体积。
- 历史缩略图可能缺失、体积过大或回退原图。
- 品牌列表 Banner、品牌列表 Logo、品牌详情 Logo、证书图片的小程序懒加载覆盖需复核。
- `/media/{object_key}` 为后端受控读取路径，生产侧缓存或 CDN 策略需复核。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-11 23:24:11 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-miniapp-brand-media-performance） |
| 2026-08-11 23:24:05 | /opsx-archive | Change `fix-miniapp-brand-media-performance` 已归档，状态同步完成。 |
| 2026-08-10 23:48:56 | /opsx-apply | Change `fix-miniapp-brand-media-performance` apply 完成，后续已归档。 |
| 2026-08-10 23:31:00 | /bug-opsx BUG-0126 | 创建 OpenSpec 修复 Change `fix-miniapp-brand-media-performance` |
| 2026-08-10 23:24:23 | /sprint-propose --bug BUG-0126 | 纳入 sprint-022 正式范围。 |
| 2026-08-10 23:13:30 | lifecycle-stage-migrate | plan → review（/bug-review --approve） |
| 2026-08-10 23:12:56 | /bug-review --approve | 评审通过，确认进入后续 Sprint 与修复 Change 流程 |
| 2026-08-10 23:08:03 | /bug-complete | 补齐 root-cause、workaround、acceptance，状态推进为 pending_review |
| 2026-08-10 23:06:42 | /bug-generate | 根据 capture 与 explore 结论生成 bug.md，状态推进为 draft |
| 2026-08-10 22:57:12 | /bug-capture | 记录用户反馈的小程序品牌链路图片加载慢缺陷 |

- 2026-08-11 23:24:05 workflow-sync：状态同步为 done（Change archived）
