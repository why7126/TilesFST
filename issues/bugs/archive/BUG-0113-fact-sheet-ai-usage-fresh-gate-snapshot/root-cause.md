---
bug_id: BUG-0113-fact-sheet-ai-usage-fresh-gate-snapshot
created_at: 2026-08-04 08:22:00
updated_at: 2026-08-04 08:22:00
root_cause_status: completed
category: code
---

# Root Cause

## 直接原因

Fact Sheet AI usage fresh gate 读取到的 freshness 输入与已刷新 snapshot 的真实状态不一致。当前缺陷尚未进入代码定位阶段，直接原因需要在后续 `/bug-explore` 或修复 Change 中确认，重点怀疑以下任一偏差：

- stale 判定使用了错误的时间来源，例如旧 snapshot 时间、命令运行时间、文件 mtime 或未刷新缓存。
- fresh gate 对 snapshot 状态字段的解释与 snapshot 生成端不一致。
- usage mode 映射表未覆盖已刷新状态，导致 refreshed / actual 类状态被误映射为 stale、skipped 或 unavailable。
- snapshot 刷新成功后，gate 仍读取旧路径或旧 payload。

## 根本原因

AI usage snapshot 与 fresh gate 之间缺少统一的状态契约和回归覆盖。生成端、刷新端、gate 校验端和 mode 映射端如果各自维护状态语义，就容易在字段名、时间戳、刷新结果或 fallback mode 上产生漂移。

## 触发条件

- Fact Sheet AI usage snapshot 已刷新，但 fresh gate 随后执行。
- snapshot 状态、时间戳或 usage mode 需要被 gate 二次解释。
- gate 读取到的 payload、路径或映射逻辑与刷新流程输出不完全一致。

## 分类

- 类型：code
- 子类：state-mapping / freshness-gate
- 风险：校验误报、发布/验收证据状态不可信

## 待确认

- fresh gate 当前读取的 snapshot 路径和刷新流程写入路径是否一致。
- stale 判定使用的是 snapshot 内部时间戳、文件 mtime，还是命令运行记录时间。
- usage mode 映射是否显式覆盖 refreshed / actual / skipped / unavailable / stale。
- 已刷新 snapshot 的状态字段是否被后续流程覆盖或降级。
