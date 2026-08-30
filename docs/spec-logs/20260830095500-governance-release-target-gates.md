---
created_at: 2026-08-30 09:55:00
updated_at: 2026-08-30 09:55:00
---

# Governance Log: Release Target Gates

## 迭代目标

固化开发环境发布与生产发布分离，避免开发环境发布被生产 env、生产备份、生产公开 API、生产 no-fallback 媒体证据或生产 smoke 阻断，同时保留生产发布的强门禁。

## 变更摘要

- 新增 `release_target` 元数据模型，用于声明 `development` 或 `production` 发布目标。
- 新增 `production_deployment` 生产专属证据模型，生产发布确认时由 validator 强制校验。
- `validate-release.py` 在 publish 阶段按 release target 校验默认升级计划和生产证据。
- `validate-release-upgrade.py` 支持 `--target development|production`，并在计划中写入 `deployment_target`。
- v1.2.1 当前发布对象标记为 development release，并重建两条带 `.development.json` 后缀的默认升级计划。

## 影响范围

- 规则：发布治理、上下文预算发布摘要。
- 技能：release propose / prepare / publish、upgrade plan / validate。
- 脚本：release validator、upgrade plan generator / validator。
- Release 模板与 v1.2.1 发布对象。

## 更新文件

- `AGENTS.md`
- `rules/release.md`
- `rules/agent-context-budget.md`
- `docs/02-deployment.md`
- `.agents/skills/release-propose/SKILL.md`
- `.agents/skills/release-prepare/SKILL.md`
- `.agents/skills/release-publish/SKILL.md`
- `.agents/skills/upgrade-plan/SKILL.md`
- `.agents/skills/upgrade-validate/SKILL.md`
- `scripts/validate-release.py`
- `scripts/validate-release-upgrade.py`
- `releases/templates/release.json`
- `releases/v1.2.1/release.json`
- `releases/v1.2.1/upgrade-plans/fresh-to-v1.2.1.development.json`
- `releases/v1.2.1/upgrade-plans/v1.2.0-to-v1.2.1.development.json`
- `openspec/changes/separate-dev-prod-release-gates/**`

## 关键决策

已采纳：

- 开发发布和生产发布使用同一 release 事实源，但通过 `release_target` 明确环境边界。
- 开发目标升级计划不作为生产升级验证证据。
- 生产发布使用独立 `production_deployment` 对象承载生产 env、备份、API、媒体、smoke 和回滚证据。

未采纳：

- 未把生产证据继续作为所有 publish 的通用 blocker，因为这会阻断开发环境发布。
- 未修改 `docs/08-production-image-release.md`，因为它属于当前 v1.2.1 image manifest 的稳定输入，治理文档改动会使已构建镜像证据漂移。

## 验证结果

- `python -m py_compile scripts/validate-release.py scripts/validate-release-upgrade.py`：通过。
- `python scripts/validate-release.py --release-dir releases/v1.2.1 --stage publish`：通过。
- `python scripts/validate-release.py --release-dir releases/v1.2.1 --stage publish --target production`：按预期失败，提示 development 计划不匹配 production target 且缺 `production_deployment`。
- `python scripts/validate-release-upgrade.py validate-plan --plan releases/v1.2.1/upgrade-plans/fresh-to-v1.2.1.development.json`：通过。
- `python scripts/validate-release-upgrade.py validate-plan --plan releases/v1.2.1/upgrade-plans/v1.2.0-to-v1.2.1.development.json`：通过。

## 业务影响

- API：不涉及。
- DB：不涉及 schema 或 migration。
- Web / 小程序 / 管理端：不涉及业务运行时代码。
- Orval：不需要。
- Docker：不改 Compose 或 Dockerfile；仅发布治理和升级计划语义变化。

## 后续建议

生产环境发布 v1.2.1 时，显式执行 production target 发布确认，补齐 production 目标升级计划和 `production_deployment` 证据。
