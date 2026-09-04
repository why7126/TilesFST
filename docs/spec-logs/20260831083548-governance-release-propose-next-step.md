---
purpose: 规范工程迭代日志
content: release-propose 默认下一步调整
source: /spec-opt make-release-propose-next-step-prepare
update_method: 本日志记录单次治理变更事实；后续变更另开日志或更新 CHANGELOG 摘要
created_at: 2026-08-31 08:35:48
updated_at: 2026-08-31 08:41:22
---

# release-propose 默认下一步调整治理日志

## 迭代目标

将 `/release-propose <version>` 的默认下一步从 `/release-status <version>` 调整为 `/release-prepare <version>`，并明确 `/release-status` 只是只读状态面板和阻塞排查入口。

## 变更摘要

- `/release-propose` 技能成功路径下一步改为 `/release-prepare <version>`。
- `/release-status` 技能说明补充其非主线必经步骤的定位。
- `rules/release.md` 发布流程图改为 propose → prepare → status 按需检查 → image / upgrade / publish。
- `rules/agent-context-budget.md` 和 `AGENTS.md` 同步发布命令族摘要。
- OpenSpec Change `make-release-propose-next-step-prepare` 已补充 proposal、design、tasks、trace、test-plan、acceptance 和 delta spec。

## 影响范围

| 层级 | 影响 |
|---|---|
| API | 不适用，未修改接口。 |
| DB | 不适用，未修改 schema、migration 或数据模型。 |
| Web | 不适用，未修改业务实现。 |
| 小程序 | 不适用，未修改业务实现。 |
| 管理端 | 不适用。 |
| Orval | 不适用。 |
| Docker Compose | 不适用。 |

## 更新文件

- `.agents/skills/release-propose/SKILL.md`
- `.agents/skills/release-status/SKILL.md`
- `rules/release.md`
- `rules/agent-context-budget.md`
- `AGENTS.md`
- `openspec/changes/make-release-propose-next-step-prepare/`
- `iterations/change/sprint-029/`
- `docs/spec-logs/CHANGELOG.md`

## 关键决策

- 已采纳：propose 后默认进入 prepare，因为 prepare 是第一个补齐版本源、公告和发布前门禁证据的变更型命令。
- 已采纳：status 保持只读，作为操作者主动排查当前阶段、默认 upgrade 路径和 blocker 的入口。
- 未采纳：继续把 status 放在 propose 与 prepare 之间作为主线步骤；该方式会增加一次不必要的只读跳转。

## 验证结果

- OpenSpec validate、目录结构、上下文预算和 Sprint scope 校验通过。
- 文档卫生校验仅返回既有启发式 warning，无阻断。
- Workflow Sync 与 AI Usage hook 通过；AI Usage `usage_mode=actual`，warning 0。

## 后续建议

- 后续调整发布命令顺序时，应同步更新技能输出契约、`rules/release.md` 流程图和上下文预算规则。
