---
change_id: fix-miniapp-usage-events-contract-drift
status: proposed
created_at: 2026-07-21 15:01:40
updated_at: 2026-07-21 15:26:34
source: bug
source_bug: BUG-0072-miniapp-usage-events-bad-request
related_requirement: REQ-0024-product-usage-logging
iteration: sprint-010
capabilities:
  - product-usage-logging
---

# Trace - fix-miniapp-usage-events-contract-drift

## 来源

| 类型 | ID | 说明 |
|---|---|---|
| BUG | `BUG-0072-miniapp-usage-events-bad-request` | 微信小程序 usage-events 上报接口频繁返回 400 |
| REQ | `REQ-0024-product-usage-logging` | 产品使用行为埋点与接口请求日志详情 |
| Capability | `product-usage-logging` | 产品使用行为事件采集与使用行为事件接收 API |

## Bug Analysis Report

| 项 | 内容 |
|---|---|
| 现象 | 微信小程序多个页面或组件调用 `POST /api/v1/usage-events` 返回 400 |
| 复现 | 进入收藏页、品牌详情页、SKU 详情页品牌入口或商品/品牌卡片组件，观察 usage-events 请求 |
| 影响 | 控制台和 Network 400 噪音；收藏、品牌、卡片等行为事件统计缺失；影响热销/访问分析和排查 |
| 根因分类 | code / contract |
| 严重等级 | high |
| Hotfix | 常规优先；生产环境刷屏严重时可热修 |

## 状态记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-21 15:01:40 | /bug-opsx | 创建修复 Change，状态 proposed |
| 2026-07-21 15:26:34 | /sprint-propose | 纳入 sprint-010，等待 `/opsx-apply fix-miniapp-usage-events-contract-drift` |
