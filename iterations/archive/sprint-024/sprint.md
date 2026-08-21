---
note: workflow-sync — workflow-sync 自动同步 — 5/5 Change archived；0 applied；Sprint `completed`
created_at: 2026-08-21 08:18:18
updated_at: 2026-08-21 14:42:16
---

# sprint-024 规划

## 1. 目标

### Sprint 目标编号列表

- apply-moonbox-governance-quality-learnings
- BUG-0130-miniapp-home-no-jump-banner-internal-title
- apply-deepseek-harness-doc-governance-learnings
- BUG-0131-miniapp-sku-detail-carousel-original-image-height
- default-review-approve-command

### apply-moonbox-governance-quality-learnings 要点

应用 MoonBox 后续治理质量能力，补强根因证据、命令复盘、UI 返修截图对照、Workflow Sync next 复核和治理脚本门禁矩阵。

### BUG-0130-miniapp-home-no-jump-banner-internal-title 要点

修复小程序首页无跳转轮播图显示内部标题的问题，净化公开 Banner DTO 与小程序展示/点击兜底链路，并覆盖首页轮播、品牌列表页轮播和媒体 key/object/URL/render 四联验收。

### apply-deepseek-harness-doc-governance-learnings 要点

应用 deepseek-harness 文档治理能力，补强事实唯一归属、治理决策字段、文档表达卫生、最小相关验证和防御性模式模板。

### BUG-0131-miniapp-sku-detail-carousel-original-image-height 要点

修复小程序商品详情页轮播首屏使用 `.thumb` 导致大图区域清晰度不足的问题，同时将固定 `680rpx` 媒体高度调整为更适合瓷砖详情展示的比例，并保持商品名称或关键商品信息在首屏可见。列表、卡片、推荐位和 Banner 仍保留 `.thumb` 性能策略。

### default-review-approve-command 要点

调整 `/req-review` 与 `/bug-review` 的正向命令体验，将无 flag 调用定义为默认通过，并同步规则、技能示例和治理日志；反向评审结果继续要求显式 flag。

## 2. Scope

| 类型 | 编号 | 标题 | 状态 | 估算 | 说明 |
|---|---|---|---|---:|---|
| BUG | BUG-0130-miniapp-home-no-jump-banner-internal-title | 小程序首页无跳转轮播图显示内部标题 | done | 1 人天 | archived `fix-miniapp-home-no-jump-banner-internal-title`（2026-08-21 13:45:41） |
| BUG | BUG-0131-miniapp-sku-detail-carousel-original-image-height | 小程序商品详情页轮播图清晰度不足且高度偏小 | done | 1 人天 | archived `fix-miniapp-sku-detail-carousel-original-image-height`（2026-08-21 13:52:48） |
| Change | apply-moonbox-governance-quality-learnings | apply moonbox governance quality learnings | archived | 0.75 人天 | archived `apply-moonbox-governance-quality-learnings`（2026-08-21 08:32:51） |
| Change | apply-deepseek-harness-doc-governance-learnings | apply deepseek harness doc governance learnings | archived | 0.75 人天 | archived `apply-deepseek-harness-doc-governance-learnings`（2026-08-21 08:51:36） |
| Change | default-review-approve-command | default review approve command | archived | 0.5 人天 | archived `default-review-approve-command`（2026-08-21 13:52:00） |

<!-- workflow-sync:scope-requirements:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
<!-- workflow-sync:scope-requirements:end -->

<!-- workflow-sync:scope-bugs:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| BUG-0130 | 小程序首页无跳转轮播图显示内部标题 | medium | done | archived `fix-miniapp-home-no-jump-banner-internal-title`（2026-08-21 13:45:41） |
| BUG-0131 | 小程序商品详情页轮播图清晰度不足且高度偏小 | medium | done | archived `fix-miniapp-sku-detail-carousel-original-image-height`（2026-08-21 13:52:48） |
<!-- workflow-sync:scope-bugs:end -->

<!-- workflow-sync:scope-changes:start -->
| Change ID | 关联需求 | 状态 | Sprint 目标 |
|---|---|---|---|
| `apply-moonbox-governance-quality-learnings` | — | archived | archived `apply-moonbox-governance-quality-learnings`（2026-08-21 08:32:51） |
| `apply-deepseek-harness-doc-governance-learnings` | — | archived | archived `apply-deepseek-harness-doc-governance-learnings`（2026-08-21 08:51:36） |
| `fix-miniapp-home-no-jump-banner-internal-title` | BUG-0130-miniapp-home-no-jump-banner-internal-title | archived | archived `fix-miniapp-home-no-jump-banner-internal-title`（2026-08-21 13:45:41） |
| `default-review-approve-command` | — | archived | archived `default-review-approve-command`（2026-08-21 13:52:00） |
| `fix-miniapp-sku-detail-carousel-original-image-height` | BUG-0131-miniapp-sku-detail-carousel-original-image-height | archived | archived `fix-miniapp-sku-detail-carousel-original-image-height`（2026-08-21 13:52:48） |
<!-- workflow-sync:scope-changes:end -->

REQ：无 已纳入正式范围；BUG：BUG-0130、BUG-0131 已纳入正式范围，优先级高于新增体验能力；当前完成度与验收风险以 Scope 表状态、关联 Change 和 acceptance-report 为准。

Change：已回填 2 个范围项关联 Change，另有 3 个纯治理 Change；5/5 Change 均已归档，执行闭环以 Scope 表和归档 trace 为准。

## 风险

- 当前工作区存在大量无关未提交变更，本 Sprint 只复核本次触达治理资产和 `src/` 未新增改动。
- BUG-0130 修复 Change 已归档；小程序 DevTools、真机或体验版 render evidence 作为发布前补证建议保留。
- Sprint 当前估算 3.5 人天，已超过单日双角色容量上限；BUG 修复需要保留小程序体验版或 DevTools render evidence，避免验收证据后置。
- BUG-0131 修复 Change 已创建并回填同一 Sprint scope；进入实现前已通过 `/opsx-apply` dry-run 门禁。

## 知识库承接

- `docs/knowledge-base/retrospectives/sprint-023-retrospective.md`：小程序媒体验收从个案上升为 key/object/URL/render 四联证据链，BUG-0130 继续沿用该口径。
- `docs/knowledge-base/retrospectives/sprint-023-retrospective.md`：小程序媒体四联验收对 BUG-0131 仍适用，尤其需要区分详情页高清展示 URL 与列表 `.thumb` 性能 URL。
- `docs/knowledge-base/best-practices/miniapp-media-four-part-acceptance-practice.md`：BUG-0130 与 BUG-0131 均必须补齐小程序 DevTools、真机或体验版 Network/render evidence，不以对象存在或接口字段替代端侧可见证据。
- `docs/knowledge-base/retrospectives/sprint-024-retrospective.md`：本 Sprint 复盘，沉淀公开 Banner 字段净化、小程序 SKU 媒体 URL 语义、Sprint close stale scan 与模型 Token 使用经验。

## 横切预防清单

- 小程序媒体四联验收：key、object、URL、render 均需明确 pass/fail/blocked/n/a。
- 详情页媒体 URL 语义：大图展示、点击预览、列表卡片缩略图必须分别断言，避免修复清晰度时回退列表性能。
- 公开字段净化：后台内部标题、枚举、时间戳不得进入公开 Banner DTO、toast、搜索、分享或埋点展示摘要。
- 回归范围：小程序首页轮播、品牌列表页轮播、商品详情页轮播、后台 Banner 列表/编辑、无跳转点击兜底。

## 关闭记录

- 2026-08-21 14:42:16 `/sprint-archive sprint-024`：5/5 Change 已归档，2 个 BUG 已进入 archive，Sprint readiness 与 stale scan 均通过，Sprint 状态关闭为 completed/archive。
