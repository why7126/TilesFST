---
req_id: REQ-0094-mintlify-versioned-docs-directory
status: done
created_at: 2026-08-03 13:15:49
updated_at: 2026-08-03 20:28:42
recorded_by: product
source: /capture 产品文档多版本目录讨论
priority_hint: P1
parent_requirement: REQ-0088-versioned-product-usage-docs
captured_via: capture
classification_rationale: 用户提出将所有版本的产品文档集中到类似 mintlify 的一级目录，并按版本分子目录，以便文档站一次性浏览多个版本；这是对版本化产品使用文档发布形态与目录治理的新增能力诉求，而非既有实现偏差。
---

# 一句话

将产品使用文档从分散在各 `releases/vX.Y.Z/` 下的发布产物，扩展为可被 Mintlify 站点统一浏览的多版本文档目录结构。

# 原始描述

所有版本的产品文档是否应该是放在同一个目录下，比如一级目录 `mintlify`，然后不同的版本分别有不同的子目录，这样子的话，在 Mintlify 网站就可以一次性浏览多个不同版本的产品文档呢？现在都是放在 `releases` 目录的每个版本下。

# 背景

当前产品使用文档按发布版本沉淀在 `releases/vX.Y.Z/` 中，适合保留发布证据和版本归档，但不一定适合直接作为 Mintlify 站点的多版本浏览入口。若要支持线上文档站同时浏览多个产品版本，需要明确站点源目录、版本目录命名、导航生成、发布产物与站点源文件之间的同步关系。

该需求与 `REQ-0088-versioned-product-usage-docs` 相关，属于版本化使用文档能力的发布形态增强。由于可能新增一级目录或改变长期文档目录边界，后续进入开发前必须通过 OpenSpec Change 同步目录规范、文档治理规则和 Mintlify 导航维护方式。

# 影响范围

- 产品使用文档源文件目录结构。
- `releases/vX.Y.Z/` 发布证据与公开文档站源文件的职责边界。
- Mintlify 站点配置、导航与版本切换体验。
- `usage-docs-generate`、`usage-docs-update`、`usage-docs-validate` 命令产物路径和校验逻辑。
- `rules/directory-structure.md`、`rules/document-governance.md` 与 AGENTS 目录边界说明。
- 发布流程中使用文档生成、校验、发布确认和历史版本维护。

# 待澄清

- [ ] 一级目录名称是否采用 `mintlify/`，还是采用更通用的 `docs-site/`、`site-docs/` 或 `docs/usage/versions/`。
- [ ] `releases/vX.Y.Z/` 是否继续保留版本发布证据和公告源文件，Mintlify 目录只承载公开文档站源文件。
- [ ] 多版本目录是否按 `vX.Y.Z/`、`latest/`、`stable/` 或 Mintlify 官方版本机制组织。
- [ ] 历史版本文档是否允许在新版本发布后修订，还是只能通过勘误或新版本文档覆盖。
- [ ] Mintlify 导航是否由 manifest 自动生成，还是手工维护。
- [ ] 当前已存在的版本文档是否需要一次性迁移或复制到新目录。

# 建议验收要点

- [ ] 明确产品使用文档的长期源目录，并能支持 Mintlify 网站一次性浏览多个版本。
- [ ] 明确 `releases/vX.Y.Z/` 与 Mintlify 文档目录的职责边界，避免发布证据和站点源文件互相污染。
- [ ] 每个产品版本具备独立目录、导航入口、版本元数据和公开/非公开边界。
- [ ] `latest` 或默认版本指向规则清晰，发布新版本时可以稳定更新。
- [ ] 使用文档生成、更新、校验命令同步支持新目录结构，并能校验 manifest、Mintlify 导航和禁止公开的敏感内容。
- [ ] 如新增一级目录，必须同步更新目录结构规则、AGENTS 和相关文档治理说明，并通过目录结构校验。
- [ ] 历史 `releases/vX.Y.Z/` 下已有文档的迁移策略明确，且不破坏已有发布证据。

# 探索结论

（/req-explore 后人工确认写入）
