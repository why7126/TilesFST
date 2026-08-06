---
req_id: REQ-0100-mintlify-docs-site-ia-content-experience
status: done
created_at: 2026-08-05 09:50:32
updated_at: 2026-08-06 08:17:58
recorded_by: product
source: 用户反馈 + 竞品参照
priority_hint: P1
parent_requirement: REQ-0094-mintlify-versioned-docs-directory
---

# 一句话

参照 ProjectDocs/promptt 与 langgenius/dify-docs 优化 Mintlify 公开文档站的信息架构、首页入口、导航层级和内容体验，避免当前站点显得简陋。

# 原始描述

用户反馈当前 Mintlify 文档站“太简陋了”，要求先参照 `/Users/why7126/CodeSpaces/Projects/ProjectDocs/promptt` 项目进行优化探索，随后补充参照 `https://github.com/langgenius/dify-docs` 仓库。

探索结论倾向：当前 `mintlify/` 已有版本化 usage docs、公告与截图资产，但站点导航与首页表达较薄；`latest` 入口未充分呈现已有管理端、小程序、公开浏览、FAQ 等页面。参考项目和 Dify Docs 的价值主要在于完整产品文档站的信息架构、分层导航、首页卡片入口、写作治理和站点级配置，而不是简单增加页面数量。

# 待澄清

- [ ] 是否将 Mintlify 配置从当前 `mint.json` 升级为 Dify Docs 风格的 `docs.json`。
- [ ] 首页是否需要独立 `index.mdx`，并使用产品简介、角色入口和常用任务卡片承接首屏。
- [ ] 是否只优化最新版本 `latest`，还是同步调整 `v0.3.3`、`v0.3.4` 等历史版本导航。
- [ ] 是否需要增加文档写作规范、链接检查或 Mintlify 本地预览校验脚本。
- [ ] 是否需要补充公开 API / 管理员接口说明入口，还是继续仅面向产品使用文档。

# 探索结论

（/req-explore 后人工确认写入）
