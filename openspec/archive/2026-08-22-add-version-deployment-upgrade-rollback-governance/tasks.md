## 1. 规范与文档

- [x] 1.1 更新 `rules/release.md`，定义升级路径对象、支持级别、首次部署、相邻升级、跨版本升级和回滚证据门禁。
- [x] 1.2 更新 `rules/environment.md`，定义 env diff 输入范围、分类、生产必填项和真实 env 脱敏边界。
- [x] 1.3 更新 `rules/database.md`，区分幂等 migration 存在与升级路径已验证，并补充 MySQL drift/smoke、备份和回滚证据要求。
- [x] 1.4 更新 `rules/directory-structure.md`、`docs/02-deployment.md` 和 `docs/08-production-image-release.md`，说明 `releases/<version>/upgrade-plans/`、同一目标版本复用同一组镜像、三类部署路径和回滚边界。
- [x] 1.5 更新 `AGENTS.md` 命令速查和 Docker / 发布部署读取路由，加入 upgrade 计划与校验能力。

## 2. 升级计划与校验脚本

- [x] 2.1 新增或扩展脚本以读取 release、image manifest、Git ref、PRODUCT_VERSION、部署 env 版本摘要并输出版本事实源一致性结果。
- [x] 2.2 新增 env diff 能力，比较 `.env.example`、`src/backend/.env.example`、`src/backend/.env.docker`、`deploy/**/*.env.example` 和 `scripts/build-images.env.example`，输出分类且不读取真实 env。
- [x] 2.3 新增升级路径计划生成能力，支持 `fresh -> <version>`、`<previous> -> <version>` 和 `<old> -> <version>`，写入 `releases/<version>/upgrade-plans/`。
- [x] 2.4 新增升级计划校验能力，检查 support level、blockers、warnings、DB 证据、对象存储证据、回滚证据和敏感信息。
- [x] 2.5 为历史 release 事实源缺失场景提供 `verified`、`reconstructed`、`partial` 或等价来源可信度标记，不伪造 verified release。

## 3. 命令技能与工作流

- [x] 3.1 新增或扩展 `.agents/skills/upgrade-*` 命令技能，覆盖 plan、validate 或等价入口。
- [x] 3.2 命令技能必须接入 Workflow Sync、AI Usage post-command hook、下一步输出契约和待用户决策/处理输出契约。
- [x] 3.3 命令技能必须声明上下文预算，跨版本分析先定位版本范围和影响摘要，不默认全量展开历史归档、生成物、大日志或 manifest 全文。
- [x] 3.4 命令输出必须明确不自动执行生产升级、真实 env 修改、数据库写入迁移或对象存储写入维护任务。

## 4. 样例计划与验收证据

- [x] 4.1 为当前目标版本或可用样例版本生成 fresh install 升级路径计划，并记录 `fresh-install-supported` 或 blocker。
- [x] 4.2 为相邻版本升级生成计划和回滚计划，并记录 image、env、DB、Compose、backup 和 smoke 证据缺口。
- [x] 4.3 为跨版本升级生成计划，并在缺少完整演练或历史事实源时标记 `cross-version-upgrade-requires-manual-review` 或 `unsupported`。
- [x] 4.4 验证升级路径对象、回滚证据和命令输出不包含真实 `.env`、密钥、连接串、本机绝对路径或真实客户数据。

## 5. 测试与校验

- [x] 5.1 为版本事实源一致性、env diff、支持级别判定和升级计划 schema 增加聚焦单测或脚本测试。
- [x] 5.2 为数据库影响门禁、对象存储维护任务 dry-run 边界和回滚证据缺失降级增加测试。
- [x] 5.3 运行 `python scripts/validate-openspec-language.py`。
- [x] 5.4 运行 `openspec validate add-version-deployment-upgrade-rollback-governance --strict`。
- [x] 5.5 运行 Workflow Sync，确认 REQ-0114、Change 和 sprint-025 scope 已同步。

## 验收返修记录

- [x] 2026-08-21 22:09:09：按验收反馈将用户命令与 Skill 名称从 `release-upgrade-plan` / `release-upgrade-validate` 简化为 `upgrade-plan` / `upgrade-validate`，同步 AGENTS、rules、docs、REQ、OpenSpec delta、Sprint 验收文案和 Skill 目录；底层脚本 `scripts/validate-release-upgrade.py` 保持不改名。
- [x] 2026-08-22 08:13:49：按验收反馈移除正式 release 事实源中的解释用跨版本路径 `v0.0.5-to-v1.1.2.json`；`releases/v1.1.2/upgrade-plans/` 仅保留已确认真实路径 `fresh` 与 `v1.1.1`，跨版本降级逻辑由单测临时构造版本覆盖。
- [x] 2026-08-22 09:14:33：按验收反馈明确每次正常发布默认生成 `fresh` 和上一正式版本两类升级计划；跨版本计划不默认生成，改为用户按需通过 `/upgrade-plan --from <old-version> --to <target-version>` 手工触发，并同步规则、部署文档、OpenSpec delta、Skill 说明和测试。
