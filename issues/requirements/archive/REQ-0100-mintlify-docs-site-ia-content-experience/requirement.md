---
requirement_id: REQ-0100-mintlify-docs-site-ia-content-experience
title: Mintlify 文档站信息架构与内容体验优化
terminal: multi
version: v1
status: done
owner: product
source: capture.md
priority: P1
parent_requirement: REQ-0094-mintlify-versioned-docs-directory
created_at: 2026-08-05 10:00:41
updated_at: 2026-08-06 08:17:58
---

# REQ-0100 Mintlify 文档站信息架构与内容体验优化

## 1. 需求背景

项目已通过 REQ-0088 建立版本化产品使用文档生成与发布治理，并通过 REQ-0094 建立 `mintlify/` 文档站源目录、多版本投影、`latest` 指针、公告投影和共享截图资产治理。当前 `mintlify/` 已包含 `docs/v0.3.3/`、`docs/v0.3.4/`、`docs/latest/`、发布公告与截图资产，但站点呈现仍偏“发布快照目录”，没有形成对用户友好的产品文档站入口。

用户反馈当前 Mintlify 文档站“太简陋了”，并要求参照 `/Users/why7126/CodeSpaces/Projects/ProjectDocs/promptt` 与 `langgenius/dify-docs` 的文档站组织方式进行优化。探索结论表明，参考项目的价值不在于照搬大量页面，而在于完整的信息架构、首页入口、分层导航、角色化路径、站点级配置和写作治理。

本需求用于在现有版本化文档治理基础上，把 Mintlify 从“可浏览的版本快照”升级为“可面向客户、店主、企业员工和实施团队使用的产品文档站”。后续实现必须继续遵守 release 快照事实源边界：`releases/vX.Y.Z/usage-docs/` 保持版本文档事实源，`mintlify/docs/**` 作为公开站点投影和体验层，不得绕过 release 快照直接改写历史版本产品语义。

## 2. 目标用户

| 角色 | 诉求 |
|---|---|
| 店主 / 导购 / 公开访客 | 快速找到小程序浏览、搜索、商品详情、品牌证书和收藏等操作说明。 |
| 企业内部员工 | 快速找到管理端资料维护、品牌证书、Banner、SKU、媒体上传等操作说明。 |
| 系统管理员 | 快速找到账号、日志审计、系统设置、接口文档入口和权限边界说明。 |
| 实施 / 培训 / 客服 | 用清晰的首页、导航和版本入口向客户交付当前版本使用说明。 |
| 产品负责人 | 通过文档站展示产品能力、版本差异和常见问题，减少“文档有但用户找不到”的问题。 |
| 开发 / 测试 / AI Agent | 在不破坏发布快照治理的前提下维护 Mintlify 页面、导航、链接和公开安全边界。 |

## 3. 范围

### 3.1 本期包含

- 优化 Mintlify 文档站首页，使首屏具备产品定位、主要用户角色入口和常用任务入口。
- 优化 `latest` 导航，完整呈现当前版本已有的管理端、小程序、公开浏览、FAQ 和发布公告页面。
- 参照 Dify Docs 的分层导航思想，建立适合瓷砖平台的“角色 + 场景 + 版本”信息架构。
- 参照 ProjectDocs/promptt 的首页卡片、功能模块入口和 FAQ 表达方式，增强页面可读性和可浏览性。
- 明确当前版本与历史版本的导航边界，避免用户误读历史版本页面为最新产品能力。
- 允许在 `mintlify/` 增加必要的首页、快速开始、导航聚合页、文档站 README 或写作规范文档。
- 使用已有共享截图资产强化关键页面表达，截图引用继续遵守 `mintlify/assets/screenshots/` 与 manifest 追溯规则。
- 校验 Mintlify 配置、页面路径、站内链接、图片引用和公开安全边界。
- 保持 `releases/vX.Y.Z/usage-docs/` 作为版本使用文档事实源，站点优化不得直接改写历史 release 语义。

### 3.2 本期不包含

- 不新增后端 API、数据库表、Web 管理端功能、小程序功能或权限模型。
- 不实现真实 Mintlify 账号、域名、DNS、CDN、Vercel、Cloudflare 或生产托管配置。
- 不把内部技术文档、OpenSpec、Issue、Sprint、真实运维配置或敏感信息公开到 Mintlify。
- 不要求一次性补齐所有历史版本的完整产品使用文档；缺少 usage docs 的版本可仅保留公告或不可用说明。
- 不自动重写历史版本产品行为说明、操作步骤、功能可用性或已知问题。
- 不把参考项目的 AI 平台、多语言、多产品线或 API 文档结构原样照搬到瓷砖平台。
- 不在本需求阶段直接创建 OpenSpec Change 或修改 `src/` 代码。

## 4. 功能要求

### FR-001 首页产品化入口

Mintlify 文档站 SHOULD 提供独立首页或等价首页入口，用于展示瓷砖信息管理平台的产品定位、适用角色和主要使用路径。

首页 SHOULD 至少包含：

| 区块 | 内容要求 |
|---|---|
| 产品概览 | 说明平台用于瓷砖资料展示、查询、维护和版本化交付文档浏览。 |
| 角色入口 | 面向企业员工、系统管理员、店主/导购、公开访客提供不同阅读路径。 |
| 常用任务 | 提供商品资料维护、品牌证书、媒体上传、小程序浏览、公开浏览、FAQ 等入口。 |
| 当前版本 | 明确当前 `latest` 指向的产品版本和可用文档范围。 |
| 发布公告 | 提供最近版本公告入口。 |

首页内容 MUST 使用公开产品表述，不得包含真实客户数据、密钥、内部数据库连接串、Authorization header、Cookie、生产私有运维域名或不可公开操作信息。

### FR-002 当前版本导航完整化

Mintlify 配置 MUST 让 `latest` 当前版本页面完整可达。

当前版本导航 SHOULD 至少包含：

- `docs/latest/overview`
- `docs/latest/admin/index`
- `docs/latest/admin/catalog`
- `docs/latest/admin/media`
- `docs/latest/admin/governance`
- `docs/latest/miniapp/index`
- `docs/latest/miniapp/browse`
- `docs/latest/miniapp/brand-certificate`
- `docs/latest/public/index`
- `docs/latest/faq`
- 最新发布公告入口

若某个页面在 `releases/<version>/usage-docs/manifest.json` 中存在，但未进入 Mintlify 导航，校验 SHOULD 报告导航缺页。

### FR-003 角色与场景分层导航

Mintlify 导航 SHOULD 从单纯版本列表升级为角色与场景分层结构。

推荐结构：

```text
开始
├── 产品简介
├── 快速开始
└── 当前版本总览

当前版本
├── 管理端
│   ├── 管理端使用说明
│   ├── 商品资料维护
│   ├── 品牌、证书、Banner 与媒体
│   └── 账号、设置、日志与接口文档
├── 小程序
│   ├── 小程序使用说明
│   ├── 浏览、搜索、商品与收藏
│   └── 品牌与证书
├── 公开浏览
└── 常见问题

历史版本
├── v0.3.4
└── v0.3.3

发布公告
├── v0.3.4
└── v0.3.3
```

导航命名 MUST 面向用户理解，不应暴露内部脚本、OpenSpec Change、Issue 编号或非公开研发流程。

### FR-004 版本上下文提示

版本化页面 MUST 让用户清楚知道当前阅读的是 `latest`、具体版本页面，还是历史版本页面。

页面 SHOULD 在总览或关键入口中说明：

- 当前页面对应的产品版本。
- `latest` 指向的实际版本。
- 历史版本内容默认冻结，仅允许非内容性维护和明确授权的内容更正。
- 当某版本缺少 usage docs 时，页面应展示“该版本暂未生成产品使用文档”或等价说明。

### FR-005 页面表达增强

Mintlify 页面 SHOULD 使用适合 Mintlify 的 MDX 组件增强可读性，例如 CardGroup、Card、Accordion、Steps、Info/Warning 类提示。

页面表达增强 MUST 满足：

- 卡片入口对应真实页面或真实任务，不创建空链接。
- FAQ 使用折叠或清晰分组，避免长段落堆叠。
- 截图用于解释真实产品页面、状态或操作，不使用无来源装饰图替代系统截图。
- 截图引用使用 `/assets/screenshots/<file>`，并能追溯到 release manifest 或 site manifest。
- 页面内容中文优先，路径、命令、版本号和 Mintlify 专名可保留英文。

### FR-006 参考项目裁剪原则

实现方案 SHOULD 参考 ProjectDocs/promptt 与 Dify Docs，但必须按瓷砖平台裁剪。

参考项 SHOULD 包括：

| 参考来源 | 可借鉴内容 |
|---|---|
| ProjectDocs/promptt | 首页图片/卡片、产品简介、用户指南、快速上手、FAQ、更新公告的组织方式。 |
| langgenius/dify-docs | 多层导航、产品/场景分组、站点级 metadata、footer、redirects、文档贡献和写作治理。 |

不应照搬：

- Dify 的 Cloud / Self-hosted / Developer Resources 多产品线结构。
- Dify 的多语言体系，除非后续明确需要英文文档。
- AI 平台、模型、工作流、API endpoint 示例等与瓷砖平台无关的内容。
- 参考项目中的外部域名、品牌、logo、analytics ID 或版权配置。

### FR-007 站点级配置优化

Mintlify 站点配置 SHOULD 补齐必要的站点级信息。

可评估配置包括：

- 站点名称、描述、主题颜色和 logo。
- 首页入口或 landing page。
- 顶部导航按钮，例如“查看当前版本”或“返回产品入口”。
- footer、社交链接或公开支持入口。
- redirects，用于兼容旧路径或从短路径跳转到 `latest`。
- broken link 检查和导航缺页检查。

若从 `mint.json` 升级到 `docs.json`，MUST 明确兼容性、迁移方式和校验命令；不得同时维护两份互相冲突的 Mintlify 主配置。

### FR-008 文档站治理说明

`mintlify/README.md` 或等价治理文档 SHOULD 说明文档站维护规则。

说明内容 SHOULD 包括：

- `releases/vX.Y.Z/usage-docs/` 与 `mintlify/docs/vX.Y.Z/` 的事实源关系。
- `latest` 更新规则。
- 历史版本内容冻结和允许的非内容性维护范围。
- 新增页面时需要同步的配置、manifest 和校验。
- 截图资产命名、复用和来源记录规则。
- 禁止公开敏感信息的边界。
- 本地预览或链接校验方式。

### FR-009 校验与质量门禁

实现后 SHOULD 提供或更新校验，覆盖以下内容：

- Mintlify 配置结构合法。
- 导航中引用的页面存在。
- `usage-docs/manifest.json` 页面清单与站点投影目录一致。
- `latest` 指向最新可用 usage docs 版本。
- 站内链接、公告链接和图片引用有效。
- 公开文档不包含密钥、真实客户数据、数据库连接串、Authorization header、Cookie、生产私有域名或不可公开运维信息。
- `.DS_Store`、构建产物、`node_modules/`、`.mintlify/`、`dist/`、`build/` 等不进入公开文档站源目录。

### FR-010 文档事实源边界

Mintlify 体验优化 MUST 不改变既有发布事实源职责。

实现时 MUST 保持：

- `releases/vX.Y.Z/release.json` 是版本发布事实源。
- `releases/vX.Y.Z/usage-docs/manifest.json` 是该版本使用文档事实源。
- `mintlify/site-manifest.json` 或等价文件记录站点投影、截图资产、同步状态和人工覆盖记录。
- `mintlify/docs/latest/` 是当前站点默认版本投影，不是独立产品事实源。
- 历史版本页面内容性更正必须有授权记录。

## 5. UI 与内容约束

- 文档站页面必须中文优先，面向产品使用者，不用研发内部黑话组织导航。
- 首页和入口页可以使用 Mintlify MDX 组件增强扫描效率，但不得用大量装饰内容替代真实产品说明。
- 页面应优先使用真实系统截图和已有共享截图资产。
- 文档站颜色、logo 和品牌表达应与瓷砖信息管理平台定位一致，避免照搬参考项目品牌。
- 站点页面中的按钮、卡片和链接必须指向真实存在页面。
- 所有公开页面不得出现真实客户数据、内部账号密码、密钥、Cookie、Authorization header、数据库连接串、生产私有域名或不可公开运维信息。

## 6. 关联需求

| 需求 | 关系 | 说明 |
|---|---|---|
| REQ-0088-versioned-product-usage-docs | 上游能力 | 已定义版本化产品使用文档生成、校验与发布治理。 |
| REQ-0094-mintlify-versioned-docs-directory | 父需求 | 已定义 `mintlify/` 站点源目录、多版本投影和截图资产治理。 |

## 7. 状态

```yaml
status: done
readiness: Ready
next: /req-opsx REQ-0100-mintlify-docs-site-ia-content-experience
expected_openspec_change: improve-mintlify-docs-site
```
