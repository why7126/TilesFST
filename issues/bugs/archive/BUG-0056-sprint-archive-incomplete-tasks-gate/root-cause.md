---
bug_id: BUG-0056-sprint-archive-incomplete-tasks-gate
created_at: 2026-07-04 15:04:22
updated_at: 2026-07-04 15:04:22
---

# Root Cause

## 直接原因

`/sprint-archive` 的命令说明中虽然声明 `tasks_incomplete > 0` 默认阻断，但归档流程没有调用一个会返回非零退出码的校验脚本。

## 根本原因

Sprint 归档门禁主要依赖人工阅读 Archive Queue Report，缺少自动化、可测试、可复用的前置检查。已有 `workflow_sync` 能统计 change task 进度，但它属于状态同步工具，不会在归档前阻断执行。

## 触发条件

- change 的 `tasks.md` 存在 `- [ ]` 项；
- 执行者继续执行 `/sprint-archive`；
- 流程没有先运行硬校验命令并检查退出码。

## 分类

workflow / tooling / process-gate
