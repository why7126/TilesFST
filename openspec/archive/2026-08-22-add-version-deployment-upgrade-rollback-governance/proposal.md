## 背景

项目当前已经具备产品发布对象、镜像构建计划、镜像 manifest、部署环境矩阵、生产 env 校验、MySQL 幂等迁移和 schema drift 检查等发布治理基础，但这些事实源主要围绕“目标版本”组织，尚未把“从哪个运行版本升级到哪个目标版本”作为一等对象管理。

首次部署、相邻版本升级、跨多个版本升级与回滚需要不同证据：首次部署关注空环境初始化，相邻升级关注上一版本到目标版本的 env、DB、镜像和 smoke 闭环，跨版本升级还需要聚合中间版本影响并明确人工复核边界。若没有升级路径对象和回滚证据模型，容易把“存在幂等迁移代码”误判为“任意版本升级已验证”。

## 变更内容

- 新增版本部署升级与回滚治理能力，定义 `from_version -> to_version` 升级路径对象、支持级别、执行步骤、验证证据和回滚证据。
- 新增首次部署计划要求，覆盖目标 release、目标镜像、生产 env、MySQL 空库初始化、对象存储配置、Compose 校验和部署后 smoke。
- 新增相邻版本升级与回滚计划要求，覆盖 release 事实源、image manifest、env diff、DB drift/smoke、备份、镜像切换、服务重启和回滚后 smoke。
- 新增跨版本升级与回滚计划要求，聚合中间版本的 DB、env、Docker、API、对象存储和维护任务影响，并以证据驱动方式输出 `supported`、`requires_manual_review` 或 `unsupported`。
- 新增 env diff 能力，比较各类 env 示例文件中的变量增删、默认值变化、生产必填项和不安全示例值。
- 补强发布、部署、镜像、数据库、对象存储与 Agent workflow tooling 规范，使 upgrade 命令只生成计划和校验证据，不自动执行生产升级、真实 env 修改或写入型维护任务。
- 不新增 Web 管理端、店主 Web、微信小程序 UI 或可视化升级平台。

## 能力范围

### 新增能力

- `version-deployment-upgrade-rollback-governance`：版本部署升级与回滚治理，覆盖升级路径对象、支持级别、首次部署、相邻升级、跨版本升级、env diff、DB 升级验证、回滚证据和 upgrade 命令边界。

### 修改能力

- `product-release-management`：产品发布对象和发布门禁需要引用升级路径、支持级别和回滚证据。
- `deployment`：部署能力需要补齐首次部署、相邻升级、跨版本升级、回滚计划和真实 env 安全边界。
- `deployment-image-build`：镜像构建计划和 manifest 需要作为升级计划的目标版本镜像证据，且同一目标版本复用同一组业务镜像。
- `database`：数据库发布与迁移验证需要区分幂等迁移存在和目标升级路径已验证，并要求 MySQL drift/smoke、备份和回滚证据。
- `object-storage`：对象存储影响需要纳入跨版本升级和回滚计划，写入型维护任务必须 dry-run、备份确认和人工授权。
- `agent-workflow-tooling`：新增或扩展 upgrade 命令族时必须接入 Workflow Sync、AI Usage、上下文预算和安全输出契约。

## 影响

- 影响治理文档：`rules/release.md`、`rules/environment.md`、`rules/database.md`、`rules/directory-structure.md`、`docs/02-deployment.md`、`docs/08-production-image-release.md`。
- 影响发布与部署脚本：可能新增或扩展 `scripts/validate-release.py`、`scripts/validate-image-build.py`、`deploy/scripts/validate-env.py` 及 upgrade 相关脚本。
- 影响 Codex skills：可能新增或扩展 upgrade 相关技能，并同步 AGENTS 命令速查与 Workflow Sync 输出契约。
- 影响 release 事实源：目标版本目录可新增 `upgrade-plans/`，但不得存放真实 env、密钥、连接串、本机绝对路径或真实客户数据。
- 不影响业务运行时功能，不新增后端 API、数据库表、Web 页面、小程序页面或管理端菜单。
