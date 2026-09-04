---
created_at: 2026-08-31 09:10:00
updated_at: 2026-08-31 09:10:00
---

# 设计说明

## 决策归属

发布产物决策统一写入 `releases/<version>/release.json`：

- `announcement_decision`：默认 `required=true`，由 `/release-prepare` 生成或更新 `announcement.mdx`。
- `usage_docs.generation_decision`：默认 `required=false`，状态为 `skipped`，并记录自动默认跳过原因；用户显式 `--usage-docs` 时置为 `required=true`，prepare 阶段生成并校验。
- `upgrade_plans`：默认来源为 `fresh` 和上一正式版本；`--upgrade-from` 追加显式来源，去重后由 prepare 阶段生成与校验。

## 命令边界

`/release-propose` 是计划创建命令，只负责生成可读、可校验的计划决策，不生成大产物。`/release-prepare` 是产物生成与 prepare 证据收敛命令，负责把 release 决策实际落到公告、usage docs、Mintlify 投影和升级计划。`/release-status` 不写文件，只读汇总当前状态。`/release-publish` 只写发布确认字段，不反向生成主产物。

## 脚本门禁

`scripts/validate-release.py --status` 继续提供状态面板，但默认升级路径缺失或声明升级路径缺失时，安全修复路径改为 `/release-prepare <version>`。这样 status 面板可以解释阻塞原因，却不会把主线默认产物拆散到多个人工命令。

`scripts/validate-release.py --stage publish` 仍要求必需升级计划存在并通过 `validate-release-upgrade.py validate-plan` 校验；这保证 publish 不生成产物也能阻断缺证据发布。

## 兼容

历史 `pending_confirmation`、旧 `release_target` 和旧 `--target` 入参继续兼容读取，但新模板和新命令默认不再产生这些状态。历史 release 如仍处于 pending，可由 `/release-propose --no-usage-docs` 或 `/release-prepare` 依据 release.json 决策收敛。
