---
bug_id: BUG-0129-miniapp-rum-app-version-production
created_at: 2026-08-12 14:19:46
updated_at: 2026-08-12 14:19:46
root_cause_status: completed
category:
  - code
  - ui
  - observability-design
---

# 根因分析

## 直接原因

小程序 RUM 与 Web 管理端 RUM 在字段来源、追踪标识和展示映射上没有统一：

1. `app_version` 直接原因：小程序 `appVersion()` 在无法读取 `wx.getAccountInfoSync().miniProgram.version` 时，兜底使用 `miniappApiConfig.environment`，生产策略下写入 `production`。
2. `request_id` 直接原因：小程序 `reportPerformanceMetric()` 构造上报 payload 时没有携带 `request_id`；后端 `PerformanceEventCreate.request_id` 允许为空，repository 原样保存。
3. 指标不可读直接原因：管理后台性能聚合页和样本页各自维护指标 label，当前只覆盖部分 Web 指标，缺少小程序指标 `app_launch_ready`、`api_duration`、`api_failed_duration`。
4. 空态样式直接原因：性能观测页使用通用 `empty-state` class，未定义性能表格内局部空态样式。
5. 聚合疑似重复直接原因：后端按 `client_type + page_key + metric_name + app_version + network_type + device_class` 聚合；前端列表只展示页面、版本号、端类型和指标，隐藏了 `network_type` 与 `device_class`。

## 根本原因

小程序 RUM 接入时更偏向“能上报”，没有形成与 Web RUM 和管理端观测页面一致的字段契约：

- 版本字段没有统一产品版本来源，误把运行环境作为版本兜底。
- 追踪字段缺少跨端统一生成策略；小程序 API 封装已有 `clientRequestId`，但性能 RUM 没有复用或生成独立 `request_id`。
- 管理端展示没有把后端聚合契约中的所有分组维度作为用户可见信息。
- 指标 label 没有集中维护，导致新增小程序指标后聚合页和样本页映射漂移。
- 空态样式没有复用管理端列表的表格空态模式，导致性能观测页在无数据时视觉层级异常。

## 触发条件

- 使用生产策略或生产等价配置运行微信小程序。
- 小程序平台版本号读取为空，或本地/体验环境无法提供真实 `miniProgram.version`。
- 小程序页面启动、接口成功或接口失败触发 RUM 上报。
- 管理后台性能观测页查看 `wechat_miniapp` 聚合数据或样本明细。
- 聚合数据中存在不同 `network_type` 或 `device_class` 的同页面、同版本、同端、同指标记录。

## 证据

| 问题 | 证据 |
|---|---|
| 环境名写入版本号 | `src/miniapp/services/performance.ts` 中 `appVersion()` 使用 `account.miniProgram.version || miniappApiConfig.environment || 'dev'` |
| request_id 为空 | `src/miniapp/services/performance.ts` 的 RUM payload 未包含 `request_id` |
| API 封装已有客户端 ID 但 RUM 未用 | `src/miniapp/services/api.ts` 生成 `clientRequestId` 并写入 `x-client-request-id`，但 `reportPerformanceMetric()` 调用未传 request_id |
| 指标 label 不完整 | `PerformanceRumPage.tsx`、`PerformanceSamplesPage.tsx` 只映射部分 Web 指标 |
| 聚合隐藏维度 | `performance_repository.py` 按 `network_type`、`device_class` 分组，但 `PerformanceRumPage.tsx` 表格未展示这两列 |
| 空态样式不完整 | 性能观测页直接使用 `empty-state`，而日志审计、接口文档有独立表格空态样式 |

## 修复方向

1. 小程序 RUM 版本号与 Web 管理后台统一到产品版本来源；禁止环境名进入 `app_version`。
2. 小程序 RUM 生成或传递稳定的性能样本 `request_id`，并确保后端保存、管理端展示和复制。
3. 将性能指标 label 抽成聚合页和样本页共用映射，补齐小程序指标。
4. 聚合列表补充“网络”“设备”列，并在“查看样本”跳转中继续传递这两个上下文。
5. 为性能观测空态添加局部表格空态样式，避免受未规范化通用 class 影响。
