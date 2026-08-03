## ADDED Requirements

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
产品使用文档能力 SHALL 使用 manifest 记录版本化文档的来源、页面、覆盖和维护策略。

#### Scenario: Manifest 记录生成事实
- **WHEN** 生成某个版本的产品使用文档
- **THEN** `usage-docs/manifest.json` SHALL 记录产品版本、生成时间、来源版本、来源 release、输入文件、页面清单、覆盖摘要、人工覆盖记录和自动化维护策略。
- **AND** 所有项目新增时间字段 SHALL 使用 `YYYY-MM-DD HH:mm:ss`。

#### Scenario: Manifest 支持覆盖校验
- **WHEN** 校验某个版本的产品使用文档
- **THEN** 校验流程 SHALL 使用 manifest 判断页面清单与实际文件是否一致。
- **AND** 校验流程 SHALL 判断管理端菜单、小程序主要页面和发布影响范围是否有文档覆盖或明确豁免。

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
