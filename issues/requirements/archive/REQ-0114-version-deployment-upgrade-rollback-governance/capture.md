---
req_id: REQ-0114-version-deployment-upgrade-rollback-governance
status: done
created_at: 2026-08-21 18:29:40
updated_at: 2026-08-22 20:06:55
recorded_by: product
source: 用户反馈
priority_hint: P1
parent_requirement:
---

# 一句话

项目需要建立版本部署升级与回滚治理能力，覆盖首次部署、相邻版本升级与回滚、跨多个版本升级与回滚，并补齐版本事实源、升级路径、环境变量差异、数据库升级验证和回滚证据。

# 原始描述

标题：版本部署升级与回滚治理能力

背景：当前项目已经具备 `release.json`、镜像构建计划、镜像 manifest、环境变量示例、部署 env 校验、MySQL 幂等迁移和 schema drift 检查等发布治理底座。但要支持某个版本的首次部署、相邻版本升级部署与回滚、跨多个版本升级部署与回滚，还缺少完整的升级路径对象、支持级别判定、差异分析、升级验证和回滚证据模型。

本需求暂不包含可视化/平台化能力；先聚焦底层治理、命令、事实源与校验闭环。

影响范围：

- release 规范与 `releases/vX.Y.Z/` 事实源
- 版本一致性：`release.json`、`PRODUCT_VERSION`、image tag、image manifest、Git tag / commit
- 首次部署计划与验收证据
- 相邻版本升级计划、升级校验与回滚计划
- 跨版本升级计划、跨版本影响聚合、人工复核与回滚计划
- 环境变量示例、env diff、生产 env 安全边界
- SQLite / MySQL schema、幂等迁移、schema drift、数据库备份与回滚证据
- Docker Compose、镜像 tarball、sha256、目标部署 env 的 `TILESFST_IMAGE_TAG`
- 对象存储和生产维护任务的 dry-run / apply 证据边界

# 背景与关联

- 探索来源：围绕 v1.1.2 首次部署、v1.1.1 → v1.1.2 相邻升级、v0.0.5 → v1.1.2 跨版本升级的发布治理讨论
- 当前已具备：release 发布对象、image prepare/build、deploy env 示例和校验、后端启动幂等 DB 初始化、MySQL schema drift 检查
- 当前缺口：缺少 `from_version -> to_version` 的升级计划事实源、支持级别判定、env diff、DB 升级路径验证、回滚证据模型和版本一致性门禁
- 范围排除：暂不建设可视化平台，不自动执行生产升级，不自动修改真实生产 `.env`，不自动执行对象存储写入维护任务

# 待澄清

- [ ] 首次部署、相邻升级、跨版本升级是否统一放入 `releases/<to-version>/upgrade-plans/`，还是单独新建 `upgrade-plans/` 顶层目录。
- [ ] 升级支持级别枚举是否采用 `fresh-install-supported`、`adjacent-upgrade-supported`、`cross-version-upgrade-supported`、`cross-version-upgrade-requires-manual-review`、`unsupported`。
- [ ] `release.json` 是否必须记录 Git tag / commit；若 Git tag 缺失，发布门禁应阻断还是 warning。
- [ ] env diff 的事实源是 release 阶段快照，还是通过 Git tag 对比 `.env.example`、`deploy/**/*.env.example` 和 `scripts/build-images.env.example`。
- [ ] 跨版本升级支持是否必须有演练证据才能标记为 supported；缺少演练时是否默认 requires_manual_review。
- [ ] 回滚证据是否必须包含旧镜像 sha256、旧 env 摘要、DB 备份校验、对象存储备份或只读确认、回滚后 smoke。

# 建议验收要点

- [ ] 版本事实源：发布对象能够记录并校验 `release.json.version`、`PRODUCT_VERSION`、image tag、image manifest、Git tag / commit 的一致性；缺失或漂移时给出明确 blocker 或 warning 策略。
- [ ] 首次部署：能够生成目标版本 fresh install 计划，覆盖 env 安全检查、空库初始化、镜像 manifest 校验、Compose 配置校验、健康检查和首次部署 smoke。
- [ ] 相邻升级与回滚：能够生成 `previous_version -> target_version` 升级计划，覆盖目标镜像校验、env diff、DB drift、备份确认、`TILESFST_IMAGE_TAG` 更新、服务重启、升级后 smoke 和回滚步骤。
- [ ] 跨版本升级与回滚：能够聚合多个中间版本的 DB、env、Docker、对象存储、API 和维护任务影响，输出支持级别、人工复核项、阻塞项、升级顺序、回滚策略和演练证据要求。
- [ ] env diff：能够识别新增、删除、默认值变化、生产必须显式配置、示例值禁止进入生产的变量；不得输出真实密钥或真实 `.env` 值。
- [ ] DB 升级验证：能够区分 SQLite / MySQL，记录 schema/migration 输入、目标 MySQL drift 或 smoke 证据、备份/回滚证据；不得只凭本地 SQLite 通过宣称生产 DB 升级安全。
- [ ] 回滚证据：能够结构化记录旧镜像 tag / sha256、旧 env 摘要、DB 备份路径或校验摘要、对象存储备份/只读确认、回滚命令、回滚后 smoke 结果。
- [ ] 命令与工作流：新增或扩展 upgrade 相关命令时，必须接入 Workflow Sync / AI Usage 输出契约，并遵守发布、环境变量、数据库、Docker 和文档治理规则。

# 探索结论

（/req-explore 后人工确认写入）
