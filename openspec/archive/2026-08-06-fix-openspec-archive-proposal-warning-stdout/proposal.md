---
change_id: fix-openspec-archive-proposal-warning-stdout
type: fix
status: proposed
created_at: 2026-08-06 13:45:35
updated_at: 2026-08-06 13:45:35
related_bug: BUG-0123-openspec-archive-proposal-warning-stdout
related_sprint: sprint-021
---

# 修复 OpenSpec CLI proposal warning stdout 噪音

## 背景

BUG-0123 记录了 `/opsx-archive` 成功路径仍暴露 OpenSpec CLI stdout 中 proposal scaffold warning 的问题。BUG-0119 已修复项目自定义固定说明噪音，但底层归档 wrapper 仍未吸收 CLI stdout 中的已知 warning 块。

该 warning 与项目中文优先 OpenSpec 文档规范存在兼容性关系，不应要求回填英文脚手架标题；但未知 stdout/stderr 与失败诊断必须继续保留。

## 变更内容

- 扩展 `scripts/archive-change.sh` 的成功路径输出过滤策略，识别并吸收 OpenSpec CLI stdout 中已知 proposal scaffold warning 块。
- 保留未知 stdout/stderr、语言校验失败、OpenSpec CLI 非零退出和真实归档错误的可见诊断。
- 补充回归测试，覆盖已知 stdout warning 吸收、未知 stdout/stderr 保留、BUG-0119 不回归和失败路径诊断不丢失。
- 更新 `agent-workflow-tooling` 规格，明确已知兼容 warning 可能出现在 stdout 或 stderr。

## 回滚计划

若过滤策略误伤未知诊断输出，回滚 `scripts/archive-change.sh` 的过滤逻辑与对应测试，恢复为原始 stdout/stderr 透传；同时保留 BUG-0123 文档作为后续重新设计过滤边界的依据。

## 影响范围

- `scripts/archive-change.sh`
- `/opsx-archive` 成功路径体验
- OpenSpec 归档输出过滤相关测试
- `openspec/specs/agent-workflow-tooling/spec.md`

## 不影响

- 不修改 API、数据库、Web、小程序或管理端运行时代码。
- 不需要 Orval。
- 不修改 Docker Compose。
