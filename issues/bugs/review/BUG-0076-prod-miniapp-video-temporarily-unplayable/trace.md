---
bug_id: BUG-0076-prod-miniapp-video-temporarily-unplayable
status: approved
lifecycle_stage: review
severity: high
created_at: 2026-07-21 10:23:03
updated_at: 2026-07-22 10:40:27
lifecycle:
  captured: 2026-07-21 10:23:03
  generated: 2026-07-21 14:59:56
  completed: 2026-07-21 15:21:40
  reviewed: 2026-07-21 15:24:31
  approved: 2026-07-21 15:24:31
iteration: null
related_requirement: null
related_bug: BUG-0069-miniapp-sku-detail-carousel-video-not-playable
related_change: fix-prod-miniapp-video-upstream-502
source_command: /capture
captured_via: capture
classification_rationale: 项目已有微信小程序视频展示/播放能力，生产环境出现“视频暂时无法播放”提示属于既有播放链路的行为偏差，倾向记录为 BUG。
openspec_changes:
  - change_id: fix-prod-miniapp-video-upstream-502
    type: fix
    status: proposed
related_bugs:
  - BUG-0069-miniapp-sku-detail-carousel-video-not-playable
---

```yaml
bug_id: BUG-0076-prod-miniapp-video-temporarily-unplayable
status: approved
severity: high
lifecycle_stage: review
created_at: 2026-07-21 10:23:03
updated_at: 2026-07-22 10:40:27
lifecycle:
  captured: 2026-07-21 10:23:03
  generated: 2026-07-21 14:59:56
  completed: 2026-07-21 15:21:40
  reviewed: 2026-07-21 15:24:31
  approved: 2026-07-21 15:24:31
iteration: null
related_requirement: null
related_bug: BUG-0069-miniapp-sku-detail-carousel-video-not-playable
related_change: fix-prod-miniapp-video-upstream-502
source_command: /capture
captured_via: capture
classification_rationale: 项目已有微信小程序视频展示/播放能力，生产环境出现“视频暂时无法播放”提示属于既有播放链路的行为偏差，倾向记录为 BUG。
openspec_changes:
  - change_id: fix-prod-miniapp-video-upstream-502
    type: fix
    status: proposed
related_bugs:
  - BUG-0069-miniapp-sku-detail-carousel-video-not-playable
scope:
  terminal: miniapp
  environment: production
  module: video_playback
  media_type: video
  issue_type: playback_unavailable
readiness:
  capture: done
  bug: done
  root_cause: done
  workaround: done
  acceptance: done
  review: done
  trace: done
  next: bug-opsx
```

## 来源

| 类型 | ID / 路径 | 说明 |
|---|---|---|
| 用户反馈 | `/capture` | 生产环境微信小程序显示「视频暂时无法播放」 |

## 建议复现要点

| 要点 | 说明 |
|---|---|
| 页面路径 | 确认发生在 SKU 商品详情页、品牌/产品内容页、Banner 视频入口或其他小程序页面 |
| 业务对象 | 记录 SKU、品牌、Banner 或内容 ID，确认是否为单个视频或所有视频均失败 |
| 小程序环境 | 记录微信版本、基础库版本、iOS/Android、真机/开发者工具表现 |
| 视频地址 | 确认 API 返回的视频 URL 是否为空、是否为 HTTPS、是否在小程序 download/video 合法域名内、签名是否过期 |
| 资源响应 | 检查视频 URL HTTP 状态码、Content-Type、Content-Length、Range 请求支持和跨域/防盗链策略 |
| 后端与存储 | 对照 FastAPI、媒体模块和 MinIO 日志，确认对象是否存在、权限是否正确、签名 URL 或代理读取链路是否可用 |
| 历史回归 | 对比 `BUG-0069-miniapp-sku-detail-carousel-video-not-playable` 的修复范围，确认生产是否缺部署、配置或新增场景未覆盖 |

## 建议验收要点

| 验收点 | 说明 |
|---|---|
| 生产可播放 | 生产环境微信小程序中合法配置的视频可加载封面并正常播放 |
| 链路可诊断 | 视频缺失、过期、权限不足、格式不支持等失败场景有明确日志与用户可理解提示 |
| 域名与 HTTPS 合规 | 小程序视频资源域名、协议、证书和白名单配置满足微信平台限制 |
| 存储读取合规 | 视频读取通过后端授权或受控媒体链路，不绕过对象存储安全策略 |
| 回归覆盖 | 覆盖历史 SKU 详情页视频场景以及本次生产反馈页面的真机回归 |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-22 10:40:27 | /sprint-propose | 因暂时无法提供生产修复与验收条件，移出 sprint-010 正式范围，状态回到 approved，待条件具备后重新规划 |
| 2026-07-21 15:37:29 | /sprint-propose | 纳入 sprint-010 正式范围，容量估算更新为 16.0/30.0 人天 |
| 2026-07-21 15:32:00 | /bug-opsx | 创建 OpenSpec Change `fix-prod-miniapp-video-upstream-502`，状态 proposed |
| 2026-07-21 15:25:11 | lifecycle-stage-migrate | plan → review（/bug-review --approve） |
| 2026-07-21 15:24:31 | /bug-review --approve | 评审通过，状态更新为 approved，准备由 plan 迁入 review 阶段 |
| 2026-07-21 15:21:40 | /bug-complete | 补齐 root-cause、workaround、acceptance；状态更新为 pending_review |
| 2026-07-21 14:59:56 | /bug-generate | 生成 bug.md，状态更新为 draft |
| 2026-07-21 10:23:03 | /capture | 记录生产环境微信小程序视频暂时无法播放缺陷 |
