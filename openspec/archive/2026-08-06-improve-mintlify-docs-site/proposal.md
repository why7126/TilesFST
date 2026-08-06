---
created_at: 2026-08-05 14:39:06
updated_at: 2026-08-05 14:39:06
source_requirement: REQ-0100-mintlify-docs-site-ia-content-experience
change_type: update
---

# 改进 Mintlify 文档站信息架构与内容体验

## 背景

项目已通过 REQ-0088 建立版本化产品使用文档生成与发布治理，并通过 REQ-0094 建立 `mintlify/` 公开文档站源目录、多版本投影、`latest` 指针、公告投影和共享截图资产治理。当前 `mintlify/` 已具备基本目录和版本文档，但站点呈现仍偏“版本快照目录”，首页入口、角色路径、当前版本导航和页面表达都较薄。

用户明确反馈当前 Mintlify 文档站“太简陋了”，并要求参照 `/Users/why7126/CodeSpaces/Projects/ProjectDocs/promptt` 与 `langgenius/dify-docs` 的文档站组织方式进行优化。探索结论是：参考价值主要在完整信息架构、首页卡片、分层导航、站点级配置和写作治理，不是照搬 AI 平台、多语言、多产品线或 API 示例内容。

## 变更范围

- 优化 Mintlify 文档站首页或等价首页入口，使其具备产品定位、角色入口、常用任务、当前版本和发布公告入口。
- 完整挂载 `latest` 当前版本已有 usage docs 页面，覆盖管理端、小程序、公开浏览和 FAQ。
- 将站点导航从扁平版本列表升级为“开始 / 当前版本 / 历史版本 / 发布公告”的用户可理解结构。
- 为版本化页面补充 `latest`、具体版本和历史版本上下文，避免误读历史页面为最新能力。
- 使用 Mintlify MDX 组件增强页面扫描效率，但所有卡片、按钮和图片必须服务于真实产品说明。
- 明确参考项目裁剪原则，禁止照搬参考项目品牌、外部域名、analytics、多语言体系、AI 平台产品线或 API 示例。
- 补充 `mintlify/README.md` 或等价治理说明，记录 release 快照与站点投影关系、`latest` 更新、历史版本冻结、截图资产和公开安全边界。
- 增加或更新校验，覆盖导航缺页、broken links、图片引用、`latest` 指针漂移、site manifest 漂移、`.DS_Store` 和公开安全。

## 不包含

- 不新增后端 API、数据库表、Web 管理端功能、小程序功能或权限模型。
- 不实现真实 Mintlify 账号、域名、DNS、CDN、Vercel、Cloudflare 或生产托管配置。
- 不把内部技术文档、OpenSpec、Issue、Sprint、真实运维配置或敏感信息公开到 Mintlify。
- 不要求一次性补齐所有历史版本的完整 usage docs。
- 不自动重写历史版本产品行为说明、操作步骤、功能可用性或已知问题。
- 不改变 `releases/vX.Y.Z/usage-docs/manifest.json` 作为版本使用文档事实源的边界。

## 影响分析

```yaml
impact:
  backend: false
  web: false
  miniapp: false
  admin: false
  database: false
  storage: false
  api: false
  docs_site: true
  release_governance: true
  tests: true
capabilities:
  new: []
  modified:
    - product-release-management
```

## 风险与缓解

| 风险 | 缓解 |
|---|---|
| `mintlify/` 反向成为产品文档事实源 | design 和 spec 明确 release usage docs manifest 仍是事实源，站点只做公开投影和体验层。 |
| 参考项目结构被照搬 | 设计中列出可借鉴项与不可照搬项，验收阻断外部品牌、域名、analytics 和无关产品线。 |
| 历史版本语义被误改 | 校验要求历史版本内容性更正必须记录授权来源、原因、时间和文件范围。 |
| 首页或卡片出现空链接 | 校验必须发现导航缺页、空链接和 broken links。 |
| 公开文档泄露敏感信息 | 校验继续拒绝密钥、真实客户数据、Authorization header、Cookie、生产私有域名、本地绝对路径等。 |

## 后续流程

本 Change 来源于已评审需求 `REQ-0100-mintlify-docs-site-ia-content-experience`。作为 REQ 来源 Change，执行 `/opsx-apply` 前必须先纳入某个 `sprint-xxx` 正式范围。
