---
bug_id: BUG-0123-openspec-archive-proposal-warning-stdout
title: OpenSpec CLI proposal warning 仍通过 stdout 出现在归档成功输出中
severity: medium
status: done
owner:
discovered_at: 2026-08-06 12:10:56
environment: local
related_requirement:
related_change: fix-openspec-archive-proposal-warning-stdout
related_bug: BUG-0119-openspec-archive-scaffold-warning-noise
created_at: 2026-08-06 13:16:09
updated_at: 2026-08-06 13:57:15
---

# OpenSpec CLI proposal warning 仍通过 stdout 出现在归档成功输出中

## 现象

`scripts/archive-change.sh` 的归档成功路径仍会输出 OpenSpec CLI stdout 中的 proposal warning 块。BUG-0119 已处理项目自定义固定说明带来的噪音，但当前归档 wrapper 尚未吸收 CLI stdout 中已知的 proposal scaffold warning，导致 `/opsx-archive` 成功验收时仍出现不应暴露给用户的兼容性提示。

## 复现步骤

1. 准备一个中文优先的 OpenSpec Change，并使其满足归档条件。
2. 执行 `scripts/archive-change.sh <change-id>`，或通过 `/opsx-archive` 间接触发该 wrapper。
3. 观察归档成功输出中的 stdout 内容。

## 期望结果

- 归档成功时，stdout 不展示已知 proposal scaffold warning。
- 未知 stdout/stderr 仍需保留并展示，以免吞掉真实异常或诊断信息。
- BUG-0119 已修复的自定义固定说明噪音不回归。

## 实际结果

归档 wrapper 仍未过滤 OpenSpec CLI stdout 中的 proposal warning 块，导致归档成功输出出现已知噪音，影响 `/opsx-archive` 验收体验，也容易让用户误以为中文优先 Change 存在未处理的归档问题。

## 影响范围

- `scripts/archive-change.sh` 成功路径输出
- `/opsx-archive` 验收体验
- OpenSpec CLI stdout/stderr 噪音过滤策略

## 严重等级说明

严重等级：medium。

该问题不影响归档结果本身，也不改变 OpenSpec spec 合并结果，但会污染成功路径输出，降低 `/opsx-archive` 的验收清晰度。由于未知 stdout/stderr 仍必须保留，修复需要精确识别已知 proposal scaffold warning 块，避免过度吞输出。
