---
note: workflow-sync — workflow-sync 自动同步 — 18/18 Change archived；0 applied；Sprint `completed`
created_at: 2026-08-07 09:06:21
updated_at: 2026-08-12 00:25:00
sprint_id: sprint-022
status: completed
---

# sprint-022

## 0. 关闭记录

2026-08-12 00:20:00 执行 `/sprint-archive sprint-022`：18/18 Change 已归档，229/229 tasks 完成，Sprint close stale scan 与 archive readiness 均通过；Sprint 目录进入 archive 阶段。

复盘文档：`docs/knowledge-base/retrospectives/sprint-022-retrospective.md`。

## 1. 目标

新增 `/spec-study` Harness 学习同步技能，支持学习其他项目治理资产并在用户确认后应用到本项目；同时统一 `/spec-study` 学习报告与 `/spec-opt` 治理迭代日志的 `docs/spec-logs/` 命名约定，并约束同一次 `/spec-study` 流程只生成一份正式学习报告。

追加修复微信小程序商品详情页媒体加载慢问题，补齐详情页缩略图覆盖范围，降低 SKU 详情首屏大图加载风险。

追加纳入 REQ-0103 商品召回列表排序置顶能力，完成管理端 SKU 召回排序配置、后端公开列表排序与小程序普通商品列表展示顺序的 OpenSpec 准备。

追加纳入 REQ-0104 小程序召回置顶商品“置顶”标识展示能力，基于 REQ-0103 的后端置顶生效判断补齐前台可解释性，同时保持新品榜、热销榜无置顶逻辑的边界。

追加纳入 REQ-0106 Banner 标题隐藏与小程序前台标题遮罩移除能力，降低后台运营无效录入成本，并让小程序首页与品牌列表页 Banner 回到图片驱动展示。

追加纳入 REQ-0107 微信小程序和 Web 页面真实用户加载耗时监控能力，建设轻量自建 RUM，采集真实用户页面加载耗时并为后端聚合、管理端性能观测与发布性能回归提供依据。

追加纳入 BUG-0126 小程序品牌链路图片加载慢修复，聚焦品牌列表、品牌详情页和品牌分类商品列表的缩略图体积、历史缩略图回填、懒加载与 `/media` 缓存策略。

追加纳入 REQ-0108 Web 管理后台 Banner 列表显示内容优化，聚焦 Banner 列只显示主图，并新增独立跳转对象列展示品牌名称、SKU 名称、专题名称、外部链接或无跳转占位。

追加纳入 REQ-0109 管理后台主题切换入口与模式收敛，聚焦主题入口移入用户菜单、可见模式收敛为暗色旗舰与跟随系统，并同步历史主题偏好兼容、API/OpenAPI/Orval 与前端测试边界。

追加纳入 BUG-0127 管理后台日志审计表数据加载慢修复，聚焦日志列表 UNION 查询过滤下推、指定日志类型单表路径、全量计数与摘要指标解耦、SQLite/MySQL 索引和查询计划回归。

追加纳入 BUG-0128 管理后台身份展示伪邮箱修复，聚焦用户菜单栏移除邮箱副标题、个人资料页顶部身份栏不再拼接伪邮箱，并保留个人资料联系邮箱编辑入口。

追加纳入 REQ-0110 用户管理页维护用户联系邮箱和手机号码能力，聚焦管理端添加/编辑用户联系信息、列表状态列后新增联系邮箱与手机号码独立列、空值显示 `-`、搜索范围扩展和 API/OpenAPI/Orval/测试同步。

Sprint 目标编号列表：

- add-spec-sync-skill
- rename-spec-sync-to-spec-study
- add-spec-logs-governance-log-convention
- avoid-duplicate-spec-study-reports
- BUG-0125-miniapp-sku-detail-media-original-load
- REQ-0103-product-recall-list-pin-priority
- REQ-0104-miniapp-recall-pinned-product-badge
- REQ-0106-admin-banner-title-hidden
- add-spec-logs-change-history
- apply-projectmoonbox-governance-learnings
- refine-capture-explore-modify-stage-routing
- REQ-0107-real-user-page-load-rum
- BUG-0126-miniapp-brand-media-slow-load
- REQ-0108-admin-banner-list-display-optimization
- REQ-0109-admin-theme-user-menu-modes
- BUG-0127-admin-log-audit-slow-load
- BUG-0128-admin-user-menu-email-subtitle
- REQ-0110-admin-user-contact-info-management

## 2. Scope

| 类型 | 编号 | 标题 | 状态 | 估算 | 说明 |
|---|---|---|---|---:|---|
| REQ | REQ-0103-product-recall-list-pin-priority | 商品召回列表支持少量商品排序置顶 | done | 3 人天 | archived `add-product-recall-list-pin-priority`（2026-08-08 07:18:00） |
| REQ | REQ-0104-miniapp-recall-pinned-product-badge | 小程序召回置顶商品展示“置顶”标识 | done | 1 人天 | archived `update-miniapp-recall-pinned-product-badge`（2026-08-11 23:18:40） |
| REQ | REQ-0106-admin-banner-title-hidden | Banner 标题隐藏与小程序前台标题遮罩移除 | done | 1 人天 | archived `update-banner-title-hidden-display`（2026-08-11 23:15:05） |
| REQ | REQ-0107-real-user-page-load-rum | 微信小程序和 Web 页面真实用户加载耗时监控 | done | 5 人天 | archived `add-real-user-page-load-rum`（2026-08-11 22:11:27） |
| REQ | REQ-0108-admin-banner-list-display-optimization | Web 管理后台 Banner 列表显示内容优化 | done | 1 人天 | archived `update-admin-banner-list-display-optimization`（2026-08-11 23:19:21） |
| REQ | REQ-0109-admin-theme-user-menu-modes | 管理后台主题切换入口与模式收敛 | done | 1 人天 | archived `update-admin-theme-user-menu-modes`（2026-08-11 09:26:44） |
| REQ | REQ-0110-admin-user-contact-info-management | 用户管理页支持维护用户联系邮箱和手机号码 | done | 3 人天 | archived `update-admin-user-contact-info-management`（2026-08-12 00:12:00） |
| BUG | BUG-0125-miniapp-sku-detail-media-original-load | 微信小程序商品详情页媒体加载慢 | done | 1 人天 | archived `fix-miniapp-sku-detail-media-thumbnails`（2026-08-07 22:55:00） |
| BUG | BUG-0126-miniapp-brand-media-slow-load | 小程序品牌链路图片加载速度慢 | done | 3 人天 | archived `fix-miniapp-brand-media-performance`（2026-08-11 23:25:07） |
| BUG | BUG-0127-admin-log-audit-slow-load | 管理后台日志审计表数据加载很慢 | done | 3 人天 | archived `fix-admin-log-audit-slow-load`（2026-08-11 23:36:00） |
| BUG | BUG-0128-admin-user-menu-email-subtitle | 管理后台身份展示不应显示伪邮箱 | done | 1 人天 | archived `fix-admin-identity-fake-email-display`（2026-08-11 22:25:00） |
| Change | add-spec-sync-skill | add spec sync skill | archived | — | archived `add-spec-sync-skill`（2026-08-07 09:20:34） |
| Change | rename-spec-sync-to-spec-study | rename spec sync to spec study | archived | 0.25 人天 | archived `rename-spec-sync-to-spec-study`（2026-08-07 09:56:44） |
| Change | add-spec-logs-governance-log-convention | add spec logs governance log convention | archived | 0.25 人天 | archived `add-spec-logs-governance-log-convention`（2026-08-07 10:46:39） |
| Change | avoid-duplicate-spec-study-reports | avoid duplicate spec study reports | archived | 0.25 人天 | archived `avoid-duplicate-spec-study-reports`（2026-08-07 11:54:47） |
| Change | add-spec-logs-change-history | add spec logs change history | archived | 0.25 人天 | archived `add-spec-logs-change-history`（2026-08-11 23:24:54） |
| Change | apply-projectmoonbox-governance-learnings | apply projectmoonbox governance learnings | archived | 2 人天 | archived `apply-projectmoonbox-governance-learnings`（2026-08-10 23:28:57） |
| Change | refine-capture-explore-modify-stage-routing | refine capture explore modify stage routing | archived | 0.25 人天 | archived `refine-capture-explore-modify-stage-routing`（2026-08-11 23:28:30） |

### 包含需求

<!-- workflow-sync:scope-requirements:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| REQ-0103 | 商品召回列表支持少量商品排序置顶 | P1 | done | archived `add-product-recall-list-pin-priority`（2026-08-08 07:18:00） |
| REQ-0104 | 小程序召回置顶商品展示“置顶”标识 | P1 | done | archived `update-miniapp-recall-pinned-product-badge`（2026-08-11 23:18:40） |
| REQ-0106 | Banner 标题隐藏与小程序前台标题遮罩移除 | P1 | done | archived `update-banner-title-hidden-display`（2026-08-11 23:15:05） |
| REQ-0107 | 微信小程序和 Web 页面真实用户加载耗时监控 | P1 | done | archived `add-real-user-page-load-rum`（2026-08-11 22:11:27） |
| REQ-0108 | Web 管理后台 Banner 列表显示内容优化 | P1 | done | archived `update-admin-banner-list-display-optimization`（2026-08-11 23:19:21） |
| REQ-0109 | 管理后台主题切换入口与模式收敛 | P1 | done | archived `update-admin-theme-user-menu-modes`（2026-08-11 09:26:44） |
| REQ-0110 | 用户管理页支持维护用户联系邮箱和手机号码 | P1 | done | archived `update-admin-user-contact-info-management`（2026-08-12 00:12:00） |
<!-- workflow-sync:scope-requirements:end -->

<!-- workflow-sync:scope-changes:start -->
| Change ID | 关联需求 | 状态 | Sprint 目标 |
|---|---|---|---|
| `add-spec-sync-skill` | — | archived | archived `add-spec-sync-skill`（2026-08-07 09:20:34） |
| `rename-spec-sync-to-spec-study` | — | archived | archived `rename-spec-sync-to-spec-study`（2026-08-07 09:56:44） |
| `add-spec-logs-governance-log-convention` | — | archived | archived `add-spec-logs-governance-log-convention`（2026-08-07 10:46:39） |
| `avoid-duplicate-spec-study-reports` | — | archived | archived `avoid-duplicate-spec-study-reports`（2026-08-07 11:54:47） |
| `fix-miniapp-sku-detail-media-thumbnails` | BUG-0125-miniapp-sku-detail-media-original-load | archived | archived `fix-miniapp-sku-detail-media-thumbnails`（2026-08-07 22:55:00） |
| `add-product-recall-list-pin-priority` | REQ-0103-product-recall-list-pin-priority | archived | archived `add-product-recall-list-pin-priority`（2026-08-08 07:18:00） |
| `update-miniapp-recall-pinned-product-badge` | REQ-0104-miniapp-recall-pinned-product-badge | archived | archived `update-miniapp-recall-pinned-product-badge`（2026-08-11 23:18:40） |
| `add-spec-logs-change-history` | — | archived | archived `add-spec-logs-change-history`（2026-08-11 23:24:54） |
| `update-banner-title-hidden-display` | REQ-0106-admin-banner-title-hidden | archived | archived `update-banner-title-hidden-display`（2026-08-11 23:15:05） |
| `add-real-user-page-load-rum` | REQ-0107-real-user-page-load-rum | archived | archived `add-real-user-page-load-rum`（2026-08-11 22:11:27） |
| `apply-projectmoonbox-governance-learnings` | — | archived | archived `apply-projectmoonbox-governance-learnings`（2026-08-10 23:28:57） |
| `fix-miniapp-brand-media-performance` | BUG-0126-miniapp-brand-media-slow-load | archived | archived `fix-miniapp-brand-media-performance`（2026-08-11 23:25:07） |
| `update-admin-banner-list-display-optimization` | REQ-0108-admin-banner-list-display-optimization | archived | archived `update-admin-banner-list-display-optimization`（2026-08-11 23:19:21） |
| `update-admin-theme-user-menu-modes` | REQ-0109-admin-theme-user-menu-modes | archived | archived `update-admin-theme-user-menu-modes`（2026-08-11 09:26:44） |
| `fix-admin-log-audit-slow-load` | BUG-0127-admin-log-audit-slow-load | archived | archived `fix-admin-log-audit-slow-load`（2026-08-11 23:36:00） |
| `refine-capture-explore-modify-stage-routing` | — | archived | archived `refine-capture-explore-modify-stage-routing`（2026-08-11 23:28:30） |
| `fix-admin-identity-fake-email-display` | BUG-0128-admin-user-menu-email-subtitle | archived | archived `fix-admin-identity-fake-email-display`（2026-08-11 22:25:00） |
| `update-admin-user-contact-info-management` | REQ-0110-admin-user-contact-info-management | archived | archived `update-admin-user-contact-info-management`（2026-08-12 00:12:00） |
<!-- workflow-sync:scope-changes:end -->

<!-- workflow-sync:scope-bugs:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| BUG-0125 | 微信小程序商品详情页媒体加载慢 | high | done | archived `fix-miniapp-sku-detail-media-thumbnails`（2026-08-07 22:55:00） |
| BUG-0126 | 小程序品牌链路图片加载速度慢 | high | done | archived `fix-miniapp-brand-media-performance`（2026-08-11 23:25:07） |
| BUG-0127 | 管理后台日志审计表数据加载很慢 | medium | done | archived `fix-admin-log-audit-slow-load`（2026-08-11 23:36:00） |
| BUG-0128 | 管理后台身份展示不应显示伪邮箱 | low | done | archived `fix-admin-identity-fake-email-display`（2026-08-11 22:25:00） |
<!-- workflow-sync:scope-bugs:end -->

REQ：`REQ-0103` 已纳入正式范围；BUG：3 个已纳入正式范围，优先级高于新增体验能力；当前完成度与验收风险以 Scope 表状态、关联 Change 和 acceptance-report 为准。

Change：BUG-0127 的 OpenSpec 修复 Change `fix-admin-log-audit-slow-load` 已 apply 完成，待验收后归档。其余范围项执行与归档状态以 Scope 表和派生 Change 表为准。

## 3. 验收

- 技能入口、命令速查和上下文预算规则已同步。
- OpenSpec 与目录结构校验通过。
- BUG-0125 修复完成前，Sprint 验收不得保持 passed；需补齐后端接口测试、小程序静态测试和媒体四联 evidence。
- BUG-0126 修复完成前，Sprint 验收不得保持 passed；需补齐品牌列表、品牌详情页、品牌分类商品列表的小程序真机/DevTools evidence、缩略图对象审计与 `/media` 缓存验证。
- BUG-0127 修复完成前，Sprint 验收不得保持 passed；需补齐日志列表查询计划证据、分页响应耗时对比、指标聚合不阻塞首屏的验证，以及 SQLite/MySQL 索引或迁移覆盖。

## 4. 工作量与容量

| 指标 | 值 |
|---|---:|
| 容量 | 30 人天 |
| 估算 | 23.25 人天 |
| 容量占用 | 77.50% |
| 剩余 fix 缓冲 | 6.75 人天 |

容量已修正为 30 人天；当前总估算 23.25 人天，容量占用约 77.50%，剩余 fix 缓冲约 22.50%，未超过容量门禁但低于推荐 30% fix 缓冲。BUG-0128 仅涉及 Web 前端展示逻辑与测试，已创建 OpenSpec 修复 Change，后续可进入 apply。

## 5. 知识库承接

- `docs/knowledge-base/retrospectives/sprint-021-retrospective.md`：继续遵守 Sprint Scope 一致性校验，新增范围必须同时出现在目标编号列表、Scope 主表和派生表。
- `docs/knowledge-base/best-practices/admin-list-page-consistency.md`：管理后台列表修复必须保持筛选、分页、空态、加载态和错误反馈一致，避免只优化后端而破坏审计表交互一致性。
- `docs/knowledge-base/incidents/miniapp-product-card-thumbnail-url-regression.md`：媒体性能修复不得只改 URL 形态，必须验证 `/media/{object_key}` 可访问和小程序实际请求路径。
- `docs/knowledge-base/incidents/media-thumbnail-copy-regression.md`：缩略图对象存在不等于有性能收益，验收需检查大小、像素或 bytes 差异。

## 6. 横切预防清单

| 项 | 要求 |
|---|---|
| API 契约 | SKU 详情接口需区分展示缩略图、预览原图、视频 URL 和封面 URL |
| 小程序 | 详情页首屏图片请求 `.thumb`，预览仍走原图 |
| 品牌链路 | 品牌列表、品牌详情页、品牌分类商品列表必须优先使用有效缩略图，并启用非首屏懒加载 |
| 媒体四联 | key、object、URL、render 均需记录 evidence |
| 历史对象 | 如发现缺失或无收益缩略图，记录 dry-run / apply / 幂等摘要 |
| Scope 校验 | 每次新增 BUG/Change 后运行 `validate-sprint-scope.py sprint-022 --item <id>` |
| RUM 观测 | 端侧上报必须采样、脱敏并可降级；小程序真实环境证据不得写作自动通过；API/DB/Orval/docs/tests 同步作为后续 Change 门禁 |
| 主题偏好 | 用户菜单主题按钮不得新增裸 Hex；主题枚举收敛必须同步 API/OpenAPI/Orval，历史 `light` 与 `comfort_dark` 需兼容归一 |
| 日志审计性能 | 列表查询需优先按 log_type/date/status/client_type/result 下推过滤；默认分页不得被全量 UNION 排序、COUNT 或同步指标聚合阻塞；验收需保留查询计划和耗时证据 |

## 7. 依赖树

```text
sprint-022
├── 已归档治理 Change
│   ├── add-spec-sync-skill
│   ├── rename-spec-sync-to-spec-study
│   ├── add-spec-logs-governance-log-convention
│   └── avoid-duplicate-spec-study-reports
├── BUG-0125-miniapp-sku-detail-media-original-load
    └── 修复 Change fix-miniapp-sku-detail-media-thumbnails 已归档
└── REQ-0103-product-recall-list-pin-priority
│   └── 需求 Change add-product-recall-list-pin-priority 已归档
└── REQ-0104-miniapp-recall-pinned-product-badge
    └── 需求 Change update-miniapp-recall-pinned-product-badge 已归档
└── REQ-0107-real-user-page-load-rum
    └── 需求 Change add-real-user-page-load-rum 已归档
└── REQ-0109-admin-theme-user-menu-modes
    └── 需求 Change update-admin-theme-user-menu-modes 已归档
└── BUG-0127-admin-log-audit-slow-load
    └── 修复 Change fix-admin-log-audit-slow-load 已归档
└── BUG-0128-admin-user-menu-email-subtitle
    └── 修复 Change fix-admin-identity-fake-email-display 已归档
```
