---
requirement_id: REQ-0088-versioned-product-usage-docs
title: 版本化产品使用文档生成与发布治理 - 验收标准
acceptance_status: passed
created_at: 2026-08-01 08:24:50
updated_at: 2026-08-02 19:32:35
owner: product
---

# 验收标准

## 功能 AC

- [ ] AC-001：每个产品版本支持独立 `releases/<version>/usage-docs/` 目录，目录内包含产品使用文档源文件和 `manifest.json`。
- [ ] AC-002：`usage-docs/manifest.json` 至少记录 version、generated_at、source_version、source_release、input_files、pages、coverage、manual_overrides 和 automation_policy。
- [ ] AC-003：`/release-prepare <version>` 必须先确认本次是否需要生成或更新产品使用文档；未确认时不得自动生成新版本产品文档。
- [ ] AC-004：用户确认不需要生成或更新产品文档时，流程不得创建空的当前版本 `usage-docs/` 目录，必须在 `release.json` 记录 skipped 状态、确认来源和跳过原因。
- [ ] AC-005：用户确认需要生成或更新产品文档时，产品文档生成命令必须读取 `releases/<version>/release.json`，缺失时阻断并提示先完成发布计划。
- [ ] AC-006：用户确认需要生成或更新产品文档时，产品文档生成命令必须生成或更新当前版本 `usage-docs/**` 和 `usage-docs/manifest.json`。
- [ ] AC-007：当存在上一版本 `usage-docs/` 时，生成命令应能以其为基础生成当前版本文档；首版文档可从模板生成并记录 `source_version: null`。
- [ ] AC-008：生成命令必须参考管理端导航、Web 路由、小程序页面配置和当前 release impact_scope，形成覆盖摘要或明确豁免。
- [ ] AC-009：产品文档校验命令必须校验 manifest 结构、版本一致性、页面清单和实际文件一致性。
- [ ] AC-010：产品文档校验命令必须校验 Mintlify 导航包含当前版本产品使用文档和当前版本发布公告。
- [ ] AC-011：产品文档校验命令必须执行 Mintlify broken links、build、preview 或等价静态校验。
- [ ] AC-012：产品文档校验命令必须扫描公开文档敏感信息，发现 `.env` 内容、数据库连接串、密钥、Authorization header、Cookie、真实客户数据或不可公开运维信息时阻断。
- [ ] AC-013：`/release-prepare <version>` 必须接入产品文档生成决策，并在 `release.json` 中记录 `usage_docs` 元数据。
- [ ] AC-014：`release.json` 必须支持 `usage_docs_preview` gate；gate 为 `pass` 时必须包含具体命令、路径、时间或校验证据；用户确认不需要生成或更新时应记录为 `na` 并填写 rationale。
- [ ] AC-015：当前版本文档生成必须以用户确认为前置条件，并以 `release.json` 正式范围为事实源，不得纳入未评审、未归档或未进入正式发布范围的 REQ / BUG / Change。
- [ ] AC-016：已发布旧版本产品文档默认视为快照；自动化在无明确授权时不得改写旧版本产品行为、操作步骤、功能可用性、版本差异和已知问题历史语义。
- [ ] AC-017：旧版本文档允许自动化执行非内容性维护和安全修复，包括 broken links、Mintlify 配置迁移、frontmatter/manifest 补齐、格式修复、导航引用修复、敏感信息移除和目录结构迁移。
- [ ] AC-018：旧版本内容性更正必须记录原因、操作者、时间、文件范围和变更说明。
- [ ] AC-019：项目文档或部署说明必须记录 `域名/docs` 的实现边界，包括 Mintlify base path、Cloudflare/Vercel/CDN rewrite 或 Nginx 反向代理方案。
- [ ] AC-020：若 `/docs` 子路径存在认证或平台能力限制，公开产品使用文档与内部敏感文档必须分离。
- [ ] AC-021：`rules/release.md`、`rules/directory-structure.md`、`rules/document-governance.md`、`releases/README.md` 和 release skill 必须同步产品文档生成决策、更新、校验和旧版本维护规则。
- [ ] AC-022：发布前校验必须能报告产品文档 blocker，包括未确认是否生成、manifest 缺失、导航缺页、broken links、敏感信息、覆盖缺口、旧版本内容性误改和 `/docs` 部署边界未确认。

## 非功能 AC

- [ ] AC-NF-001：产品使用文档、manifest、Mintlify 配置和 release gate 证据不得泄露密钥、真实客户数据、数据库连接串、Authorization header、Cookie、内部路径或不可公开运维地址。
- [ ] AC-NF-002：文档生成、校验和 release-prepare 输出必须保持摘要化，展示版本、文档路径、manifest、覆盖结果、blocker 和下一步命令。
- [ ] AC-NF-003：产品文档能力不得影响 Web 管理端、小程序、后端 API、数据库、Docker Compose 或对象存储运行链路。
- [ ] AC-NF-004：实现不得把 `usage-docs/` 替代 `docs/`、`openspec/specs/`、`issues/`、`iterations/` 或 `release.json` 的既有职责。
- [ ] AC-NF-005：实现新增或修改文档生成、校验、发布命令时必须遵守 `rules/agent-context-budget.md`，避免默认全量读取历史归档、生成物、大日志或完整 OpenAPI/Orval 文件。
- [ ] AC-NF-006：发布文档校验应能检测 release-note、acceptance、产品文档中的中间阶段语义残留，确保已发布范围不再出现未闭环表述。
- [ ] AC-NF-007：小程序设备 evidence、真机验证或体验版 Network evidence 若与产品文档相关，必须在 release-prepare 阶段集中记录补证结果或不可用原因。

## 横切 AC（knowledge-base）

本 REQ 为发布治理 / 产品使用文档 / Mintlify 文档站能力，不涉及管理端 CRUD 列表、管理端表单页、管理端弹窗或媒体上传 UI 场景；Knowledge-base UI 横切标签为 N/A，本节不新增 AC-XCUT。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-02 19:32:35
accepted_by: workflow-sync
source_change: add-versioned-product-usage-docs
source_sprint: sprint-017
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

