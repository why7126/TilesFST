---
bug_id: BUG-0124-openspec-archive-multiline-proposal-warning-stdout
title: OpenSpec CLI 多行 proposal warning stdout 块仍出现在归档成功输出中
severity: medium
status: done
owner:
discovered_at: 2026-08-06 14:02:15
environment: local
related_requirement:
related_change:
related_bug: BUG-0123-openspec-archive-proposal-warning-stdout
created_at: 2026-08-06 14:09:46
updated_at: 2026-08-06 15:08:49
---

# OpenSpec CLI 多行 proposal warning stdout 块仍出现在归档成功输出中

## 现象

`fix-openspec-archive-proposal-warning-stdout` 已归档后，真实归档成功输出中仍展示 OpenSpec CLI 的多行 proposal warning 块，例如：

```text
Proposal warnings in proposal.md ...
Missing required sections ...
```

这说明当前归档 wrapper 的 stdout 过滤仍未覆盖 CLI 返回的多行 warning 块，导致已知兼容性提示继续出现在成功路径输出里。

## 复现步骤

1. 准备或复用会触发 OpenSpec CLI proposal warning 的 Change。
2. 执行 `scripts/archive-change.sh <change-id>`，或通过 `/opsx-archive` 间接触发归档。
3. 观察归档成功路径输出中的 stdout 内容。

## 期望结果

- 真实 OpenSpec CLI 多行 proposal warning 块被整体吸收。
- 归档成功输出不展示 `Proposal warnings in proposal.md`、`Missing required sections` 等已知兼容性 warning 块。
- 未知 stdout/stderr 仍保留并展示，避免吞掉真实异常或诊断信息。
- 既有单行 warning 回归测试继续通过。

## 实际结果

归档成功输出仍展示 OpenSpec CLI 多行 proposal warning 块，说明此前修复可能只覆盖了单行 warning 或固定形态，未处理完整多行块。

## 影响范围

- `scripts/archive-change.sh` 成功路径输出。
- `/opsx-archive` 归档验收体验。
- OpenSpec CLI stdout/stderr 多行 warning 过滤策略。

## 严重等级说明

严重等级为 `medium`。该问题不影响归档事实落盘和 OpenSpec archive 结果，但会在成功路径继续暴露已知噪音，干扰 `/opsx-archive` 验收判断，并可能让用户误以为归档仍存在阻塞项。

## 来源

- 来源 Change：`fix-openspec-archive-proposal-warning-stdout`
- 来源 Sprint：`sprint-021`
- 来源命令：`/opsx-archive`
- 相关历史缺陷：`BUG-0123-openspec-archive-proposal-warning-stdout`
