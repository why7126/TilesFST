---
purpose: 环境分层验收与生产证据后置治理日志
content: 记录开发、体验版、生产发布 evidence 门禁分层规范的落地范围、验证结果和后续建议
source: /spec-opt standardize-environment-tiered-evidence-gates
update_method: 环境证据、发布门禁或 workflow 命令口径变化时更新
created_at: 2026-08-30 12:35:12
updated_at: 2026-08-30 12:39:44
---

# 环境分层验收与生产证据后置治理日志

## 迭代目标

制定环境分层验收与生产证据后置规范，明确开发、体验版、生产发布各阶段 evidence 门禁。生产环境、体验版入口或真机证据在开发阶段不可用时，不阻塞开发归档；相关缺口必须作为 `production_only_pending`、`environment_unavailable`、`follow_up` 或发布阶段待办记录，并在生产发布时重新判定。

## 变更摘要

- 新增环境 evidence 字段口径：`target_environment`、`phase`、`blocking_scope`、`classification` 和 `evidence_ref`。
- 补强测试、媒体、发布规则，明确开发证据、体验版证据和生产证据的证明边界。
- 更新小程序设备 evidence 与媒体 BUG 四联模板，允许开发阶段使用 DevTools / 开发 API / 静态校验证据闭环开发验收，同时禁止声称生产或体验版通过。
- 更新 `opsx-apply`、`opsx-archive`、`miniapp-confirm`、`release-prepare`、`release-publish` 和 `release-status` 命令说明，统一生产专属证据缺口的后置分类。
- 通过 OpenSpec Change `standardize-environment-tiered-evidence-gates` 承载 delta spec，并纳入 `sprint-028`。

## 影响范围

| 层级 | 结论 |
|---|---|
| API | 不影响；无接口契约变化 |
| DB | 不影响；无 schema 或迁移变化 |
| Web | 不影响；无运行时代码变化 |
| 小程序 | 仅影响验收 evidence 记录口径，不修改运行时代码 |
| 管理端 | 不影响 |
| Orval | 不需要 |
| Docker Compose | 不需要 |

## 更新文件

- `AGENTS.md`
- `rules/testing.md`
- `rules/release.md`
- `rules/media.md`
- `docs/standards/miniapp-device-evidence-template.md`
- `docs/standards/media-bug-four-point-acceptance-template.md`
- `.agents/skills/opsx-apply/SKILL.md`
- `.agents/skills/opsx-archive/SKILL.md`
- `.agents/skills/miniapp-confirm/SKILL.md`
- `.agents/skills/release-prepare/SKILL.md`
- `.agents/skills/release-publish/SKILL.md`
- `.agents/skills/release-status/SKILL.md`
- `openspec/changes/standardize-environment-tiered-evidence-gates/`
- `iterations/change/sprint-028/`
- `docs/spec-logs/CHANGELOG.md`

## 关键决策

| 决策 | 结论 |
|---|---|
| 已采纳原因 | 现有发布规则已区分 development / production，但 BUG、Change、小程序与媒体 evidence 模板仍可能把生产专属证据误判为开发归档 blocker。 |
| 未采纳方案 | 不新增生产自动化校验脚本；当前问题是证据语义与流程门禁，不是运行时能力缺口。 |
| 替代方案 | 仅修改 `rules/release.md` 会遗漏 `opsx.archive`、小程序 DevTools、媒体 BUG 四联和测试证据边界，因此采用跨规则和技能同步。 |
| 验证责任 | 开发归档由 `opsx-archive` 和 Sprint scope 校验承接；生产发布由 `release-status`、`release-prepare`、`release-publish` 重新判定。 |
| 后续触发条件 | 新增生产发布自动化、真机云测、体验版自动抓包或环境校验脚本时，应另起 Change 扩展脚本门禁。 |

## 验证结果

| 命令 | 结果 |
|---|---|
| `python scripts/validate-agent-context-budget.py` | 通过 |
| `python scripts/validate-openspec-language.py` | 通过 |
| `python scripts/validate-directory-structure.py` | 通过 |
| `openspec validate standardize-environment-tiered-evidence-gates` | 通过 |
| `python scripts/validate-sprint-scope.py sprint-028 --item standardize-environment-tiered-evidence-gates` | 通过 |
| `python scripts/validate-doc-prose-hygiene.py <focused-paths>` | 通过并返回 8 条既有启发式 warning；未发现敏感信息或本次阻塞项 |
| `python scripts/sync-workflow-status.py --event opsx.apply --change standardize-environment-tiered-evidence-gates --sprint auto` | 通过，Updated 1，Errors 0 |
| `python scripts/extract-ai-usage.py --post-command-hook --workflow-event opsx.apply --change standardize-environment-tiered-evidence-gates --sprint sprint-028 --json` | 通过，`usage_mode=actual`，Sprint snapshot refreshed |

## 后续建议

- 后续媒体或小程序 BUG 验收时，把开发截图和 DevTools Network 标为 `target_environment=development`。
- 发布到生产前，使用 `/release-status <version> --target production` 或等价 validator 重新检查 `production_only_pending`。
