---
bug_id: BUG-0129-miniapp-rum-app-version-production
title: 小程序 RUM 与管理后台性能观测口径不一致
severity: medium
status: done
owner:
discovered_at: 2026-08-12 09:21:24
environment: miniapp-prod
related_requirement:
related_change: fix-miniapp-rum-performance-observability
created_at: 2026-08-12 09:42:46
updated_at: 2026-08-12 21:36:48
---

# 现象

管理后台“性能观测”页面展示小程序 RUM 数据时，存在多项口径和体验不一致问题：

1. 小程序 RUM 将 `production` 环境名作为 `app_version` 上报，导致版本号列显示 `production`，而不是与 Web 管理后台一致的产品版本号。
2. 小程序性能样本中的 `request_id` 为空，无法从性能样本跳转或复制追踪标识辅助排障。
3. 小程序指标名直接显示内部枚举，例如 `api_duration`、`app_launch_ready`，管理人员难以理解含义。
4. 性能观测列表无数据时显示“暂无性能样本”，但空态样式粗糙，字体和表格内空态层级不符合管理端列表体验。
5. 聚合列表看起来出现重复项：页面、版本号、端类型和指标完全相同，但样本数和分位数不同。实际原因是后端按 `network_type`、`device_class` 等隐藏维度分组，前端没有展示完整分组键。

# 复现步骤

## 版本号显示 production

1. 使用生产策略或生产等价配置运行微信小程序。
2. 进入任意已接入 RUM 的小程序页面，触发性能指标上报。
3. 登录 Web 管理后台，进入“性能观测”页面。
4. 筛选或查看 `wechat_miniapp` 端类型的聚合记录与样本明细。
5. 观察版本号列是否显示 `production`。

## request_id 为空

1. 在小程序中触发任意 RUM 性能上报。
2. 在管理后台性能观测页点击对应聚合行的“查看样本”。
3. 查看样本列表中的 `request_id` 列。
4. 观察小程序样本是否缺少可复制的 `request_id`。

## 指标名不可读

1. 在小程序中打开页面或触发接口请求。
2. 在管理后台性能观测页查看微信小程序端类型的数据。
3. 观察指标列是否直接显示 `api_duration`、`app_launch_ready`、`api_failed_duration` 等内部枚举。

## 空态样式不佳

1. 在管理后台性能观测页选择一个无匹配数据的筛选条件。
2. 观察列表区域显示“暂无性能样本”的字体、对齐、空间和视觉层级。

## 聚合行看似重复

1. 在管理后台性能观测页查看微信小程序端类型聚合数据。
2. 找到页面、版本号、端类型和指标相同的多条记录。
3. 对比样本数、P50、P75、P95、P99 等数值。
4. 观察这些记录是否因前端隐藏 `network_type`、`device_class` 而看起来像重复数据。

# 期望 vs 实际

## 期望

- 小程序与 Web 管理后台使用统一的产品版本号口径，`app_version` 表达真实产品/客户端版本，不混入 `production`、`development` 等运行环境名。
- 小程序 RUM 样本生成可用于排障的 `request_id`，并在管理后台样本页可见、可复制。
- 管理后台聚合页和样本页对小程序指标提供可读中文标签，例如：
  - `app_launch_ready`：小程序启动就绪
  - `api_duration`：接口请求耗时
  - `api_failed_duration`：接口失败耗时
- 性能观测空态使用管理端表格内空态样式，字号、颜色、居中和高度与日志审计、接口文档等列表体验一致。
- 聚合列表展示完整分组键，至少补充“网络”和“设备”列，避免同一页面、版本、端类型、指标下因隐藏维度不同而看起来重复。

## 实际

- 小程序无法读取 `wx.getAccountInfoSync().miniProgram.version` 时，兜底使用 `miniappApiConfig.environment`，生产配置下 `app_version` 变为 `production`。
- 小程序 RUM 上报 payload 没有携带 `request_id`，后端 schema 允许为空并原样保存。
- 管理后台性能观测页只映射了部分 Web 指标，小程序指标缺少中文标签，未知指标回退展示原始枚举值。
- 性能观测空态直接使用未规范化的 `empty-state` class，表格内空态视觉粗糙。
- 后端按 `client_type + page_key + metric_name + app_version + network_type + device_class` 聚合，但前端列表未展示 `network_type` 和 `device_class`，导致不同聚合组被误认为重复项。

# 影响范围

- 微信小程序 RUM 上报链路：
  - `src/miniapp/services/performance.ts`
  - `src/miniapp/services/performance.js`
  - `src/miniapp/services/api.ts`
  - `src/miniapp/services/api.js`
  - `src/miniapp/app.ts`
  - `src/miniapp/app.js`
- Web 管理后台性能观测页：
  - 聚合列表
  - 样本明细页
  - 指标筛选
  - 空态、加载态、错误态
  - “查看样本”跳转上下文
- 后端性能观测接口的既有响应字段展示口径：
  - `app_version`
  - `request_id`
  - `network_type`
  - `device_class`
  - `metric_name`
- 管理人员按版本、网络、设备和 request_id 排查小程序性能问题的效率。

# 严重等级说明

严重等级：`medium`。

理由：

- 不阻断小程序用户主流程，也不影响 RUM 数据写入。
- 但会直接影响管理后台性能观测的可信度和可读性：版本号口径错误、追踪标识缺失、指标名不可读、聚合行看似重复，都会降低排障效率。
- 问题集中在小程序 RUM 与管理后台性能观测展示口径，适合在同一修复 Change 中闭环。

# 初步根因线索

- 小程序 RUM 的 `appVersion()` 当前使用 `account.miniProgram.version || miniappApiConfig.environment || 'dev'`，导致环境名进入版本号字段。
- 小程序 RUM 上报对象没有 `request_id` 字段；Web RUM 已有 `rum-*` 生成策略。
- 小程序统一 API 封装已有 `clientRequestId`，但接口耗时 RUM 未复用或写入 `request_id`。
- 管理后台聚合页和样本页各自维护指标 label，且未覆盖小程序指标枚举。
- 后端聚合口径包含 `network_type` 和 `device_class`，前端聚合列表没有展示这两个分组维度。
- 性能观测页空态使用通用 `empty-state`，缺少表格内局部样式约束。

# 验收要点

- [ ] 小程序 RUM 上报的 `app_version` 与 Web 管理后台使用统一产品版本号来源或等价同步机制。
- [ ] 小程序无法获取平台版本号时，不再把 `production`、`development` 等环境名写入 `app_version`。
- [ ] 小程序 RUM 样本携带可用于排障的 `request_id`；管理后台样本页显示并可复制。
- [ ] 小程序 RUM 指标在聚合页、筛选下拉和样本页展示中文可读名称，至少覆盖 `app_launch_ready`、`api_duration`、`api_failed_duration`。
- [ ] 性能观测列表空态使用规范化的表格空态样式，字号、颜色、居中和高度与管理端列表体验一致。
- [ ] 聚合列表展示完整分组键，采用“展示完整分组键”方案补充网络和设备维度，避免隐藏维度造成疑似重复项。
- [ ] 点击“查看样本”时，网络和设备等分组上下文继续传递到样本页，样本页上下文展示完整。
- [ ] 回归 Web 管理后台 RUM 上报，确保现有 `PRODUCT_VERSION`、Web 指标标签和 request_id 生成策略不被破坏。
- [ ] 后端性能观测 API 不返回隐私、Header、Cookie、Authorization、签名 URL 或 raw payload。
