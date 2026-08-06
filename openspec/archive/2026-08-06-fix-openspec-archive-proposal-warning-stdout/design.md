---
change_id: fix-openspec-archive-proposal-warning-stdout
status: proposed
created_at: 2026-08-06 13:45:35
updated_at: 2026-08-06 13:45:35
---

# 设计

## 根因

`scripts/archive-change.sh` 对 OpenSpec CLI 输出的过滤只覆盖了部分已知噪音。BUG-0119 处理了项目自定义固定说明，但未覆盖 OpenSpec CLI 通过 stdout 输出的 proposal scaffold warning 块，导致归档成功路径仍展示已知兼容 warning。

## 修复方案

在归档 wrapper 中引入更精确的输出分类：

- 将 OpenSpec CLI stdout/stderr 分别捕获。
- 对已知 proposal scaffold warning 块执行精确匹配并吸收。
- 若 stdout/stderr 中存在不属于已知 warning 的内容，继续展示。
- CLI 非零退出、语言校验失败、目录结构校验失败和真实归档错误继续阻断。

## 过滤边界

可吸收内容仅限已确认的 proposal scaffold warning，例如提示 `proposal.md` 缺少英文 `## Why` / `## What Changes` 但项目语言校验已通过的兼容性块。

不得吸收：

- 未知 stdout。
- 未知 stderr。
- OpenSpec CLI 非零退出信息。
- `python scripts/validate-openspec-language.py` 失败信息。
- 目录结构、spec 校验、归档路径或文件系统错误。

## 测试策略

- 使用 shell wrapper 或可替代命令 fixture 模拟 OpenSpec CLI stdout warning。
- 覆盖 stdout 已知 warning 被吸收。
- 覆盖未知 stdout/stderr 保留。
- 覆盖 OpenSpec CLI 失败仍返回非零。
- 覆盖 BUG-0119 自定义固定说明噪音不回归。

## 风险

主要风险是过滤模式过宽导致真实诊断被吞。实现必须使用白名单式精确匹配，并通过未知 stdout/stderr 回归测试兜底。
