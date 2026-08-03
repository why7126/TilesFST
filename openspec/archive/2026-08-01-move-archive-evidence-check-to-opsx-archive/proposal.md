## Why

当前 archived Change 缺失 `trace.md` 时的 `归档验证摘要` 完整性门禁主要在 Sprint close/readiness 阶段发现，反馈过晚，容易让单个 `/opsx-archive` 看似成功但在后续 `/sprint-archive` 才暴露证据缺口。需要将检查前移到单个 Change 归档命令，让归档动作本身产出可闭环证据。

## What Changes

- `/opsx-archive <change-id>` 在移动或完成归档后必须确认 archived Change 目录包含 `trace.md`，或在 `proposal.md`、`design.md`、`tasks.md` 中包含完整 `## 归档验证摘要` 兜底章节。
- 归档证据检查的缺失项必须在 `/opsx-archive` 输出中作为 blocker 或 warning 明确报告，包含 Change id、归档路径、候选文件和缺失摘要项。
- Sprint close/readiness 继续保留相同证据门禁，但它应作为二次防线，不再是首次发现单个 Change 归档证据缺口的位置。
- 更新 `/opsx-archive` 技能说明、归档脚本或校验脚本与测试，使前移门禁可自动验证。

## Capabilities

### New Capabilities

- 无。

### Modified Capabilities

- `agent-workflow-tooling`: 将 archived Change trace/fallback 完整性检查从 Sprint readiness 首次发现前移到 `/opsx-archive`，并保留 Sprint readiness 复核。

## Impact

- 影响 `.agents/skills/opsx-archive/SKILL.md`、`.agents/skills/sprint-archive/SKILL.md` 的职责表述与输出要求。
- 可能影响 `scripts/archive-change.sh`、`scripts/validate-sprint-archive-readiness.py` 或新增/复用归档证据校验 helper。
- 需要补充或更新 `tests/test_sprint_archive_readiness.py` 及对应 `/opsx-archive` 归档证据门禁测试。
- 不影响业务 API、数据库、Web、小程序、管理端、Orval 或 Docker Compose。
