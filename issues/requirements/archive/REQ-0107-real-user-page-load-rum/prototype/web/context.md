---
requirement_id: REQ-0107-real-user-page-load-rum
status: pending_review
created_at: 2026-08-10 22:56:55
updated_at: 2026-08-10 22:56:55
---

# Web Prototype Context

## 目标

为后续管理端真实用户性能观测页面提供信息架构和视觉验收方向。当前阶段只沉淀 prototype 策略，不替代 OpenSpec design 和实现。

## 页面定位

- 入口：管理端系统观测或日志审计相邻入口，具体路由在 OpenSpec 阶段确认。
- 用户：系统管理员、研发 / 运维人员、产品负责人。
- 目标：快速判断小程序、店主 Web、管理端 Web 的真实用户加载体验，定位慢页面、慢指标和版本波动。

## 建议布局

```text
页面标题 + 时间范围 / 端类型 / 页面 / 版本 / 网络筛选
  |
  v
摘要指标：样本量、P75 首屏可用、P95 首屏可用、慢页面数、错误上报数
  |
  v
趋势区：首屏可用 P75/P95 趋势、按版本对比
  |
  v
排行区：慢页面排行、慢指标排行
  |
  v
明细区：页面维度聚合表，支持样本不足、空数据、加载失败状态
```

## 设计约束

- 遵守“工业石材 · 暗色旗舰风” Design System。
- 使用 `bg-page`、`bg-surface`、`text-primary`、`text-secondary`、`text-brand-gold`、`border-border-default` 等 semantic token。
- 复用现有管理端筛选、指标卡、表格、分页、空态和错误态组件。
- 图表只承载趋势和对比，不做装饰性图形。
- 分位耗时必须同时展示统计口径和样本量。
- 页面不展示敏感字段原值；页面 key、版本、网络和设备类别使用受控枚举或脱敏值。

## 待导出

- PNG Golden Reference：待 OpenSpec design 确认首期是否包含管理端页面后导出。
