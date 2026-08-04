---
bug_id: BUG-0113-fact-sheet-ai-usage-fresh-gate-snapshot
title: Fact Sheet AI usage fresh gate 与已刷新 snapshot 状态不一致
status: done
severity: medium
priority: P2
source: "/bug-capture"
created_at: 2026-08-04 08:18:50
updated_at: 2026-08-04 09:17:03
related_requirement: null
related_bug: null
iteration: null
openspec_changes: []
---

# BUG-0113 Fact Sheet AI usage fresh gate 与已刷新 snapshot 状态不一致

## 现象

Fact Sheet AI usage fresh gate 与已刷新 snapshot 状态不一致。需要定位 stale 判定或 mode 映射是否存在偏差。

## 复现步骤

1. 执行或查看 Fact Sheet AI usage 相关流程，确保 snapshot 已完成刷新。
2. 观察 fresh gate 对该 snapshot 的判定结果。
3. 对比 snapshot 状态、fresh/stale 标记、usage mode 映射结果与最终门禁输出。

## 期望 vs 实际

- 期望：已刷新 snapshot 应通过 fresh gate，或给出与 snapshot 实际刷新状态一致的 usage mode / stale 判定。
- 实际：fresh gate 与已刷新 snapshot 状态不一致，表现为仍被判定为 stale 或映射到不符合当前 snapshot 状态的 mode。

## 影响范围

- Fact Sheet AI usage 生成、校验或展示流程。
- snapshot freshness 判定逻辑。
- usage mode 映射与门禁报告。
- 依赖该 gate 的发布、验收或 workflow usage 证据可信度。

## 建议验收或复现要点

- 构造已刷新 snapshot，确认 fresh gate 不再误报 stale。
- 构造过期 snapshot，确认 stale 判定仍能正确拦截。
- 覆盖 snapshot 状态到 usage mode 的映射表，确认 refreshed / skipped / unavailable 等状态不会互相串位。
- 补充回归测试，固定 fresh gate 与 snapshot timestamp / status / mode 的一致性。

## 附件

暂无。
