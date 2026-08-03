---
requirement_id: REQ-0094-mintlify-versioned-docs-directory
title: Mintlify 多版本产品文档目录与站点浏览 - 验收标准
acceptance_status: passed
created_at: 2026-08-03 18:30:03
updated_at: 2026-08-03 20:52:16
owner: product
---

# 验收标准

## 功能 AC

- [ ] AC-001：项目必须正式定义 `mintlify/` 作为 Mintlify 文档站源目录，并通过 OpenSpec Change 同步目录结构规则后才能创建或使用该一级目录。
- [ ] AC-002：`releases/vX.Y.Z/usage-docs/` 必须继续作为该版本产品使用文档事实源和发布快照，保留全量文档正文与 `manifest.json`。
- [ ] AC-003：`releases/vX.Y.Z/usage-docs/` 默认不得直接存放大体积系统截图文件；如确需保留，必须在 manifest 记录原因、大小、来源、hash 和迁移或清理策略。
- [ ] AC-004：`usage-docs/manifest.json` 必须记录页面清单、截图引用、截图 hash、截图来源、覆盖页面、站点目标路径、同步时间和手工维护记录。
- [ ] AC-005：系统必须支持将 `releases/<version>/usage-docs/**` 同步或投影到 `mintlify/docs/<version>/**`，且目标页面可追溯到来源 release 快照。
- [ ] AC-006：`mintlify/mint.json` 或等价 Mintlify 配置必须包含产品发布公告、当前版本产品使用文档、历史版本产品使用文档和 `latest` 入口。
- [ ] AC-007：`latest` 默认必须指向最新已发布且 usage docs 站点校验通过的版本；最新版本未生成 usage docs 时，`latest` 必须保持最近一个可用版本或显示当前版本文档不可用说明。
- [ ] AC-008：系统必须提供或扩展 usage docs 生成、更新、校验流程，使其能校验 release 快照、站点目录、Mintlify 导航、broken links 和公开安全。
- [ ] AC-009：系统截图必须集中写入或复用 `mintlify/assets/screenshots/`，文件名应包含内容 hash 和语义名称。
- [ ] AC-010：共享截图资产必须在 manifest 中记录 `content_hash`、`first_used_in`、`used_by_versions`、`covered_pages`、`source_type` 和 `reuse_reason`。
- [ ] AC-011：不同版本复用同一截图时，必须证明界面、字段、操作入口、数据状态和权限边界未发生影响用户理解的变化；否则必须新增截图。
- [ ] AC-012：历史截图迁移必须按内容 hash 去重，并保留来源版本、来源 manifest 和同步时间。
- [ ] AC-013：无 usage docs 的历史版本不得生成空文档目录；站点应只展示公告或明确说明该版本未生成产品使用文档。
- [ ] AC-014：站点同步或投影不得绕过 release 快照直接以 `mintlify/` 作为唯一事实源。
- [ ] AC-015：`/release-prepare <version>` 和 `/release-publish <version>` 必须纳入站点目录校验或记录未执行真实 Mintlify preview 的替代校验证据。
- [ ] AC-016：`AGENTS.md`、`rules/directory-structure.md`、`rules/document-governance.md`、`rules/release.md`、`releases/README.md` 和 usage docs 相关 Skill / 脚本说明必须同步 `releases/` 与 `mintlify/` 的职责边界。
- [ ] AC-017：目录结构校验必须识别 `mintlify/` 为允许目录，并阻断未治理的站点构建产物、真实客户数据、密钥或临时大文件进入仓库。
- [ ] AC-018：校验失败时必须输出具体 blocker、涉及路径和建议修复方向，包括站点未同步、页面 hash 漂移、截图复用依据缺失、导航缺页、broken links、敏感信息和旧版本内容性误改。
- [ ] AC-019：Docker Compose 必须支持通过 `docs-site` 或等价 profile 启动 Mintlify 文档站服务，默认 `docker compose up` 不得无条件启动该服务。
- [ ] AC-020：Mintlify Compose 服务必须使用 `mintlify/` 作为工作目录或挂载源，并以 `mintlify/mint.json` 或等价配置启动文档站。
- [ ] AC-021：Mintlify Compose 服务宿主机端口必须通过 `.env.example` 中的变量配置，例如 `HOST_PORT_MINTLIFY_DOCS`；不得在多个文件硬编码端口。
- [ ] AC-022：新增或修改 Compose service、ports、volumes、profiles、environment、command 时，必须同步 `.env.example`、`rules/environment.md`、`rules/port-management.md` 和 `docs/02-deployment.md`。
- [ ] AC-023：本地/演示部署必须提供可执行说明，能通过 Compose profile 启动 backend、web 和 Mintlify 文档站，并验证文档站导航可访问。
- [ ] AC-024：生产部署必须明确采用 Compose 内 Mintlify 服务、外部 Mintlify 托管、静态托管或反向代理中的哪一种；未确认时 `/release-prepare` 必须记录 blocker 或待确认项。
- [ ] AC-025：若发布范围包含 Mintlify Compose 服务或相关 Dockerfile/Compose 变更，发布流程必须要求 Docker Compose 验证，并按发布规范判断是否需要 `/image-prepare` 与 `/image-build` 证据。

## 非功能 AC

- [ ] AC-NF-001：`mintlify/`、release usage docs、manifest 和 Mintlify 配置不得泄露 `.env` 真实内容、数据库连接串、对象存储密钥、Authorization header、Cookie、Token、真实客户数据、本地绝对路径或生产私有域名。
- [ ] AC-NF-002：文档同步、截图去重和校验命令输出必须保持摘要化，展示版本、来源、目标目录、页面数、截图资产数、复用数、warning、blocker 和下一步命令。
- [ ] AC-NF-003：Mintlify Compose 服务不得成为 backend、web、minio 或对象存储的启动前置条件；未启用文档站 profile 时业务系统必须仍可正常启动。
- [ ] AC-NF-004：实现新增或修改命令时必须遵守 `rules/agent-context-budget.md`，避免默认全量读取所有历史 release、所有截图、生成物或大日志。
- [ ] AC-NF-005：旧版本产品文档内容默认冻结；站点迁移、路径修复、截图去重和敏感信息移除属于非内容性维护，内容性更正必须有明确授权和 manifest 留痕。
- [ ] AC-NF-006：共享截图复用必须优先保证版本真实性，不得为了节省空间让历史版本展示不属于该版本的界面。
- [ ] AC-NF-007：站点路径和导航文案应面向客户、店主、实施和支持人员理解，避免暴露 OpenSpec、Sprint、未评审 Issue 或内部验收中间态。
- [ ] AC-NF-008：Docker Compose 中 Mintlify 服务的注释、环境变量说明和发布证据不得包含真实生产域名、外部托管账号、访问 token 或不可公开运维信息。

## 横切 AC（knowledge-base）

本 REQ 为发布治理 / 产品使用文档 / Mintlify 文档站能力，不涉及管理端 CRUD 列表、管理端表单页、管理端弹窗或媒体上传 UI 场景；Knowledge-base UI 横切标签为 N/A，本节不新增 AC-XCUT。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-03 20:52:16
accepted_by: workflow-sync
source_change: add-mintlify-versioned-docs-site
source_sprint: sprint-018
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

