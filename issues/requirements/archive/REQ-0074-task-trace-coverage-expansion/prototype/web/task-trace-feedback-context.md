---
requirement_id: REQ-0074-task-trace-coverage-expansion
title: 复杂任务追踪标识反馈原型说明
status: approved
owner: product
created_at: 2026-07-26 13:02:05
updated_at: 2026-07-26 13:09:36
---

# 复杂任务追踪标识反馈原型说明

## 目标

本原型用于说明任务型接口接入 Task Trace 后，管理端在复杂任务发起后的反馈方式：展示任务状态、任务摘要、`task_trace_id`、复制入口和日志审计跳转入口。

## 适用场景

- 保存 SKU 或商品资料时需要追踪复杂保存链路。
- 批量上下架、批量删除、批量排序等批量任务。
- 导入导出、媒体处理、异步任务或复杂查询。
- 后端返回失败、处理中、部分成功或成功但需要排障标识的结果。

## 布局约束

- 追踪标识展示在任务反馈组件内，不挤占主要业务表单区域。
- 复制入口使用图标或图标 + 短文本按钮，复制反馈使用 fixed toast 或等价固定层。
- 长 `task_trace_id` 使用等宽字体、截断和 tooltip / 复制能力，不让移动端横向溢出。
- 失败摘要只展示安全错误码和脱敏说明，不展示内部路径、堆栈、原始请求体或敏感 metadata。
- 视觉必须使用 Design System semantic token；后续实现不得新增裸 Hex。

## 状态

| 状态 | 展示 |
|---|---|
| processing | 显示任务已接收、`task_trace_id`、可复制、可前往日志审计。 |
| success | 显示任务完成、耗时摘要、可复制追踪标识。 |
| failed | 显示失败错误码、失败摘要、可复制追踪标识。 |
| partial_success | 显示成功数、失败数、失败分类摘要和追踪标识。 |
| no_trace | 保持原有反馈，不显示空追踪组件。 |

## PNG Golden Reference

PNG Golden Reference 待后续设计确认后导出；当前 HTML 原型作为布局和信息层级参考。
