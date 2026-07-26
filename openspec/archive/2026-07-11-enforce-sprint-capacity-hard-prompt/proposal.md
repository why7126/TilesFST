## Why

当前 `/sprint-propose` 仅要求将容量超限写入风险或延后项，容易让明显超载的 Sprint 仍进入正式规划，后续再用验收或归档阶段补救。需要把超过容量 120% 的范围在提议阶段硬拦截，迫使团队当场拆分或替换范围。

## What Changes

- `/sprint-propose` 的 Capacity Gate 增加硬提示：估算工作量超过 Sprint 容量 120% 时，不得生成正式 Sprint 四件套或更新关联 trace。
- 超过 120% 时必须提示用户拆分 Sprint、移出低优先级项，或替换范围后重新评估。
- 容量在 100% 到 120% 之间时仍可继续，但必须写入风险、缓冲说明和延后项。
- 同步更新 sprint-propose 技能、相关规则/测试，确保治理命令行为可校验。

## Capabilities

### New Capabilities
- `sprint-planning-governance`: 约束 Sprint 提议阶段的范围准入、容量门禁和超限处理行为。

### Modified Capabilities

## Impact

- 影响 `.agents/skills/source-command-sprint-propose/SKILL.md` 的 Capacity Gate 文案与执行步骤。
- 可能影响 Sprint 提议相关规则文档或校验脚本。
- 不影响后端 API、数据库、Web、小程序、Orval 或 Docker Compose。
