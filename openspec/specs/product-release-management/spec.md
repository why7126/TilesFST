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

#### Scenario: 自动选择前一个已生成 usage docs 版本
- **WHEN** 用户确认某个版本需要生成产品使用文档
- **AND** 发布对象未显式指定 `usage_docs.source_version`
- **AND** 历史 release 中存在一个或多个已生成 `usage-docs/manifest.json` 的版本
- **THEN** 流程 SHALL 按 SemVer 语义解析候选版本并选择小于当前目标版本的最近版本作为 `source_version`
- **AND** 流程 SHALL 排除当前目标版本自身
- **AND** 若相邻上一版本未生成 usage docs，流程 SHALL 继续向更早的已生成 usage docs 版本查找
- **AND** 流程 SHALL NOT 使用字符串字典序作为版本先后判断依据。

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
产品版本发布管理能力 SHALL 定义 `mintlify/` 作为公开 Mintlify 文档站源目录，并 SHALL 将 release 使用文档快照同步或投影到站点目录，同时 SHALL 文档化文档站维护规则。

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

#### Scenario: 站点维护规则已文档化
- **WHEN** 项目维护 `mintlify/` 文档站
- **THEN** `mintlify/README.md` 或等价治理文档 SHALL 说明 release 快照与站点投影关系、`latest` 更新规则、历史版本冻结规则、截图资产规则、页面新增同步要求和敏感信息边界
- **AND** `mintlify/site-manifest.json` 或等价文件 SHALL 记录站点投影来源、当前 `latest` 版本、页面 hash 或等价一致性证据、人工覆盖和截图资产引用。

### Requirement: Mintlify 多版本导航和 latest 指针
产品版本发布管理能力 SHALL 为公开文档站维护面向用户的多版本导航，并 SHALL 定义 `latest` 指针规则。

#### Scenario: 文档站导航包含多版本入口
- **WHEN** Mintlify 站点配置生成或校验
- **THEN** 导航 SHALL 包含产品发布公告、当前版本产品使用文档、历史版本产品使用文档和 `latest` 入口
- **AND** 缺少 usage docs 的历史版本 SHALL 只展示公告或明确说明该版本未生成产品使用文档
- **AND** 站点路径 SHALL 避免版本歧义，例如 `docs/vX.Y.Z/overview`、`docs/latest/overview` 和 `releases/vX.Y.Z/announcement`。

#### Scenario: latest 指向可用文档版本
- **WHEN** 发布或同步某个产品版本
- **THEN** `latest` SHALL 指向最新已发布且 usage docs 站点校验通过的版本
- **AND** 当最新版本明确跳过 usage docs 时，`latest` SHALL 保持最近一个可用产品文档版本或展示当前版本文档不可用说明。

#### Scenario: 当前版本导航完整呈现产品使用文档
- **WHEN** `latest` 指向某个已生成 usage docs 的版本
- **THEN** Mintlify 当前版本导航 SHALL 完整呈现该版本 manifest 中已有的 overview、admin、miniapp、public 和 faq 页面
- **AND** 导航 SHALL 按管理端、小程序、公开浏览和常见问题等用户场景分组
- **AND** 若 manifest 中存在页面但 Mintlify 导航未引用，校验 SHALL 报告导航缺页。

#### Scenario: 文档站具备首页或等价开始入口
- **WHEN** 用户打开 Mintlify 文档站
- **THEN** 站点 SHALL 提供首页或等价开始入口，说明产品定位、当前版本、角色入口、常用任务和最近发布公告
- **AND** 首页卡片、按钮和链接 SHALL 指向真实存在页面
- **AND** 首页 SHALL NOT 暴露 OpenSpec、Sprint、未评审 Issue、内部研发流程、真实客户数据、密钥或不可公开运维信息。

#### Scenario: 版本化页面展示版本上下文
- **WHEN** 用户浏览 `docs/latest/*`、`docs/vX.Y.Z/*` 或 `releases/vX.Y.Z/*`
- **THEN** 页面 SHALL 让用户能识别当前页面对应 `latest`、具体产品版本或历史发布公告
- **AND** 历史版本内容 SHALL 避免被误读为最新产品能力
- **AND** 缺少 usage docs 的版本 SHALL 展示文档未生成或仅公告可用的说明。

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
产品版本发布管理能力 SHALL 在发布准备和发布确认阶段校验 Mintlify 站点源目录、站点导航、共享截图、页面表达和公开安全。

#### Scenario: 发布准备校验站点目录
- **WHEN** `/release-prepare <version>` 处理 `usage_docs.status=generated` 的版本
- **THEN** 发布准备流程 SHALL 校验 release usage docs 快照与 `mintlify/docs/<version>/**` 的页面清单一致
- **AND** SHALL 校验 `mintlify/docs.json` 或等价唯一主配置包含该版本公告、产品文档入口、站点 theme、metadata、版本、tabs 和 groups
- **AND** SHALL 校验共享截图引用、截图 hash、broken links 或等价静态构建结果
- **AND** 失败时 SHALL 记录 blocker 或阻断发布确认。

#### Scenario: 公开安全覆盖 Mintlify 目录
- **WHEN** 校验产品使用文档、manifest、Mintlify 配置或 `mintlify/` 站点源文件
- **THEN** 校验 SHALL 拒绝密钥、真实 `.env` 内容、数据库连接串、Authorization header、Cookie、对象存储凭据、非公开运维地址、本地绝对路径或真实客户数据。

#### Scenario: 站点配置和链接质量校验
- **WHEN** 校验 Mintlify 文档站体验
- **THEN** 校验 SHALL 发现导航引用缺页、首页卡片空链接、站内 broken links、图片引用错误、`latest` 指针漂移和 site manifest 漂移
- **AND** 校验 SHALL 阻断 `.DS_Store`、构建产物、`node_modules/`、`.mintlify/`、`dist/`、`build/` 等进入公开文档站源目录
- **AND** 校验输出 SHALL 摘要化展示 pass、warning、blocker、涉及路径和建议修复方向。

#### Scenario: 本地 docs-site 镜像预览 Mintlify 文档站
- **WHEN** Docker Compose 启用 `docs-site` profile
- **THEN** docs-site 服务 SHALL 使用项目内 Dockerfile 构建本地可复用镜像并预装 Mintlify CLI
- **AND** 服务 SHALL 运行 Mintlify dev preview，而不是目录索引或仅返回 MDX 原文的静态文件服务器
- **AND** Mintlify 运行缓存 SHALL 写入容器内部路径或 CLI 自行管理的临时目录，不得挂载或写入宿主机 `~/.mintlify*`
- **AND** docs-site 服务 SHALL NOT 将 Docker named volume 直接挂载到 `/home/node/.mintlify`
- **AND** Compose config 校验 SHALL 覆盖根、local 和 prod docs-site 入口。

### Requirement: 小程序发布前 Network checklist
产品版本发布管理能力 SHALL 在小程序发布准备流程中纳入 DevTools Network 与体验版 Network 人工检查清单，确保发布确认前能区分自动门禁、真实小程序网络链路验证、阻塞项和 follow-up 风险。

#### Scenario: miniapp prepare 输出 Network checklist
- **WHEN** `/miniapp-prepare` 或等价小程序发布准备命令完成自动门禁
- **THEN** 输出 SHALL 区分 prod 策略、`urlCheck=true`、静态测试和生产接口 smoke 等自动门禁
- **AND** 输出 SHALL 包含 DevTools Network 人工检查项
- **AND** 输出 SHALL 包含体验版 Network 人工检查项
- **AND** 输出 SHALL 指向 `/miniapp-confirm` 或等价确认流程记录验证结论
- **AND** 输出 SHALL NOT 将未执行的人工 Network checklist 标记为自动通过。

#### Scenario: Network checklist 覆盖关键页面和资源
- **WHEN** 发布负责人执行小程序 Network checklist
- **THEN** checklist SHALL 至少覆盖首页、一个列表页、一个详情或媒体资源页面
- **AND** 首页检查 SHALL 覆盖首页聚合接口、Banner、推荐商品、静态资源和错误态
- **AND** 列表页检查 SHALL 覆盖列表接口、分页请求、空态和网络失败提示
- **AND** 详情或媒体资源页面检查 SHALL 覆盖图片、视频、证书图片或受控媒体 URL 的加载结论。

#### Scenario: Network 失败阻断发布准备通过
- **WHEN** DevTools 或体验版实际请求仍指向本地或非预期环境
- **THEN** 发布准备 SHALL 标记 failed 或 blocker
- **AND** 关键 API 返回非 2xx HTTP 状态且页面无可接受降级时 SHALL 标记 failed
- **AND** 关键业务响应失败且影响首页、列表或详情主路径时 SHALL 标记 failed
- **AND** 图片、视频或证书资源域名不合法并导致核心内容不可用时 SHALL 标记 failed 或 blocked。

#### Scenario: miniapp confirm 承接 Network evidence
- **WHEN** `/miniapp-confirm` 或等价确认流程记录小程序体验版或正式版验证结果
- **THEN** 记录 SHALL 支持表达 DevTools Network 结论、体验版 Network 结论、失败项、阻塞项、剩余风险和下一步
- **AND** 缺少体验版 Network evidence 时 SHALL 记录 `blocked`、`follow_up` 或明确的 `not_applicable` 原因
- **AND** 记录 SHALL NOT 包含 token、Cookie、Authorization header、`.env`、真实密钥、真实客户数据或未脱敏隐私。

### Requirement: 产品发布必须关联升级路径支持级别
产品版本发布管理能力 SHALL 在发布准备或发布确认阶段引用目标版本的部署升级支持级别和回滚证据。

#### Scenario: 发布准备默认输出首次部署和相邻升级状态
- **WHEN** release preparation evaluates a target version
- **THEN** the release object SHALL record or reference fresh install and adjacent upgrade support levels
- **AND** missing upgrade plan evidence SHALL be reported as blocker, warning, manual review, or not applicable with rationale.

#### Scenario: 跨版本升级按需生成
- **WHEN** no user explicitly requested a cross-version upgrade path for the target version
- **THEN** release preparation SHALL NOT require or generate cross-version upgrade plans by default
- **AND** users MAY generate one manually with `/upgrade-plan --from <old-version> --to <target-version>`.

#### Scenario: 发布确认不夸大跨版本支持
- **WHEN** a release lacks complete cross-version rehearsal and rollback evidence
- **THEN** release publish SHALL NOT describe cross-version upgrade as supported
- **AND** public release material SHALL use manual review or unsupported wording.

### Requirement: 发布目标环境分离
产品版本发布管理 SHALL 区分开发环境发布确认与生产发布确认，并根据目标环境选择发布门禁。

#### Scenario: 开发环境发布确认不受生产证据阻断
- **WHEN** 发布对象声明 `release_target.environment=development`
- **THEN** 发布确认 SHALL 表示开发环境部署或开发交付确认
- **AND** 生产真实 env、生产 MySQL 或对象存储备份、生产公开 API、生产 no-fallback 媒体证据和生产 smoke SHALL NOT 阻断该开发环境发布确认
- **AND** 这些生产事项 SHALL 作为后续生产发布待办、known issue 或 production release blocker 记录。

#### Scenario: 生产发布确认使用生产门禁
- **WHEN** 发布对象声明 `release_target.environment=production`
- **THEN** 发布确认 SHALL 要求生产部署相关证据
- **AND** 生产 env 显式版本、生产备份、生产 smoke、生产公开 API 和生产媒体证据 SHALL 按发布范围参与门禁或记录明确不适用理由。

#### Scenario: 发布对象记录目标环境
- **WHEN** 创建或更新发布对象
- **THEN** 发布对象 SHOULD 包含 `release_target.environment`、`release_target.deployment_scope`、`release_target.production_release_required` 和 `release_target.rationale`
- **AND** `environment` 与 `deployment_scope` SHALL 使用 `development` 或 `production`。

### Requirement: 发布状态决策面板
产品版本发布管理 SHALL 提供只读发布状态决策面板，用于汇总 release、image、upgrade 和 publish 当前状态，并向操作者输出可执行的下一步。

#### Scenario: 状态面板区分决策与证据
- **WHEN** 操作者查看某个版本的发布状态
- **THEN** 状态面板 SHALL 分别列出需要用户选择的决策项、需要命令或人工补齐的证据项，以及不阻断当前目标的后续事项
- **AND** 每个阻塞项 SHALL 标明分类、影响阶段、阻塞目标、当前证据、建议动作和复核命令。

#### Scenario: 开发发布显示生产后续但不阻断
- **WHEN** 发布对象声明 `release_target.environment=development`
- **THEN** 状态面板 SHALL 将生产 env、生产备份、生产 no-fallback、公开 API 和生产 smoke 缺口归类为 `production_only_pending`
- **AND** 这些缺口 SHALL NOT 作为开发发布的阻塞项。

#### Scenario: 状态面板输出唯一下一步
- **WHEN** 状态面板能够推导出下一条安全动作
- **THEN** 输出 SHALL 提供一条可复制的下一步命令
- **AND** 若仍存在需要用户选择、补证或人工确认的事项，输出 SHALL 将其放入待用户处理区域而不是混入下一步命令。

### Requirement: 发布阻塞分类契约
产品版本发布管理 SHALL 使用统一阻塞分类表达 release、image、upgrade 和 publish 中的决策、证据、环境、范围和安全问题。

#### Scenario: 阻塞分类字段完整
- **WHEN** 发布命令、状态面板或 validator 报告发布阻塞项
- **THEN** 阻塞项 SHALL 使用 `decision_missing`、`prepare_evidence_missing`、`publish_evidence_missing`、`production_only_pending`、`input_drift`、`environment_unavailable`、`scope_incomplete`、`public_safety` 或 `schema_invalid` 等分类
- **AND** 阻塞项 SHOULD 包含 phase、blocks_target、owner、current_evidence、safe_remediation 和 rerun_check。

#### Scenario: 发布确认阶段不再重新发现普通下一步
- **WHEN** 发布状态面板已报告某版本未达到 publish ready
- **THEN** `/release-publish` SHOULD 只确认已就绪发布或报告状态面板已暴露的阻塞项
- **AND** 普通缺失的 image manifest、默认 upgrade plan 或用户决策 SHOULD 在 `/release-status` 或 `/release-prepare` 阶段提前暴露。

### Requirement: 生产证据后置承接

产品发布管理 SHALL 承接开发阶段留下的 `production_only_pending` 证据缺口，并在生产发布时重新判定阻塞状态。

#### Scenario: 开发阶段遗留生产待办
- **WHEN** REQ、BUG、Change 或 Sprint 验收记录存在 `production_only_pending`
- **THEN** 开发环境发布或开发归档 SHALL 可继续完成
- **AND** 发布状态面板 SHALL 将这些事项显示为生产发布待办或后续生产确认项
- **AND** SHALL NOT 将其混入开发阶段失败项。

#### Scenario: 生产发布重新收紧门禁
- **WHEN** 发布对象声明 `release_target.environment=production`
- **THEN** 生产证据待办 SHALL 重新按发布范围归类为 `publish_evidence_missing`、`environment_unavailable`、`schema_invalid` 或明确 N/A
- **AND** 缺少生产 env、备份、公开 API、生产 no-fallback 媒体、生产 smoke 或回滚准备证据时 SHALL 阻塞生产发布，除非该项对本次发布范围不适用。

### Requirement: 生产发布环境证据强门禁

发布状态与发布确认 SHALL 在生产目标下强制重新判定开发阶段遗留的 `production_only_pending`，不得让开发证据自动升级为生产发布证据。

#### Scenario: Development target 保留生产后置项
- **WHEN** release status 或 release validation 的目标为 `development`
- **THEN** 环境证据脚本发现 `production_only_pending` SHALL 作为 production follow-up 或非阻塞项输出
- **AND** 仅当文本把开发证据写作生产通过、体验版通过或真机通过时才作为 blocker。

#### Scenario: Production target 阻断未重判的后置项
- **WHEN** release status 或 release publish 的目标为 `production`
- **THEN** 仍残留的 `production_only_pending` SHALL 被视为未重新判定的生产证据缺口
- **AND** validation SHALL 将其归类为 `publish_evidence_missing` 或 `environment_unavailable`
- **AND** 发布确认 SHALL 阻断，直到该项被生产 evidence、明确 N/A 或具体 blocker 替代。

### Requirement: 产品版本号发布强门禁

发布准备与发布确认 SHALL 强制校验用户可见产品版本号与目标发布版本一致，不得通过说明性 rationale 放行版本漂移。

#### Scenario: Release prepare blocks product version mismatch
- **WHEN** release prepare validation runs for `<version>`
- **AND** `src/shared/product-version.ts`, `src/miniapp/utils/product-version.ts`, or `src/miniapp/utils/product-version.js` exists with `PRODUCT_VERSION` different from `<version>`
- **THEN** validation SHALL fail before marking prepare complete
- **AND** the failure SHALL identify the mismatched file and expected version.

#### Scenario: Release publish blocks user-visible version mismatch
- **WHEN** release publish validation runs for `<version>`
- **AND** any user-visible `PRODUCT_VERSION` source differs from `<version>`
- **THEN** publish SHALL be blocked even if `version_change_rationale` is present
- **AND** the release MUST NOT be marked published until the version sources are aligned.

#### Scenario: Version source change invalidates image evidence
- **WHEN** a product version source is changed after image prepare or image build evidence exists
- **THEN** the operator SHALL rerun `/image-prepare <version>` and `/image-build <version>` before publishing
- **AND** release status or validation SHALL present those commands as the safe remediation path.

