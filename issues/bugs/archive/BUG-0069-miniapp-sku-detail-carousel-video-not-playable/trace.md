---
bug_id: BUG-0069-miniapp-sku-detail-carousel-video-not-playable
status: done
lifecycle_stage: archive
severity: high
created_at: 2026-07-19 23:36:55
updated_at: 2026-07-20 22:48:26
lifecycle:
  captured: 2026-07-19 23:36:55
  generated: 2026-07-19 23:55:50
  completed: 2026-07-20 00:09:10
  reviewed: 2026-07-20 08:11:37
  approved: 2026-07-20 08:11:37
iteration: sprint-009
related_requirement: REQ-0044-miniapp-sku-detail-page
related_bug: null
related_change: fix-miniapp-sku-detail-video-url
source_command: /capture
openspec_changes:
  - change_id: fix-miniapp-sku-detail-video-url
    type: fix
    status: archived
related_bugs: []
captured_via: capture
classification_rationale: SKU 商品详情页属于已交付小程序能力，轮播图中的视频媒体不能显示和播放是既有详情页媒体展示与播放行为偏差，因此归类为 BUG。
---

```yaml
bug_id: BUG-0069-miniapp-sku-detail-carousel-video-not-playable
status: done
severity: high
lifecycle_stage: archive
created_at: 2026-07-19 23:36:55
updated_at: 2026-07-20 22:48:49
lifecycle:
  captured: 2026-07-19 23:36:55
  generated: 2026-07-19 23:55:50
  completed: 2026-07-20 00:09:10
  reviewed: 2026-07-20 08:11:37
  approved: 2026-07-20 08:11:37
iteration: sprint-009
related_requirement: REQ-0044-miniapp-sku-detail-page
related_bug: null
related_change: fix-miniapp-sku-detail-video-url
source_command: /capture
openspec_changes:
  - change_id: fix-miniapp-sku-detail-video-url
    type: fix
    status: archived
related_bugs: []
scope:
  terminal: wechat_miniapp
  page: sku_detail
  component: carousel
  media_type: video
readiness:
  capture: done
  bug: done
  root_cause: done
  workaround: done
  acceptance: done
  review: done
  trace: done
  next: archived
```

## 来源

| 类型 | ID / 路径 | 说明 |
|---|---|---|
| 用户反馈 | `/capture` | SKU 商品详情页轮播图，视频不能显示和播放 |
| REQ | `REQ-0044-miniapp-sku-detail-page` | 微信小程序 SKU 详情页已交付能力 |

## 建议验收要点

| 验收点 | 说明 |
|---|---|
| 视频展示 | 包含视频素材的 SKU 详情页轮播图能显示视频封面或播放器 |
| 视频播放 | 点击视频项后可正常播放、暂停，不出现空白、报错或无响应 |
| 图片兼容 | 同一轮播图内图片项仍可正常展示和切换 |
| 平台 evidence | 补充微信开发者工具或真机截图 / 录屏，标注设备、基础库版本和具体 SKU |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-20 22:47:43 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-miniapp-sku-detail-video-url） |
| 2026-07-20 22:47:07 | /opsx-archive | Change `fix-miniapp-sku-detail-video-url` 已归档，状态同步完成。 |
| 2026-07-20 08:57:35 | /sprint-propose | 纳入 sprint-009 正式范围，容量估算更新为 33.0/30.0 人天 |
| 2026-07-20 08:20:58 | /bug-opsx | 创建 OpenSpec Change `fix-miniapp-sku-detail-video-url`，状态 proposed |
| 2026-07-20 08:14:56 | lifecycle-stage-migrate | plan → review（/bug-review --approve） |
| 2026-07-20 08:11:37 | /bug-review --approve | 评审通过，状态更新为 approved，准备由 plan 迁入 review 阶段 |
| 2026-07-20 00:09:10 | /bug-complete | 补齐 root-cause、workaround、acceptance；状态更新为 pending_review |
| 2026-07-19 23:55:50 | /bug-generate | 生成 bug.md，状态更新为 draft |
| 2026-07-19 23:36:55 | /capture | 记录 SKU 商品详情页轮播图视频不能显示和播放缺陷 |

- 2026-07-20 22:47:07 workflow-sync：状态同步为 done（Change archived）
