---
requirement_id: REQ-0114-version-deployment-upgrade-rollback-governance
title: 版本部署升级与回滚治理能力 - 用户故事
created_at: 2026-08-21 18:34:27
updated_at: 2026-08-21 22:09:09
owner: product
---

# 用户故事

## US-001 发布负责人判断目标版本部署支持级别

作为发布负责人，我希望系统能根据目标版本 release 事实源、镜像 manifest、Git ref、env 和 DB 证据判断该版本支持首次部署、相邻升级还是跨版本升级，以便对客户和实施团队给出可靠承诺。

验收要点：

- 能输出 `fresh-install-supported`、`adjacent-upgrade-supported`、`cross-version-upgrade-supported`、`cross-version-upgrade-requires-manual-review` 或 `unsupported`。
- 缺少跨版本演练、历史 release 事实源或关键证据时，不得将跨版本升级标记为 supported。
- 输出必须说明支持级别的证据、阻塞项和人工复核项。

## US-002 运维生成首次部署计划

作为实施或运维人员，我希望为目标版本生成首次部署计划，以便在空环境中按步骤配置 env、加载镜像、初始化数据库、配置对象存储并完成 smoke。

验收要点：

- 首次部署计划包含目标版本、镜像 manifest、生产 env 检查、MySQL 初始化、对象存储配置、Compose 校验和 smoke 清单。
- 计划不得输出真实 `.env`、数据库连接串、对象存储密钥或生产私有信息。
- 首次部署通过后能沉淀部署证据和结果摘要。

## US-003 运维执行相邻版本升级与回滚

作为实施或运维人员，我希望系统能生成上一版本到目标版本的升级计划和回滚计划，以便升级时知道需要改哪些 env、如何切换镜像、如何验证 DB 和如何回退。

验收要点：

- 相邻升级计划识别 `previous_version -> target_version` 的 env diff、DB 影响、镜像 manifest、Compose 输入和备份要求。
- 计划明确 `TILESFST_IMAGE_TAG` 更新、服务重启或滚动策略、升级后健康检查和核心 smoke。
- 回滚计划包含旧镜像、旧 env 摘要、DB 备份恢复条件、对象存储影响和回滚后 smoke。

## US-004 发布负责人评估跨版本升级风险

作为发布负责人，我希望系统能聚合多个中间版本的发布影响，以便判断从较旧版本跨到目标版本是否需要人工复核、演练或先升到中间版本。

验收要点：

- 跨版本计划聚合中间版本的 DB、env、Docker、API、对象存储和维护任务影响。
- 若历史版本事实源缺失或证据不完整，计划标记为 `cross-version-upgrade-requires-manual-review`。
- 计划明确必须 dry-run 的维护任务、必须人工确认的步骤和升级演练证据要求。

## US-005 测试验证数据库升级路径

作为测试人员，我希望升级计划区分“存在幂等迁移代码”和“升级路径已验证”，以便生产 MySQL 升级不会只依赖本地 SQLite 测试通过。

验收要点：

- 数据库影响非空时，计划要求 MySQL schema drift 或目标 MySQL smoke、备份和回滚证据。
- 计划记录 SQLite schema、MySQL schema、migration 和 `schema_migrations` 等输入。
- 缺少 DB 备份、drift/smoke 或回滚证据时，升级计划必须 blocked 或 requires manual review。

## US-006 AI Agent 按发布治理边界生成升级计划

作为 AI Agent，我希望 upgrade 命令明确只生成和校验升级计划，不自动执行生产升级或修改真实 env，以便遵守安全和 OpenSpec 治理边界。

验收要点：

- 命令复用 release、image、deploy、DB 和 maintenance 脚本，不创建平行事实源。
- 命令输出遵守 Workflow Sync / AI Usage 契约。
- 需要用户确认时，命令输出结构化选项、推荐项、阻塞项和下一步。
