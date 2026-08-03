# 产品版本发布管理规范

## Purpose
定义产品版本发布对象、公开 Mintlify 发布公告、发布前门禁，以及受治理的 `releases/` 目录，用于将一个或多个 Sprint 的交付内容整理为一个对外产品版本。
## Requirements
### Requirement: 产品版本发布对象
系统 SHALL 支持产品版本发布对象，用于表示一次对外产品版本发布，并可将该发布关联到一个或多个 Sprint。

#### Scenario: 一个产品版本关联多个 Sprint
- **WHEN** 为某个版本创建产品发布对象
- **THEN** 发布对象 SHALL 支持关联一个或多个 Sprint ID。
- **AND** 发布对象 SHALL 区分产品发布范围与 Sprint 级 `release-note.md` 范围。

#### Scenario: 发布范围可追溯
- **WHEN** 从关联 Sprint 准备发布范围
- **THEN** 发布对象 SHALL 追踪相关 REQ、BUG 和 OpenSpec Change。
- **AND** 每个正式发布项 SHALL 可追溯到来源 issue 或 change 文档。

#### Scenario: 未完成工作不得进入正式发布范围
- **WHEN** REQ、BUG、Sprint 或 OpenSpec Change 未评审、未纳入交付范围，或未按要求归档
- **THEN** 发布流程 SHALL 将其排除在正式发布范围之外。
- **AND** 流程 MAY 仅以“已知问题”或“后续计划”列出，并使用明确的非发布措辞。

### Requirement: 公开 Mintlify 发布公告
产品版本发布管理能力 SHALL 生成或维护面向公开展示的 Mintlify 静态文档发布公告源文件。

#### Scenario: 公告为静态公开文档
- **WHEN** 准备发布公告
- **THEN** 公告 SHALL 以适合 Mintlify 的静态文档源文件编写。
- **AND** 公告展示 SHALL NOT 依赖后端运行时 API 或数据库查询。

#### Scenario: 公告构建或预览校验
- **WHEN** 发布准备流程运行校验
- **THEN** 流程 SHALL 执行 Mintlify build、preview 或已文档化的等价校验步骤。
- **AND** 校验失败 SHALL 阻断发布确认。

#### Scenario: 公告源文件可评审
- **WHEN** 创建发布公告源文件
- **THEN** 文件 SHALL 适合 Git Review。
- **AND** 当 metadata 记录发布时间时，SHALL 使用项目标准时间字段 `YYYY-MM-DD HH:mm:ss`。

### Requirement: 发布公告内容结构
每份产品发布公告 SHALL 包含客户、店主、实施、运维和项目团队所需的最小公开发布内容。

#### Scenario: 必填公告章节
- **WHEN** 生成产品发布公告
- **THEN** 公告 SHALL 包含版本号、发布时间、关联 Sprint 列表、新增功能、修复 BUG、发布说明、已知问题、升级步骤、回滚说明和影响范围。

#### Scenario: 影响范围分类
- **WHEN** 记录影响范围
- **THEN** 文档 SHALL 区分 Web 管理端、店主 Web、小程序、后端、数据库、对象存储和 Docker 影响。

#### Scenario: 公开安全边界
- **WHEN** 评审公告内容
- **THEN** 公告 SHALL NOT 暴露密钥、真实客户数据、私有数据库连接串、MinIO 凭据、非公开域名或敏感运维细节。

### Requirement: 发布前校验门禁
发布流程 SHALL 在必填发布就绪检查通过前阻断发布确认；若某项不适用，必须明确标记不适用并说明理由。测试门禁失败时，发布准备流程 SHALL classify failures before reporting blockers so governance drift can be fixed at the right layer. 当发布范围涉及镜像构建、Dockerfile、Compose、构建脚本、构建 env、数据库 schema / migration、API / Orval 构建输入或离线镜像交付时，发布门禁 SHALL 纳入镜像准备和镜像构建证据。

#### Scenario: 测试失败分类
- **WHEN** release preparation runs automated tests and any test fails
- **THEN** the release preparation output SHALL classify representative failures as archived path residual, fixture/schema drift, helper payload invalid, product regression, or environment blocker
- **AND** governance-drift failures SHALL include a concrete remediation such as updating shared test helpers, archived Change path resolution, or fixture schema
- **AND** the release object SHALL NOT mark the tests gate as pass until the focused regression and relevant suite pass.

#### Scenario: 发布准备识别镜像门禁
- **WHEN** release preparation evaluates a release whose impact includes backend runtime, Web build output, Dockerfile, Compose, `.env.example`, image build script, database schema / migration, API / Orval generated client, or offline image delivery
- **THEN** the release object SHALL mark `image_required` as true or record an equivalent image-required decision
- **AND** release preparation SHALL require an `image_prepare` gate to pass or record a blocker before publish can be ready
- **AND** release preparation SHALL NOT mark `image_prepare` as pass without concrete evidence from `releases/<version>/image-build-plan.json` or an equivalent validated plan.

#### Scenario: 发布准备不自动执行真实镜像构建
- **WHEN** release preparation determines that image build is required
- **THEN** it SHALL point to `/image-prepare <version>` and, when delivery requires a built image, `/image-build <version>`
- **AND** it SHALL NOT execute the heavy image build by default unless the user explicitly invokes the image build workflow or an equivalent documented build command.

#### Scenario: 发布确认校验镜像 manifest
- **WHEN** release publish runs for a release with `image_required` true or with offline image delivery in scope
- **THEN** it SHALL require `releases/<version>/image-manifest.json` or approved external build evidence
- **AND** it SHALL verify that manifest version, image tag, source plan, and input hashes match the current release inputs
- **AND** it SHALL block publish when the manifest is missing, stale, version-mismatched, tag-mismatched, or input hashes have drifted.

#### Scenario: 镜像证据公开安全
- **WHEN** release metadata, announcement, image build plan, image manifest, or external build evidence are validated
- **THEN** validation SHALL reject secrets, raw `.env` content, database connection strings, Authorization headers, cookies, MinIO credentials, non-public operational endpoints, or real customer data.

### Requirement: releases 目录治理
项目 SHALL 在目录规则更新后，使用受治理的顶层 `releases/` 目录存放产品版本发布对象和公开发布公告源文件。

#### Scenario: 使用前更新目录规则
- **WHEN** 实现创建顶层 `releases/` 目录
- **THEN** `rules/directory-structure.md` SHALL 已定义该目录职责、边界、命名规则和生命周期。
- **AND** AGENTS 指南 SHALL 在描述允许的顶层目录时提及该目录。

#### Scenario: 目录关系已文档化
- **WHEN** 引入 `releases/`
- **THEN** 文档 SHALL 说明它与 `iterations/`、`issues/`、`openspec/changes/`、已归档 specs 和 Mintlify 文档源的关系。

#### Scenario: 目录边界
- **WHEN** 发布产物存放在 `releases/` 下
- **THEN** 这些产物 SHALL 表示产品发布材料和公开公告源文件。
- **AND** 它们 SHALL NOT 替代 Sprint 四件套、issue 文档、OpenSpec changes 或运行时部署数据。

### Requirement: 发布命令族
项目 SHALL 定义用于提议、准备和确认产品发布的 release 命令族。

#### Scenario: 命令事实源
- **WHEN** 新增或修改 release 命令
- **THEN** `.cursor/commands/` SHALL 作为事实源。
- **AND** SHALL 运行 `python scripts/sync-agent-commands.py` 或已文档化的等价同步流程。

#### Scenario: release propose 命令
- **WHEN** 使用 release proposal 命令
- **THEN** 它 SHALL 为某个产品版本和选定 Sprint 范围创建或更新产品发布计划。

#### Scenario: release prepare 命令
- **WHEN** 使用 release preparation 命令
- **THEN** 它 SHALL 运行发布门禁，并生成或更新 Mintlify 公告源文件。

#### Scenario: release publish 命令
- **WHEN** 使用 release publish 或确认命令
- **THEN** 它 SHALL 记录发布确认凭据，且不引入 draft、pending、published、retracted 状态机。

### Requirement: 不新增应用内公告入口
产品版本发布管理能力 SHALL NOT 在管理端菜单、登录页、店主 Web 或小程序内新增发布公告入口。

#### Scenario: 不新增管理端菜单入口
- **WHEN** 实现产品版本发布管理
- **THEN** Web 管理端 sidebar 或菜单 SHALL NOT 新增发布公告入口。

#### Scenario: 不新增店主端或小程序入口
- **WHEN** 产品发布公告发布
- **THEN** 店主 Web 和小程序 SHALL NOT 作为本能力的一部分新增发布公告入口。

#### Scenario: 不新增后端公告服务
- **WHEN** 实现发布公告
- **THEN** 实现 SHALL NOT 新增后端公告 API 或数据库表，除非后续 OpenSpec Change 明确要求。

### Requirement: 版本化产品使用文档
产品版本发布管理能力 SHALL 支持按产品版本维护公开产品使用文档源文件，并 SHALL 将产品文档是否生成或更新作为发布准备阶段的显式决策。

#### Scenario: 发布准备先确认是否生成产品文档
- **WHEN** `/release-prepare <version>` 准备产品发布材料
- **THEN** 发布准备流程 SHALL 确认本次是否需要生成或更新产品使用文档。
- **AND** 在确认前 SHALL NOT 自动创建新的 `releases/<version>/usage-docs/` 文档版本。

#### Scenario: 用户确认不需要生成产品文档
- **WHEN** 用户确认某个版本不需要生成或更新产品使用文档
- **THEN** 发布对象 SHALL 记录 `usage_docs.status` 为 `skipped` 或等价状态。
- **AND** 发布对象 SHALL 记录确认来源、确认时间和跳过原因。
- **AND** 流程 SHALL NOT 创建空的当前版本 `usage-docs/` 目录或把空文档加入 Mintlify 当前版本导航。

#### Scenario: 用户确认需要生成产品文档
- **WHEN** 用户确认某个版本需要生成或更新产品使用文档
- **THEN** 流程 SHALL 生成或更新 `releases/<version>/usage-docs/**`。
- **AND** 流程 SHALL 生成或更新 `releases/<version>/usage-docs/manifest.json`。
- **AND** 流程 SHALL 将 `usage_docs.status` 标记为 `generated` 或等价状态。

### Requirement: 产品使用文档 Manifest
产品使用文档能力 SHALL 使用 manifest 记录版本化文档的来源、页面、覆盖、站点投影、截图引用和维护策略。

#### Scenario: Manifest 记录生成事实
- **WHEN** 生成某个版本的产品使用文档
- **THEN** `usage-docs/manifest.json` SHALL 记录产品版本、生成时间、来源版本、来源 release、输入文件、页面清单、覆盖摘要、截图引用、截图 hash、站点目标路径、同步状态、人工覆盖记录和自动化维护策略。
- **AND** 所有项目新增时间字段 SHALL 使用 `YYYY-MM-DD HH:mm:ss`。

#### Scenario: Manifest 支持覆盖校验
- **WHEN** 校验某个版本的产品使用文档
- **THEN** 校验流程 SHALL 使用 manifest 判断页面清单与实际文件是否一致。
- **AND** 校验流程 SHALL 判断管理端菜单、小程序主要页面和发布影响范围是否有文档覆盖或明确豁免。
- **AND** 校验流程 SHALL 使用 manifest 判断 release 快照、Mintlify 站点目录和共享截图资产引用是否一致。

### Requirement: 产品使用文档发布门禁
产品版本发布管理能力 SHALL 在需要生成或更新产品使用文档时校验产品文档门禁；不需要生成或更新时 SHALL 记录不适用理由。

#### Scenario: 需要产品文档时校验 usage_docs_preview
- **WHEN** 用户确认某版本需要生成或更新产品使用文档
- **THEN** 发布准备流程 SHALL 要求 `usage_docs_preview` gate 通过或记录 blocker。
- **AND** `usage_docs_preview` 为 pass 时 SHALL 包含具体命令、路径、时间或校验结果证据。

#### Scenario: 不需要产品文档时标记门禁不适用
- **WHEN** 用户确认某版本不需要生成或更新产品使用文档
- **THEN** `usage_docs_preview` gate SHALL 标记为 `na` 或等价不适用状态。
- **AND** gate SHALL 记录不适用理由。

#### Scenario: 产品文档静态校验
- **WHEN** 校验产品使用文档
- **THEN** 流程 SHALL 校验 manifest 结构、Mintlify 导航、broken links 或等价静态构建结果。
- **AND** 校验失败 SHALL 阻断发布确认或记录 blocker。

#### Scenario: 产品文档公开安全
- **WHEN** 校验产品使用文档、manifest、Mintlify 配置或 release metadata
- **THEN** 校验 SHALL 拒绝密钥、真实 `.env` 内容、数据库连接串、Authorization header、Cookie、MinIO 或对象存储凭据、非公开运维地址或真实客户数据。

### Requirement: 旧版本产品文档维护策略
产品版本发布管理能力 SHALL 将已发布旧版本产品文档视为发布快照，并 SHALL 区分内容性更正与非内容性维护。

#### Scenario: 禁止无授权内容性改写
- **WHEN** 自动化处理旧版本产品使用文档
- **THEN** 自动化 SHALL NOT 在无明确授权时改写产品行为说明、操作步骤、功能可用性、版本差异或已知问题历史语义。

#### Scenario: 允许非内容性维护
- **WHEN** 旧版本产品使用文档需要 broken links、Mintlify 配置迁移、frontmatter 补齐、manifest 补齐、格式修复、导航引用修复、敏感信息移除或目录结构迁移
- **THEN** 自动化 MAY 执行维护。
- **AND** 维护 SHALL 不改变原产品含义。
- **AND** 维护 SHALL 记录变更范围或维护说明。

#### Scenario: 内容性更正需要留痕
- **WHEN** 旧版本产品使用文档执行内容性更正
- **THEN** 流程 SHALL 记录更正原因、操作者或确认来源、时间、文件范围和变更说明。

### Requirement: 产品使用文档浏览入口边界
产品版本发布管理能力 SHALL 文档化公开产品使用文档通过 `域名/docs` 浏览的部署边界，并 SHALL 将公开产品文档与内部敏感文档分离。

#### Scenario: 记录 docs 子路径部署边界
- **WHEN** 项目声明产品使用文档通过 `域名/docs` 访问
- **THEN** 项目文档 SHALL 记录该访问方式由 Mintlify base path、Cloudflare/Vercel/CDN rewrite、Nginx 反向代理或等价方案承载。
- **AND** 若部署方式尚未确认，发布准备流程 SHALL 记录 blocker 或待确认项。

#### Scenario: 公开文档与内部文档分离
- **WHEN** 产品使用文档面向公开读者发布
- **THEN** 文档 SHALL 只包含公开产品使用说明、功能入口、操作注意事项和版本差异。
- **AND** 内部运维、API、数据库、对象存储凭据、生产私有域名或敏感配置 SHALL NOT 混入公开产品使用文档。

### Requirement: Mintlify 多版本文档站源目录
产品版本发布管理能力 SHALL 定义 `mintlify/` 作为公开 Mintlify 文档站源目录，并 SHALL 将 release 使用文档快照同步或投影到站点目录。

#### Scenario: 定义 Mintlify 站点源目录
- **WHEN** 项目启用多版本产品文档站
- **THEN** 项目 SHALL 使用受治理的 `mintlify/` 目录存放 Mintlify 配置、站点页面、公告投影和公开站点资产
- **AND** `mintlify/` SHALL 与 `releases/`、`docs/`、`issues/`、`iterations/` 和 `openspec/` 的职责边界在目录规则和发布文档中说明
- **AND** `mintlify/` SHALL NOT 存放运行时构建产物、真实客户数据、密钥、数据库连接串、Authorization header、Cookie、生产私有域名或不可公开运维信息。

#### Scenario: 从 release 快照投影到站点目录
- **WHEN** 某版本 `usage_docs.status` 为 `generated`
- **THEN** 系统 SHALL 能够将 `releases/<version>/usage-docs/**` 同步或投影到 `mintlify/docs/<version>/**`
- **AND** 目标页面 SHALL 能追溯到来源 `releases/<version>/usage-docs/manifest.json`
- **AND** 同步流程 SHALL NOT 绕过 release 快照直接把 `mintlify/` 作为唯一事实源。

### Requirement: Mintlify 多版本导航和 latest 指针
产品版本发布管理能力 SHALL 为公开文档站维护多版本导航，并 SHALL 定义 `latest` 指针规则。

#### Scenario: 文档站导航包含多版本入口
- **WHEN** Mintlify 站点配置生成或校验
- **THEN** 导航 SHALL 包含产品发布公告、当前版本产品使用文档、历史版本产品使用文档和 `latest` 入口
- **AND** 缺少 usage docs 的历史版本 SHALL 只展示公告或明确说明该版本未生成产品使用文档
- **AND** 站点路径 SHALL 避免版本歧义，例如 `docs/vX.Y.Z/overview`、`docs/latest/overview` 和 `releases/vX.Y.Z/announcement`。

#### Scenario: latest 指向可用文档版本
- **WHEN** 发布或同步某个产品版本
- **THEN** `latest` SHALL 指向最新已发布且 usage docs 站点校验通过的版本
- **AND** 当最新版本明确跳过 usage docs 时，`latest` SHALL 保持最近一个可用产品文档版本或展示当前版本文档不可用说明。

### Requirement: 共享截图资产治理
产品版本发布管理能力 SHALL 支持在 `mintlify/assets/screenshots/` 中按内容 hash 集中管理系统截图，并 SHALL 在 manifest 中记录复用依据。

#### Scenario: release manifest 记录截图引用
- **WHEN** 生成或校验某版本产品使用文档
- **THEN** `usage-docs/manifest.json` SHALL 记录截图引用、截图 hash、截图来源、覆盖页面、站点目标路径和同步时间
- **AND** `releases/<version>/usage-docs/` SHALL NOT 默认存放大体积系统截图文件
- **AND** 若确需在 release 快照内保留截图文件，manifest SHALL 记录保留原因、文件大小、来源、hash 和迁移或清理策略。

#### Scenario: 共享截图按 hash 复用
- **WHEN** 多个版本引用同一系统截图资产
- **THEN** 该截图 SHALL 位于 `mintlify/assets/screenshots/` 或等价公开站点资产目录
- **AND** manifest SHALL 记录 `content_hash`、`first_used_in`、`used_by_versions`、`covered_pages`、`source_type` 和 `reuse_reason`
- **AND** 当界面、字段、操作入口、数据状态或权限边界发生影响用户理解的变化时，系统 SHALL 要求新增截图或记录明确豁免，不得静默复用旧截图。

### Requirement: Mintlify 站点发布门禁
产品版本发布管理能力 SHALL 在发布准备和发布确认阶段校验 Mintlify 站点源目录、站点导航、共享截图和公开安全。

#### Scenario: 发布准备校验站点目录
- **WHEN** `/release-prepare <version>` 处理 `usage_docs.status=generated` 的版本
- **THEN** 发布准备流程 SHALL 校验 release usage docs 快照与 `mintlify/docs/<version>/**` 的页面清单一致
- **AND** SHALL 校验 `mintlify/mint.json` 或等价配置包含该版本公告和产品文档入口
- **AND** SHALL 校验共享截图引用、截图 hash、broken links 或等价静态构建结果
- **AND** 失败时 SHALL 记录 blocker 或阻断发布确认。

#### Scenario: 公开安全覆盖 Mintlify 目录
- **WHEN** 校验产品使用文档、manifest、Mintlify 配置或 `mintlify/` 站点源文件
- **THEN** 校验 SHALL 拒绝密钥、真实 `.env` 内容、数据库连接串、Authorization header、Cookie、对象存储凭据、非公开运维地址、本地绝对路径或真实客户数据。

