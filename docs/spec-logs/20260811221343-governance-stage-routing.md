---
purpose: 治理迭代日志
content: 固化 capture / explore / opsx-modify 对需求相关偏差的阶段分流标准
source: /spec-opt 把这套阶段分流标准正式写入 capture / explore / opsx-modify 规则中
update_method: 本次治理迭代生成；后续如阶段分流规则变化由 /spec-opt 更新
created_at: 2026-08-11 22:13:43
updated_at: 2026-08-11 23:28:30
---

# 阶段分流规则治理日志

## 迭代目标

将需求相关“不如预期”的阶段分流标准正式写入 `/capture`、`/explore` 与 `/opsx-modify`，减少验收返修、归档后缺陷和新增诉求之间的判断漂移。

## 变更摘要

- `/capture`：新增落盘前阶段分流表，明确 active Change 内返修不创建新 Issue，归档后偏差走 BUG，新增能力走 REQ。
- `/explore`：新增只读阶段分流表，输出类型倾向和建议命令，不自动落盘。
- `/opsx-modify`：新增 Stage Routing，明确仅 active Change 内原验收边界允许返修，归档或越界时阻断并转 capture 链路。
- OpenSpec：新增 `refine-capture-explore-modify-stage-routing` 纯治理 Change，并纳入 `sprint-022`。

## 影响范围

- 影响命令规则：`/capture`、`/explore`、`/opsx-modify`。
- 影响 OpenSpec 能力：`agent-workflow-tooling` delta。
- 不修改业务 `src/`。
- 不影响 API、数据库、Web、小程序、管理端、Orval 或 Docker Compose。

## 更新文件

- `.agents/skills/capture/SKILL.md`
- `.agents/skills/explore/SKILL.md`
- `.agents/skills/opsx-modify/SKILL.md`
- `openspec/archive/2026-08-11-refine-capture-explore-modify-stage-routing/proposal.md`
- `openspec/archive/2026-08-11-refine-capture-explore-modify-stage-routing/design.md`
- `openspec/archive/2026-08-11-refine-capture-explore-modify-stage-routing/tasks.md`
- `openspec/archive/2026-08-11-refine-capture-explore-modify-stage-routing/specs/agent-workflow-tooling/spec.md`
- `openspec/specs/agent-workflow-tooling/spec.md`
- `iterations/change/sprint-022/sprint.yaml`
- `docs/spec-logs/CHANGELOG.md`
- `docs/spec-logs/20260811221343-governance-stage-routing.md`

## 验证结果

- 通过：`python scripts/validate-agent-context-budget.py`
- 通过：`python scripts/validate-openspec-language.py`
- 通过：`python scripts/validate-directory-structure.py`
- 通过：`openspec validate refine-capture-explore-modify-stage-routing --strict`
- 通过：`python scripts/validate-sprint-scope.py sprint-022 --item refine-capture-explore-modify-stage-routing`
- 通过：`python scripts/sync-workflow-status.py --event opsx.apply --change refine-capture-explore-modify-stage-routing --sprint auto`
- 通过：`python scripts/extract-ai-usage.py --post-command-hook --workflow-event opsx.apply --change refine-capture-explore-modify-stage-routing --sprint sprint-022 --json`

## API / DB / Web / 小程序 / 管理端 / Orval / Docker 影响

- API：无影响。
- DB：无影响。
- Web：无业务实现影响。
- 小程序：无业务实现影响。
- 管理端：无业务实现影响。
- Orval：不需要。
- Docker Compose：不需要。

## 后续建议

- 后续如将阶段分流做成脚本校验或命令模板生成器，应另起 `/spec-opt update-script`，并补充脚本级测试。
