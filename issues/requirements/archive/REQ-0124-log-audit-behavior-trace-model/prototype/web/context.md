---
requirement_id: REQ-0124-log-audit-behavior-trace-model
title: 日志审计补齐行为链路与任务链路采集模型 - 原型策略
status: pending_review
owner: product
source: requirement.md
created_at: 2026-08-25 22:31:11
updated_at: 2026-08-25 22:31:11
---

# 原型策略

## 1. UI 判定

本需求命中 `admin-list` 横切标签，影响管理端日志审计页的筛选、列表和详情联动。核心交付仍是数据采集结构与链路关联模型，不新建独立产品页面；后续实现应在既有日志审计页扩展查询入口和详情展示。

## 2. 本期原型策略

- 不生成独立 HTML 原型。
- 不生成 PNG Golden Reference。
- 后续 OpenSpec 实现时优先复用既有日志审计页、`AdminListPage` 或等价管理端列表 shell。
- 展示结构以“筛选栏 + 请求/行为列表 + 链路详情抽屉或详情区”为主，不做独立 BI 大屏或漏斗分析。
- 详情区只展示脱敏摘要、链路 ID、状态、耗时和流程节点，不展示完整请求体、完整响应体、Header、Cookie、Authorization、Token、真实密钥、本机路径或完整内部对象 key。

## 3. 后续 UI 约束

- 查询入口支持 `behavior_trace_id`、`request_id`、`task_trace_id`，长 ID 输入框和复制入口不得破坏筛选区布局。
- 列表分页使用后端真实分页与真实 total，保持 `page-summary` + `page-right` DOM 结构。
- 表头与普通字段默认 nowrap；链路 ID、URL、错误摘要等长文本使用截断、tooltip/title 或详情展开。
- 直接 API 调用或历史日志无行为链路时，用“无界面行为来源”或等价空态展示。
- 成功 / 失败反馈使用 fixed toast，不造成列表、详情区或分页纵向位移。
- 使用 Design System semantic token，不使用裸 Hex。
