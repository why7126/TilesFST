# BUG 评审通过根因 confirmed 门禁

## 背景

BUG 流程已经要求根因状态区分 `unknown`、`hypothesis`、`probable`、`confirmed`，并要求 confirmed 根因绑定可定位证据链。现有 `/bug-review` 默认 approve 语义已经固化，但 approve 前尚未明确要求 `root_cause_status: confirmed`，可能让仍处于推测态的 BUG 进入 Sprint 和修复 Change。

## 变更内容

- 收紧 BUG 评审通过门禁：默认 approve 或显式 `--approve` 前必须校验 `root_cause_status: confirmed`。
- 缺少 `root-cause.md`、缺少根因状态、状态为 `unknown` / `hypothesis` / `probable`、或 confirmed 缺少证据链时，均阻断 approve。
- 为 `scripts/validate-root-cause-evidence.py` 增加 review/approve 专用 confirmed 模式，并补充聚焦测试。
- 同步 `rules/`、`.agents/skills/bug-review/`、入口摘要、OpenSpec Change 和治理日志。

## 不在范围

- 不修改业务 `src/`、API、数据库、Web、小程序或管理端实现。
- 不自动改写既有 BUG 的根因状态或证据内容。
- 不改变 `--reject`、`--defer`、`--wont-fix` 的非 approve 评审路径。

## 风险与回滚

- 风险：已有 `probable` 或缺证据 BUG 将无法直接 approve，需要先补证或选择非 approve 评审结果。
- 回滚：移除 `--require-confirmed` 门禁调用，并恢复规则与测试；不涉及业务数据迁移。
