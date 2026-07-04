---
requirement_id: REQ-0026-product-release-management
title: 产品版本发布与公告管理
terminal: multi
version: v1
status: done
owner: product
source: issues/requirements/archive/REQ-0026-product-release-management/capture.md
priority: P1
parent_requirement: REQ-0010-product-version-display
created_at: 2026-07-02 13:16:07
updated_at: 2026-07-03 23:56:30
---

# REQ-0026 产品版本发布与公告管理

## 1. 需求背景

TILESFST 已通过 `REQ-0010-product-version-display` 建立 Web 端用户可见产品版本号展示机制，版本号由 `src/shared/product-version.ts` 中的 `PRODUCT_VERSION` 人工维护，且不得混用 `package.json`、FastAPI `version`、OpenAPI 版本或 Git 构建信息。

当前项目还缺少“产品版本发布”这一层治理能力：Sprint 级 `release-note.md` 只能描述单个 Sprint 的交付说明，无法自然表达“多个 Sprint 合并为一个产品版本”的发布事实；同时，发布公告需要面向公开页面展示，并以静态文档形式生成，供客户、店主、实施、运维和项目团队了解每个产品版本新增了哪些功能、修复了哪些 BUG，以及上线时需要注意什么。

产品方已确认：

| 维度 | 决策 |
|---|---|
| 产品版本范围 | 一个产品版本允许合并多个 Sprint |
| 公告展示对象 | 公开页面 |
| 公告承载方式 | 静态文档生成，使用 Mintlify 工具 |
| 发布目录 | 需要新增顶层 `releases/`，但必须通过 OpenSpec Change 修改目录规范后再创建 |
| 管理端/店主端入口 | 不同步到管理端菜单、登录页或店主端入口 |
| 发布状态机 | 不需要草稿、待发布、已发布、撤回等状态 |
| 发布前门禁 | 必须校验 OpenSpec archive、测试、Orval、Docker Compose、数据库迁移和 `.env.example` 同步 |
| 公告内容 | 必须记录已知问题、升级步骤、回滚说明和影响范围 |

本需求用于把“产品版本号更新 + 产品版本公告 + 发布前校验 + 发布目录治理”纳入统一发版流程。

## 2. 目标用户

| 角色 | 诉求 |
|---|---|
| 客户 / 店主 / 公开访客 | 在公开发布公告页了解当前版本新增能力、修复问题和升级影响 |
| 项目负责人 / 产品负责人 | 将多个 Sprint 的交付结果合并成一个清晰的产品版本 |
| 开发 / 测试 | 在发布前按固定清单确认 OpenSpec、测试、Orval、Docker、数据库迁移和环境变量同步 |
| 实施 / 运维 | 根据发布公告获取升级步骤、回滚说明、已知问题和影响范围 |
| AI Agent | 依据命令和目录规范生成一致、可追踪的产品发布材料 |

## 3. 范围

### 3.1 本期包含

- 产品版本发布对象：支持一个产品版本关联多个 Sprint、REQ、BUG 和 OpenSpec Change。
- 产品版本号更新规则：发版时必须更新 `src/shared/product-version.ts` 的 `PRODUCT_VERSION`。
- 发布公告生成：面向公开页面，采用 Mintlify 静态文档方式。
- 发布公告内容结构：新增功能、修复 BUG、发布注意事项、已知问题、升级步骤、回滚说明和影响范围。
- 发布前校验清单：OpenSpec archive、测试、Orval、Docker Compose、数据库迁移、`.env.example` 同步。
- 发布目录治理：通过 OpenSpec Change 新增顶层 `releases/` 目录，并同步 `rules/directory-structure.md`、AGENTS 说明和相关文档。
- 发布命令族设计：评估并定义 `/release-propose`、`/release-prepare`、`/release-publish` 或等价命令。
- Sprint 发布说明映射：明确 `iterations/*/release-note.md` 与产品版本发布公告的汇总关系。

### 3.2 本期不包含

- 不在本阶段直接创建 `releases/` 顶层目录；必须等 OpenSpec Change 批准目录规范后创建。
- 不将发布公告入口同步到管理端菜单、登录页或店主端入口。
- 不支持草稿、待发布、已发布、撤回等复杂发布状态机。
- 不做 CI 自动递增产品版本号。
- 不把 `package.json`、FastAPI `version`、OpenAPI 版本或 Git commit 作为用户可见产品版本。
- 不新增后端发布公告 API 或数据库表，除非后续 OpenSpec Change 明确要求。
- 不新增微信小程序内的发布公告入口。
- 不替代 Sprint 四件套；产品版本公告应从已完成 Sprint / REQ / BUG / Change 中汇总。

## 4. 功能要求

### FR-001 产品版本发布对象

- 系统 MUST 定义产品版本发布对象，用于表达一次对外产品发版。
- 一个产品版本 MUST 支持关联多个 Sprint。
- 一个产品版本 SHOULD 汇总关联 Sprint 范围内的 REQ、BUG、OpenSpec Change 和关键交付说明。
- 产品版本标识 SHOULD 采用 SemVer 风格，例如 `v0.1.0`。
- 产品版本发布对象 MUST 与 Sprint 级 `release-note.md` 职责分离：Sprint release note 描述迭代交付，产品发布公告描述对外版本。

### FR-002 产品版本号更新

- 发布时 MUST 更新 `src/shared/product-version.ts` 中的 `PRODUCT_VERSION`。
- `PRODUCT_VERSION` MUST 继续作为用户可见产品版本号的单一事实源。
- 发布流程 MUST 校验产品版本号与本次产品发布对象版本一致。
- MUST NOT 使用 `package.json`、FastAPI `version`、OpenAPI 版本、Git commit 或 CI 构建号作为用户可见产品版本。
- 若本次发布不改变产品版本语义，发布流程 MUST 明确记录不更新 `PRODUCT_VERSION` 的原因。

### FR-003 发布公告静态生成

- 发布公告 MUST 面向公开页面展示。
- 发布公告 MUST 采用静态文档生成方式，并使用 Mintlify 工具。
- 发布公告源文件 MUST 可纳入 Git 管理，便于审查、追踪和回滚。
- 发布公告 MUST 不依赖后端运行时 API 或数据库查询才能展示。
- Mintlify 生成流程 MUST 支持本地预览或等价校验方式，确保发布前可验证公告可构建。

### FR-004 发布公告内容结构

每个产品版本公告 MUST 至少包含：

| 内容 | 要求 |
|---|---|
| 版本号 | 与 `PRODUCT_VERSION` 和发布对象一致 |
| 发布日期 | 使用 `YYYY-MM-DD HH:mm:ss` 标准时间格式 |
| 关联 Sprint | 可列出一个或多个 Sprint |
| 新增功能 | 按 REQ 或业务模块汇总 |
| 修复 BUG | 按 BUG 汇总，并标注影响范围 |
| 发布注意事项 | 包含部署、配置、兼容性或操作提示 |
| 已知问题 | 发布时仍存在但可接受的问题 |
| 升级步骤 | 运维或实施执行步骤 |
| 回滚说明 | 回滚条件、回滚步骤和注意事项 |
| 影响范围 | Web 管理端、店主 Web、小程序、后端、数据库、对象存储、Docker 等影响 |

发布公告 SHOULD 避免泄露敏感信息、真实客户数据、密钥、内部数据库连接串或不可公开的运维信息。

### FR-005 发布前校验清单

发布前 MUST 校验以下事项：

- OpenSpec Change 已完成 archive，相关能力已合并到 `openspec/specs/`。
- 测试已按变更范围执行并记录结果。
- 涉及 API 变更时，OpenAPI 已同步且 Orval 已生成前端类型和请求客户端。
- Docker Compose 配置与部署文档已同步；本地或目标部署路径具备明确验证结论。
- 涉及数据库迁移时，迁移脚本、数据库文档和回滚说明已同步。
- 涉及环境变量时，`.env.example` 及相关 `.env.example` / `.env.docker` 注释已同步。
- 产品版本号 `PRODUCT_VERSION` 与发布公告版本号一致。
- 发布公告 Mintlify 构建或预览校验通过。

若任一必填校验失败，发布流程 MUST 阻断，并输出失败原因与修复建议。

### FR-006 发布目录与目录规范

- 本需求需要新增顶层 `releases/` 目录，用于承载产品版本发布对象、公告源文件、生成配置或索引材料。
- 新增顶层 `releases/` MUST 通过 OpenSpec Change 进入开发，不得在 PRD 或 capture 阶段直接创建。
- OpenSpec Change MUST 说明：
  - 现有 `iterations/` 和 `docs/` 为什么无法承载产品版本发布对象。
  - `releases/` 的职责、边界、命名规则和生命周期。
  - `releases/` 与 `iterations/`、`issues/`、`openspec/changes/`、Mintlify 文档源之间的关系。
  - 需要同步更新的规则和文档，包括 `rules/directory-structure.md`、`AGENTS.md`、`rules/release.md` 和相关 README。

### FR-007 发布命令族

后续 OpenSpec Change SHOULD 定义发布命令族，例如：

| 命令 | 目标 |
|---|---|
| `/release-propose <version>` | 创建产品版本发布计划，选择关联 Sprint / REQ / BUG / Change |
| `/release-prepare <version>` | 执行发布前校验，生成或更新 Mintlify 公告草稿 |
| `/release-publish <version>` | 确认发布材料，记录发布结果和最终公告 |

命令设计 MUST 遵守 `.cursor/commands/` 为 slash 命令事实源的规则；新增或修改命令后 MUST 运行命令同步脚本。

### FR-008 与 Sprint / REQ / BUG / OpenSpec 的追踪关系

- 产品版本发布对象 MUST 能追踪关联 Sprint。
- 发布公告中的新增功能 MUST 能追踪到 REQ。
- 发布公告中的修复项 MUST 能追踪到 BUG。
- 发布公告中的能力变更 MUST 能追踪到 OpenSpec Change 或 archived spec。
- 未评审、未纳入 Sprint 或未 archive 的 REQ / BUG / Change MUST NOT 被写入正式发布公告范围；如需记录，仅可放入已知问题或后续计划，并明确非本次正式交付。

## 5. UI / UE 约束

- 本需求不新增管理端菜单、登录页入口或店主端入口。
- 本需求不修改既有产品版本 badge 展示位置和样式。
- 若后续公开页面由 Mintlify 输出，其视觉与交互 SHOULD 以 Mintlify 文档站能力为准；不强制套用 Web 应用 Design System。
- 公告内容 MUST 面向公开读者，语言应清晰、克制、可执行，避免内部实现细节堆砌。

## 6. 非功能约束

| 项 | 要求 |
|---|---|
| 安全 | 公告不得泄露密钥、真实客户数据、内部连接串、不可公开域名或敏感运维信息 |
| 可追踪 | 每个发布版本应能追溯到 Sprint、REQ、BUG、OpenSpec Change |
| 可回滚 | 公告必须包含回滚说明；发布材料自身应可通过 Git 回退 |
| 可审查 | 发布公告源文件和发布清单必须适合代码评审 |
| 兼容性 | Mintlify 静态文档不得影响现有 Web 管理端、店主端、小程序和后端服务 |
| 可维护 | 目录、命令、规范必须形成稳定流程，避免每次发版临时拼接材料 |

## 7. 关联需求与规范

| 需求 / 规范 | 关系 |
|---|---|
| REQ-0010-product-version-display | 父/关联需求，提供用户可见产品版本号展示机制 |
| `rules/release.md` | 需要扩展产品版本发布检查与公告生成规则 |
| `rules/directory-structure.md` | 需要通过 OpenSpec Change 新增 `releases/` 顶层目录职责 |
| `rules/document-governance.md` | 发布公告、时间字段、文档元数据需遵守 |
| `rules/requirement-management.md` | 只有已评审范围可进入正式发布公告 |
| `rules/bug-management.md` | 修复 BUG 需可追踪到 BUG 文档 |
| `rules/iterations-lifecycle.md` | 产品版本可合并多个已归档或已完成 Sprint |
| `src/shared/product-version.ts` | 用户可见产品版本号单一事实源 |

## 8. 状态

```yaml
requirement_id: REQ-0026-product-release-management
priority: P1
status: approved
iteration: null
owner: product
parent_requirement: REQ-0010-product-version-display
openspec_change: null
target_clients:
  web_admin: 不新增入口
  web_catalog: 不新增入口
  miniapp: 不新增入口
  public_docs: 本期目标
release_docs:
  tool: Mintlify
  directory: releases/  # 须经 OpenSpec Change 批准后创建
```
