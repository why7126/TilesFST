---
created_at: 2026-08-12 10:30:00
updated_at: 2026-08-12 10:30:00
---

# 强化 sprint-exps AI usage fresh gate 与矩阵写入流程

## 背景

`/sprint-exps` 首次复盘时可能遇到 AI usage snapshot 已存在但相对 Sprint 四件套或命令后置 hook 过期的情况。若执行者只依据首次 `--summary` 结论继续写复盘，容易把 stale snapshot 的矩阵当作真实成本矩阵展示，导致复盘成本分析口径失真。

## 变更内容

- 强化 `/sprint-exps` 命令规范：复盘前必须先检查 compact summary 的 fresh gate；遇到 stale/blocker 时先提示刷新 snapshot，刷新后必须重新运行 summary。
- 强化 Fact Sheet 脚本：`--ai-usage-markdown` 只有在 `fresh_gate.status=pass`、`snapshot_status=present`、`ai_usage_mode=actual` 且矩阵存在时才输出真实矩阵。
- 在 summary 中显式暴露矩阵写入 gate，避免只凭 `usage_matrices` 原始存在误判为可写入。
- 同步 AI usage 治理日志和变更历史。

## 边界

- 不修改 `src/` 业务运行时代码。
- 不改变后端 API、数据库、Web、小程序或管理端业务行为。
- 不直接修改 `openspec/specs/` 正式规格。
