---
created_at: 2026-08-24 16:39:04
updated_at: 2026-08-24 16:40:37
---

# BUG Review 根因 confirmed 门禁治理

## 迭代目标

收紧 `/bug-review` 默认 approve 和显式 `--approve` 的前置门禁，禁止 `root_cause_status` 非 `confirmed` 的 BUG 进入 `approved`、Sprint 和修复 Change。

## 变更摘要

- `/bug-review` approve 前必须运行 `python scripts/validate-root-cause-evidence.py --bug <BUG-id> --require-confirmed`。
- `unknown`、`hypothesis`、`probable`、缺少 `root-cause.md`、缺少根因状态、confirmed 缺少证据链均阻断 approve。
- 普通根因审计仍保留非 confirmed warning 语义，避免探索和批量扫描被误作为评审门禁。
- 新增聚焦测试覆盖 confirmed gate 与默认模式兼容。

## 影响范围

- 规则：BUG 生命周期、根因证据治理、上下文预算技能要求。
- 命令：`/bug-review`。
- 脚本：根因证据校验脚本。
- OpenSpec：`agent-workflow-tooling` delta spec。
- Sprint：`sprint-025` 纳入本治理 Change。

## 更新文件

- `AGENTS.md`
- `docs/README.md`
- `docs/spec-logs/CHANGELOG.md`
- `rules/root-cause-evidence.md`
- `rules/bug-management.md`
- `rules/agent-context-budget.md`
- `.agents/skills/bug-review/SKILL.md`
- `scripts/validate-root-cause-evidence.py`
- `tests/test_validate_root_cause_evidence.py`
- `openspec/changes/tighten-bug-review-root-cause-confirmed-gate/`
- `iterations/change/sprint-025/`

## 关键决策

- 已采纳：把非 confirmed 根因作为 approve blocker，确保已确认修复的 BUG 具备闭环证据。
- 已采纳：保留默认审计模式 warning 行为，只在 `--require-confirmed` 模式下硬阻断，避免影响探索态 BUG 的批量审计。
- 未采纳：自动升级 `probable` 为 `confirmed`；原因是 confirmed 必须由可定位证据链支撑，不能由门禁脚本推断。
- 替代方案：若后续需要更强自动化，可为 `/bug-complete` 增加交互式补证检查，但仍不得自动确认根因。

## 验证结果

- `uv run pytest tests/test_validate_root_cause_evidence.py`：通过，4 passed。
- `python scripts/validate-root-cause-evidence.py --bug BUG-0137-miniapp-lightweight-image-variant-consumption --require-confirmed`：预期阻断，`probable` 被报告为 blocker。
- `python scripts/validate-root-cause-evidence.py --bug BUG-0134-miniapp-certificate-detail-display-url --require-confirmed`：通过。
- `python scripts/validate-agent-context-budget.py`：通过。
- `python scripts/validate-openspec-language.py`：通过。
- `python scripts/validate-directory-structure.py`：通过。
- `openspec validate tighten-bug-review-root-cause-confirmed-gate`：通过。
- `python scripts/validate-sprint-scope.py sprint-025 --item tighten-bug-review-root-cause-confirmed-gate`：通过。
- `python scripts/validate-doc-prose-hygiene.py <focused-paths>`：退出码 0，报告 3 条启发式 warning，未发现敏感信息或需阻断问题。

## 产品影响

- API：无影响。
- 数据库：无影响。
- Web：无影响。
- 小程序：无影响。
- 管理端：无影响。
- Orval：不需要。
- Docker Compose：不需要。
- 测试：新增治理脚本聚焦测试。

## 后续建议

后续若发现 `/bug-complete` 经常产出 `probable` 后直接尝试 review，可另行优化 `/bug-complete` 输出，让下一步在证据不足时优先提示补证而不是 `/bug-review`。
