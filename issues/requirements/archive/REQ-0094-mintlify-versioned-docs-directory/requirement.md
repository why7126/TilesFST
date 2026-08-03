---
requirement_id: REQ-0094-mintlify-versioned-docs-directory
title: Mintlify 多版本产品文档目录与站点浏览
terminal: multi
version: v1
status: done
owner: product
source: capture.md
priority: P1
parent_requirement: REQ-0088-versioned-product-usage-docs
created_at: 2026-08-03 13:39:27
updated_at: 2026-08-03 20:28:42
---

# REQ-0094 Mintlify 多版本产品文档目录与站点浏览

## 1. 需求背景

项目已通过 REQ-0088 建立版本化产品使用文档治理：每个发布版本可以在 `releases/vX.Y.Z/usage-docs/` 下维护独立的公开产品使用文档快照，并通过 `usage-docs/manifest.json`、`releases/mint.json` 和发布校验保障内容、导航与公开安全。

当前结构适合保留发布证据与版本快照，但如果 Mintlify 网站需要一次性浏览多个产品版本，继续把文档站源文件完全放在 `releases/` 内会让站点导航、`latest` 指针、多版本入口和站点构建配置越来越依赖发布归档目录。长期看，`releases/` 会同时承担“发布事实源”和“线上文档站源目录”两种职责，容易出现边界不清、旧版本误改、导航维护分散和站点体验受限的问题。

本需求采用探索确认的方案 B：新增面向 Mintlify 的文档站源目录，例如一级 `mintlify/`，由 `releases/vX.Y.Z/usage-docs/` 的版本快照同步或投影生成站点可浏览目录。`releases/` 继续作为发布事实源和审计快照，`mintlify/` 负责文档站导航、多版本浏览、`latest` 默认版本和站点构建配置。

由于新增一级目录会改变项目目录边界，后续实现前必须通过 OpenSpec Change 同步 `AGENTS.md`、`rules/directory-structure.md`、`rules/document-governance.md`、`rules/release.md`、`releases/README.md` 和相关 usage docs 技能/脚本。

## 2. 目标用户

| 角色 | 诉求 |
|---|---|
| 店主 / 客户 / 公开访客 | 在 Mintlify 网站中查看当前版本和历史版本产品使用说明，并能清楚知道正在阅读哪个版本。 |
| 企业内部员工 | 在培训、交付和客户支持时快速切换不同版本文档，避免用新版本说明解释旧版本系统行为。 |
| 实施 / 运维 | 在上线交付时使用与目标版本一致的文档站链接，而不是临时翻找 `releases/` 目录。 |
| 产品负责人 / 项目负责人 | 保留发布版本快照的审计价值，同时获得更适合公开站点的多版本浏览结构。 |
| 开发 / 测试 | 通过脚本校验 release 快照、站点投影目录、Mintlify 导航和 `latest` 指针一致。 |
| AI Agent | 按规范生成、同步、校验站点源文件，不绕过 release 快照直接改写历史版本产品语义。 |
| 评审者 | 通过 `release.json`、`usage-docs/manifest.json`、站点 manifest 和 Mintlify 配置追踪来源、同步状态与公开边界。 |

## 3. 范围

### 3.1 本期包含

- 新增或正式定义 `mintlify/` 作为 Mintlify 文档站源目录。
- 保留 `releases/vX.Y.Z/usage-docs/` 作为发布版本使用文档事实源和快照。
- 定义从 release 快照到 `mintlify/` 站点目录的同步或投影策略。
- 定义多版本产品文档目录结构，例如 `mintlify/docs/vX.Y.Z/`、`mintlify/docs/latest/`。
- 定义系统截图资产治理：`releases/vX.Y.Z/usage-docs/` 默认不直接存放大截图文件，只在 manifest 中记录截图引用、hash、来源和覆盖页面；Mintlify 站点集中维护可复用截图资产。
- 定义发布公告在 `mintlify/` 中的站点入口，例如 `mintlify/releases/vX.Y.Z/announcement.mdx` 或等价投影路径。
- 迁移或生成 Mintlify 配置，例如 `mintlify/mint.json`，并明确 `releases/mint.json` 的保留、迁移或兼容策略。
- 定义 `latest`、`stable` 或默认版本指针规则。
- 扩展 usage docs 生成、更新、校验流程，使其能校验 release 快照与站点源目录一致。
- 支持对已有版本文档执行一次性受控迁移、复制或投影，并保留来源记录。
- 同步目录结构、文档治理、发布治理和技能命令说明。
- 支持 Docker Compose 以可选 profile 启动 Mintlify 文档站服务，用于本地预览、演示或受控部署。
- 增加校验，覆盖站点导航、多版本目录、release 快照一致性、敏感信息和旧版本内容性改写风险。

### 3.2 本期不包含

- 不删除 `releases/vX.Y.Z/usage-docs/` 快照目录。
- 不把 `mintlify/` 作为发布证据事实源替代 `release.json` 或 `usage-docs/manifest.json`。
- 不实现真实 Mintlify 账号、域名、DNS、Cloudflare、Vercel、CDN 或生产 Nginx 配置。
- 不把内部技术文档、OpenSpec 规格、Issue 文档、Sprint 文档或运维密钥文档公开到 `mintlify/`。
- 不新增后端 API、数据库表、Web 管理端入口、小程序入口或用户权限模型。
- 不要求默认 `docker compose up` 无条件启动 Mintlify 服务；文档站服务应通过 profile 或明确配置启用。
- 不把 Mintlify 服务作为后端、Web、MinIO 或对象存储运行链路的强依赖。
- 不自动重写历史版本产品行为说明；旧版本内容性更正仍需明确授权和记录。
- 不要求所有历史版本都必须有完整 usage docs；无文档版本可以只展示公告或记录文档不可用说明。

## 4. 功能要求

### FR-001 文档站源目录

系统 MUST 定义 `mintlify/` 作为 Mintlify 文档站源目录。

推荐结构：

```text
mintlify/
├── mint.json
├── assets/
│   └── screenshots/
│       ├── sha256-abcd1234-admin-sku-list.png
│       └── sha256-efgh5678-miniapp-home.png
├── releases/
│   └── vX.Y.Z/
│       └── announcement.mdx
└── docs/
    ├── latest/
    ├── stable/
    └── vX.Y.Z/
        ├── overview.mdx
        ├── admin/
        ├── miniapp/
        └── public/
```

`mintlify/` MUST 只承载公开文档站源文件、站点配置、公开截图和必要的站点级 manifest，不得存放运行时构建产物、真实客户数据、密钥、数据库连接串、Authorization header、Cookie、生产私有域名或不可公开运维信息。

### FR-002 release 快照职责保留

系统 MUST 保留 `releases/vX.Y.Z/usage-docs/` 作为该版本产品使用文档事实源和发布快照。

`releases/vX.Y.Z/usage-docs/manifest.json` MUST 继续记录当前版本文档页面、截图引用、截图 hash、截图来源、覆盖页面、人工维护和自动化策略。

`releases/vX.Y.Z/usage-docs/` SHOULD NOT 默认存放大体积系统截图文件。若因发布审计、离线交付或临时兼容必须保留截图文件，MUST 在 manifest 中记录保留原因、文件大小、来源、hash 和清理或迁移策略。

`mintlify/` 中的同版本文档 MUST 能追溯到对应 release 快照、manifest 和发布版本，不得把站点源文件视为唯一事实源。

### FR-003 站点投影或同步策略

系统 MUST 定义从 release 快照到 `mintlify/` 的投影或同步策略。

同步策略 MUST 至少明确：

| 字段 | 说明 |
|---|---|
| `source_release` | 来源发布目录，例如 `releases/v0.3.3/`。 |
| `source_manifest` | 来源 manifest，例如 `releases/v0.3.3/usage-docs/manifest.json`。 |
| `target_site_root` | 目标站点目录，例如 `mintlify/docs/v0.3.3/`。 |
| `mode` | 同步、复制、投影或链接策略。 |
| `content_hashes` | 来源页面、截图资产引用和目标页面的 hash 或等价一致性证据。 |
| `synced_at` | 同步时间，格式 `YYYY-MM-DD HH:mm:ss`。 |
| `manual_overrides` | 站点层允许的非语义改动记录，例如导航标题、slug 或链接修复。 |

同步流程 MUST 默认从 release 快照生成或刷新站点目录，而不是绕过 release 快照直接生成站点文档。

### FR-004 共享截图资产库

系统 MUST 支持 Mintlify 站点级共享截图资产库，减少不同版本重复存放相同图片。

推荐结构：

```text
mintlify/
├── assets/
│   └── screenshots/
│       └── sha256-<hash>-<semantic-name>.png
└── docs/
    └── vX.Y.Z/
        └── ...
```

截图文件名 SHOULD 包含内容 hash 和语义名称。不同版本页面 MAY 引用同一截图资产，但必须满足以下条件：

| 场景 | 复用规则 |
|---|---|
| 界面、字段、操作入口、数据状态均未变化 | MAY 复用 |
| 仅文案或轻微样式变化且不影响用户理解 | MAY 复用，但 manifest MUST 标注复用原因 |
| 页面布局、字段、按钮、流程或权限边界变化 | MUST 新增截图 |
| 截图包含版本号、日期、真实数据或发布特征 | SHOULD 新增截图，除非有明确复用说明 |
| `latest` 页面 | MAY 引用当前目标版本使用的截图资产 |

站点 manifest 或 release manifest MUST 记录截图资产的 `content_hash`、`first_used_in`、`used_by_versions`、`covered_pages`、`source_type` 和 `reuse_reason`。

示例：

```json
{
  "asset": "mintlify/assets/screenshots/sha256-abcd1234-admin-sku-list.png",
  "content_hash": "abcd1234",
  "first_used_in": "v0.3.3",
  "used_by_versions": ["v0.3.3", "v0.3.4"],
  "covered_pages": ["mintlify/docs/v0.3.4/admin/catalog.mdx"],
  "source_type": "runtime_system",
  "reuse_reason": "SKU 列表界面和操作入口未变化"
}
```

### FR-005 多版本导航

Mintlify 配置 MUST 支持一次性浏览多个产品版本。

导航 SHOULD 至少包含：

- 产品发布公告入口。
- 当前版本产品使用文档入口。
- 历史版本产品使用文档入口。
- `latest` 默认版本入口。
- 对缺少 usage docs 的历史版本给出清晰不可用或仅公告可用说明。

Mintlify 页面路径 MUST 避免歧义，例如 `docs/v0.3.3/overview`、`docs/latest/overview`、`releases/v0.3.3/announcement`。

### FR-006 latest / stable 指针

系统 MUST 定义 `latest` 指针更新规则。

`latest` SHOULD 默认指向最新已发布且 usage docs 校验通过的版本。若最新版本明确跳过 usage docs，则 `latest` MUST 继续指向最近一个有可用产品使用文档的已发布版本，或显示当前最新版本未生成产品使用文档的说明。

若引入 `stable` 指针，`stable` MUST 由人工确认或发布配置显式声明，不得自动等同于最新版本。

### FR-007 usage docs 命令扩展

`/usage-docs-generate <version>`、`/usage-docs-update <version>` 和 `/usage-docs-validate <version>` SHOULD 支持站点目录。

命令扩展 SHOULD 包括：

- 生成或刷新 `releases/<version>/usage-docs/**` 后，同步或投影到 `mintlify/docs/<version>/**`。
- 将系统截图写入或复用 `mintlify/assets/screenshots/`，并在 release manifest 或站点 manifest 中记录引用。
- 更新或生成 `mintlify/mint.json` 导航。
- 更新 `latest` 指针。
- 校验 release manifest 页面清单与站点目录页面一致。
- 校验站点截图引用、截图 hash、链接和公开安全。
- 报告站点目录未同步、hash 漂移、截图复用依据缺失、导航缺页或旧版本内容性误改。

### FR-008 发布流程集成

`/release-prepare <version>` 和 `/release-publish <version>` SHOULD 纳入站点目录校验。

发布准备阶段 SHOULD 在 usage docs 生成或跳过决策之后，校验 `mintlify/` 站点目录状态：

```text
release.json
  └─ usage_docs decision
      ├─ generated: releases/<version>/usage-docs/** → mintlify/docs/<version>/** + mintlify/assets/screenshots/** → mintlify/mint.json
      └─ skipped: release gate 记录跳过原因，站点可只展示公告或文档不可用说明
```

发布确认阶段 SHOULD 记录 Mintlify 站点校验结果或明确未执行真实站点 preview 的替代校验证据。

### FR-009 Docker Compose 文档站服务

系统 SHOULD 支持通过 Docker Compose 启动 Mintlify 文档站服务，用于本地预览、演示部署或受控生产部署。

Compose 集成 SHOULD 满足：

- 新增 `mintlify` 或 `docs` 服务时，必须通过 `docs-site` 或等价 profile 启动，避免默认部署无条件增加非业务服务。
- 服务工作目录 SHOULD 指向 `mintlify/`，并使用 `mintlify/mint.json` 作为站点配置。
- 宿主机端口 MUST 通过 `.env.example` 中的变量配置，例如 `HOST_PORT_MINTLIFY_DOCS`；不得硬编码多个端口入口。
- 容器内端口 SHOULD 遵循 Mintlify 服务默认端口或项目明确约定，并在 `rules/port-management.md` 和部署文档中说明。
- `docker-compose.yml`、`docker-compose.prod*.yml` 是否启用文档站服务必须按场景说明：本地/演示可启用，生产可选择外部 Mintlify/静态托管或 Compose 内服务。
- 新增 service、ports、volumes、environment、command、profiles 时，必须有邻近注释，且同步 `.env.example`、`docs/02-deployment.md`、`rules/environment.md` 和发布门禁说明。
- 若文档站服务进入生产镜像或 Compose 发布范围，发布流程 MUST 将 Docker Compose 验证和镜像构建证据纳入 release gates。

### FR-010 历史版本迁移

系统 MAY 提供一次性迁移或投影命令，将已有 `releases/vX.Y.Z/usage-docs/` 复制或投影到 `mintlify/docs/vX.Y.Z/`。

历史版本迁移 MUST：

- 不改变 release 快照原始语义。
- 保留来源版本、来源 manifest 和同步时间。
- 将历史截图迁移或去重到 `mintlify/assets/screenshots/`，并按内容 hash 合并重复图片。
- 允许非内容性修复，例如相对链接、frontmatter、Mintlify slug、导航标题和敏感信息移除。
- 对内容性更正记录授权来源、原因、时间和文件范围。
- 对缺失 usage docs 的版本给出可解释状态，不强行生成空文档。

### FR-011 目录治理同步

如果新增 `mintlify/` 一级目录，实现前 MUST 通过 OpenSpec Change 同步：

- `AGENTS.md` 目录边界和发布/文档说明。
- `rules/directory-structure.md` 一级目录白名单。
- `rules/document-governance.md` 产品使用文档快照与站点源目录职责。
- `rules/release.md` 发布准备、发布确认和 Mintlify 校验门禁。
- `rules/environment.md` 与 `rules/port-management.md` 中 Mintlify 服务端口、环境变量和 Docker Compose profile 说明。
- `docs/02-deployment.md` 中 Docker Compose 启动 Mintlify 服务、外部托管替代和 `/docs` 访问边界。
- `releases/README.md` 中 `releases/` 与 `mintlify/` 的职责边界。
- usage docs 相关 Skill 和脚本说明。
- 目录结构校验脚本和测试。

### FR-012 公开安全

`mintlify/` MUST 继承公开文档安全扫描规则。

校验 MUST 阻断：

- `.env` 真实内容。
- 数据库连接串。
- 对象存储密钥、云厂商密钥和 Bucket 私有配置。
- Authorization header、Cookie、Token。
- 真实客户数据。
- 生产私有域名、内网地址或不可公开运维信息。
- 本地绝对路径或开发者个人路径。

## 5. UI / 站点体验约束

- 文档站导航必须清楚区分“产品发布公告”和“产品使用文档”。
- 多版本入口必须明确版本号，不得让用户误以为旧版本文档是当前版本说明。
- `latest` 页面必须有可追溯的目标版本。
- 缺少 usage docs 的历史版本不得展示空页面，应显示仅公告可用或文档未生成状态。
- 页面引用共享截图时，manifest 必须能说明该截图适用于当前版本，避免历史版本展示不属于该版本的界面。
- Docker Compose 启动的 Mintlify 服务不得展示内部文档、未评审 Issue、OpenSpec 中间态、真实 `.env`、生产私有域名或本地绝对路径。
- Mintlify 页面标题、分组和路径命名应优先面向客户、店主和实施人员理解，避免暴露内部工作流术语。
- 公开页面不得显示 OpenSpec 内部状态、Sprint 中间态、未评审 REQ/BUG、内部验收失败项或敏感部署细节。

## 6. 关联需求

| 需求 | 关系 | 说明 |
|---|---|---|
| REQ-0088-versioned-product-usage-docs | 父需求 | 已建立 `releases/<version>/usage-docs/` 快照、manifest、生成/校验和发布门禁。 |
| REQ-0026-product-release-management | 相关 | 发布目录、公告、release gate 和 Mintlify 公告治理基础。 |
| REQ-0081-release-image-build-governance | 弱相关 | 发布证据与 release 目录治理原则一致，但本需求不涉及镜像构建。 |

## 7. 状态块

```yaml
requirement_id: REQ-0094-mintlify-versioned-docs-directory
status: done
priority: P1
parent_requirement: REQ-0088-versioned-product-usage-docs
selected_solution: B
selected_solution_summary: 新增 mintlify 文档站源目录，release 快照同步或投影到站点目录；系统截图集中到 mintlify/assets/screenshots 并按内容 hash 跨版本复用。
requires_openspec_change: true
impacts:
  api: false
  database: false
  web: false
  miniapp: false
  admin: false
  docs: true
  release: true
  directory_structure: true
  media_assets: true
  docker_compose: true
  environment_variables: true
orval_required: false
docker_compose_validation_required: true
readiness: Ready
next_command: /req-opsx REQ-0094-mintlify-versioned-docs-directory
```
