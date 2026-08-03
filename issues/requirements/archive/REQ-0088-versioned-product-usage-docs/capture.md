---
req_id: REQ-0088-versioned-product-usage-docs
status: done
created_at: 2026-08-01 08:10:11
updated_at: 2026-08-02 17:59:12
recorded_by: product
source: /capture
priority_hint: P1
parent_requirement:
captured_via: capture
classification_rationale: 该事项描述尚未交付的新发布治理能力：基于 Mintlify 生成和维护版本化产品使用文档，并纳入发版流程与规范，不属于既有能力偏差。
---

# 一句话

建立基于 Mintlify 的版本化产品使用文档生成、更新、校验与发布治理能力，使产品文档可通过域名 `/docs` 浏览，并在每次发版时生成当前版本使用文档。

# 原始描述

围绕产品使用文档的探索形成以下方向：

- 基于 Mintlify 搭建本项目产品使用文档站，计划通过 `域名/docs` 访问。
- 每次发版时生成新版本产品使用文档。
- 产品文档生成、产品文档更新需要落地成明确命令、流程和规范，避免依赖人工记忆。
- 当前版本文档应与 `releases/<version>/release.json`、发布公告、管理端导航、小程序页面和发布门禁关联。
- 旧版本文档不应被随意改写产品行为说明，但原先“旧版本自动化不得覆盖，只允许人工修改”的规则过硬，应放松为：旧版本产品内容默认冻结；自动化可做非内容性维护和安全修复；内容性更正需明确授权并留痕。

# 初步范围

- 新增或扩展产品使用文档命令，例如 `/usage-docs-generate <version>`、`/usage-docs-validate <version>`，并将其接入 `/release-prepare <version>`。
- 在 `releases/vX.Y.Z/usage-docs/` 下生成当前版本文档与 `manifest.json`。
- 更新 Mintlify 配置，使版本公告和产品使用文档均可在文档站导航中访问。
- 扩展 `release.json`，增加 `usage_docs` 字段和 `usage_docs_preview` 发布门禁。
- 更新发布、目录、文档治理和 release skill 规范，明确产品文档生成、更新、冻结、人工修改和自动化维护边界。
- 增加校验与测试，覆盖文档 manifest、导航、broken links、敏感信息扫描、菜单/页面覆盖和旧版本内容改写策略。

# 待澄清

- [ ] Mintlify 配置继续使用现有 `mint.json`，还是在本需求中升级为官方推荐的 `docs.json`。
- [ ] `/docs` 访问由 Mintlify 子路径、自定义域名配置、Cloudflare/Vercel rewrite，还是生产 Nginx 反向代理承载。
- [ ] 产品使用文档是否只公开面向店主/客户与管理端操作说明，内部运维/API/敏感配置是否继续留在仓库 `docs/` 或鉴权页面。
- [ ] 文档正文是完全模板生成、从上一版本复制增量更新，还是由 AI 生成草稿后人工 Review。
- [ ] 旧版本内容性更正的授权方式和留痕字段放在 `manifest.json`、frontmatter 还是 `release.json`。

# 探索结论

本事项归类为单条 REQ：它是围绕版本化产品使用文档的一组发布治理能力，命令、流程、规范、Mintlify 导航与校验应作为同一交付单元推进。后续可通过 `/req-generate` 展开 PRD，通过 `/req-complete` 补齐验收标准，再评审进入 OpenSpec Change。
