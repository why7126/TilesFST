---
title: upgrade 部署升级与回滚治理
purpose: 记录 REQ-0114 / add-version-deployment-upgrade-rollback-governance 对发布升级治理、脚本、技能和文档的更新
source: /opsx-apply REQ-0114-version-deployment-upgrade-rollback-governance
change_id: add-version-deployment-upgrade-rollback-governance
created_at: 2026-08-21 18:58:37
updated_at: 2026-08-22 09:14:33
---

# upgrade 部署升级与回滚治理

## 更新摘要

本次变更为项目新增版本部署升级与回滚治理能力，覆盖首次部署、相邻版本升级、跨版本升级和回滚计划。能力以 release 事实源和升级路径对象为核心，不建设可视化平台，不自动执行生产升级，不自动修改真实 env，不自动执行写入型 DB 或对象存储维护任务。

## 已采纳

- 新增 `scripts/validate-release-upgrade.py`，提供 `plan`、`validate-plan` 和 `env-diff` 子命令。
- 新增 `releases/v1.1.2/upgrade-plans/` 正式计划，覆盖已确认真实路径 `fresh -> v1.1.2` 与 `v1.1.1 -> v1.1.2`；跨版本支持级别由单测临时构造版本覆盖，不将解释用版本写入正式 release 事实源。
- 新增 `.agents/skills/upgrade-plan` 与 `.agents/skills/upgrade-validate`。
- 固化发布默认计划策略：每次正常发布默认覆盖 `fresh` 与上一正式版本；跨版本升级计划由用户按需通过 `/upgrade-plan --from <old-version> --to <target-version>` 手工生成。
- 同步 `rules/release.md`、`rules/environment.md`、`rules/database.md`、`rules/directory-structure.md`、`docs/02-deployment.md`、`docs/08-production-image-release.md` 和 `AGENTS.md`。
- 新增 `tests/test_release_upgrade_validation.py` 覆盖支持级别、env diff 和敏感信息扫描。

## 未采纳

- 未建设可视化升级平台；REQ-0114 明确本期排除。
- 未自动执行生产升级、DB restore、真实 env 写入或对象存储写入维护任务；这些仍由人工授权和实际运维流程承载。
- 未把升级路径做成不同业务镜像；同一目标版本仍引用同一份 image manifest。

## 验证责任

- 脚本单测：`uv run pytest tests/test_release_upgrade_validation.py`。
- 正式计划校验：`python scripts/validate-release-upgrade.py validate-plan --plan releases/v1.1.2/upgrade-plans/<plan>.json`。
- OpenSpec 与语言：`python scripts/validate-openspec-language.py`、`openspec validate add-version-deployment-upgrade-rollback-governance --strict`。
- Workflow Sync：`python scripts/sync-workflow-status.py --event opsx.apply --change add-version-deployment-upgrade-rollback-governance --sprint auto`。

## 后续触发条件

当发布流程需要承诺某个版本支持首次部署或相邻升级时，必须先生成并校验对应升级计划。跨版本升级不属于每次发布默认生成范围；只有用户明确指定来源旧版本时才生成。跨版本升级若缺少演练、DB/env/object storage 或回滚证据，应保留 `cross-version-upgrade-requires-manual-review` 或 `unsupported`，不得直接宣称 supported。
