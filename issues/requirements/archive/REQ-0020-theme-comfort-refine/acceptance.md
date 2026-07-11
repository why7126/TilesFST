---
requirement_id: REQ-0020-theme-comfort-refine
title: Web / 管理端主题舒适度优化与主题切换 - 验收标准
status: archived
owner: product
source: requirement.md
created_at: 2026-07-11 17:22:09
updated_at: 2026-07-11 20:13:04
---

# 验收标准

## 功能 AC

- [ ] AC-001 主题模式：系统必须支持「系统默认」「暗色旗舰」「舒适暗色」「浅色」四类主题模式。
- [ ] AC-002 管理端入口：Web 管理端必须提供清晰的主题切换入口，用户能够识别当前主题并切换到其他主题。
- [ ] AC-003 即时生效：主题切换后当前页面必须即时应用，不需要刷新浏览器。
- [ ] AC-004 状态不丢失：主题切换不得丢失当前页面筛选条件、分页状态、表单输入、dirty 状态、弹窗打开状态或上传状态。
- [ ] AC-005 本地持久化：主题偏好必须写入本地持久化，用于首屏快速恢复，避免无主题闪烁。
- [ ] AC-006 账号级持久化：主题偏好必须写入认证用户账号级配置，支持跨设备和重新登录恢复。
- [ ] AC-007 账号隔离：退出登录或切换账号后，不得错误沿用其他账号的账号级主题偏好。
- [ ] AC-008 API / DB / Orval：若实现账号级主题偏好，必须同步后端 API、Pydantic Schema、数据库结构或用户配置存储、OpenAPI、Orval 和测试。
- [ ] AC-009 登录页覆盖：管理端登录页必须覆盖四类主题，表单、按钮、错误提示、语言切换和品牌区均可读、稳定、舒适。
- [ ] AC-010 登录前偏好：若登录页允许登录前切换主题，登录成功后必须延续该主题偏好。
- [ ] AC-011 瓷砖 SKU 列表覆盖：瓷砖 SKU 管理列表必须覆盖四类主题，指标卡、筛选区、表格、sticky 操作列和分页均不重叠、不裁切、不丢失层级。
- [ ] AC-012 瓷砖 SKU 表单覆盖：瓷砖 SKU 编辑 / 表单区域必须覆盖四类主题，输入框、选择器、帮助文案、错误提示和保存 CTA 清晰可用。
- [ ] AC-013 瓷砖 SKU 弹窗覆盖：瓷砖 SKU 新建 / 编辑弹窗必须覆盖四类主题，遮罩、弹窗卡片、滚动、表单、按钮和错误区域层级清楚。
- [ ] AC-014 媒体上传状态覆盖：瓷砖 SKU 弹窗内图片 / 视频上传状态必须在四类主题下清楚展示 idle、uploading、done、failed 状态。
- [ ] AC-015 `/design-system` 覆盖：`/design-system` 必须提供主题切换或主题对比入口，展示四类主题的 token、基础组件和管理端代表组件状态。
- [ ] AC-016 店主 Web 舒适主题：店主 Web 除品牌展示页、首页 Hero 和品牌氛围区域外，商品列表、筛选、详情阅读和询价路径必须支持舒适主题。
- [ ] AC-017 品牌展示页边界：店主 Web 品牌展示页允许保持暗色旗舰风，不得被管理端舒适主题强制改为浅色模板。
- [ ] AC-018 Semantic Token：主题实现必须基于 Design System semantic token、CSS variables 和 Tailwind 语义 class，不得在业务 TSX/CSS 中新增裸 Hex 或 token 等价硬编码 `rgba(...)`。
- [ ] AC-019 可访问性：四类主题下主要文字、表单、按钮、错误提示和表格内容必须满足可读性要求；不得出现文字被背景吞没或状态色无法辨识。
- [ ] AC-020 视觉回归：实现阶段必须提供登录页、瓷砖 SKU 列表、瓷砖 SKU 弹窗/表单、店主 Web 舒适主题和 `/design-system` 的截图或等价视觉验收材料。
- [ ] AC-021 测试覆盖：主题模式解析、偏好持久化、管理端主题切换入口、账号隔离和至少一个代表页面渲染状态必须有自动化测试或等价验证脚本。
- [ ] AC-022 文档同步：实现后必须同步 `rules/ui-design.md`、Design System 说明或 Web README，说明四类主题、使用边界、店主 Web 例外和 token 约束。

## 横切 AC（knowledge-base）

> 来源：`docs/knowledge-base/best-practices/admin-list-page-consistency.md`、`docs/knowledge-base/best-practices/admin-form-page-consistency.md`、`docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md`、`docs/knowledge-base/best-practices/admin-media-upload-chain.md` — 预防 Sprint 002/003/004/005 复发类缺陷。

- [ ] AC-XCUT-001 admin-list：瓷砖 SKU 列表页主题验收必须保持用户管理基准分页 DOM：左侧 `page-summary`，右侧 `page-right` / `page-buttons` / 每页条数控件。
- [ ] AC-XCUT-002 admin-list：瓷砖 SKU 列表页指标卡必须保持 `.metric-label` / `.metric-value` / `.metric-desc` 或等价 `MetricCard` 契约，不得因主题适配回退为裸 `strong` / `span`。
- [ ] AC-XCUT-003 admin-list：主题切换后的成功 / 失败反馈必须使用 fixed toast，不得在 hero、summary、筛选区或表格前插入文档流 notice 导致 layout shift。
- [ ] AC-XCUT-004 admin-list：瓷砖 SKU 启停、上架 / 下架、删除等状态变更仍必须使用 Design System confirm modal，MUST NOT 使用 `window.confirm`。
- [ ] AC-XCUT-005 admin-form：若主题设置进入系统设置或表单页，全页只能有一处保存主题 / 保存设置主 CTA，且位于表单 footer；页头不得重复渲染保存按钮。
- [ ] AC-XCUT-006 admin-form：恢复默认主题、放弃未保存主题切换、dirty Tab 切换必须使用 Design System modal，MUST NOT 使用 `window.confirm` 或 `window.alert`。
- [ ] AC-XCUT-007 admin-form：主题保存成功 / 失败反馈必须使用 AdminLayout fixed toast 或等价固定反馈，不得推挤 `settings-layout`、SKU 表单区或主内容。
- [ ] AC-XCUT-008 admin-modal：瓷砖 SKU 弹窗 TSX 不得同时挂载通用 `modal-card` 与 `sku-modal-card` 等专属类；主题类名不得重新引入 modal 宽度层叠冲突。
- [ ] AC-XCUT-009 admin-modal：瓷砖 SKU 弹窗在 1440px 视口下 Computed width 必须与 SKU 设计基准一致；主题切换不得把宽弹窗覆盖为 520px。
- [ ] AC-XCUT-010 admin-modal：矮视口下瓷砖 SKU 弹窗 body scroll 必须可用，主题切换不得导致弹窗底部按钮不可达。
- [ ] AC-XCUT-011 media-upload：瓷砖 SKU 媒体上传控件在四类主题下必须清楚展示 `idle → uploading → done / failed` 状态。
- [ ] AC-XCUT-012 media-upload：同一会话上传成功后，缩略图或文件卡片必须即时回显；主题切换不得清空预览或让预览不可读。
- [ ] AC-XCUT-013 media-upload：上传失败必须在控件内展示错误状态；主题切换不得只保留全局 toast 而丢失控件级失败反馈。
- [ ] AC-XCUT-014 media-upload：若本 Change 不修改上传大小、Nginx 或 MinIO 链路，Docker `:3000` 边界文件上传可标记为 N/A；若同时触碰上传链路，则必须按 best-practice 通过边界文件验收。

## Readiness

```yaml
readiness: Ready
knowledge_base_gate: Pass
cross_cutting_tags:
  - admin-list
  - admin-form
  - admin-modal
  - media-upload
next: /req-review REQ-0020-theme-comfort-refine --approve
```
