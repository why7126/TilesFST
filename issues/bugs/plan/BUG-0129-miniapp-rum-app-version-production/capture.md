---
bug_id: BUG-0129-miniapp-rum-app-version-production
status: captured
created_at: 2026-08-12 09:21:24
updated_at: 2026-08-12 09:21:24
severity_hint: medium
environment: miniapp-prod
related_requirement:
related_bug:
lifecycle_stage: plan
---

# 现象

小程序 RUM 将 `production` 环境名作为 `app_version` 上报，导致管理后台性能观测表中小程序样本的版本号显示为 `production`。

# 复现步骤

1. 使用生产策略或生产等价配置运行微信小程序。
2. 进入任意已接入 RUM 的小程序页面，触发性能指标上报。
3. 登录 Web 管理后台，进入“性能观测”页面。
4. 筛选或查看 `wechat_miniapp` 端类型的聚合记录与样本明细。
5. 观察版本号列是否显示 `production`。

# 期望 vs 实际

- 期望：小程序与 Web 管理后台使用统一的产品版本号口径，`app_version` 应表达真实产品/客户端版本，不应混入 `production`、`development` 等运行环境名；管理后台性能观测表可按统一版本号筛选、聚合和排障。
- 实际：小程序在无法读取 `wx.getAccountInfoSync().miniProgram.version` 时，兜底使用 `miniappApiConfig.environment`，生产配置下会把 `production` 写入 `app_version` 并展示到管理后台性能观测表。

# 影响范围

- 微信小程序 RUM 上报的 `app_version` 字段。
- 管理后台性能观测页的版本号展示、版本筛选、聚合分组和样本明细。
- 小程序与 Web 管理后台跨端性能数据对比和版本排障口径。

# 初步线索

- `src/miniapp/services/performance.ts` 的 `appVersion()` 当前使用 `account.miniProgram.version || miniappApiConfig.environment || 'dev'`。
- `src/miniapp/utils/env.ts` 生产策略默认 `environment: 'production'`。
- Web RUM 使用共享 `PRODUCT_VERSION` 上报，当前小程序与 Web 管理后台版本来源不一致。

# 建议验收或复现要点

- [ ] 小程序 RUM 上报的 `app_version` 与 Web 管理后台使用统一产品版本号来源或等价同步机制。
- [ ] 小程序无法获取平台版本号时，不再把 `production`、`development` 等环境名写入 `app_version`。
- [ ] 管理后台性能观测聚合表和样本明细中，小程序版本号不再显示 `production`。
- [ ] 保留运行环境与产品版本的语义边界；如需要环境信息，应使用独立字段或明确不纳入版本号列。
- [ ] 回归 Web 管理后台 RUM 上报，确保现有 `PRODUCT_VERSION` 口径不被破坏。

# 附件

- 暂无。
