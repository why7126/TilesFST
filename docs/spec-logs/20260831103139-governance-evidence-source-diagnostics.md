---
created_at: 2026-08-31 10:31:39
updated_at: 2026-08-31 10:31:39
source: /spec-opt deactivate-environment-tiered-evidence-gates
---

# 证据来源诊断降级治理日志

## 迭代目标

将“环境分层 evidence / 生产证据后置”从默认 workflow 阻断门禁降级为手动证据来源诊断工具，避免与本项目单一发布语义冲突。

## 变更摘要

- 保留 `scripts/validate-environment-tiered-evidence.py` 和 `scripts/environment_tiered_evidence.py` 的诊断能力。
- 从 `validate-release.py`、`validate-sprint-archive-readiness.py`、`validate-archive-evidence.py` 默认链路中移除自动诊断调用。
- 将规则、Skill 和 standards 文案收敛为“证据来源声明 / 证据来源诊断”。
- 新流程不再推荐 `production_only_pending`，仅作为历史兼容字段或诊断脚本内部兼容逻辑保留。
- 补充 release 默认校验不被证据来源诊断阻断的回归测试，调整 sprint archive readiness 预期。

## 影响范围

| 层级 | 影响 |
|---|---|
| API | 不涉及 |
| DB | 不涉及 |
| Web | 不涉及 |
| 小程序 | 仅更新小程序 evidence 模板文案，不改运行时代码 |
| 管理端 | 不涉及 |
| Orval | 不涉及 |
| Docker Compose | 不涉及 |
| 发布治理 | release validator 不再自动应用证据来源诊断 |
| Sprint / OpenSpec 归档治理 | sprint archive readiness 与 archive evidence validator 不再自动应用证据来源诊断 |

## 更新文件

- `scripts/validate-release.py`
- `scripts/validate-sprint-archive-readiness.py`
- `scripts/validate-archive-evidence.py`
- `scripts/validate-environment-tiered-evidence.py`
- `scripts/environment_tiered_evidence.py`
- `tests/test_release_validation.py`
- `tests/test_sprint_archive_readiness.py`
- `AGENTS.md`
- `rules/testing.md`
- `rules/agent-context-budget.md`
- `rules/media.md`
- `.agents/skills/opsx-archive/SKILL.md`
- `.agents/skills/sprint-archive/SKILL.md`
- `.agents/skills/release-publish/SKILL.md`
- `.agents/skills/opsx-apply/SKILL.md`
- `.agents/skills/miniapp-confirm/SKILL.md`
- `docs/standards/command-execution-order.md`
- `docs/standards/miniapp-device-evidence-template.md`
- `docs/standards/media-bug-four-point-acceptance-template.md`
- `openspec/changes/deactivate-environment-tiered-evidence-gates/`
- `iterations/change/sprint-029/`

## 关键决策

| 项目 | 结论 |
|---|---|
| 已采纳原因 | 单一项目发布语义已经生效，默认 workflow 继续应用生产目标分层门禁会造成理解冲突。 |
| 未采纳原因 | 不删除诊断脚本；历史记录和专项排查仍需要识别证据来源混淆。 |
| 替代方案 | 将诊断能力作为手动工具保留，只有其他明确门禁主动采纳诊断结果时才转化为阻断项。 |
| 验证责任 | 脚本聚焦测试、OpenSpec 校验、目录结构校验、上下文预算校验和文档卫生校验。 |
| 后续触发条件 | 若未来重新引入多目标发布或上线阶段硬门禁，应通过新的 OpenSpec Change 显式恢复自动应用。 |

## 验证结果

| 命令 | 结果 |
|---|---|
| `uv run pytest tests/test_environment_tiered_evidence_validation.py tests/test_release_validation.py tests/test_sprint_archive_readiness.py tests/test_archive_change_script.py -q` | 67 passed |
| `openspec validate deactivate-environment-tiered-evidence-gates` | 通过 |
| `python scripts/validate-openspec-language.py` | 通过 |
| `python scripts/validate-directory-structure.py` | 通过 |
| `python scripts/validate-agent-context-budget.py` | 通过 |
| `python scripts/validate-sprint-scope.py sprint-029 --item deactivate-environment-tiered-evidence-gates` | 通过 |
| `python scripts/validate-environment-tiered-evidence.py --change deactivate-environment-tiered-evidence-gates` | PASS |
| `python scripts/validate-doc-prose-hygiene.py <focused paths>` | 8 条启发式 warning，无阻断 |

## 后续建议

- 后续可在 `/opsx-archive` 或 `/sprint-archive` 输出中保留“如需排查证据来源可手动运行诊断脚本”的轻提示，但不应恢复默认阻断。
