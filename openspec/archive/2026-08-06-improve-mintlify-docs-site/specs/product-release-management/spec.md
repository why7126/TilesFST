## MODIFIED Requirements

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
- **AND** Mintlify 运行缓存 SHALL 写入 Docker named volume 或容器内部路径，不得挂载或写入宿主机 `~/.mintlify*`
- **AND** Compose config 校验 SHALL 覆盖根、local 和 prod docs-site 入口。

#### Scenario: 参考项目内容裁剪
- **WHEN** 根据外部或本地参考文档站优化 Mintlify 页面
- **THEN** 实现 SHALL 只吸收适合瓷砖信息管理平台的首页、角色入口、用户指南、快速开始、FAQ、更新公告、分层导航和写作治理模式
- **AND** 实现 SHALL NOT 照搬参考项目品牌、logo、外部域名、analytics ID、多语言体系、AI 平台产品线或 API endpoint 示例
- **AND** 所有新增页面内容 SHALL 中文优先，并围绕瓷砖资料、品牌证书、SKU、媒体、小程序浏览和公开使用场景组织。

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
