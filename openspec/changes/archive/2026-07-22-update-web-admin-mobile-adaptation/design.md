## Context

`REQ-0027-mobile-page-adaptation` 聚焦当前已实现 Web 管理端在手机和小屏平板上的基础可用性。现状中，`AdminLayout` 已有 `≤1023px` 响应式结构，多个列表页也已有筛选栅格、表格横向滚动或弹窗 `max-width/max-height` 规则，但这些策略分散在页面样式内，缺少统一的验收矩阵与横切质量门禁。

本 Change 的原型优先级为：

1. `issues/requirements/archive/REQ-0027-mobile-page-adaptation/prototype/web/web-admin-mobile-adaptation.html`
2. `issues/requirements/archive/REQ-0027-mobile-page-adaptation/prototype/web/web-admin-mobile-adaptation-context.md`
3. `issues/requirements/archive/REQ-0027-mobile-page-adaptation/acceptance.md`
4. `issues/requirements/archive/REQ-0027-mobile-page-adaptation/requirement.md`
5. `rules/ui-design.md`
6. `openspec/specs/`

PNG Golden Reference 当前待导出，不阻断 req-opsx；实现完成前 SHOULD 用 Playwright screenshot 或等价截图补足移动端验收证据。

## Goals / Non-Goals

**Goals:**

- 让当前 Web 管理端已实现页面在 `375x812`、`390x844`、`768x1024` 下达到基础可用，并在 `1440x1024` 下保持桌面回归稳定。
- 统一 Shell、Sidebar、内容区、列表筛选、表格、分页、弹窗、抽屉、设置页、个人资料页、登录页和无权限页的移动端验收标准。
- 保留管理端“工业石材 · 暗色旗舰风”，继续使用 Design System semantic token、现有 admin CSS 变量和 `cn()` 合并约定。
- 将 `knowledge_base_refs` 中的 `admin-list`、`admin-form`、`admin-modal`、`media-upload` 横切 AC 转为实现任务和验收记录。

**Non-Goals:**

- 不重做完整手机办公信息架构，不新增底部 Tab、移动专属导航抽屉或卡片化重构。
- 不修改店主 Web 展示端、微信小程序、后端 API、数据库、OpenAPI、Orval、Docker Compose、Nginx、MinIO 或媒体上传后端策略。
- 不调整 Design Token 值；除非实现阶段证明现有 token 无法支撑基础可用，并另走评审。

## Decisions

### D1. UI 策略：沿用既有 DS 与页面 CSS 的响应式修补

采用 `DS + existing admin CSS refinement` 策略。实现阶段应优先复用 `AdminLayout`、`AdminListPage` 或等价模板、`MetricCard` / `MetricCardGrid`、统一分页 DOM、DS modal、已有上传控件状态机和页面专属 CSS。跨页通用移动端规则放在既有管理端共享样式或 `admin-home.css` 等约定位置，页面特有修补保留在对应页面 CSS。

不采用完整 CSS Port 重写或移动端独立主题，因为本需求目标是基础可用与横切回归，不是重新设计管理端移动办公体验。也不采用页面级临时媒体查询堆叠来复制组件逻辑，避免后续列表和弹窗契约继续漂移。

### D2. 断点与滚动边界

实现阶段沿用现有断点语义：`≤1023px` 进入窄屏 Shell，`≤639px` 进入手机小屏布局；页面已有 `720px`、`760px`、`960px`、`1120px`、`1279px` 等过渡断点可保留。Shell 与 body 不应产生不可控横向滚动，宽表格的横向滚动必须限制在表格容器内。

### D3. 列表与分页以现有基准收敛

列表页继续以已归档的管理端列表横切一致性为基线：模块顺序、指标卡 DOM、筛选区、固定操作列、`page-summary` + `page-right` + `page-buttons` + `page-size-wrap` 分页结构必须保留。移动端允许换行或分组展示，但不得改变语义结构。

### D4. 弹窗、表单与上传控件以可操作为第一验收

SKU、Banner 等大弹窗保持专属宽度策略，并在窄屏下让 `max-width`、`max-height`、内容区滚动和 footer 操作可达。风险操作继续使用 DS modal，禁止 `window.confirm` / `window.alert` 回归。上传控件只验收已有 `idle -> uploading -> done/failed` 状态、同会话回显和错误展示，不修改后端上传链路。

### D5. 验收方式

实现阶段 MUST 使用 Playwright 或等价浏览器 smoke 覆盖 `375x812`、`390x844`、`768x1024`、`1440x1024`。必测路由至少包含 `/admin/login`、`/admin/dashboard`、`/admin/tile-skus`、`/admin/brands`、`/admin/users`、`/admin/logs`、`/admin/settings/basic`。每个 smoke 结果需记录页面级横向溢出、控件重叠、弹窗不可关闭、底部按钮不可达、筛选/分页不可操作等检查项。

## Conflict Resolution

- HTML 原型与 acceptance 冲突时，以 `prototype/web/web-admin-mobile-adaptation.html` 的验收矩阵范围优先，但不得扩大到店主 Web 或微信小程序。
- `acceptance.md` 中 PNG Golden Reference 待导出不阻断本 Change；apply 完成前用 Playwright screenshot 或等价截图补充即可。
- 已有 `openspec/specs/admin-dashboard` 规定了 Shell 桌面布局与响应式 padding，本 Change 只补充移动端基础可用细节，不改变桌面 Sidebar 展开/收起契约。
- 已有 `openspec/specs/web-client` 规定了列表页横切一致性、分页 DOM、表单错误解析和主题验收，本 Change 在其上增加移动端视口矩阵与页面范围，不移除既有要求。

## Knowledge-Base Trace

- `docs/knowledge-base/best-practices/admin-list-page-consistency.md`：用于分页 DOM、指标卡结构、固定 toast、DS confirm modal 的横切验收。
- `docs/knowledge-base/best-practices/admin-form-page-consistency.md`：用于单一保存 CTA、dirty 切换、fixed toast 与原生 confirm 禁止项。
- `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md`：用于宽弹窗 className、computed width/max-width 和矮视口滚动验收。
- `docs/knowledge-base/best-practices/admin-media-upload-chain.md`：本 Change 仅引用上传控件前端状态与同会话回显；Docker `:3000` 上传边界默认 N/A，除非实现触及上传代理或部署配置。
- `docs/knowledge-base/retrospectives/sprint-004-retrospective.md`：用于提醒列表横切不一致和验收门禁漂移风险。

## Risks / Trade-offs

- 页面已有响应式规则分散，修复可能出现 CSS 层叠回归。Mitigation：优先复用共享 admin 类与 DS 模板，任务中要求按页面矩阵逐页 smoke。
- 宽表格在 375px 下仍需要横向滚动，无法做到所有列同时可见。Mitigation：要求页面级无横向溢出，并保证关键标识、状态和操作列可访问。
- 弹窗 footer 固定与内容滚动可能受移动浏览器视口高度影响。Mitigation：任务中必须验收 375px 宽度和矮视口 body 滚动、关闭按钮、主操作可达。
- 上传控件移动端验收可能需要测试数据和登录态。Mitigation：可使用 mock、fixtures 或现有测试账号；若上传链路本身需变更，拆分独立 REQ/Change。
