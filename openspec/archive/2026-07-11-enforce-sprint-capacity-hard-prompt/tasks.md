## 1. Sprint Propose 门禁实现

- [x] 1.1 更新 `.agents/skills/source-command-sprint-propose/SKILL.md` 的 Capacity Gate，明确 `estimated_person_days > capacity_person_days * 1.2` 时必须阻断正式规划。
- [x] 1.2 在超限处理说明中要求输出拆分 Sprint、移出低优先级项或替换范围的硬提示，并要求调整后重新运行 `/sprint-propose`。
- [x] 1.3 明确阻断发生在生成 `iterations/change/<sprint>/` 四件套和更新 REQ/BUG/Change trace 之前。
- [x] 1.4 保留 100% 到 120% 的弹性区间，并要求写入容量风险、fix 缓冲影响和延后项建议。

## 2. 规则与校验同步

- [x] 2.1 按需更新 Sprint 生命周期、文档治理或相关命令规则，确保 120% 硬门槛成为长期治理要求。
- [x] 2.2 补充或更新针对 sprint-propose 技能/规则的校验测试，覆盖超过 120% 阻断、100% 到 120% 风险继续、不超过容量正常通过。
- [x] 2.3 运行 OpenSpec 校验，确认 `sprint-planning-governance` delta spec 格式正确。
- [x] 2.4 运行受影响的 agent/规则校验脚本，确认技能仍遵守上下文预算与目录边界要求。

## 3. 验收与同步

- [x] 3.1 复核变更不影响 API、数据库、Web、小程序、Orval、Docker Compose。
- [x] 3.2 记录验证命令与结果，更新 tasks 勾选状态。
- [x] 3.3 完成后运行 workflow sync 对应事件，确保 OpenSpec/Sprint 状态同步。

## Verification

- `openspec validate enforce-sprint-capacity-hard-prompt --strict`：通过。
- `python scripts/validate-agent-context-budget.py`：通过，26 个 source-command 技能均已接入预算规则。
- `python -m pytest tests/test_sprint_propose_capacity_gate.py`：通过，3 passed。
- `git diff --name-only -- .agents/skills/source-command-sprint-propose/SKILL.md rules/iterations-lifecycle.md tests/test_sprint_propose_capacity_gate.py openspec/changes/enforce-sprint-capacity-hard-prompt`：确认本变更不涉及 API、数据库、Web、小程序、Orval、Docker Compose。
