---
change_id: tighten-bug-review-root-cause-confirmed-gate
status: applied
created_at: 2026-08-24 16:35:51
updated_at: 2026-08-24 16:40:37
source_command: /spec-opt
source_issue: null
sprint: sprint-025
---

# OpenSpec Change Trace

## 目标

收紧 BUG 评审通过门禁，确保 `/bug-review` 默认 approve 或显式 `--approve` 前，目标 BUG 的根因状态已经达到 `confirmed` 并具备可定位证据链。

## 影响范围

- `.agents/skills/bug-review/SKILL.md`
- `rules/root-cause-evidence.md`
- `rules/bug-management.md`
- `rules/agent-context-budget.md`
- `AGENTS.md`
- `docs/README.md`
- `scripts/validate-root-cause-evidence.py`
- `tests/test_validate_root_cause_evidence.py`
- `docs/spec-logs/`

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-24 16:40:37 | `/spec-opt` | 已完成规则、技能、脚本、测试、Sprint scope、验收和治理日志同步，目标 Change 进入 applied。 |
| 2026-08-24 16:35:51 | `/spec-opt` | 创建治理 Change，准备收紧 BUG review approve 根因 confirmed 门禁。 |
