---
note: workflow-sync — workflow-sync 自动同步 — 6/6 Change archived；0 applied；Sprint `completed`
sprint_id: sprint-017
title: Sprint 017 发布文档、媒体验收与工作流状态治理
status: completed
lifecycle_stage: archive
created_at: 2026-08-01 10:35:08
updated_at: 2026-08-02 19:32:35
owner: product
---

# Sprint 017 发布文档、媒体验收与工作流状态治理

## 1. Sprint 目标

本 Sprint 聚焦五个治理/媒体能力与一个小程序展示修复：REQ-0088 补齐“产品使用文档”的版本化、按需生成、发布确认、校验门禁和旧版本维护策略；REQ-0090 建立媒体五联验收模板；REQ-0091 建立媒体类 BUG 四联验收模板；REQ-0089 补齐 REQ/BUG 子文档状态同步、验收结果回填、drift check 与 Sprint close 中间态残留扫描；REQ-0092 将真实缩略图生成与优先读取能力扩展到品牌图片和图片类品牌证书；BUG-0102 修复小程序品牌列表页轮播图多余说明文案展示，避免正式 UI 出现开发/验收说明。

正式范围：

- `REQ-0088-versioned-product-usage-docs`
- `REQ-0090-media-five-point-acceptance-template`
- `REQ-0091-media-bug-four-point-acceptance-template`
- `REQ-0089-workflow-subdocument-status-sync`
- `REQ-0092-brand-certificate-image-thumbnails`
- `BUG-0102-miniapp-brand-list-carousel-brand-gallery-text`

### REQ-0088-versioned-product-usage-docs 要点

- 产品使用文档不是每个产品版本都必须生成或更新，发布准备阶段必须先向用户确认。
- 确认需要时，生成当前版本 `usage-docs/**` 与 `manifest.json`，并校验 Mintlify 导航、broken links、公开安全扫描和覆盖度。
- 确认不需要时，不创建空的当前版本 `usage-docs/`，在 `release.json` 中记录 skipped 状态、确认来源和跳过原因。
- 已发布旧版本产品文档默认作为快照；非内容性维护和安全修复可自动化，内容性更正必须授权并留痕。
- `/docs` 浏览方式属于部署边界，需要在项目文档中明确 base path、rewrite、反向代理或托管平台方案。

### REQ-0090-media-five-point-acceptance-template 要点

- 建立媒体五联验收模板，覆盖上传、API/对象、URL、前端/小程序渲染和性能/降级。
- 将模板用于媒体能力、媒体链路返修、Sprint 验收和发布前检查。
- 保留 media-upload 横切 gate，并明确 N/A、blocked 与证据记录口径。

### REQ-0091-media-bug-four-point-acceptance-template 要点

- 建立媒体类 BUG 四联验收模板，覆盖原 BUG 场景、key、object、URL、render。
- 将模板沉淀为 BUG 修复、返修、回归测试、Sprint 验收和发布前检查的标准证据结构。
- 保留 media-upload 横切 gate：上传状态机、同会话即时回显、Docker Web `http://localhost:3000` 边界验收、媒体代理一致性和小程序 evidence。
- 明确不新增上传接口、对象存储能力、缩略图/转码能力、自动化测试实现或运行时 UI。

### REQ-0089-workflow-subdocument-status-sync 要点

- 明确 `trace.md`、`requirement.md`、`bug.md`、`acceptance.md`、`review.md`、BUG 分析文档等顶层子文档的状态字段职责。
- 常规 workflow event 后同步人类入口文档，避免主文档长期停留在 `draft`、`pending_review`、`approved` 等旧状态。
- 为 `acceptance.md` 或等价文档建立验收状态、证据、失败项、来源 Change/Sprint 的回填结构。
- 增强 drift check，覆盖 trace、registry、目录阶段、子文档状态与验收结果。
- 历史 archive 漂移治理必须走 scan / classify / dry-run / human confirmation / apply / check，禁止批量修复绕过门禁。
- `/opsx-archive` 与 `/sprint-archive` 前后要检查子文档状态、验收结果和中间态残留。

### BUG-0102-miniapp-brand-list-carousel-brand-gallery-text 要点

- 小程序品牌列表页轮播图不得显示 `BRAND GALLERY` 文案。
- 小程序品牌列表页轮播图不得显示 `轮播图保持现有品牌页能力` 文案。
- 修复必须保持品牌页轮播图现有图片加载、展示、切换、指示点和点击/跳转能力。
- 文案删除后不得留下空白占位、遮挡、错位、高度异常或内容重叠。
- 默认不影响后端 API、数据库、Orval、Web 管理端或 Docker Compose。

### REQ-0092-brand-certificate-image-thumbnails 要点

- 将 SKU 商品图片已验证的真实缩略图生成能力扩展到品牌图片和图片类品牌证书。
- 管理端品牌列表 Logo、品牌编辑弹窗小预览、品牌证书列表/卡片优先使用缩略图，预览仍使用原图或原文件。
- 小程序和店主 Web 的品牌/证书列表、卡片、默认主图优先使用后端受控缩略图，失败时安全回退。
- 存量品牌图片和证书图片需要 dry-run / apply 补齐或重生成方案，输出脱敏统计摘要并支持幂等。
- 媒体五联验收必须覆盖对象 key、对象存在、URL 可访问、真实缩略收益和端上渲染 evidence。
- API、DB、Orval 和 Docker 为条件性影响：新增字段、持久化字段或图片处理依赖时必须同步相应文档、生成物和验证。

## 2. Scope

| 类型 | 编号 | 标题 | 状态 | 估算 | 说明 |
|---|---|---|---|---:|---|
| REQ | REQ-0088-versioned-product-usage-docs | 版本化产品使用文档生成与发布治理 | done | 1 人天 | archived `add-versioned-product-usage-docs`（2026-08-02 17:58:38） |
| REQ | REQ-0090-media-five-point-acceptance-template | 媒体五联验收模板 | done | 3 人天 | archived `add-media-five-point-acceptance-template`（2026-08-01 11:13:14） |
| REQ | REQ-0091-media-bug-four-point-acceptance-template | 媒体类 BUG 四联验收模板 | done | 3 人天 | archived `add-media-bug-four-point-acceptance-template`（2026-08-01 11:04:15） |
| REQ | REQ-0089-workflow-subdocument-status-sync | REQ/BUG 子文档状态同步与验收结果回填机制 | done | 5 人天 | archived `improve-workflow-subdocument-status-sync`（2026-08-01 11:46:37） |
| REQ | REQ-0092-brand-certificate-image-thumbnails | 品牌图片与证书图片真实缩略图生成与使用 | done | 5 人天 | archived `add-brand-certificate-image-thumbnails`（2026-08-02 19:21:07） |
| BUG | BUG-0102-miniapp-brand-list-carousel-brand-gallery-text | 小程序品牌列表页轮播图不应显示多余说明文案 | done | 0.5 人天 | archived `fix-miniapp-brand-list-carousel-text`（2026-08-02 16:51:12） |

<!-- workflow-sync:scope-requirements:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| REQ-0088 | 版本化产品使用文档生成与发布治理 | P1 | done | archived `add-versioned-product-usage-docs`（2026-08-02 17:58:38） |
| REQ-0090 | 媒体五联验收模板 | P1 | done | archived `add-media-five-point-acceptance-template`（2026-08-01 11:13:14） |
| REQ-0091 | 媒体类 BUG 四联验收模板 | P1 | done | archived `add-media-bug-four-point-acceptance-template`（2026-08-01 11:04:15） |
| REQ-0089 | REQ/BUG 子文档状态同步与验收结果回填机制 | P1 | done | archived `improve-workflow-subdocument-status-sync`（2026-08-01 11:46:37） |
| REQ-0092 | 品牌图片与证书图片真实缩略图生成与使用 | P1 | done | archived `add-brand-certificate-image-thumbnails`（2026-08-02 19:21:07） |
<!-- workflow-sync:scope-requirements:end -->

<!-- workflow-sync:scope-bugs:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| BUG-0102 | 小程序品牌列表页轮播图不应显示多余说明文案 | low | done | archived `fix-miniapp-brand-list-carousel-text`（2026-08-02 16:51:12） |
<!-- workflow-sync:scope-bugs:end -->

<!-- workflow-sync:scope-changes:start -->
| Change ID | 关联需求 | 状态 | Sprint 目标 |
|---|---|---|---|
| `add-versioned-product-usage-docs` | REQ-0088-versioned-product-usage-docs | archived | archived `add-versioned-product-usage-docs`（2026-08-02 17:58:38） |
| `add-media-five-point-acceptance-template` | REQ-0090-media-five-point-acceptance-template | archived | archived `add-media-five-point-acceptance-template`（2026-08-01 11:13:14） |
| `add-media-bug-four-point-acceptance-template` | REQ-0091-media-bug-four-point-acceptance-template | archived | archived `add-media-bug-four-point-acceptance-template`（2026-08-01 11:04:15） |
| `improve-workflow-subdocument-status-sync` | REQ-0089-workflow-subdocument-status-sync | archived | archived `improve-workflow-subdocument-status-sync`（2026-08-01 11:46:37） |
| `fix-miniapp-brand-list-carousel-text` | BUG-0102-miniapp-brand-list-carousel-brand-gallery-text | archived | archived `fix-miniapp-brand-list-carousel-text`（2026-08-02 16:51:12） |
| `add-brand-certificate-image-thumbnails` | REQ-0092-brand-certificate-image-thumbnails | archived | archived `add-brand-certificate-image-thumbnails`（2026-08-02 19:21:07） |
<!-- workflow-sync:scope-changes:end -->

Change：已纳入 5 个 REQ 关联 Change 与 1 个小程序 BUG 修复 Change。执行开发与归档时以 Scope 表逐项状态为准。

## 3. 工作量与容量

| 项 | 值 |
|---|---:|
| developers | 2 |
| testers | 1 |
| capacity_person_days | 30 |
| estimated_story_points | 17.5 |
| estimated_person_days | 17.5 |
| capacity_usage | 58.33% |
| fix_buffer_person_days | 12.5 |
| fix_buffer_ratio | 41.67% |

容量门禁：Pass。`project.yaml` 未提供显式 Sprint 容量，沿用 sprint-016 已确认容量基线 2 dev + 1 tester / 30 人天。本 Sprint 当前纳入 5 个 P1 REQ、1 个 low BUG 与 6 个 Change，估算 17.5 人天，占用 58.33%，满足容量硬门禁，fix buffer 12.5 人天 / 41.67%，满足建议缓冲。

## 4. 里程碑

| 阶段 | 目标日期 | 交付 |
|---|---|---|
| 规划确认 | 2026-08-01 10:42:25 | Sprint 四件套、REQ/Change trace 同步 |
| 实现完成 | 2026-08-07 18:00:00 | release 文档治理、媒体五联/BUG 四联模板、Workflow Sync 子文档状态模型、品牌/证书缩略图扩展、验收回填、drift check、相关 Skill/规则和 focused pytest 完成 |
| 验收归档 | 2026-08-15 18:00:00 | 6 个 Change archive、5 个 REQ archive、1 个 BUG archive、验收报告闭环 |

## 5. 风险

| 风险 | 缓解 |
|---|---|
| release-prepare 自动生成 usage docs，违背“先确认是否需要”的用户约束 | 将 generation_decision 作为生成命令和 release gate 的前置条件；pending_confirmation 必须阻断 |
| 用户确认不需要时仍生成空 `usage-docs/` 目录，造成版本文档噪音 | skipped 流程明确不创建空目录，并在 `release.json` 记录 rationale、确认时间和确认来源 |
| 旧版本产品文档被自动化内容性改写，破坏历史版本语义 | manifest 和校验区分非内容性维护、安全修复与内容性更正；内容性更正必须授权留痕 |
| 媒体五联模板与媒体 BUG 四联模板边界混淆 | apply 阶段必须明确通用媒体能力使用五联，媒体类 BUG 修复闭环使用四联，并保持互相引用 |
| `trace.md` 与子文档状态职责边界不清，导致同步脚本误改历史事实或评审事实 | 先定义字段语义；保留 `trace.md` 为机器事实源；对不代表当前主状态的字段改名或说明语义 |
| 批量修复历史 archive 漂移时误覆盖人工验收结论 | 历史治理默认 dry-run；apply 仅处理分类为可安全同步的项，并输出人工确认前置要求 |
| `/sprint-archive` 中间态残留扫描误报计划态文档 | 扫描范围由 Sprint scope 定位；按文档角色与阶段区分 planned/pending 的合法语义 |
| 小程序轮播图文案清理误伤正式轮播能力 | 只移除 `BRAND GALLERY` 与 `轮播图保持现有品牌页能力` 等说明文案；验收必须覆盖图片展示、切换、指示点和点击/跳转不回归 |
| 品牌/证书缩略图扩展跨 Backend、Web/Admin、Miniapp、Store-owner Web 和 Storage，范围比纯文档治理更宽 | 以媒体五联验收约束 key、object、URL、thumbnail benefit、render evidence；API/DB/Orval/Docker 仅在新增字段或依赖时触发同步 |
| 存量品牌/证书图片补齐脚本误处理真实客户数据或泄露本地路径 | dry-run 先行，apply 输出脱敏统计摘要；禁止提交运行时对象、真实数据、本机绝对路径、密钥或 Authorization 信息 |

## 6. 知识库承接

| 来源 | 承接动作 |
|---|---|
| `docs/knowledge-base/retrospectives/sprint-016-retrospective.md` | 承接 close stale scan 思路，发布文档和 Sprint close 校验需扫描中间态文案残留。 |
| `docs/knowledge-base/retrospectives/sprint-016-retrospective.md` | 承接 archive trace 完整性经验，usage-docs 生成、跳过、人工维护、旧版本更正和 workflow 子文档回填都需要可追踪证据。 |
| `docs/knowledge-base/retrospectives/sprint-016-retrospective.md` | 承接 residual reconcile 只能补救的问题，将 Issue 子文档状态同步前移到常规 workflow event。 |
| `docs/knowledge-base/retrospectives/sprint-015-retrospective.md` | 承接媒体类 BUG 四联验收行动项：URL 可访问、对象存在、小程序渲染和性能懒加载必须一起验收。 |
| `docs/knowledge-base/best-practices/admin-media-upload-chain.md` | 将上传状态机、同会话即时回显、Docker `:3000` 边界文件验收和媒体代理一致性写入媒体验收模板。 |
| `docs/knowledge-base/best-practices/miniapp-custom-navigation.md` | BUG-0102 涉及小程序品牌列表页首屏轮播展示；验收需关注常见视口、首屏内容不遮挡、布局稳定和 DevTools/真机 evidence 边界。 |
| `docs/knowledge-base/best-practices/admin-list-page-consistency.md` | REQ-0092 涉及管理端品牌/证书列表小图展示；分页 DOM、fixed toast、DS confirm 和筛选控件不得回归。 |
| `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md` | REQ-0092 涉及品牌/证书上传弹窗；必须避免 `modal-card` 与专属类双挂载导致 computed width 回归。 |

## 7. 横切预防清单

- [ ] release：`/release-prepare <version>` 先确认是否需要生成或更新产品使用文档。
- [ ] release：未确认时不得自动生成 `usage-docs/`，并记录 pending_confirmation 或 blocker。
- [ ] release：确认不需要时，`release.json` 记录 skipped、rationale、confirmed_at、confirmed_by，不创建空 `usage-docs/`。
- [ ] docs：确认需要时生成当前版本 `usage-docs/**` 与 `manifest.json`。
- [ ] security：公开文档扫描密钥、真实客户数据、数据库连接串、Authorization header、Cookie、内部路径和不可公开运维地址。
- [ ] media-five：模板必须覆盖上传、API/对象、URL、render、性能/降级五联。
- [ ] media-bug-four：模板必须覆盖原 BUG 场景、key、object、URL、render 四联。
- [ ] media-bug-four：失败记录必须包含实际结果、期望结果、复现步骤、影响范围和排查线索，可支撑后续 `/bug-capture` 或返修。
- [ ] media-upload：涉及上传的媒体 BUG 必须检查上传状态机、同会话即时回显、Docker Web `http://localhost:3000` 边界文件或记录 N/A 理由。
- [ ] workflow-sync：`trace.md` 继续作为 REQ/BUG 机器状态事实源。
- [ ] workflow-sync：常规状态变化后同步 `requirement.md` / `bug.md` / `acceptance.md` / `review.md` 等人类入口状态或语义引用。
- [ ] acceptance：`acceptance.md` 能表达验收状态、时间、来源、证据、失败项或豁免说明。
- [ ] drift-check：检查 trace frontmatter、fenced yaml、registry、目录阶段、子文档状态与验收结果。
- [ ] archive：历史漂移治理默认 dry-run，apply 仅处理可安全同步项。
- [ ] sprint-close：`/sprint-archive` 前扫描 Issue 包与 Sprint 四件套中的中间态残留。
- [ ] miniapp-ui：品牌列表页轮播图不得显示开发/验收说明文案，且文案移除后首屏轮播布局不遮挡、不错位。
- [ ] miniapp-ui：DevTools 或真机验收不得把 DevTools 通过表述为真机通过；真机不可用时记录 blocked/follow_up。
- [ ] admin-list：品牌列表与证书列表若调整小图展示 DOM，分页结构、fixed toast、DS confirm 和筛选控件必须保持管理端列表基准。
- [ ] admin-modal：品牌/证书上传弹窗不得同时挂载 `modal-card` 与专属类；需验证 computed width 与矮视口滚动。
- [ ] media-upload：品牌/证书图片上传控件必须覆盖 `idle -> uploading -> done/failed`、同会话即时回显、字段级失败和 Docker Web `:3000` 边界文件。
- [ ] media-thumbnail：品牌/证书缩略图验收必须覆盖 key、object、URL、thumbnail benefit、render evidence，且缩略图不得是原图 bytes 复制品。
- [ ] miniapp-media：小程序品牌/证书缩略图 evidence 不得用 Web 静态测试替代真机通过；缺真机证据时进入 release-prepare 检查清单。

## 8. 依赖 ASCII 树

```text
REQ-0088-versioned-product-usage-docs
└── add-versioned-product-usage-docs
    ├── release rules / directory structure / document governance
    ├── releases/<version>/usage-docs/ templates and manifest
    ├── usage docs generate / validate command or script
    ├── release-prepare / release-publish integration
    ├── Mintlify navigation and /docs deployment boundary
    └── release validation tests and OpenSpec strict validation

REQ-0090-media-five-point-acceptance-template
└── add-media-five-point-acceptance-template
    ├── object-storage OpenSpec capability
    ├── 媒体五联验收模板落点
    ├── media-upload 横切 gate
    └── openspec validate / 文档安全扫描

REQ-0091-media-bug-four-point-acceptance-template
└── add-media-bug-four-point-acceptance-template
    ├── object-storage OpenSpec capability
    ├── 媒体类 BUG 四联验收模板落点
    ├── BUG acceptance / Sprint / Release 引用方式
    ├── media-upload 横切 gate
    └── openspec validate / 文档安全扫描

REQ-0089-workflow-subdocument-status-sync
└── improve-workflow-subdocument-status-sync
    ├── Workflow Sync 子文档状态模型
    ├── acceptance.md 验收结果回填
    ├── trace / registry / 目录阶段 / 子文档 drift check
    ├── 历史 archive scan / classify / dry-run / apply / check
    ├── /opsx-archive 与 /sprint-archive stale gate
    └── rules / skills / focused pytest

BUG-0102-miniapp-brand-list-carousel-brand-gallery-text
└── fix-miniapp-brand-list-carousel-text
    ├── miniapp-brand-list-page OpenSpec delta
    ├── 品牌列表页轮播图文案清理
    ├── 小程序静态测试或等价检查
    └── DevTools / 真机回归 evidence

REQ-0092-brand-certificate-image-thumbnails
└── add-brand-certificate-image-thumbnails
    ├── object-storage / brand-management / brand-certificate-management delta
    ├── Backend media storage and thumbnail generation
    ├── Web Admin brand / certificate list and upload preview
    ├── Miniapp brand / certificate thumbnail rendering
    ├── Store-owner Web thumbnail-first display
    ├── legacy media dry-run / apply backfill
    └── media five-point validation evidence
```

## 9. 发布计划

- 本 Sprint 主要交付 release 文档治理、媒体验收治理、workflow 治理脚本、品牌/证书缩略图媒体能力、规则文档、命令 Skill 和相关测试；同时纳入 1 个小程序品牌列表页展示修复。
- 小程序修复仅清理品牌列表页轮播图多余说明文案，不新增 API、DB、Orval 或 Docker Compose 变更。
- REQ-0092 可能影响 Backend、Web/Admin、小程序、店主 Web 和 Storage；API/DB/Orval/Docker 仅在新增字段、持久化字段或图片处理依赖时同步。
- 归档前必须通过 OpenSpec strict、Workflow Sync、Sprint Scope 校验、媒体五联验收和 focused pytest。

## 10. 关联文档

- `issues/requirements/archive/REQ-0088-versioned-product-usage-docs/requirement.md`
- `issues/requirements/archive/REQ-0088-versioned-product-usage-docs/acceptance.md`
- `issues/requirements/archive/REQ-0088-versioned-product-usage-docs/trace.md`
- `openspec/archive/2026-08-02-add-versioned-product-usage-docs/proposal.md`
- `openspec/archive/2026-08-02-add-versioned-product-usage-docs/design.md`
- `openspec/archive/2026-08-02-add-versioned-product-usage-docs/tasks.md`
- `openspec/archive/2026-08-02-add-versioned-product-usage-docs/trace.md`
- `issues/requirements/archive/REQ-0090-media-five-point-acceptance-template/requirement.md`
- `issues/requirements/archive/REQ-0090-media-five-point-acceptance-template/acceptance.md`
- `issues/requirements/archive/REQ-0090-media-five-point-acceptance-template/trace.md`
- `openspec/archive/2026-08-01-add-media-five-point-acceptance-template/proposal.md`
- `openspec/archive/2026-08-01-add-media-five-point-acceptance-template/design.md`
- `openspec/archive/2026-08-01-add-media-five-point-acceptance-template/tasks.md`
- `openspec/archive/2026-08-01-add-media-five-point-acceptance-template/trace.md`
- `issues/requirements/archive/REQ-0091-media-bug-four-point-acceptance-template/requirement.md`
- `issues/requirements/archive/REQ-0091-media-bug-four-point-acceptance-template/acceptance.md`
- `issues/requirements/archive/REQ-0091-media-bug-four-point-acceptance-template/trace.md`
- `openspec/archive/2026-08-01-add-media-bug-four-point-acceptance-template/proposal.md`
- `openspec/archive/2026-08-01-add-media-bug-four-point-acceptance-template/design.md`
- `openspec/archive/2026-08-01-add-media-bug-four-point-acceptance-template/tasks.md`
- `openspec/archive/2026-08-01-add-media-bug-four-point-acceptance-template/trace.md`
- `issues/requirements/archive/REQ-0089-workflow-subdocument-status-sync/requirement.md`
- `issues/requirements/archive/REQ-0089-workflow-subdocument-status-sync/acceptance.md`
- `issues/requirements/archive/REQ-0089-workflow-subdocument-status-sync/trace.md`
- `openspec/archive/2026-08-01-improve-workflow-subdocument-status-sync/proposal.md`
- `openspec/archive/2026-08-01-improve-workflow-subdocument-status-sync/design.md`
- `openspec/archive/2026-08-01-improve-workflow-subdocument-status-sync/tasks.md`
- `openspec/archive/2026-08-01-improve-workflow-subdocument-status-sync/trace.md`
- `docs/knowledge-base/retrospectives/sprint-016-retrospective.md`
- `issues/bugs/archive/BUG-0102-miniapp-brand-list-carousel-brand-gallery-text/bug.md`
- `issues/bugs/archive/BUG-0102-miniapp-brand-list-carousel-brand-gallery-text/acceptance.md`
- `issues/bugs/archive/BUG-0102-miniapp-brand-list-carousel-brand-gallery-text/trace.md`
- `openspec/archive/2026-08-02-fix-miniapp-brand-list-carousel-text/proposal.md`
- `openspec/archive/2026-08-02-fix-miniapp-brand-list-carousel-text/design.md`
- `openspec/archive/2026-08-02-fix-miniapp-brand-list-carousel-text/tasks.md`
- `openspec/archive/2026-08-02-fix-miniapp-brand-list-carousel-text/specs/miniapp-brand-list-page/spec.md`
- `docs/knowledge-base/best-practices/miniapp-custom-navigation.md`
- `issues/requirements/archive/REQ-0092-brand-certificate-image-thumbnails/requirement.md`
- `issues/requirements/archive/REQ-0092-brand-certificate-image-thumbnails/acceptance.md`
- `issues/requirements/archive/REQ-0092-brand-certificate-image-thumbnails/trace.md`
- `openspec/archive/2026-08-02-add-brand-certificate-image-thumbnails/proposal.md`
- `openspec/archive/2026-08-02-add-brand-certificate-image-thumbnails/design.md`
- `openspec/archive/2026-08-02-add-brand-certificate-image-thumbnails/tasks.md`
- `openspec/archive/2026-08-02-add-brand-certificate-image-thumbnails/trace.md`
- `docs/knowledge-base/best-practices/admin-list-page-consistency.md`
- `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md`
- `docs/knowledge-base/best-practices/admin-media-upload-chain.md`
- `docs/knowledge-base/retrospectives/sprint-017-retrospective.md`

## 11. 关闭记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-02 19:31:01 | `/sprint-archive sprint-017` | 6/6 Change 已归档，5 个 REQ 与 1 个 BUG 已处于 archive/done；readiness、Issue promote gate 与 stale scan 通过，Sprint 目录准备迁入 `iterations/archive/sprint-017/`。 |
| 2026-08-02 19:39:19 | `/sprint-exps sprint-017` | 已生成 Sprint 017 经验复盘并写入 `docs/knowledge-base/retrospectives/sprint-017-retrospective.md`。 |

## 12. 延后项

无。
