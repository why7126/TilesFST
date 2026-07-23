---
requirement_id: REQ-0027-mobile-page-adaptation
title: Web 管理端移动端基础适配优化
terminal: web-admin
version: v1
status: done
owner: product
source: issues/requirements/archive/REQ-0027-mobile-page-adaptation/capture.md
priority: P1
parent_requirement: REQ-0004-admin-home
created_at: 2026-07-05 07:56:17
updated_at: 2026-07-22 09:23:55
---

# REQ-0027 Web 管理端移动端基础适配优化

## 1. 需求背景

当前 Web 管理端已实现登录页、管理端 Shell、Dashboard、SKU / 品牌 / 类目 / 规格 / Banner / 用户等列表页，以及个人资料、系统设置、日志审计、接口文档等页面。多数页面以桌面管理后台为主要使用场景，已存在部分响应式规则：

- `/admin/login` 已有 `<1024px` 单栏登录布局。
- `AdminLayout` 在 `≤1023px` 下改为顶部导航布局，并隐藏侧栏用户区。
- 多个列表页已有筛选区栅格降级、表格横向滚动或局部断点规则。
- 部分弹窗已设置 `max-width: 100%`、`max-height` 与滚动内容区。

但这些移动端策略目前分散在各页面 CSS 中，缺少统一验收口径。产品侧本次明确：**只优化当前已经实现的 Web 管理端**，不扩展店主 Web 展示端或微信小程序。目标是让管理端在手机与小屏平板上达到基础可用，避免出现明显横向溢出、控件重叠、弹窗无法关闭、分页/筛选不可操作等问题。

## 2. 目标用户

- **后台管理员 / 内部员工**：在手机、小屏平板或窄浏览器窗口下临时查看、筛选、编辑管理端数据。
- **测试 / 验收人员**：需要用固定移动端视口对当前管理端页面做 smoke 验收，确认布局不会阻塞核心操作。

## 3. 范围

### 3.1 本期包含

仅覆盖当前路由表中已经实现的 Web 管理端页面：

| 路由 | 页面 | 移动端关注点 |
|---|---|---|
| `/admin/login` | 管理端登录页 | 保持既有单栏登录布局，不回归 |
| `/admin/dashboard` | 管理首页 | 指标卡、快捷操作、最近更新表格不重叠 |
| `/admin/brands` | 品牌管理 | 筛选、表格、分页、Logo 展示、弹窗可操作 |
| `/admin/banners` | Banner 管理 | 筛选、表格、分页、Banner 弹窗可滚动 |
| `/admin/tile-categories` | 瓷砖类目管理 | 筛选、树/表格区域、类目弹窗可操作 |
| `/admin/tile-specs` | 瓷砖规格管理 | 筛选、表格、分页、规格弹窗可操作 |
| `/admin/tile-skus` | 瓷砖 SKU 管理 | 宽表格、筛选区、SKU 大弹窗、媒体字段可操作 |
| `/admin/profile` | 个人资料 | 双栏信息降为单栏，表单和操作按钮可见 |
| `/admin/users` | 用户管理 | 筛选、表格、分页、用户/重置密码弹窗可操作 |
| `/admin/logs` | 日志审计 | 多条件筛选、宽表格、日志详情抽屉可用 |
| `/admin/api-docs` | 接口文档 | 筛选、接口表格、Swagger 入口不重叠 |
| `/admin/settings/:tab` | 系统设置 | 设置导航、配置表单、确认弹窗可操作 |
| `/admin/forbidden` | 无权限页 | 页面信息居中可读 |

本期改造类型：

- 管理端 Shell 与内容区在移动视口下的布局稳定性。
- 筛选区、指标卡、表格、分页、弹窗、抽屉的基础移动端可用性。
- 统一移动端验收视口与 smoke 页面清单。
- 必要的前端样式与测试补充。

### 3.2 本期不包含

- 店主 Web 展示端、首页、商品列表、商品详情。
- 微信小程序页面或小程序端管理能力。
- 新增管理端业务页面、业务流程或字段。
- 新增移动端专属导航抽屉、底部 Tab、卡片化完整重构等手机办公体验。
- API 请求参数、响应结构、错误码、OpenAPI、Orval 客户端变更。
- SQLite / MySQL 表结构、迁移脚本或 Pydantic Schema 变更。
- Docker Compose、Nginx、环境变量、MinIO、媒体上传策略变更。
- Design Token 值大改；除非实现阶段证明现有 token 无法支撑移动端基础可用。

## 4. 功能要求

### FR-001 管理端移动端适配边界

- 本需求 MUST 仅作用于 Web 管理端 `/admin/*` 已实现页面。
- Web 展示端 `/`、店主端模板、微信小程序 MUST 不作为本需求交付范围。
- 所有页面 MUST 保持当前鉴权、路由守卫、权限边界和已有业务交互，不得为了移动端适配绕过权限或隐藏关键鉴权入口。
- 本需求 SHOULD 定义为“基础可用”而非“完整移动办公”：用户能阅读主要信息、完成核心单项操作、关闭弹窗、返回或切换页面即可。

### FR-002 断点与布局策略

- 移动端断点 SHOULD 优先沿用现有体系：
  - `≤1023px`：管理端 Shell 进入窄屏布局。
  - `≤639px`：手机小屏布局。
  - 单页已有 `720px`、`760px`、`960px`、`1120px`、`1279px` 等过渡断点 MAY 保留。
- 实现 MUST 优先修复布局稳定性，避免新增一套与现有 `admin-home.css` 冲突的响应式体系。
- 页面级样式 SHOULD 收敛到当前页面对应 CSS 文件中；跨页通用规则 SHOULD 优先放在 `admin-home.css` 或既有共享样式约定中，避免多处重复。
- 所有新增或修改 UI 样式 MUST 使用 Design System / admin semantic token，MUST NOT 在 TSX/CSS 中新增裸 Hex 或随意硬编码 `rgba(...)` 作为设计色。

### FR-003 AdminLayout 与导航基础可用

- `AdminLayout` 在 `≤1023px` 下 MUST 保持单列 Shell，不得出现侧栏遮挡主内容或主内容被挤出视口。
- 侧栏导航在小屏下 MUST 可滚动或完整访问当前已有导航项，且当前 active 路由状态仍可识别。
- 侧栏折叠 chevron 在 `≤1023px` 下 MUST 不与移动端导航模型冲突；可隐藏或禁用，但不得造成布局跳动。
- `.main-content` 与 `.content-inner` 在移动视口下 MUST 不引入页面级横向滚动；宽表格等内容型横向滚动应限制在对应容器内。

### FR-004 列表页筛选、表格与分页

适用于 `/admin/brands`、`/admin/banners`、`/admin/tile-categories`、`/admin/tile-specs`、`/admin/tile-skus`、`/admin/users`、`/admin/logs`、`/admin/api-docs`。

- 筛选区在 `≤1023px` SHOULD 降为 2 列或 1 列，在 `≤639px` MUST 可单列展示。
- 筛选输入框、选择框、查询/重置按钮 MUST 不互相重叠，不得超出父容器。
- 表格内容较宽时 MUST 使用容器级横向滚动或明确的列降级策略；不得让整个页面出现不可控横向滚动。
- 表头、关键标识列、状态列和操作列在移动视口下 MUST 保持可访问；若需要隐藏次要列，MUST 不影响核心操作。
- 分页区在手机宽度下 MUST 可换行或分组显示；页码按钮、每页条数和总数摘要不得压缩到不可点击。
- 空状态、加载状态、错误提示在移动视口下 MUST 不推挤页面造成明显跳动。

### FR-005 表单弹窗与确认弹窗

- 新增/编辑弹窗、状态确认弹窗、删除确认弹窗、重置密码弹窗、修改密码弹窗、系统设置确认弹窗在 `375px` 宽度下 MUST 可完整操作。
- 弹窗 MUST 适配移动视口高度：头部、内容区、底部按钮区域应可见或可滚动访问。
- 大表单弹窗（如 SKU、Banner）MUST 保持内容区滚动，底部主操作按钮不得丢失。
- 弹窗关闭按钮、取消按钮和主操作按钮 MUST 可点击，且不会被浏览器安全区、底部或滚动容器遮挡。
- 表单字段错误提示出现后 MUST 不导致显示/隐藏按钮、上传控件或底部操作区明显错位。

### FR-006 系统设置、个人资料与日志详情专项

- `/admin/settings/:tab` 在移动视口下 MUST 保持设置分组导航、表单字段和保存/重置操作可访问。
- `/admin/profile` 的主信息与账号安全区域在小屏下 MUST 单列可读，操作按钮不重复、不遮挡内容。
- `/admin/logs` 的日志详情抽屉在手机宽度下 MUST 可关闭、可滚动查看详情；不得因抽屉宽度导致页面失控横向滚动。
- `/admin/api-docs` 的接口路径、方法、状态、操作入口在移动视口下 MUST 可读或可横向滚动查看。

### FR-007 登录页与无权限页回归

- `/admin/login` MUST 保持既有移动端契约：`<1024px` 隐藏左侧品牌区，登录表单居中，最大宽度 520px。
- 登录页账号、密码、记住登录状态、登录按钮和语言占位 MUST 在 `375px` 宽度下可见且可操作。
- `/admin/forbidden` MUST 在手机视口下保持文案可读，返回或跳转入口不溢出。

### FR-008 测试与验收

- 实现阶段 MUST 至少补充管理端移动端 smoke 验收，推荐覆盖视口：
  - `375x812`
  - `390x844`
  - `768x1024`
  - `1440x1024`（桌面回归）
- SHOULD 使用 Playwright 或等价浏览器截图/交互 smoke 检查关键页面；Vitest 可补充结构性断言。
- 必测页面 SHOULD 包含：
  - `/admin/login`
  - `/admin/dashboard`
  - `/admin/tile-skus`
  - `/admin/brands`
  - `/admin/users`
  - `/admin/logs`
  - `/admin/settings/basic`
- 验收 MUST 明确记录是否存在页面级横向溢出、弹窗不可关闭、底部按钮不可达、筛选/分页控件重叠等问题。

## 5. UI / UE 约束

- 管理端仍保持“工业石材 · 暗色旗舰风”，不得因移动端适配切换为独立移动主题。
- 视觉应以“可读、可点、无明显溢出”为主，不追求手机端全新信息架构。
- 管理端页面为工作型界面，移动端布局 SHOULD 保持密度克制，避免引入营销式大卡片或大段说明文案。
- 按钮、输入框、选择框、分页按钮在手机宽度下 SHOULD 保持足够点击区域，文字不得被截断到不可理解。
- 表格若采用横向滚动，滚动容器 SHOULD 有清晰边界，避免用户误以为页面整体溢出。
- 弹窗底部操作区 SHOULD 与内容区分离，保证长表单滚动时主操作仍易于找到。
- 新增 UI 代码 MUST 优先复用现有 `AdminLayout`、页面样式、shadcn 基础组件和已有管理端交互模式。

## 6. 依赖与实施顺序

| 依赖 | 说明 |
|---|---|
| REQ-0004-admin-home | 管理端 Shell、Dashboard 与移动端基础结构来源 |
| REQ-0011-admin-sidebar-expand-collapse | 侧栏折叠与 `≤1023px` 响应式边界 |
| REQ-0013-admin-shell-padding-refine | 管理端 Shell padding 与 fluid 布局相关约束 |
| REQ-0000-build-design-system | Design Token 与组件使用约束 |
| `rules/ui-design.md` | Web 管理端视觉与 token 规范 |
| `src/web/README.md` | Web 目录与 Design System 使用约定 |

建议实施顺序：

1. 先确认 `/admin/*` 当前实现页面清单与移动端验收视口。
2. 处理 `AdminLayout` / `admin-home.css` 全局移动端稳定性。
3. 处理列表页筛选、表格、分页的共性问题。
4. 处理大弹窗、确认弹窗、日志详情抽屉。
5. 补充移动端 smoke 测试与截图验收记录。

**建议 OpenSpec change 命名**：`update-web-admin-mobile-adaptation`。

## 7. 关联需求

| 需求 / 模块 | 关系 |
|---|---|
| REQ-0004-admin-home | 父需求；管理端 Shell 与 Dashboard 基础 |
| REQ-0011-admin-sidebar-expand-collapse | 侧栏折叠与移动端断点边界 |
| REQ-0013-admin-shell-padding-refine | 内容区宽度、padding 与响应式布局策略 |
| REQ-0000-build-design-system | token、组件与视觉约束 |
| 店主 Web 展示端 | 明确不涉及 |
| 微信小程序 | 明确不涉及 |

## 8. 状态

```yaml
requirement_id: REQ-0027-mobile-page-adaptation
priority: P1
status: done
iteration: sprint-010
owner: product
parent_requirement: REQ-0004-admin-home
openspec_change: update-web-admin-mobile-adaptation
target_clients:
  web_admin: 本期
  web_catalog: 不涉及
  wechat_miniapp: 不涉及
api_change: false
database_change: false
orval_required: false
docker_compose_required: false
```
