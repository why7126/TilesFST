---
requirement_id: REQ-0100-mintlify-docs-site-ia-content-experience
title: Mintlify 文档站信息架构与内容体验优化 - 验收标准
acceptance_status: passed
created_at: 2026-08-05 10:03:45
updated_at: 2026-08-06 08:23:35
owner: product
---

# 验收标准

## 功能 AC

- [ ] AC-001：Mintlify 文档站必须提供首页或等价首页入口，展示产品定位、当前版本、角色入口、常用任务和最近发布公告。
- [ ] AC-002：首页或入口页中的卡片、按钮和链接必须全部指向真实存在页面，不得保留空链接、模板链接或参考项目外链。
- [ ] AC-003：`latest` 当前版本导航必须完整挂载当前版本 usage docs manifest 中已有的 overview、admin、miniapp、public 和 faq 页面。
- [ ] AC-004：导航必须按“开始 / 当前版本 / 历史版本 / 发布公告”或等价结构组织，并在当前版本下按管理端、小程序、公开浏览和常见问题分组。
- [ ] AC-005：导航文案必须面向客户、店主、企业员工、实施和客服理解，不得暴露 OpenSpec、Sprint、未评审 Issue 或内部研发流程。
- [ ] AC-006：版本化页面必须说明当前页面对应 `latest`、具体版本或历史版本，并能追溯到实际产品版本。
- [ ] AC-007：缺少 usage docs 的历史版本不得生成空目录或空页面；站点必须只展示公告或明确说明该版本暂未生成产品使用文档。
- [ ] AC-008：页面表达可以使用 Mintlify MDX 组件增强扫描效率，但每个 Card、Accordion、Steps 或提示块必须服务于真实产品说明。
- [ ] AC-009：FAQ 必须按用户问题或场景分组，避免只有长段落堆叠。
- [ ] AC-010：截图引用必须使用 `mintlify/assets/screenshots/` 下的共享公开资产，并能通过 release manifest 或 site manifest 追溯来源。
- [ ] AC-011：不得照搬 ProjectDocs/promptt 或 Dify Docs 的品牌、外部域名、analytics、AI 平台产品线、多语言体系或 API 示例内容。
- [ ] AC-012：站点配置若从 `mint.json` 升级到 `docs.json`，必须明确迁移方式、兼容性和唯一主配置；不得让两份主配置互相冲突。
- [ ] AC-013：`mintlify/README.md` 或等价治理说明必须记录 release 快照与站点投影关系、`latest` 更新规则、历史版本冻结规则、截图资产规则和敏感信息边界。
- [ ] AC-014：`mintlify/site-manifest.json` 或等价文件必须记录站点投影来源、当前 latest 版本、页面 hash 或等价一致性证据、人工覆盖和截图资产引用。
- [ ] AC-015：实现后必须提供或更新校验，能发现导航缺页、broken links、图片引用错误、`latest` 指针漂移和 site manifest 漂移。
- [ ] AC-016：实现后必须清理或阻断 `.DS_Store`、构建产物、`node_modules/`、`.mintlify/`、`dist/`、`build/` 等进入公开文档站源目录。
- [ ] AC-017：站点优化不得绕过 `releases/vX.Y.Z/usage-docs/manifest.json` 直接改写历史版本产品语义。
- [ ] AC-018：历史版本内容性更正必须记录授权来源、原因、时间和文件范围；非内容性维护必须不改变产品行为说明。

## 非功能 AC

- [ ] AC-NF-001：公开文档不得包含真实客户数据、真实账号密码、密钥、Cookie、Authorization header、数据库连接串、对象存储凭据、生产私有域名或本地绝对路径。
- [ ] AC-NF-002：页面内容中文优先；路径、命令、版本号、Mintlify 专名和必要技术名词可保留英文。
- [ ] AC-NF-003：站点首页和导航应优先提升查找效率，避免大量装饰内容、模板占位文案或无业务含义的图片。
- [ ] AC-NF-004：校验输出必须摘要化，包含 pass、warning、blocker、涉及路径和建议修复方向，不输出完整大文件或敏感内容。
- [ ] AC-NF-005：本需求不应引入 API、数据库、Web 管理端、小程序或 Docker Compose 默认启动链路变更；若后续设计确认需要，应在 OpenSpec Change 中单独说明影响和验证。

## 横切 AC（knowledge-base）

本 REQ 为 Mintlify 文档站信息架构与内容体验优化，不涉及管理端 CRUD 列表、管理端表单页、管理端弹窗或媒体上传 UI 场景；Knowledge-base UI 横切标签为 N/A，本节不新增 AC-XCUT。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-06 08:23:35
accepted_by: workflow-sync
source_change: improve-mintlify-docs-site
source_sprint: null
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

