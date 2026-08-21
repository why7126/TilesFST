---
change_id: default-review-approve-command
status: proposed
created_at: 2026-08-21 13:45:41
updated_at: 2026-08-21 13:45:41
sprint: sprint-024
---

# 调整评审命令默认通过行为

## 背景

`/req-review` 与 `/bug-review` 是需求和缺陷进入 Sprint 前的高频评审命令。当前正向路径需要反复显式追加 `--approve`，而多数评审命令调用本身已经表达“确认通过并继续推进”的意图，导致用户操作冗余，也让命令示例在多个治理文件中持续传播旧写法。

## 变更内容

- 将 `/req-review REQ-xxxx` 默认解释为 `approve`。
- 将 `/bug-review BUG-xxxx` 默认解释为 `approve`。
- 保留反向结果的显式 flag：`--reject`、`--defer`，BUG 额外保留 `--wont-fix`。
- 同步 `AGENTS.md`、`rules/` 与相关 Skill 的命令示例，使后续提示默认使用无 flag 正向路径。
- 保留目录迁移、Workflow Sync、AI Usage hook 与 Sprint 门禁不变。

## 影响范围

- 影响治理命令语义和文档提示。
- 不修改业务 `src/` 代码。
- 不影响 API、数据库、Web、小程序、管理端、Orval 或 Docker Compose。

## 回滚计划

如后续评审希望恢复显式 approve，可将 `/req-review` 与 `/bug-review` 的无 flag 行为恢复为评审检查清单提示，并把正向示例恢复为带 `--approve` 的形式。
