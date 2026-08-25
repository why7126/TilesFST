---
created_at: 2026-08-22 14:12:50
updated_at: 2026-08-22 14:12:50
---

# Sprint 提议选择与归档冻结治理

## 迭代目标

收紧 `/sprint-propose` 未指定 Sprint 时的默认选择、显式新建 Sprint 的连续编号门禁、容量硬阻断后的拆分引导，以及 Sprint 归档后的研发事实冻结边界。

## 变更摘要

- `/sprint-propose` 未指定 Sprint 时：无 active Sprint 自动创建下一个连续编号；一个 active Sprint 默认使用当前 Sprint；两个及以上 active Sprint 阻断并要求 `--sprint`。
- 显式新建 Sprint 必须为当前最大规范编号加一，不允许跳号；已有两个 active Sprint 时不得创建第三个。
- 保留容量策略：`<=100%` 通过，`100%~120%` 风险通过，`>120%` 硬阻断并引导拆分范围或指定下一个连续 Sprint。
- Sprint 归档后关联 REQ、BUG、Change 和四件套默认冻结；只读探索、复盘、发布、镜像与升级命令仅可消费归档事实。
- 新增 `scripts/validate-sprint-selection.py` 与聚焦测试，承接 active Sprint 数量和连续编号门禁。

## 影响范围

- 规则：Sprint 生命周期与容量门禁。
- 命令：`/sprint-propose`。
- 脚本：Sprint 选择校验。
- OpenSpec：`sprint-planning-governance` delta spec。
- Sprint：`sprint-025` 纳入本治理 Change。

## 更新文件

- `AGENTS.md`
- `rules/iterations-lifecycle.md`
- `.agents/skills/sprint-propose/SKILL.md`
- `scripts/validate-sprint-selection.py`
- `tests/test_sprint_selection_validation.py`
- `openspec/changes/tighten-sprint-propose-active-sprint-governance/`
- `iterations/change/sprint-025/sprint.yaml`
- `iterations/change/sprint-025/sprint.md`
- `docs/spec-logs/CHANGELOG.md`

## 关键决策

- 已采纳：保留 `100%~120%` 容量风险通过区间，避免把可控轻微超载误判为硬失败。
- 已采纳：未指定 Sprint 时默认当前 Sprint，但多个 active Sprint 时必须显式指定，降低误写范围风险。
- 未采纳：超过 `100%` 即硬失败；原因是现有规范已定义 20% 风险缓冲，且用户确认保留该区间。
- 替代方案：若后续团队希望更严格容量治理，可另行将风险通过区间调整为人工确认通过。

## 验证结果

- `python scripts/validate-sprint-selection.py`：通过，当前唯一 active Sprint 为 `sprint-025`，下一个允许编号为 `sprint-026`。
- `uv run pytest tests/test_sprint_selection_validation.py`：通过，7 passed。
- `python scripts/validate-agent-context-budget.py`：通过。
- `python scripts/validate-openspec-language.py`：通过。
- `python scripts/validate-directory-structure.py`：通过。
- `openspec validate tighten-sprint-propose-active-sprint-governance`：通过。
- `python scripts/validate-doc-prose-hygiene.py <focused-paths>`：退出码 0，报告 5 条既有规范句式 warning，未发现本次新增敏感内容。

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

后续若 `/sprint-propose` 实现为可执行脚本或自动化命令，应在真实执行入口强制调用 `scripts/validate-sprint-selection.py`，并将容量硬阻断后的下一个 Sprint 引导接入同一门禁。
