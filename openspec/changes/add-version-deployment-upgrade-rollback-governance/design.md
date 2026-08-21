## 上下文

当前发布治理以 `releases/<version>/release.json`、`image-build-plan.json`、`image-manifest.json`、部署 env 示例、生产 env 校验和数据库迁移脚本为主要事实源。这些材料可以说明目标版本是否具备发布条件，但不能单独证明某个运行版本可以直接升级到目标版本，也不能证明升级失败后可回滚。

REQ-0114 要求把升级路径作为独立治理对象：`fresh -> vX.Y.Z`、`vA.B.C -> vX.Y.Z` 和跨多个版本的升级路径都要有支持级别、影响摘要、步骤、证据和回滚边界。该能力是发布/部署/数据库/对象存储/命令治理的横切增强，不新增业务页面和运行时 API。

## 目标与非目标

目标：

- 定义升级路径对象和 `fresh-install-supported`、`adjacent-upgrade-supported`、`cross-version-upgrade-supported`、`cross-version-upgrade-requires-manual-review`、`unsupported` 支持级别。
- 生成或校验首次部署、相邻升级、跨版本升级与回滚计划。
- 复用既有 release、image、deploy、DB、object storage 和 Workflow Sync 能力，不创建平行发布事实源。
- 为后续 `/upgrade-plan`、`/upgrade-validate` 或等价命令提供规范和任务边界。

非目标：

- 不建设可视化升级平台。
- 不自动执行生产升级、真实 env 修改、数据库写入迁移或对象存储写入维护任务。
- 不为不同部署场景构建不同业务镜像；同一目标版本继续复用同一组 backend / web 镜像。
- 不新增后端 API、数据库表、Web 管理端、小程序或店主 Web 页面。

## 技术决策

### D1：升级路径对象存放在目标 release 目录

`releases/<to-version>/upgrade-plans/` 作为升级路径对象默认位置。这样目标版本仍是发布事实入口，同时每个计划明确 `from_version`，避免把跨版本升级事实拆散到多个历史版本目录。

替代方案是按来源版本建目录，例如 `releases/<from-version>/upgrade-to/<to-version>`。该方式不利于发布负责人在目标版本发布时集中审查所有可支持路径，因此不采用。

### D2：支持级别必须证据驱动

支持级别不从版本号距离直接推导。相邻升级也必须有 release、image、env、DB、备份和 smoke 证据；跨版本只有在中间版本事实源完整且演练证据齐全时才可标记为 `cross-version-upgrade-supported`。证据不足时降级到 manual review 或 unsupported。

### D3：env diff 只读取示例和脱敏摘要

env diff 默认比较 `.env.example`、`src/backend/.env.example`、`src/backend/.env.docker`、`deploy/**/*.env.example` 与 `scripts/build-images.env.example`。命令输出仅包含变量名、分类、说明和建议，不读取或输出真实生产 `.env` 值。

### D4：数据库验证区分 SQLite 与 MySQL

SQLite 初始化和本地测试不能替代生产 MySQL 升级验证。数据库影响非空时，计划必须要求 MySQL drift 或目标 MySQL smoke、备份和回滚证据。反向迁移不可用时，DB 回滚只能基于备份恢复或人工方案。

### D5：命令只做计划和校验

upgrade 命令族只读取事实源、生成计划、验证证据和输出阻断项。生产升级、DB 恢复、对象存储写入维护任务必须由人工显式执行或授权，并在计划中记录 dry-run、备份和责任边界。

## 风险与缓解

- 历史版本 release 事实源不完整 → 使用 `source_confidence: reconstructed|partial`，并将跨版本支持级别降级到 manual review 或 unsupported。
- 中间版本影响被遗漏 → 跨版本计划必须聚合 release、env、DB、Docker、API、对象存储和维护任务摘要；缺失事实源即 blocker 或 warning。
- 输出泄露敏感信息 → 计划和校验结果只记录变量名、hash、摘要、路径和命令，不写真实 env、密钥、连接串或客户数据。
- 回滚能力被过度承诺 → 回滚计划必须显式记录旧镜像、旧 env 摘要、DB 备份、对象存储影响和回滚后 smoke；缺证据不得标记 supported。

## 迁移计划

1. 补充 OpenSpec specs，定义升级路径、发布、部署、镜像、数据库、对象存储和工作流命令边界。
2. 更新 `rules/`、`docs/`、`.agents/skills/` 与命令速查。
3. 新增或扩展脚本，支持 release fact 一致性、env diff、upgrade plan 生成和验证。
4. 为 `v1.1.2` 或后续版本生成样例升级路径计划，覆盖 fresh、相邻和跨版本 manual review 场景。
5. 运行 OpenSpec、语言、目录、Workflow Sync 和脚本测试。

## 原型与冲突处理

本 Change 不涉及 UI、prototype、Web 管理端、小程序或店主端页面；UI Contract、CSS Port、视觉 token 和截图验收门禁均为 N/A。
