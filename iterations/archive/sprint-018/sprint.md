---
note: workflow-sync — workflow-sync 自动同步 — 10/10 Change archived；0 applied；Sprint `completed`
sprint_id: sprint-018
title: Sprint 018 部署、文档站治理与展示缺陷修复
status: completed
lifecycle_stage: archive
created_at: 2026-08-03 08:40:00
updated_at: 2026-08-03 20:52:16
owner: product
---

# Sprint 018 部署、文档站治理与展示缺陷修复

## 1. Sprint 目标

本 Sprint 在已完成的管理后台与小程序展示缺陷修复基础上，纳入 `REQ-0093-standardize-deployment-environment-matrix` 与 `REQ-0094-mintlify-versioned-docs-directory` 两条治理需求：前者建立部署环境矩阵与 `deploy/` 目录治理，后者建立 Mintlify 多版本产品文档站源目录治理，让 release usage docs 继续作为发布事实源，同时支持站点侧多版本浏览、latest 指针、共享截图资产和 Docker Compose 可选文档站服务。

正式范围：

- `REQ-0093-standardize-deployment-environment-matrix`

- `REQ-0094-mintlify-versioned-docs-directory`

- `BUG-0110-miniapp-card-banner-thumbnail-usage`

- `BUG-0105-admin-brand-list-logo-renders-text`

### REQ-0093-standardize-deployment-environment-matrix 要点

- 建立部署环境矩阵和 `deploy/` 目录治理，区分 local/prod 的 Compose、env 示例、部署脚本和校验入口。
- 同步目录结构、环境变量、部署文档、发布镜像输入追踪和相关校验测试。
- 默认不影响 API、数据库 Schema、Web 管理端业务 UI、小程序或 Orval。

### REQ-0094-mintlify-versioned-docs-directory 要点

- 新增或正式定义 `mintlify/` 作为 Mintlify 文档站源目录，并同步目录结构、文档治理、发布治理和 Agent 入口边界。
- `releases/vX.Y.Z/usage-docs/` 继续作为全量文档正文、manifest 和发布事实源，不改为增量目录。
- 系统截图默认集中到 `mintlify/assets/screenshots/`，按内容 hash 去重，并通过 manifest 记录来源、覆盖页面、复用版本和复用依据。
- 支持 `mintlify/docs/vX.Y.Z/`、`latest` 和发布公告入口的同步或投影策略，站点内容必须可追溯到 release 快照。
- Docker Compose 通过 `docs-site` 或等价 profile 启动 Mintlify 文档站服务，不作为默认业务服务依赖；端口通过 `.env.example` 变量治理。

### BUG-0105-admin-brand-list-logo-renders-text 要点

- 管理后台品牌列表 Logo 列必须渲染图片或缩略图。
- Logo 列不得直接展示图片 URL、对象 key、文件名或普通文本字段值。
- 未上传 Logo 和图片加载失败时必须展示设计系统内稳定占位。
- 修复需验证品牌列表字段映射与 `GET /api/v1/admin/brands` 返回的 `thumbnail_url`、`logo_url` 或等价预览 URL 一致。
- 默认不影响数据库、小程序或 Docker Compose；API/Orval 仅在实现确认 Schema 变化时触发。


### BUG-0110-miniapp-card-banner-thumbnail-usage 要点

- 商品卡片、品牌卡片、证书卡片和 Banner 应优先使用缩略图或符合性能策略的轻量展示图。
- 缩略图缺失、为空或加载失败时，应安全回退原图、占位或首字母占位。
- 详情页、图片预览、PDF 打开、Banner 跳转和卡片点击能力不得回归。
- 若实现新增或调整公开 API 响应字段，必须同步 OpenAPI、Orval、docs 和 tests。

## 2. Scope

| 类型 | 编号 | 标题 | 状态 | 估算 | 说明 |
|---|---|---|---|---:|---|
| REQ | REQ-0094-mintlify-versioned-docs-directory | Mintlify 多版本产品文档目录与站点浏览 | done | 8 人天 | archived `add-mintlify-versioned-docs-site`（2026-08-03 19:40:00） |
| REQ | REQ-0093-standardize-deployment-environment-matrix | 标准化部署环境矩阵与 deploy 目录治理 | done | 3 人天 | archived `standardize-deployment-environment-matrix`（2026-08-03 20:35:23） |
| BUG | BUG-0105-admin-brand-list-logo-renders-text | 管理后台品牌列表第一列品牌 Logo 显示为文字 | done | 1 人天 | archived `fix-admin-brand-list-logo-rendering`（2026-08-03 09:01:17） |
| BUG | BUG-0109-miniapp-home-button-one-time-failure | 小程序返回首页按钮每个页面点击一次后失效 | done | 1 人天 | archived `fix-miniapp-home-navigation-repeat-click`（2026-08-03 10:22:09） |
| BUG | BUG-0108-admin-certificate-edit-file-ready-text-and-image-info | 管理后台证书编辑弹窗文件就绪文案冗余且图片信息无法正常显示 | done | 3 人天 | archived `fix-admin-certificate-edit-file-image-display`（2026-08-03 12:51:57） |
| BUG | BUG-0110-miniapp-card-banner-thumbnail-usage | 小程序卡片与 Banner 可能未统一使用缩略图 | done | 3 人天 | archived `fix-miniapp-card-banner-thumbnail-usage`（2026-08-03 13:37:15） |
| BUG | BUG-0107-admin-certificate-list-main-image-name-only | 管理后台证书列表证书字段额外显示图片或文件名称 | done | 1 人天 | archived `fix-admin-certificate-list-main-image-name-only`（2026-08-03 12:01:13） |
| BUG | BUG-0104-admin-sku-list-headers-wrap | 管理后台 SKU 列表表头字段换行 | done | 1 人天 | archived `fix-admin-sku-list-header-wrapping`（2026-08-03 09:02:03） |
| BUG | BUG-0106-admin-brand-edit-logo-uploaded-text | 管理后台品牌编辑弹窗 Logo 旁显示冗余已上传文案 | done | 1 人天 | archived `fix-admin-brand-edit-logo-uploaded-text`（2026-08-03 12:51:02） |
| BUG | BUG-0103-admin-category-name-chinese-parentheses | 管理后台瓷砖类目名称不支持中文括号 | done | 3 人天 | archived `fix-admin-category-name-chinese-parentheses`（2026-08-03 08:40:04） |

<!-- workflow-sync:scope-requirements:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| REQ-0094 | Mintlify 多版本产品文档目录与站点浏览 | P1 | done | archived `add-mintlify-versioned-docs-site`（2026-08-03 19:40:00） |
| REQ-0093 | 标准化部署环境矩阵与 deploy 目录治理 | P1 | done | archived `standardize-deployment-environment-matrix`（2026-08-03 20:35:23） |
<!-- workflow-sync:scope-requirements:end -->

<!-- workflow-sync:scope-bugs:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| BUG-0105 | 管理后台品牌列表第一列品牌 Logo 显示为文字 | medium | done | archived `fix-admin-brand-list-logo-rendering`（2026-08-03 09:01:17） |
| BUG-0109 | 小程序返回首页按钮每个页面点击一次后失效 | high | done | archived `fix-miniapp-home-navigation-repeat-click`（2026-08-03 10:22:09） |
| BUG-0108 | 管理后台证书编辑弹窗文件就绪文案冗余且图片信息无法正常显示 | medium | done | archived `fix-admin-certificate-edit-file-image-display`（2026-08-03 12:51:57） |
| BUG-0110 | 小程序卡片与 Banner 可能未统一使用缩略图 | high | done | archived `fix-miniapp-card-banner-thumbnail-usage`（2026-08-03 13:37:15） |
| BUG-0107 | 管理后台证书列表证书字段额外显示图片或文件名称 | low | done | archived `fix-admin-certificate-list-main-image-name-only`（2026-08-03 12:01:13） |
| BUG-0104 | 管理后台 SKU 列表表头字段换行 | low | done | archived `fix-admin-sku-list-header-wrapping`（2026-08-03 09:02:03） |
| BUG-0106 | 管理后台品牌编辑弹窗 Logo 旁显示冗余已上传文案 | low | done | archived `fix-admin-brand-edit-logo-uploaded-text`（2026-08-03 12:51:02） |
| BUG-0103 | 管理后台瓷砖类目名称不支持中文括号 | medium | done | archived `fix-admin-category-name-chinese-parentheses`（2026-08-03 08:40:04） |
<!-- workflow-sync:scope-bugs:end -->

<!-- workflow-sync:scope-changes:start -->
| Change ID | 关联需求 | 状态 | Sprint 目标 |
|---|---|---|---|
| `add-mintlify-versioned-docs-site` | REQ-0094-mintlify-versioned-docs-directory | archived | archived `add-mintlify-versioned-docs-site`（2026-08-03 19:40:00） |
| `standardize-deployment-environment-matrix` | REQ-0093-standardize-deployment-environment-matrix | archived | archived `standardize-deployment-environment-matrix`（2026-08-03 20:35:23） |
| `fix-admin-brand-list-logo-rendering` | BUG-0105-admin-brand-list-logo-renders-text | archived | archived `fix-admin-brand-list-logo-rendering`（2026-08-03 09:01:17） |
| `fix-miniapp-home-navigation-repeat-click` | BUG-0109-miniapp-home-button-one-time-failure | archived | archived `fix-miniapp-home-navigation-repeat-click`（2026-08-03 10:22:09） |
| `fix-admin-certificate-edit-file-image-display` | BUG-0108-admin-certificate-edit-file-ready-text-and-image-info | archived | archived `fix-admin-certificate-edit-file-image-display`（2026-08-03 12:51:57） |
| `fix-miniapp-card-banner-thumbnail-usage` | BUG-0110-miniapp-card-banner-thumbnail-usage | archived | archived `fix-miniapp-card-banner-thumbnail-usage`（2026-08-03 13:37:15） |
| `fix-admin-certificate-list-main-image-name-only` | BUG-0107-admin-certificate-list-main-image-name-only | archived | archived `fix-admin-certificate-list-main-image-name-only`（2026-08-03 12:01:13） |
| `fix-admin-sku-list-header-wrapping` | BUG-0104-admin-sku-list-headers-wrap | archived | archived `fix-admin-sku-list-header-wrapping`（2026-08-03 09:02:03） |
| `fix-admin-brand-edit-logo-uploaded-text` | BUG-0106-admin-brand-edit-logo-uploaded-text | archived | archived `fix-admin-brand-edit-logo-uploaded-text`（2026-08-03 12:51:02） |
| `fix-admin-category-name-chinese-parentheses` | BUG-0103-admin-category-name-chinese-parentheses | archived | archived `fix-admin-category-name-chinese-parentheses`（2026-08-03 08:40:04） |
<!-- workflow-sync:scope-changes:end -->

Change：已纳入 2 个需求治理 Change 与 8 个 BUG 修复 Change。执行开发与归档时以 Scope 表逐项状态为准。

## 3. 工作量与容量

| 项 | 值 |
|---|---:|
| developers | 2 |
| testers | 1 |
| capacity_person_days | 30 |
| estimated_story_points | 25 |
| estimated_person_days | 25 |
| capacity_usage | 83.33% |
| fix_buffer_person_days | 5 |
| fix_buffer_ratio | 16.67% |

容量门禁：Pass。`project.yaml` 未提供显式 Sprint 容量，沿用 sprint-017 已确认容量基线 2 dev + 1 tester / 30 人天。本 Sprint 当前纳入 2 个 REQ、8 个 BUG、2 个治理 Change 与 8 个 fix Change，估算 25 人天，占用 83.33%，低于 30 人天容量，满足容量硬门禁。fix buffer 5 人天 / 16.67%，低于 30% 建议缓冲；实现时应优先完成 REQ-0093/REQ-0094 的目录/脚本/Compose 骨架和发布校验主链路，历史迁移和生产托管细节按 tasks 明确边界控制范围。

## 4. 里程碑

| 阶段 | 目标日期 | 交付 |
|---|---|---|
| 规划确认 | 2026-08-03 08:40:00 | Sprint 四件套、BUG/Change trace 同步 |
| 实现完成 | 2026-08-05 18:00:00 | 管理后台品牌列表 Logo 列渲染修复、占位/fallback、相关测试完成 |
| 文档站治理完成 | 2026-08-12 18:00:00 | `mintlify/` 目录、站点投影、共享截图资产、usage docs / release 校验和 Compose profile 完成 |
| 验收归档 | 2026-08-07 18:00:00 | `fix-admin-brand-list-logo-rendering` 验收通过并完成 OpenSpec archive |

## 5. 风险

| 风险 | 缓解 |
|---|---|
| Logo 列字段映射错误，图片仍不显示 | 实现前确认品牌列表响应字段；测试覆盖 `thumbnail_url`、`logo_url` 与缺失字段 |
| 图片加载失败或无 Logo 时出现破图、空白错位或布局跳动 | 固定 Logo 单元格尺寸，补齐 fallback 和占位状态 |
| 修复时误改 API Schema 却未同步 Orval | 默认不改 API；若改响应字段，必须同步 OpenAPI、Orval、API 文档和测试 |
| 直接展示对象 key、内部路径或 URL 文本 | 验收 AC-001/AC-003 明确禁止；测试覆盖不显示文本 URL/key |
| 列渲染调整影响品牌列表操作 | 回归品牌搜索、编辑入口、上下架和分页 |
| REQ-0093 与 REQ-0094 都触及部署/目录治理，可能互相改动同一规则或 Compose 文档 | 实现时先处理目录边界和环境变量矩阵，再落 Mintlify docs-site profile，避免重复改写同一段规范 |
| REQ-0094 涉及目录、发布、部署和脚本多条治理链路，易出现文档与校验不同步 | 以 `tasks.md` 分组推进，目录规则、usage docs 校验、release 校验、Compose config 和 pytest 必须一并验收 |
| 共享截图为了节省空间误复用不属于历史版本的界面 | manifest 必须记录 `reuse_reason`，界面/字段/流程/权限变化时新增截图 |
| Mintlify Compose 服务误变成默认业务依赖 | 使用 `docs-site` profile，默认 `docker compose up` 不启动文档站，并补充 `.env.example` 与部署说明 |
| Sprint fix buffer 低于 30% 建议值 | 不再扩张低优先级范围；若 REQ-0093/REQ-0094 实现发现真实生产托管、域名或迁移扩张需求，拆为后续 REQ |

## 6. 知识库承接

| 来源 | 承接动作 |
|---|---|
| `docs/knowledge-base/retrospectives/sprint-017-retrospective.md` | 承接媒体 evidence 分层经验，本次至少记录字段映射、URL 渲染、fallback 和列表操作回归证据。 |
| `docs/knowledge-base/retrospectives/sprint-017-retrospective.md` | 承接 high token 阶段 summary-first 经验，apply 阶段优先读取 Change tasks、BUG acceptance 和聚焦代码片段。 |
| `docs/knowledge-base/retrospectives/sprint-017-retrospective.md` | 承接 usage docs gate 经验，release-prepare 必须保持 generate / skip / pending_confirmation 三态，不为无文档版本生成空目录。 |
| `docs/02-deployment.md`、`rules/environment.md`、`rules/port-management.md` | REQ-0094 实现需同步 Mintlify Compose profile、宿主机端口变量和本地/演示部署说明。 |
| `docs/knowledge-base/best-practices/admin-list-page-consistency.md` | Logo 列修复不得破坏管理端列表分页、筛选、fixed toast、操作列和表格布局基准。 |
| `docs/knowledge-base/best-practices/admin-media-upload-chain.md` | 媒体展示修复需验证受控 URL、同会话/刷新后回显语义和不暴露对象 key 或内部路径。 |

## 7. 横切预防清单

- [ ] admin-list：Logo 列修复不得破坏品牌列表分页结构、筛选、操作列和表格布局。
- [ ] admin-list：图片加载中、成功、失败和占位状态不得造成行高或列宽明显跳动。
- [ ] media-upload：前端不得直连未授权对象存储，Logo 展示必须使用后端返回的受控 URL 或等价预览 URL。
- [ ] media-upload：不得在 UI 中展示对象 key、内部路径、文件名噪音、异常堆栈或调试文案。
- [ ] API：若 `GET /api/v1/admin/brands` 响应 Schema 变化，必须同步 OpenAPI、Orval、API 文档和测试。
- [ ] acceptance：按 `BUG-0105` AC-001 至 AC-006 回归验收，并记录无需 Orval 或已同步 Orval 的结论。
- [ ] knowledge-base：实现后评估是否需要沉淀 `docs/knowledge-base/incidents/`；若无复用价值，记录不适用。
- [ ] usage-docs：release 快照仍为事实源，`mintlify/` 只作为站点源目录和投影目录，不得绕过 release manifest 改旧版本语义。
- [ ] screenshots：共享截图必须有 hash、来源、覆盖页面和复用依据；界面、字段、流程或权限边界变化时新增截图。
- [ ] docker-compose：Mintlify 文档站必须通过 profile 启用，默认业务服务启动链路不依赖 docs-site。
- [ ] deploy：`deploy/`、`deploy-local/`、`deploy-prod/` 与脚本入口必须符合目录边界，不引入根目录业务代码或真实密钥。
- [ ] deploy：Compose 与 env 示例需保持同一治理边界，并能覆盖 SQLite/MySQL + MinIO/COS 的本地矩阵与生产矩阵。
- [ ] release-image：Compose 文件、deploy 脚本和 env 示例变更需纳入镜像构建输入追踪或发布前校验说明。

## 8. 依赖 ASCII 树

```text
BUG-0105-admin-brand-list-logo-renders-text
└── fix-admin-brand-list-logo-rendering
    ├── openspec/archive/2026-08-03-fix-admin-brand-list-logo-rendering/proposal.md
    ├── openspec/archive/2026-08-03-fix-admin-brand-list-logo-rendering/tasks.md
    ├── openspec/archive/2026-08-03-fix-admin-brand-list-logo-rendering/specs/brand-management/spec.md
    ├── issues/bugs/archive/BUG-0105-admin-brand-list-logo-renders-text/acceptance.md
    └── docs/knowledge-base/best-practices/{admin-list-page-consistency,admin-media-upload-chain}.md

REQ-0094-mintlify-versioned-docs-directory
└── add-mintlify-versioned-docs-site
    ├── openspec/archive/2026-08-03-add-mintlify-versioned-docs-site/proposal.md
    ├── openspec/archive/2026-08-03-add-mintlify-versioned-docs-site/design.md
    ├── openspec/archive/2026-08-03-add-mintlify-versioned-docs-site/tasks.md
    ├── openspec/archive/2026-08-03-add-mintlify-versioned-docs-site/specs/product-release-management/spec.md
    ├── openspec/archive/2026-08-03-add-mintlify-versioned-docs-site/specs/deployment/spec.md
    ├── issues/requirements/archive/REQ-0094-mintlify-versioned-docs-directory/acceptance.md
    └── docs/02-deployment.md + rules/{directory-structure,document-governance,release,environment,port-management}.md

REQ-0093-standardize-deployment-environment-matrix
└── standardize-deployment-environment-matrix
    ├── openspec/archive/2026-08-03-standardize-deployment-environment-matrix/proposal.md
    ├── openspec/archive/2026-08-03-standardize-deployment-environment-matrix/design.md
    ├── openspec/archive/2026-08-03-standardize-deployment-environment-matrix/tasks.md
    ├── openspec/archive/2026-08-03-standardize-deployment-environment-matrix/specs/deployment/spec.md
    ├── openspec/archive/2026-08-03-standardize-deployment-environment-matrix/specs/deployment-image-build/spec.md
    └── issues/requirements/archive/REQ-0093-standardize-deployment-environment-matrix/acceptance.md
```

## 9. 发布计划

该 Sprint 默认随下一个产品版本发布。已完成的 BUG 修复按对应验收报告进入发布说明；REQ-0094 属于文档站、发布治理和部署辅助能力，发布前需验证 release usage docs 快照、`mintlify/` 站点投影、共享截图 manifest、公开安全和 Docker Compose `docs-site` profile；REQ-0093 属于部署环境矩阵治理，发布前需验证 `deploy/` 目录、env 示例、Compose/脚本入口、部署文档和镜像构建输入追踪。若实现只修改文档/脚本/Compose，不需要 Orval；若新增 API 字段则必须另行同步 OpenAPI、Orval、API 文档和测试。

## 10. 关联文档

| 类型 | 路径 |
|---|---|
| BUG | `issues/bugs/archive/BUG-0105-admin-brand-list-logo-renders-text/` |
| REQ | `issues/requirements/archive/REQ-0093-standardize-deployment-environment-matrix/` |
| REQ | `issues/requirements/archive/REQ-0094-mintlify-versioned-docs-directory/` |
| Change | `openspec/archive/2026-08-03-fix-admin-brand-list-logo-rendering/` |
| Change | `openspec/archive/2026-08-03-standardize-deployment-environment-matrix/` |
| Change | `openspec/archive/2026-08-03-add-mintlify-versioned-docs-site/` |
| Spec Delta | `openspec/archive/2026-08-03-fix-admin-brand-list-logo-rendering/specs/brand-management/spec.md` |
| Spec Delta | `openspec/archive/2026-08-03-standardize-deployment-environment-matrix/specs/deployment/spec.md` |
| Spec Delta | `openspec/archive/2026-08-03-add-mintlify-versioned-docs-site/specs/product-release-management/spec.md` |
| Spec Delta | `openspec/archive/2026-08-03-add-mintlify-versioned-docs-site/specs/deployment/spec.md` |
| Admin List BP | `docs/knowledge-base/best-practices/admin-list-page-consistency.md` |
| Media Upload BP | `docs/knowledge-base/best-practices/admin-media-upload-chain.md` |

## 11. 关闭记录

- 2026-08-03 20:50:43 `/sprint-archive sprint-018`：10/10 Change 已归档，readiness、stale scan 与 issue promote gate 通过；Sprint 目录迁移到 `iterations/archive/sprint-018/`。
- AI Usage：Fact Sheet 显示 snapshot 存在但为 `estimated_fallback` 且 stale；本次关闭记录该 warning，未声明真实 token usage。

## 12. 复盘记录

- 2026-08-03 20:54:07 `/sprint-exps sprint-018`：已生成复盘文档 `docs/knowledge-base/retrospectives/sprint-018-retrospective.md`；行动项仅输出 capture 文案，未自动创建 Issue。
