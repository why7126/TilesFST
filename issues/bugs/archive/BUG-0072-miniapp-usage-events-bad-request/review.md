---
bug_id: BUG-0072-miniapp-usage-events-bad-request
title: 微信小程序 usage-events 上报接口频繁返回 400
status: done
review_result: approved
reviewed_at: 2026-07-21 14:57:01
reviewer: AI
severity: high
created_at: 2026-07-21 14:57:01
updated_at: 2026-07-22 08:47:45
related_requirement: REQ-0024-product-usage-logging
related_change: fix-miniapp-usage-events-contract-drift
---

# 评审结论

确认修复，状态评审为 `approved`。

# 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | 已通过静态枚举对比和 TestClient 验证未知事件返回 `40001 未知埋点事件`，字段缺失返回明确 400 |
| 严重等级合理 | 通过 | 影响多个小程序页面和通用组件，导致大量 400 噪音与使用行为统计缺失，`high` 合理 |
| 回归验收明确 | 通过 | `acceptance.md` 已覆盖事件字典、收藏页、品牌详情页、商品/品牌卡片、安全校验、统计写入与防漂移测试 |
| 是否需 hotfix 路径 | 常规优先，必要时热修 | 不阻断用户主流程，但影响统计完整性和调试体验；若生产环境 400 刷屏严重，可纳入热修 |

# 批准理由

`BUG-0072` 属于已交付产品使用事件上报能力与小程序新增埋点之间的契约漂移。后端保持未知事件和敏感字段拒绝是正确安全边界，但小程序合法事件未同步进入后端事件字典，导致大量 400 和统计缺失，应进入修复流程。

# 后续门禁

- 可执行 `/bug-opsx BUG-0072-miniapp-usage-events-bad-request` 创建 OpenSpec 修复 Change。
- 可纳入 Sprint 正式范围。
- 来源于 BUG 的 Change 在 `/opsx-apply` 前必须先纳入某个 `sprint-xxx`。
