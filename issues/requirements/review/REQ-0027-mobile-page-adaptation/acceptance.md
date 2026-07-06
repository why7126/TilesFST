---
title: 需求验收标准
purpose: REQ-0027 Web 管理端移动端基础适配优化验收标准
content: 基于 requirement.md v1、用户故事、业务流程与知识库横切最佳实践生成
source: AI 根据 PRD 与知识库最佳实践生成，项目团队确认
update_method: PRD、原型、知识库最佳实践或验收范围变更时同步更新
owner: product
status: draft
created_at: 2026-07-05 10:17:18
updated_at: 2026-07-05 10:17:18
note: REQ-0027-mobile-page-adaptation
---

# 验收标准

## 1. 范围与边界

- [ ] **AC-001** 本 REQ 仅修改或验收 Web 管理端 `/admin/*` 当前已实现页面，不改店主 Web 展示端、微信小程序、后端 API、数据库、Orval 或 Docker 配置。
- [ ] **AC-002** 若实现阶段发现必须修改 API、数据库、环境变量、MinIO 或小程序，MUST 回到 PRD 评审或拆分独立 REQ。
- [ ] **AC-003** 管理端鉴权、`ProtectedRoute`、`requireAdmin` 和无权限页行为不因移动端适配回归。
- [ ] **AC-004** 移动端目标为“基础可用”：阅读主要信息、完成核心单项操作、关闭弹窗、切换页面；不要求完整手机办公重构。

## 2. 验收视口与页面清单

- [ ] **AC-005** 必测视口包含 `375x812`、`390x844`、`768x1024`、`1440x1024`。
- [ ] **AC-006** `/admin/login` 在 `375x812` 与 `390x844` 下隐藏左侧品牌区，登录表单居中，账号、密码、记住登录状态、登录按钮可操作。
- [ ] **AC-007** `/admin/dashboard` 在移动视口下指标卡、快捷操作、最近更新表格不重叠，页面级无不可控横向溢出。
- [ ] **AC-008** `/admin/tile-skus` 在移动视口下筛选区、宽表格、分页、SKU 弹窗和媒体字段可访问。
- [ ] **AC-009** `/admin/brands` 在移动视口下筛选区、Logo 列、表格、分页、品牌弹窗和状态确认可访问。
- [ ] **AC-010** `/admin/users` 在移动视口下筛选区、用户表格、分页、用户弹窗和重置密码确认可访问。
- [ ] **AC-011** `/admin/logs` 在移动视口下多条件筛选、日志表格、分页和日志详情抽屉可关闭、可滚动。
- [ ] **AC-012** `/admin/settings/basic` 在移动视口下设置导航、表单字段、保存/重置操作和确认弹窗可访问。
- [ ] **AC-013** `/admin/forbidden` 在移动视口下文案和返回/跳转入口不溢出。

## 3. Shell 与导航

- [ ] **AC-014** `≤1023px` 下 `AdminLayout` 保持单列 Shell，Sidebar 不遮挡主内容。
- [ ] **AC-015** `≤1023px` 下 Sidebar 导航项可完整访问或可滚动访问，当前 active 路由仍可识别。
- [ ] **AC-016** `≤1023px` 下侧栏折叠 chevron 隐藏或禁用，不与移动端导航布局冲突。
- [ ] **AC-017** `.main-content` 与 `.content-inner` 不产生页面级不可控横向滚动；宽表格的横向滚动限制在表格容器内。
- [ ] **AC-018** 页面级 notice / toast 不以文档流方式推挤主内容；成功/失败反馈不造成 Shell 纵向跳动。

## 4. 列表页筛选、表格与分页

- [ ] **AC-019** 列表页筛选区在 `≤1023px` 下可降为 2 列或适配布局，在 `≤639px` 下可单列展示。
- [ ] **AC-020** 筛选输入框、选择框、查询按钮、重置按钮不重叠、不超出父容器，且可键盘聚焦。
- [ ] **AC-021** 表格较宽时采用 `table-card` 或等价容器级横向滚动；页面 body 不出现不可控横向滚动。
- [ ] **AC-022** 关键标识列、状态列、操作列在移动视口下可访问；隐藏次要列时不得隐藏核心操作。
- [ ] **AC-023** 分页在 `375px` 宽度下可换行或分组展示，页码、上一页/下一页、每页条数和总数摘要不互相覆盖。
- [ ] **AC-024** 空状态、加载状态、错误提示在移动视口下不造成 hero / 表格 / 分页明显跳动。

## 5. 表单、弹窗与抽屉

- [ ] **AC-025** 新增/编辑弹窗在 `375px` 宽度下不超出视口，头部标题、关闭按钮、内容区和底部操作可访问。
- [ ] **AC-026** SKU、Banner 等大弹窗在矮视口下 body 可滚动，footer 主操作按钮不丢失。
- [ ] **AC-027** 删除、启停、上下架、重置密码、恢复默认、dirty Tab 切换等风险操作使用 DS modal；无 `window.confirm` / `window.alert`。
- [ ] **AC-028** 表单错误提示出现后，显示/隐藏按钮、上传控件、底部操作区不明显错位。
- [ ] **AC-029** `/admin/profile` 小屏下主信息区、账号安全区和修改密码弹窗单列可读、可操作。
- [ ] **AC-030** `/admin/settings/:tab` 小屏下设置分组导航、配置表单、保存/重置和确认弹窗可操作。
- [ ] **AC-031** `/admin/logs` 日志详情抽屉在手机宽度下可关闭、可滚动查看详情，不导致页面整体横向失控。

## 6. 媒体上传移动端回归

- [ ] **AC-032** 品牌 Logo、Banner 图片、SKU 图片/视频、用户头像等已有上传控件在移动视口下选择文件后仍展示上传中、成功或失败状态。
- [ ] **AC-033** 同会话上传成功后缩略图或文件卡片即时回显，不要求刷新页面才能看到结果。
- [ ] **AC-034** 上传失败信息展示在控件附近或既有错误区域内，不遮挡底部操作按钮。
- [ ] **AC-035** 本 REQ 不新增媒体 API、存储桶、上传大小限制或 Nginx 配置；若实现阶段触及，MUST 拆分独立变更。

## 7. 技术与测试验收

- [ ] **AC-036** 新增或修改的 UI 样式使用 semantic token / admin token，TSX/CSS 不新增裸 Hex 或任意设计色 `rgba(...)`。
- [ ] **AC-037** Playwright 或等价浏览器 smoke 覆盖 `375x812`、`390x844`、`768x1024`、`1440x1024`。
- [ ] **AC-038** smoke 记录每个必测页面是否存在：页面级横向溢出、控件重叠、弹窗不可关闭、底部按钮不可达、筛选/分页不可操作。
- [ ] **AC-039** Vitest 可补充结构性断言，例如分页 DOM、弹窗 class、保存按钮数量、无原生 confirm mock 调用。
- [ ] **AC-040** `pnpm --dir src/web test` 或项目等价前端测试通过；若仅执行子集，MUST 在 trace 中记录原因与剩余风险。
- [ ] **AC-041** 本需求不要求执行 Orval；若实现阶段改 API，MUST 重新运行 OpenAPI/Orval 门禁。
- [ ] **AC-042** 本需求不要求 Docker Compose 验证；若实现阶段改上传、Nginx、Docker 或环境变量，MUST 补 Docker 验证。

## 8. 视觉验收 Trace

原型优先级：

```text
1. prototype/web/web-admin-mobile-adaptation.html
2. prototype/web/web-admin-mobile-adaptation-context.md
3. acceptance.md（本文件）
4. requirement.md
5. rules/ui-design.md
6. openspec/specs/（已归档能力）
```

- [ ] **AC-043** 以 `prototype/web/web-admin-mobile-adaptation.html` 的页面矩阵和视口矩阵作为后续 `/req-opsx` design 参考。
- [ ] **AC-044** PNG Golden Reference 本阶段可标记为待导出；apply 完成前 SHOULD 补充移动端截图或等价 Playwright screenshot。
- [ ] **AC-045** `trace.md` MUST 记录移动端截图/Playwright smoke 的执行日期、视口、页面和结果。

## 9. 横切 AC（knowledge-base）

> 来源：`docs/knowledge-base/best-practices/admin-list-page-consistency.md`、`admin-form-page-consistency.md`、`admin-modal-width-css-cascade.md`、`admin-media-upload-chain.md` — 预防 Sprint 002/003/004 复发类缺陷。

- [ ] **AC-XCUT-001** 列表页分页 DOM MUST 对齐用户管理基准：左侧 `page-summary`，右侧 `page-right` 页码与每页条数；移动视口下允许换行但不得改变语义结构。
- [ ] **AC-XCUT-002** 列表页摘要指标卡 MUST 使用 `.metric-label` / `.metric-value` / `.metric-desc` 或等价共享结构，不得只复用外层卡片后使用裸 `strong` / `span` 承载数值。
- [ ] **AC-XCUT-003** 列表页操作成功/失败反馈 MUST 使用 fixed toast 或等价固定反馈区域，不得用文档流 notice 推挤 hero、筛选区或表格。
- [ ] **AC-XCUT-004** 启停、冻结、上架/下架、删除、重置密码等状态/危险操作 MUST 使用 DS confirm modal；MUST NOT 使用 `window.confirm`。
- [ ] **AC-XCUT-005** 管理端表单页全页 MUST 仅保留一处主要保存 CTA；移动端不得因响应式布局重新出现页头和页尾双保存按钮。
- [ ] **AC-XCUT-006** 系统设置恢复默认、dirty Tab 切换、修改密码取消等风险操作 MUST 使用 DS modal；MUST NOT 使用原生 `window.confirm` / `window.alert`。
- [ ] **AC-XCUT-007** 表单保存成功/失败反馈 MUST 使用 fixed toast 或等价固定反馈，不得在 summary 与主表单之间插入会造成 layout shift 的块级 success banner。
- [ ] **AC-XCUT-008** 业务弹窗 TSX className MUST NOT 同时挂载通用 `modal-card` 与专属类；宽弹窗使用专属类（如 `sku-modal-card`、`banner-modal-card`）避免 CSS 层叠覆盖。
- [ ] **AC-XCUT-009** 宽弹窗与窄弹窗在桌面和移动视口下 MUST 验收 computed width / max-width，而不只检查源 CSS。
- [ ] **AC-XCUT-010** 矮视口下弹窗 body MUST 可滚动，头部关闭按钮与底部主操作按钮可访问。
- [ ] **AC-XCUT-011** 含上传控件的页面 MUST 保持 `idle → uploading → done / failed` 状态机，移动端不得隐藏上传中或失败状态。
- [ ] **AC-XCUT-012** 含上传控件的页面在同会话上传成功后 MUST 即时回显缩略图或文件卡片。
- [ ] **AC-XCUT-013** Docker `:3000` 上传边界文件验收对本 REQ 默认 **N/A — 本需求不修改上传链路、Nginx 或 Docker**；若实现阶段触及上传或代理配置，MUST 恢复为必测项。
- [ ] **AC-XCUT-014** 后续 `/req-opsx` 的 `design.md` MUST 引用本需求 trace 中的 `knowledge_base_refs`，并说明每个横切标签如何落实或 N/A。
