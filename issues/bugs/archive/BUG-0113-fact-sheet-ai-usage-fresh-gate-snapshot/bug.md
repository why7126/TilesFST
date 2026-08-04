---
bug_id: BUG-0113-fact-sheet-ai-usage-fresh-gate-snapshot
title: Fact Sheet AI usage fresh gate 与已刷新 snapshot 状态不一致
severity: medium
status: done
owner:
discovered_at: 2026-08-04 08:18:50
environment: local
related_requirement:
related_change: fix-fact-sheet-ai-usage-fresh-gate-snapshot
created_at: 2026-08-04 08:22:39
updated_at: 2026-08-04 09:16:43
---

# BUG-0113 Fact Sheet AI usage fresh gate 与已刷新 snapshot 状态不一致

## 现象

Fact Sheet AI usage fresh gate 与已刷新 snapshot 状态不一致。snapshot 已完成刷新后，门禁结果仍可能表现为 stale，或 usage mode 被映射为与刷新状态不匹配的值。

## 复现步骤

1. 执行 Fact Sheet AI usage 相关命令或校验流程，使目标 snapshot 完成刷新。
2. 查看 snapshot 的刷新时间、状态字段和输出路径，确认它不是过期或缺失状态。
3. 继续执行 fresh gate 或依赖该 gate 的 Fact Sheet 校验。
4. 对比 fresh gate 输出的 stale/fresh 判断、usage mode、warning/recommended action 与 snapshot 实际状态。

## 期望

- 已刷新且有效的 snapshot 应通过 fresh gate。
- usage mode 应与 snapshot 状态一致，例如 refreshed/actual 类状态不应被映射为 unavailable、skipped 或 stale。
- 如果 snapshot 确实过期，fresh gate 应明确给出 stale 原因，并与 timestamp / status 字段一致。

## 实际

fresh gate 与已刷新 snapshot 状态不一致，表现为已刷新 snapshot 仍可能被 stale 判定拦截，或 mode 映射结果与 snapshot 实际刷新状态不一致。

## 影响范围

- Fact Sheet AI usage 证据生成、刷新和校验。
- snapshot freshness gate 的可信度。
- usage mode 映射与报告展示。
- 依赖 AI usage snapshot 的发布、验收、workflow 追踪或 Fact Sheet 输出判断。

## 严重等级说明

严重等级为 `medium`。该问题不会直接破坏业务数据或线上核心功能，但会影响 AI usage 证据的准确性和门禁可信度，可能导致已刷新证据被误拦截，或让验收/发布流程依据错误状态继续推进。
