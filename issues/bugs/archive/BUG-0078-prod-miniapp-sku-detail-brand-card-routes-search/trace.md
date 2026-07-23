---
bug_id: BUG-0078-prod-miniapp-sku-detail-brand-card-routes-search
status: done
lifecycle_stage: archive
severity: medium
created_at: 2026-07-21 10:29:03
updated_at: 2026-07-22 09:00:50
lifecycle:
  captured: 2026-07-21 10:29:03
  generated: 2026-07-21 14:00:16
  completed: 2026-07-21 14:40:30
  reviewed: 2026-07-21 14:56:26
  approved: 2026-07-21 14:56:26
iteration: sprint-010
related_requirement: REQ-0044-miniapp-sku-detail-page
related_bug: null
related_change: fix-miniapp-sku-detail-brand-card-route
source_command: /bug-capture
openspec_changes:
  - change_id: fix-miniapp-sku-detail-brand-card-route
    type: fix
    status: archived
related_bugs: []
---

```yaml
bug_id: BUG-0078-prod-miniapp-sku-detail-brand-card-routes-search
status: done
severity: medium
lifecycle_stage: review
created_at: 2026-07-21 10:29:03
updated_at: 2026-07-21 22:55:44
lifecycle:
  captured: 2026-07-21 10:29:03
  generated: 2026-07-21 14:00:16
  completed: 2026-07-21 14:40:30
  reviewed: 2026-07-21 14:56:26
  approved: 2026-07-21 14:56:26
iteration: sprint-010
related_requirement: REQ-0044-miniapp-sku-detail-page
related_bug: null
related_change: fix-miniapp-sku-detail-brand-card-route
source_command: /bug-capture
openspec_changes:
  - change_id: fix-miniapp-sku-detail-brand-card-route
    type: fix
    status: archived
related_bugs: []
scope:
  terminal: miniapp
  environment: prod
  page: sku_detail
  module: product_parameters_brand_card
  issue_type: route_target_mismatch
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
| 用户反馈 | `/bug-capture` | 生产环境微信小程序商品详情页「商品参数」品牌卡片误跳搜索页 |
| 关联需求 | `REQ-0044-miniapp-sku-detail-page` | 商品详情页能力已交付，当前为品牌入口路由行为偏差 |

## 建议复现要点

| 要点 | 说明 |
|---|---|
| 环境 | 使用生产环境微信小程序复现，并记录小程序版本、基础库版本、iOS / Android 设备信息 |
| 商品样例 | 记录至少 2 个带品牌参数的商品 SKU，确认是否所有品牌卡片均误跳搜索页 |
| 品牌数据 | 确认商品返回的品牌 ID、品牌 slug 或品牌详情页所需路由参数是否存在 |
| 跳转路径 | 对比点击品牌卡片时实际 `navigateTo` 路径与预期品牌详情页路径 |
| 回归范围 | 同步检查详情页其他品牌入口或底部品牌按钮，避免存在重复或不一致跳转 |

## 建议验收要点

| 验收点 | 说明 |
|---|---|
| 路由正确 | 商品详情页「商品参数」品牌卡片点击后进入对应品牌详情页 |
| 参数正确 | 品牌详情页能收到正确品牌 ID / slug，并展示对应品牌信息 |
| 无搜索误跳 | 点击品牌卡片不再跳转搜索页或搜索结果页 |
| 异常兜底 | 缺少品牌 ID 或品牌未上架时有明确不可跳转/提示策略，不误导到搜索页 |
| 生产回归 | 微信开发者工具、体验版和生产环境至少各完成一次路由回归 |

## 验收证据

| 时间 | 类型 | 证据 |
|---|---|---|
| 2026-07-21 22:55:44 | API 回归 | `uv run pytest tests/test_miniapp_home.py` 通过 29 项；`GET /api/v1/miniapp/skus/1` 返回 `data.brand.brand_entry_path` 为 `/pages/brand-detail/index?brandId=1` |
| 2026-07-21 22:55:44 | 路由契约 | `tests/test_miniapp_home.py` 同时回归品牌列表页入口仍返回 `/pages/brand-detail/index?brandId=1` |
| 2026-07-21 22:55:44 | 小程序静态回归 | `uv run pytest tests/test_miniapp_static.py` 通过 27 项；SKU 详情页继续使用 `brand-card`，品牌详情页继续注册在 `app.json` |
| 2026-07-21 22:55:44 | 影响评估 | 仅调整既有字段取值，不改 API Schema、数据库、Web 管理端、媒体上传、MinIO 或 Docker；不需要 OpenAPI / Orval |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-22 09:00:45 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-miniapp-sku-detail-brand-card-route） |
| 2026-07-22 09:00:17 | /opsx-archive | Change `fix-miniapp-sku-detail-brand-card-route` 已归档，状态同步完成。 |
| 2026-07-21 22:57:10 | /opsx-apply | Change `fix-miniapp-sku-detail-brand-card-route` apply 完成，待 archive。 |
| 2026-07-21 22:55:44 | /opsx-apply | 修复 SKU 详情品牌卡片误跳搜索页，回归接口与小程序静态测试 |
| 2026-07-21 15:22:32 | /sprint-propose | 纳入 sprint-010 正式范围 |
| 2026-07-21 15:01:23 | /bug-opsx | 创建 OpenSpec Change `fix-miniapp-sku-detail-brand-card-route` |
| 2026-07-21 14:56:59 | lifecycle-stage-migrate | plan → review（/bug-review --approve） |
| 2026-07-21 14:56:26 | /bug-review --approve | 评审通过，允许进入 bug-opsx 与 Sprint 规划 |
| 2026-07-21 14:40:30 | /bug-complete | 补齐 root-cause、workaround、acceptance，状态推进为 pending_review |
| 2026-07-21 14:00:16 | /bug-generate | 生成缺陷正式说明 bug.md，状态推进为 draft |
| 2026-07-21 10:29:03 | /bug-capture | 记录生产环境小程序商品详情页品牌卡片误跳搜索页缺陷 |
