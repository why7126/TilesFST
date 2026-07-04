---
req_id: REQ-0026-product-release-management
status: captured
created_at: 2026-07-02 13:04:17
updated_at: 2026-07-02 13:11:29
recorded_by: product
source: 用户输入
priority_hint: P1
parent_requirement: REQ-0010-product-version-display
---

# 产品版本发布与公告管理

建立产品版本发布管理能力：发布时更新产品页面显示的版本号，并公告每个版本发布了哪些功能、修复了哪些 BUG，以及必要的发布注意事项。

# 原始描述

产品版本发布，一方面，发布时用于变更产品页面显示的版本号；另一方面，用于公告每个版本发布了哪些功能，修复了哪些 BUG。

用户确认以 `/req-capture` 记录为：

> 产品版本发布与公告管理：发布时更新产品页面版本号，并公告每个版本新增功能、修复 BUG 和发布注意事项。

2026-07-02 13:11:29 用户补充确认：

- 产品发布允许多个 Sprint 合并为一个产品版本。
- 发布公告面向公开页面展示。
- 发布公告采用静态文档生成，使用 Mintlify 工具。
- 需要新增顶层 `releases/` 目录，并通过 OpenSpec Change 修改目录规范。
- 不需要把发布公告同步到管理端菜单、登录页或店主端入口。
- 不需要支持草稿、待发布、已发布、撤回等发布状态。
- 发布时必须校验 OpenSpec archive、测试、Orval、Docker Compose、数据库迁移和 `.env.example` 同步。
- 需要记录已知问题、升级步骤、回滚说明和影响范围。

# 初步拆分判断

本次作为单条 REQ 记录，不拆分。理由：版本号更新、发布公告、功能与 BUG 摘要、发布注意事项属于同一个“产品发版管理”闭环；后续可在 PRD 中按“发布流程规范”“发布命令”“公告展示/存储”拆成功能模块或子任务。

# 初步范围

- 发布时必须更新用户可见产品版本号，优先复用既有 `src/shared/product-version.ts` 的 `PRODUCT_VERSION` 机制。
- 发布公告需按产品版本汇总新增功能、修复 BUG 和发布注意事项。
- 一个产品版本允许合并多个 Sprint 的交付内容；需明确 Sprint 级 `release-note.md` 与产品版本发布公告之间的映射关系。
- 发布公告面向公开页面，采用静态文档生成，并使用 Mintlify 工具承载。
- 需要评估是否新增发布命令族，例如 `/release-propose`、`/release-prepare`、`/release-publish`。
- 需要新增产品版本发布规范，并评估发布命令与 Mintlify 静态文档生成流程的边界。
- 需要通过 OpenSpec Change 新增顶层 `releases/` 目录，并同步修改目录规范；当前 capture 阶段不直接创建该目录。
- 发布公告必须包含新增功能、修复 BUG、发布注意事项、已知问题、升级步骤、回滚说明和影响范围。
- 发布前必须校验 OpenSpec archive、测试、Orval、Docker Compose、数据库迁移和 `.env.example` 同步状态。
- 发布公告不需要同步到管理端菜单、登录页或店主端入口。
- 本期不需要草稿、待发布、已发布、撤回等发布状态机。

# 已确认约束

- [x] 产品发布允许多个 Sprint 合并为一个产品版本。
- [x] 发布公告面向公开页面展示。
- [x] 发布公告采用静态文档生成，使用 Mintlify 工具。
- [x] 需要新增顶层 `releases/` 目录，且必须通过 OpenSpec Change 修改目录规范后再创建。
- [x] 不需要把发布公告同步到管理端菜单、登录页或店主端入口。
- [x] 不需要支持草稿、待发布、已发布、撤回等发布状态。
- [x] 发布时必须校验 OpenSpec archive、测试、Orval、Docker Compose、数据库迁移和 `.env.example` 同步。
- [x] 需要记录已知问题、升级步骤、回滚说明和影响范围。

# 后续 PRD 重点

- 定义 `releases/` 目录职责、结构、命名、生命周期和与 `iterations/` 的关系。
- 定义 Mintlify 静态文档生成输入、输出、发布路径和本地/CI 校验方式。
- 定义产品版本号更新规则与 `src/shared/product-version.ts` 的发版检查关系。
- 定义从多个 Sprint、REQ、BUG、OpenSpec Change 汇总发布公告的来源规则。
- 定义发布前校验清单及失败时的阻断策略。

# 探索结论

（/req-explore 后人工确认写入）
