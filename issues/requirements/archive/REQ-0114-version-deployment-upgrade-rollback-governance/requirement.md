---
requirement_id: REQ-0114-version-deployment-upgrade-rollback-governance
title: 版本部署升级与回滚治理能力
terminal: multi
version: v1
status: done
owner: product
source: capture.md
priority: P1
parent_requirement:
created_at: 2026-08-21 18:31:45
updated_at: 2026-08-25 14:53:29
related_change: add-version-deployment-upgrade-rollback-governance
---

# REQ-0114 版本部署升级与回滚治理能力

## 1. 需求背景

项目当前已经具备产品发布对象、镜像构建计划、镜像 manifest、部署环境矩阵、环境变量示例、生产 env 校验、MySQL 幂等兼容迁移和 schema drift 检查等发布治理基础。`releases/vX.Y.Z/release.json` 可以表达单个产品版本是否完成发布准备和发布确认，`image-build-plan.json` 与 `image-manifest.json` 可以表达目标版本镜像构建输入和离线包产物。

但部署升级关注的是“从哪个运行状态升级到哪个目标版本”。首次部署、相邻版本升级和跨多个版本升级所需证据并不相同：首次部署需要证明目标版本可在空环境初始化；相邻升级需要证明从上一版本切换到目标版本时 env、DB、镜像和 smoke 可闭环；跨版本升级还需要聚合中间版本的环境变量、数据库、Docker、API、对象存储和维护任务影响，并明确是否需要人工复核。

当前缺口是：发布事实源按目标版本组织，尚未把 `from_version -> to_version` 升级路径作为一等对象；回滚说明多为文本描述，尚未结构化记录旧镜像、旧 env、数据库备份、对象存储备份或回滚后 smoke 证据。若直接宣称跨版本升级支持，容易把“存在幂等迁移”和“升级路径已验证”混为一谈。

本需求用于建立版本部署升级与回滚治理能力，覆盖首次部署、相邻版本升级与回滚、跨多个版本升级与回滚，并补齐版本事实源一致性、升级路径对象、环境变量差异、数据库升级验证和回滚证据模型。可视化/平台化能力不在本期范围内。

## 2. 目标用户

| 角色 | 诉求 |
|---|---|
| 发布负责人 | 能判断某个目标版本支持哪些部署路径，哪些路径需要人工复核或阻断。 |
| 实施 / 运维 | 能按升级计划执行首次部署、相邻升级、跨版本升级和回滚，不依赖口头记忆。 |
| 开发 / 测试 | 能明确 env、DB、Docker、对象存储、API 和 smoke 证据在升级路径中的要求。 |
| 产品负责人 | 能确认一个版本是否可对客户承诺首次部署、相邻升级或跨版本升级支持。 |
| AI Agent | 能基于 release 事实源生成升级计划、校验升级证据，并避免自动修改生产敏感配置。 |
| 评审者 | 能通过结构化计划和证据审查升级路径是否真实可执行、可回滚、可追溯。 |

## 3. 范围

### 3.1 本期包含

- 定义版本事实源一致性要求，覆盖 `release.json.version`、`PRODUCT_VERSION`、image tag、image manifest、Git tag / commit 和部署 env 版本。
- 定义首次部署、相邻版本升级、跨多个版本升级的支持级别和判定规则。
- 定义 `from_version -> to_version` 升级路径对象，承载升级计划、风险、阻塞项、执行步骤、验证证据和回滚证据。
- 定义首次部署计划，覆盖目标版本镜像、生产 env、空库初始化、对象存储配置、Compose 校验和部署后 smoke。
- 定义相邻版本升级计划与回滚计划，覆盖上一版本到目标版本的 env diff、镜像切换、DB drift、备份确认、重启、smoke 和回滚。
- 定义跨版本升级计划与回滚计划，覆盖多个中间版本影响聚合、人工复核、维护任务 dry-run、演练证据和回滚边界。
- 定义 env diff 能力，识别新增、删除、默认值变化、生产必须显式配置和示例值禁止进入生产的变量。
- 定义数据库升级验证证据，区分 SQLite / MySQL，覆盖 schema/migration 输入、目标 MySQL drift 或 smoke、备份和回滚证据。
- 定义回滚证据模型，结构化记录旧镜像、旧 env 摘要、DB 备份、对象存储备份或只读确认、回滚命令和回滚后 smoke。
- 定义 upgrade 相关命令、脚本或校验入口的职责边界，并接入既有发布治理、Workflow Sync 和 AI Usage 输出契约。

### 3.2 本期不包含

- 不建设可视化升级平台或 Web 管理页面。
- 不自动执行生产升级。
- 不自动修改真实生产 `.env`、云平台配置、数据库连接串或对象存储凭据。
- 不自动执行对象存储写入维护任务；写入型维护任务仍必须显式 dry-run、备份确认和人工授权。
- 不引入 Kubernetes、Helm、Terraform、Ansible 或外部 CI/CD 平台托管能力。
- 不为首次部署、相邻升级、跨版本升级构建不同业务镜像；同一目标版本仍复用同一组 backend / web 镜像。
- 不把历史缺失 release 事实源伪造成 verified release；历史信息不足时应标记为 reconstructed、partial 或 requires manual review。
- 不改变既有产品版本发布命令的基本职责；本需求是在 release 事实源之上补升级路径治理。

## 4. 功能要求

### FR-001 版本事实源一致性

系统 MUST 明确区分产品版本、发布版本、镜像版本、源码版本和部署运行版本。

版本事实源 SHOULD 至少包含：

| 事实源 | 说明 |
|---|---|
| `releases/<version>/release.json.version` | 产品发布版本事实源。 |
| `src/shared/product-version.ts` | 用户可见产品版本事实源。 |
| `releases/<version>/image-manifest.json.image_tag` | 目标部署镜像 tag。 |
| Git tag / commit | 源码快照锚点。 |
| 生产 env `TILESFST_IMAGE_TAG` | 实际部署目标镜像版本。 |

发布或升级校验 MUST 能发现版本事实源缺失、漂移或不一致，并按规则输出 blocker 或 warning。Git tag 不应替代 `release.json`，但目标版本发布确认后 SHOULD 具备可追溯 Git tag 或 commit。

### FR-002 升级支持级别

系统 MUST 为每条部署或升级路径输出支持级别。

支持级别 SHOULD 包含：

| 支持级别 | 含义 |
|---|---|
| `fresh-install-supported` | 目标版本支持空环境首次部署。 |
| `adjacent-upgrade-supported` | 支持从上一发布版本升级到目标版本。 |
| `cross-version-upgrade-supported` | 支持从指定旧版本跨多个版本升级到目标版本，且已有完整验证证据。 |
| `cross-version-upgrade-requires-manual-review` | 跨版本升级理论上可规划，但缺少完整演练或存在 DB/env/object storage 等需人工复核项。 |
| `unsupported` | 不支持直接升级，需要专项迁移、先升中间版本或人工方案。 |

缺少 release 事实源、缺少中间版本影响证据或缺少跨版本演练证据时，系统 MUST NOT 将跨版本升级标记为 `cross-version-upgrade-supported`。

### FR-003 升级路径对象

系统 SHOULD 为目标版本生成升级路径对象。

升级路径对象 MAY 放在：

```text
releases/<to-version>/upgrade-plans/
```

升级路径对象 SHOULD 至少覆盖：

| 字段 | 说明 |
|---|---|
| `from_version` | 来源版本，可为 `fresh` 或具体版本号。 |
| `to_version` | 目标版本。 |
| `support_level` | 支持级别。 |
| `source_confidence` | 来源版本事实可信度，如 verified、reconstructed、partial。 |
| `impact_summary` | DB、env、Docker、API、对象存储、维护任务影响摘要。 |
| `required_checks` | 升级前必须完成的检查。 |
| `steps` | 升级执行步骤。 |
| `rollback` | 回滚步骤和证据要求。 |
| `blockers` | 阻断项。 |
| `warnings` | 可接受但需关注的风险。 |
| `evidence` | 校验、演练、备份、smoke 等证据摘要。 |

升级路径对象 MUST NOT 存储真实 `.env` 内容、密钥、数据库连接串、Authorization header、Cookie、本机绝对路径或真实客户数据。

### FR-004 首次部署计划

系统 MUST 能为目标版本生成首次部署计划。

首次部署计划 MUST 覆盖：

- 目标版本 `release.json` 存在且版本一致。
- 目标版本 image manifest 存在，image tag、tarball 和 sha256 可校验。
- 生产 env 示例与真实 env 必填变量检查，不输出真实值。
- `APP_ENV=production` 时必须使用 MySQL `DATABASE_URL`。
- 对象存储 provider、bucket、region、endpoint 和自动建桶策略检查。
- Docker Compose config 校验。
- 空库初始化路径和 `init_database()` 幂等初始化说明。
- 首次管理员初始化和密码安全边界。
- 部署后健康检查、登录、核心 API、Web 静态资源、对象存储读写或只读 smoke。

首次部署计划通过后，系统 MAY 将该路径标记为 `fresh-install-supported`。

### FR-005 相邻版本升级计划与回滚

系统 MUST 能为上一发布版本到目标版本生成相邻升级计划。

相邻升级计划 MUST 覆盖：

- 来源版本和目标版本 release 事实源存在。
- 目标版本 image manifest、tarball sha256 和 input hash 未漂移。
- 生产 env 的 `TILESFST_IMAGE_TAG` 需要更新为目标版本。
- env diff，包括新增变量、删除变量、默认值变化和生产必须显式配置项。
- DB 影响判断；若影响数据库，必须要求 MySQL drift 或目标 MySQL smoke、备份和回滚证据。
- Docker Compose、deploy env 示例和构建输入是否漂移。
- 升级前备份确认。
- 停止或滚动重启策略。
- 升级后健康检查、登录、核心 API、Web、小程序或对象存储 smoke。

相邻升级回滚计划 MUST 覆盖：

- 回退旧镜像 tag 或旧镜像 tarball。
- 恢复旧 env 摘要或人工确认的旧 env。
- DB 备份恢复条件和执行责任。
- 对象存储写入影响和恢复边界。
- 回滚后 smoke 和结果记录。

### FR-006 跨版本升级计划与回滚

系统 MUST 能为指定旧版本到目标版本生成跨版本升级计划。

跨版本升级计划 MUST 聚合 `from_version` 到 `to_version` 之间的发布影响，至少覆盖：

- 中间版本 release 事实源完整性。
- DB schema、migration、MySQL drift 和数据修复影响。
- env 示例变化和生产必须显式配置变化。
- Dockerfile、Compose、镜像构建输入和 image manifest 变化。
- API / Orval 变化和兼容风险。
- 对象存储 bucket、prefix、object key、缩略图、历史媒体维护任务影响。
- 必须 dry-run 的生产维护任务。
- 必须人工确认或演练的步骤。
- 是否需要先升到中间版本再升目标版本。

当缺少跨版本演练证据或中间版本事实源不完整时，系统 SHOULD 将支持级别标记为 `cross-version-upgrade-requires-manual-review`。只有完成升级演练、DB drift/smoke、env diff、对象存储审计、回滚证据和升级后 smoke 后，才可标记为 `cross-version-upgrade-supported`。

跨版本回滚计划 MUST 明确：

- 升级前全量备份要求。
- 旧镜像和旧 env 恢复方式。
- DB 回滚只能基于备份或明确的反向迁移策略。
- 对象存储写入型维护任务的不可逆风险和人工确认。
- 回滚后需要执行的核心 smoke。

### FR-007 环境变量差异分析

系统 SHOULD 提供 env diff 能力，支持比较来源版本和目标版本的 env 示例。

env diff MUST 覆盖：

- 根目录 `.env.example`。
- `src/backend/.env.example`。
- `src/backend/.env.docker`。
- `deploy/**/*.env.example`。
- `scripts/build-images.env.example`。

env diff SHOULD 输出：

| 类别 | 说明 |
|---|---|
| added | 目标版本新增变量。 |
| removed | 目标版本删除变量。 |
| changed_default | 示例默认值变化。 |
| required_in_production | 生产必须显式配置。 |
| unsafe_example_value | 生产不得使用示例值。 |
| manual_review | 无法自动判断，需要人工复核。 |

env diff MUST 只输出变量名、分类、说明和修复建议，不得输出真实生产 env 值。

### FR-008 数据库升级验证

系统 MUST 区分“存在幂等迁移代码”和“升级路径已验证”。

数据库升级验证 MUST 覆盖：

- SQLite schema 和 migration 输入。
- MySQL `schema.mysql.sql` 和 `mysql_migrations.py` 输入。
- `schema_migrations` 或等价版本记录。
- 目标 MySQL schema drift 或 smoke 证据。
- DB 备份、恢复或回滚责任说明。
- 关键业务读写 smoke。

当 `impact_scope.database` 非 `none` / `na` / `不涉及` 时，升级计划 MUST 要求数据库门禁为 pass，并记录 MySQL drift/smoke、备份和回滚证据。不得仅凭本地 SQLite 测试通过宣称生产 DB 升级安全。

### FR-009 回滚证据模型

系统 MUST 为升级和跨版本升级定义结构化回滚证据。

回滚证据 SHOULD 包含：

| 证据 | 说明 |
|---|---|
| `previous_image` | 旧 backend / web 镜像 tag、manifest 或 sha256。 |
| `target_image` | 目标版本镜像 tag、manifest 或 sha256。 |
| `env_snapshot` | 旧 env 变量名摘要、hash 或人工确认记录，不含真实值。 |
| `database_backup` | DB 备份时间、校验摘要、恢复责任或路径占位，不含连接串。 |
| `object_storage_backup` | 对象存储备份、只读确认或写入影响说明。 |
| `rollback_steps` | 回滚命令或人工步骤。 |
| `post_rollback_smoke` | 回滚后健康检查和核心功能 smoke。 |

若缺少必要回滚证据，系统 MUST 将升级计划标记为 blocked 或 requires_manual_review。

### FR-010 命令与工作流集成

系统 SHOULD 新增或扩展 upgrade 命令族。

候选命令包括：

```text
/upgrade-plan --from <fresh|version> --to <version>
/upgrade-validate --plan <path>
```

命令 MUST：

- 读取相关 release 事实源、image manifest、env 示例、DB schema/migration、Compose 和维护任务文档。
- 输出升级支持级别、阻塞项、warning、执行步骤和回滚证据要求。
- 遵守上下文预算治理，不为跨版本分析全量展开历史归档。
- 不自动执行生产升级，不自动修改真实 env，不自动执行写入型 DB 或对象存储维护任务。
- 接入 Workflow Sync 和 AI Usage 输出契约。
- 在需要用户确认时使用结构化选项，明确推荐项和风险。

## 5. UI / UE 约束

本需求不新增 Web 管理端、店主 Web 或微信小程序 UI。

命令输出 SHOULD 面向发布、实施、运维和评审读者，重点展示：

- 来源版本和目标版本。
- 支持级别。
- 升级影响摘要。
- blocker / warning。
- 升级前检查。
- 升级步骤。
- 回滚步骤。
- 证据缺口。

命令输出 MUST 保持安全，不展示真实密钥、真实 `.env` 内容、数据库连接串、Authorization header、Cookie、生产私有域名或真实客户数据。

## 6. 非功能约束

| 项 | 要求 |
|---|---|
| 安全 | 所有升级计划、回滚证据和命令输出不得泄露密钥、连接串、真实 env、对象存储凭据或客户数据。 |
| 可追踪 | 每条升级路径必须能追溯到 from version、to version、release、image manifest、Git ref、env diff、DB 证据和 smoke 证据。 |
| 可验证 | 支持级别必须由证据驱动，缺少证据时降级为 requires manual review 或 unsupported。 |
| 可回滚 | 升级计划必须包含回滚前置条件、回滚步骤和回滚后验证。 |
| 可维护 | 复用现有 release、image、deploy、DB 和 maintenance 脚本，不重复发明平行流程。 |
| 可扩展 | 未来可在本能力上建设可视化升级平台，但本期不要求 UI。 |

## 7. 关联需求与规范

| 关联项 | 关系 |
|---|---|
| REQ-0081-release-image-build-governance | 已有镜像准备、构建计划和 manifest 能力，本需求复用并扩展到升级路径。 |
| REQ-0093-standardize-deployment-environment-matrix | 已有 deploy 环境矩阵、env 示例和生产 env 校验能力，本需求复用并扩展 env diff。 |
| `rules/release.md` | 需要补充升级路径、支持级别和回滚证据门禁。 |
| `rules/environment.md` | 需要补充 env diff、真实 env 安全边界和升级计划输出限制。 |
| `rules/database.md` | 需要补充升级路径验证、MySQL drift/smoke 和回滚证据要求。 |
| `docs/02-deployment.md` | 需要同步首次部署、相邻升级、跨版本升级和回滚说明。 |
| `docs/08-production-image-release.md` | 需要同步镜像产物在升级计划中的引用方式。 |
| `scripts/validate-release.py` | 可能需要扩展版本一致性与升级支持级别校验。 |
| `scripts/validate-image-build.py` | 可能需要为升级计划提供 image manifest 校验复用接口。 |
| `deploy/scripts/validate-env.py` | 可能需要扩展 env diff 或升级前 env 检查。 |
| `scripts/check-mysql-schema-drift.py` | 作为数据库升级验证证据来源。 |
| `deploy/scripts/media-maintenance.sh` | 作为跨版本对象存储和历史媒体维护 dry-run 证据来源。 |

## 8. 状态块

```yaml
requirement_id: REQ-0114-version-deployment-upgrade-rollback-governance
priority: P1
status: done
readiness: Ready
next_step: /opsx-apply REQ-0114-version-deployment-upgrade-rollback-governance
related_change: add-version-deployment-upgrade-rollback-governance
```
openspec_changes:
  - change_id: add-version-deployment-upgrade-rollback-governance
    type: update
    status: archived
