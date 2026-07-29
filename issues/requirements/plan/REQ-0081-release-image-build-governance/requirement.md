---
requirement_id: REQ-0081-release-image-build-governance
title: 发布镜像准备与构建治理
terminal: multi
version: v1
status: pending_review
owner: product
source: capture.md
priority: P1
parent_requirement:
created_at: 2026-07-29 10:04:35
updated_at: 2026-07-29 10:07:04
---

# REQ-0081 发布镜像准备与构建治理

## 1. 需求背景

项目已建立产品版本发布流程，包含 `/release-propose`、`/release-prepare`、`/release-publish`，并通过 `releases/<version>/release.json` 汇总版本范围、门禁、公告、影响范围、升级步骤与回滚说明。生产部署也已有镜像构建脚本 `scripts/build-images.sh`、构建配置示例 `scripts/build-images.env.example`、生产 Compose 文件和生产镜像包构建文档。

当前风险在于：发布范围如果涉及数据库 schema、迁移脚本、Dockerfile、Compose、环境变量、镜像构建脚本或基础镜像参数变更，仅靠发布说明和普通测试门禁不足以保证“下一次构建镜像一定使用当前版本的脚本和配置”。如果镜像构建脚本、构建 env、Compose image tag 或数据库迁移证据没有进入发布门禁，就可能出现发布流程看似通过，但实际交付镜像仍沿用旧脚本、旧 tag、旧 schema 或旧构建输入的情况。

本需求用于把镜像准备与镜像构建纳入发布治理，明确 `/image-prepare` 与 `/image-build` 的职责边界、产物、依赖关系和发布门禁，使发布版本、镜像 tag、构建脚本、Dockerfile、Compose、数据库迁移和离线镜像包形成可追踪的一致性契约。

## 2. 目标用户

| 角色 | 诉求 |
|---|---|
| 产品负责人 / 项目负责人 | 能确认一次产品发布是否需要构建新镜像，以及镜像证据是否满足发布门禁。 |
| 开发 / 测试 | 在发布前明确哪些源码、脚本、Schema、Compose 或 env 变化会触发镜像准备和构建校验。 |
| 实施 / 运维 | 使用清晰的镜像构建计划和 manifest 执行交付，不再靠人工猜测 tag、构建目录或脚本版本。 |
| AI Agent | 按命令依赖和文件事实源生成、校验、引用镜像构建证据，避免越过 OpenSpec 或发布门禁。 |
| 评审者 | 能通过 `release.json`、`image-build-plan.json` 和 `image-manifest.json` 追踪版本与镜像产物的一致性。 |

## 3. 范围

### 3.1 本期包含

- 定义 `/image-prepare <version>` 命令：负责镜像构建前的轻量契约校验与构建计划生成。
- 定义 `/image-build <version>` 命令：负责真实镜像构建、镜像验证、离线包导出和 manifest 生成。
- 定义五个命令的依赖关系：`/release-propose`、`/release-prepare`、`/image-prepare`、`/image-build`、`/release-publish`。
- 定义 `image_required` 判定规则，用于判断发布版本是否必须执行镜像准备或镜像构建。
- 定义 `releases/<version>/image-build-plan.json` 的职责、核心字段和校验规则。
- 定义 `releases/<version>/image-manifest.json` 的职责、核心字段和校验规则。
- 将镜像准备与构建证据纳入 `release.json` 门禁或影响范围。
- 定义数据库、Dockerfile、Compose、`.env.example`、构建脚本、构建 env 示例变化与镜像构建的关系。
- 明确 Docker 或网络不可用时的 blocker 记录方式和人工外部构建证据边界。

### 3.2 本期不包含

- 不直接实现 CI/CD 自动发布流水线。
- 不自动推送镜像到远程镜像仓库，除非后续 OpenSpec Change 单独确认。
- 不改变用户可见产品版本号事实源，`PRODUCT_VERSION` 仍按发布规范维护。
- 不替代 `/release-propose`、`/release-prepare`、`/release-publish` 的发布职责。
- 不在 PRD 阶段创建 OpenSpec Change、修改脚本或构建镜像。
- 不引入复杂发布状态机，如草稿、待发布、已发布、撤回。
- 不把真实 `.env`、数据库连接串、密钥或不可公开运维地址写入镜像计划、manifest 或公告。

## 4. 功能要求

### FR-001 镜像影响判定

发布流程 MUST 能判断当前版本是否需要镜像准备或镜像构建。

当发布范围存在以下任一变化时，系统 MUST 将 `image_required` 判定为 `true`，并要求至少执行 `/image-prepare`：

- 后端运行代码、依赖、启动命令或 `src/backend/Dockerfile` 变化。
- Web 构建代码、共享资源、Nginx 配置或 `src/web/Dockerfile` 变化。
- `docker-compose*.yml`、`.env.example`、`scripts/build-images.env.example` 或镜像构建参数变化。
- 数据库 schema、迁移脚本、MySQL schema drift 校验或回滚策略变化。
- API / Orval 生成物变化影响 Web 构建产物。
- 发布计划明确要求生成离线镜像包或交付镜像。

若 `image_required` 为 `false`，发布对象 MUST 记录明确 rationale。

### FR-002 `/image-prepare` 构建前契约校验

系统 SHOULD 提供 `/image-prepare <version>` 命令，用于轻量校验镜像构建输入。

`/image-prepare` MUST：

- 读取 `releases/<version>/release.json`。
- 校验发布版本、`PRODUCT_VERSION`、`TILESFST_IMAGE_TAG`、`IMAGE_BUILD_TAG` 的一致性或记录明确差异理由。
- 校验 `scripts/build-images.env` 是否存在，或说明应由 `scripts/build-images.env.example` 复制生成。
- 校验 `scripts/build-images.env.example` 中常规发版路径只需要修改 `IMAGE_BUILD_TAG`。
- 校验生产 Compose 默认镜像 tag 与发布版本一致。
- 校验 Dockerfile、Compose、构建脚本、构建 env 示例、数据库 schema / migration 的输入是否纳入计划。
- 在 Docker 不可用或网络不可用时，不执行真实构建，但 MUST 记录 blocker 或外部证据要求。
- 生成或更新 `releases/<version>/image-build-plan.json`。

### FR-003 `image-build-plan.json` 构建计划

`image-build-plan.json` MUST 作为镜像构建前计划事实源，记录本次镜像构建所需输入。

构建计划 SHOULD 至少包含：

| 字段 | 说明 |
|---|---|
| `version` | 产品发布版本，例如 `v0.2.0`。 |
| `image_required` | 是否需要镜像构建。 |
| `image_tag` | backend / web 默认共用的镜像 tag。 |
| `source_scope` | 关联 Sprint、REQ、BUG、Change。 |
| `build_env` | 构建 env 文件路径与关键非敏感变量摘要。 |
| `input_files` | Dockerfile、Compose、构建脚本、schema、migration、Nginx 配置等输入文件列表。 |
| `input_hashes` | 输入文件 hash，用于后续 manifest 与当前源码比对。 |
| `database_impact` | 是否涉及数据库，以及 MySQL schema drift / rollback 证据要求。 |
| `required_commands` | 后续 `/image-build` 应执行的构建与验证命令摘要。 |
| `blockers` | 当前阻断项，如缺少 env、Docker 不可用、版本不一致。 |

构建计划 MUST NOT 包含真实 `.env` 内容、密钥、数据库连接串、Authorization header、Cookie 或真实客户数据。

### FR-004 `/image-build` 镜像构建与验证

系统 SHOULD 提供 `/image-build <version>` 命令，用于执行真实镜像构建和产物导出。

`/image-build` MUST：

- 读取 `releases/<version>/image-build-plan.json`。
- 拒绝在缺少有效 image build plan 时自行猜测构建输入。
- 执行或封装现有 `scripts/build-images.sh`。
- 构建 backend 和 web 镜像。
- 验证镜像平台与目标平台一致。
- 验证后端关键依赖可导入。
- 验证 Web Nginx 配置可通过。
- 按配置导出离线镜像包和 `.sha256`。
- 生成或更新 `releases/<version>/image-manifest.json`。

如果 Docker、buildx、网络或基础镜像源不可用，`/image-build` MUST 记录失败分类与可执行修复建议，不得伪造构建成功证据。

### FR-005 `image-manifest.json` 镜像产物清单

`image-manifest.json` MUST 作为镜像构建结果事实源，记录镜像构建产物和输入快照。

manifest SHOULD 至少包含：

| 字段 | 说明 |
|---|---|
| `version` | 产品发布版本。 |
| `image_tag` | 本次构建使用的镜像 tag。 |
| `built_at` | 构建完成时间，格式为 `YYYY-MM-DD HH:mm:ss`。 |
| `platform` | 构建平台，例如 `linux/amd64`。 |
| `backend_image` | backend 镜像名、tag、image id 或 digest。 |
| `web_image` | web 镜像名、tag、image id 或 digest。 |
| `tarball` | 离线镜像包路径、文件名和 sha256。 |
| `input_hashes` | 从 build plan 继承并确认的输入文件 hash。 |
| `validation` | 平台、后端依赖、Web Nginx、Compose 或 smoke 的验证摘要。 |
| `source_plan` | 对应 `image-build-plan.json` 路径和 hash。 |

manifest MUST 支持 release-publish 阶段比对当前输入是否已漂移。若 Dockerfile、构建脚本、schema、migration 或 Compose 在 manifest 生成后又发生变化，发布流程 MUST 视为镜像证据失效。

### FR-006 发布命令依赖关系

五个命令 MUST 形成门禁依赖：

```text
/release-propose
  → /release-prepare
  → /image-prepare   # image_required=true 时必须
  → /image-build     # 需要交付镜像或 manifest 时必须
  → /release-publish
```

依赖规则：

- `/release-prepare` MUST 依赖已存在的 `releases/<version>/release.json`。
- `/image-prepare` MUST 依赖 `release.json`，并 SHOULD 在 `/release-prepare` 明确影响范围后执行。
- `/image-build` MUST 依赖有效的 `image-build-plan.json`。
- `/release-publish` MUST 依赖通过的 `/release-prepare` 结果。
- 当 `image_required=true` 时，`/release-publish` MUST 依赖有效的 `image-manifest.json` 或明确批准的外部构建证据。

### FR-007 发布门禁集成

发布对象 SHOULD 增加镜像相关门禁，例如 `image_prepare` 与 `image_build`。

发布准备阶段 MUST：

- 当 `image_required=true` 时，要求 `image_prepare` 为 `pass` 或记录 blocker。
- 当发布目标包含离线镜像包或生产镜像交付时，要求 `image_build` 为 `pass` 或记录 blocker。
- 在 `release.json` 中引用 `image-build-plan.json` 和 `image-manifest.json` 的路径与摘要。
- 不得在没有具体证据时将镜像门禁标记为 `pass`。

发布确认阶段 MUST：

- 校验 manifest 的版本、tag、输入 hash 与当前发布输入一致。
- 阻止 manifest 过期、缺失或与当前发布版本不匹配的发布。
- 保留人工外部构建证据入口，但必须记录证据来源、校验方式和风险。

### FR-008 数据库变更与镜像构建关系

当发布范围涉及数据库 schema 或迁移时：

- `/image-prepare` MUST 将 SQLite schema、MySQL schema、迁移脚本、数据库文档和回滚说明纳入输入或证据检查。
- `/image-build` 的 manifest MUST 记录数据库相关输入 hash。
- `/release-publish` MUST 确认 manifest 中的数据库输入未过期。
- 若数据库门禁依赖目标 MySQL smoke 或 schema drift，发布对象 MUST 记录不含敏感连接串的证据摘要。

数据库影响不允许仅凭本地 SQLite 测试通过就放行生产发布。

## 5. UI / UE 约束

本需求不新增 Web 管理端、店主 Web 或小程序 UI。

命令输出 SHOULD 面向开发、测试和运维读者，保持短摘要化，重点展示：

- 当前版本是否需要镜像。
- 哪些输入触发镜像准备或构建。
- 构建计划或 manifest 路径。
- 当前 blocker 与下一步命令。

命令输出 MUST NOT 展示真实密钥、真实 `.env` 内容、数据库连接串或不可公开运维地址。

## 6. 非功能约束

| 项 | 要求 |
|---|---|
| 安全 | 构建计划、manifest、发布公告不得泄露密钥、连接串、Authorization header、Cookie 或真实客户数据。 |
| 可追踪 | 镜像产物必须能追溯到 release、Sprint、REQ、BUG、Change 和构建输入。 |
| 可复现 | 镜像 tag、构建 env、Dockerfile、Compose、schema、migration 与离线包应形成可复核链路。 |
| 可阻断 | 缺少构建计划、manifest 过期、版本不一致、输入 hash 漂移时必须阻断发布或记录 blocker。 |
| 可维护 | `/image-prepare` 与 `/image-build` 分离，避免重构建动作被隐藏在普通发布准备中。 |
| 兼容性 | 复用现有 `scripts/build-images.sh`、Dockerfile 和 Compose；不破坏已有生产镜像构建手册。 |

## 7. 关联需求与规范

| 关联项 | 关系 |
|---|---|
| REQ-0026-product-release-management | 已有产品版本发布与公告管理能力，本需求扩展镜像构建治理。 |
| `rules/release.md` | 需要增加镜像准备和镜像构建门禁。 |
| `rules/environment.md` | 构建 env、Compose、Dockerfile 和 `.env.example` 注释边界需遵守。 |
| `rules/directory-structure.md` | 镜像计划和 manifest 应放入 `releases/<version>/`，不得新增无治理目录。 |
| `docs/08-production-image-release.md` | 需要同步镜像准备、构建和 manifest 交付说明。 |
| `scripts/build-images.sh` | 现有镜像构建脚本，应由 `/image-build` 复用或封装。 |
| `scripts/build-images.env.example` | 构建配置示例，应由 `/image-prepare` 校验。 |
| `docker-compose.prod.yml` / `docker-compose.prod.external.yml` | 生产镜像 tag 和 repository 变量事实源。 |

## 8. 状态块

```yaml
requirement_id: REQ-0081-release-image-build-governance
priority: P1
status: pending_review
iteration: null
owner: product
parent_requirement: null
openspec_changes: []
next: /req-review REQ-0081-release-image-build-governance --approve
```
