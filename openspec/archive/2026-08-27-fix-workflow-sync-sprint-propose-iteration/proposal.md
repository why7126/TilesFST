---
created_at: 2026-08-27 00:00:00
updated_at: 2026-08-27 00:00:00
---

# 修复 Sprint Propose 后 Issue 迭代回填

## 背景

`/sprint-propose` 将已评审 REQ/BUG 纳入 `sprint.yaml` 正式范围后，Workflow Sync 会把 Issue 状态推导为 `in_sprint`，但当前 `patch_issue_trace()` 未同步写入 `trace.md` 的 `iteration` 字段。后续 `/req-opsx`、`/bug-opsx`、`/opsx-apply --sprint auto` 依赖 Issue 与 Sprint 机器事实一致，缺少 `iteration` 会造成状态漂移和人工误判。

## 变更内容

- 调整 Workflow Sync，使已纳入 Sprint 正式范围的 focused REQ/BUG 在 `sprint.propose` 同步后自动回填 `iteration: sprint-xxx`。
- 保持未纳入 Sprint 的 Issue 不写入 `iteration`，避免绕过评审和 Sprint scope 门禁。
- 补充聚焦回归测试，覆盖 `approved + iteration: null` 的 REQ 在 `sprint.propose` 后同步为 `in_sprint + iteration: sprint-xxx`。

## 影响范围

- 影响治理脚本：`scripts/workflow_sync/patch.py`、`scripts/workflow_sync/engine.py`。
- 影响测试：Workflow Sync 聚焦测试。
- 不影响业务 `src/`、API、数据库、Web、小程序、管理端、Orval 或 Docker Compose。

