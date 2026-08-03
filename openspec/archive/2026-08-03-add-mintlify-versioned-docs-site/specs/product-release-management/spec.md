## ADDED Requirements

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

## MODIFIED Requirements

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
