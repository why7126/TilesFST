---
title: 需求验收标准
purpose: 定义管理后台首页的功能、技术、UI 与异常场景验收标准
content: 基于 requirement.md 与 prototype/web/admin-home 提炼
source: AI 根据 PRD 与原型生成，项目团队确认
update_method: PRD 或原型变更时同步更新
owner: 产品负责人
status: draft
note: REQ-0004 管理后台首页
---

# 验收标准

## 1. 功能验收

### 1.1 页面访问与布局

- [ ] **AC-001** 已登录 `admin`/`employee` 用户访问 `/admin/dashboard` 可看到管理后台首页。
- [ ] **AC-002** 页面采用左右布局：左侧 Sidebar 264px，右侧内容区独立滚动。
- [ ] **AC-003** Sidebar 高度为 `100vh`，`position: sticky`，不随右侧内容高度变化。
- [ ] **AC-004** 右侧内容区高度 `100vh`，`overflow: auto`，主内容最大宽度 1080px 居中。
- [ ] **AC-005** 未登录访问 `/admin/dashboard` 仍由路由守卫跳转 `/admin/login`（REQ-0001 行为保持）。

### 1.2 品牌与 Sidebar 导航

- [ ] **AC-006** Sidebar 顶部品牌名为 **TILESFST**（大写），不出现 STONEX。
- [ ] **AC-007** OPERATIONS 分组包含：首页、瓷砖 SKU、瓷砖品牌、瓷砖类目、Banner 管理。
- [ ] **AC-008** SYSTEM 分组包含：用户管理、系统设置。
- [ ] **AC-009** 当前页「首页」导航项为 active 态（品牌金弱强调 + 左侧指示条）。
- [ ] **AC-010** 非首页导航项点击后行为符合 design 约定（占位路由或建设中提示），不导致白屏。

### 1.3 用户菜单

- [ ] **AC-011** 用户菜单固定在 Sidebar 底部（`margin-top: auto`）。
- [ ] **AC-012** 用户菜单展示头像缩写、用户名、邮箱、展开箭头；数据来自 `auth/me` 或合理 fallback。
- [ ] **AC-013** 用户菜单按钮下方**不得**直接展示「退出登录」按钮。
- [ ] **AC-014** 点击用户菜单展开下拉框，位于按钮上方。
- [ ] **AC-015** 下拉框包含：个人资料、密码修改、0.5px 分隔线、退出登录。
- [ ] **AC-016** 「退出登录」使用风险色弱强调，与上方两项有分隔线区分。
- [ ] **AC-017** 点击「退出登录」清除登录态并跳转 `/admin/login`。
- [ ] **AC-018** 个人资料、密码修改为占位行为，不阻塞首页验收。

### 1.4 工作台内容 — 数据概览

- [ ] **AC-019** 展示 4 个指标卡：SKU 总数、品牌数量、Banner 数量、用户数量。
- [ ] **AC-020** 指标卡为四列网格（桌面端），含标签、数值、辅助说明。
- [ ] **AC-021** 关键数值使用品牌金强调；本期数据可为 mock，与 HTML 原型样例一致即可。

### 1.5 工作台内容 — 快捷操作

- [ ] **AC-022** 快捷操作为单行四列宫格，仅包含：新增 SKU、新增品牌、新增类目、新增 Banner。
- [ ] **AC-023** 不得出现：导入 SKU、导入图片、价格管理、操作日志。
- [ ] **AC-024** 每项含图标区、标题、简短说明；hover 有边框/位移反馈。
- [ ] **AC-025** 点击快捷操作有占位反馈（跳转占位页或 toast），不报错。

### 1.6 工作台内容 — 最近更新

- [ ] **AC-026** 最近更新为表格，列：更新时间、类型、名称、操作人。
- [ ] **AC-027** 类型列使用 badge 样式（SKU / 品牌 / Banner / 类目 / 系统）。
- [ ] **AC-028** 表格行 hover 有弱背景反馈；本期数据可为 mock（≥5 行样例）。

### 1.7 删除项验证

- [ ] **AC-029** 页面不得出现：顶部欢迎区域、今日待办、数据质量概览、风险提醒、热门材质、门店同步、材质库存分布。

## 2. 接口验收

| 范围 | 说明 |
|---|---|
| 本期 | **不新增** Dashboard 统计或审计 API |
| 复用 | `GET /api/v1/auth/me` 提供用户菜单展示信息 |
| 复用 | `POST /api/v1/auth/logout` 支持退出登录 |
| 后续 | 真实 summary / recent-updates 接口需单独 OpenSpec Change |

## 3. 数据验收

- [ ] 本期不新增 SQLite 表或迁移。
- [ ] Dashboard mock 数据集中定义（如 `sample-content` 或页面内常量），便于后续替换为 API。

## 4. 技术验收

- [ ] **AC-030** 重构 `AdminLayout`：由顶栏布局改为 Sidebar + 内容区布局。
- [ ] **AC-031** `DashboardPage` 实现三模块工作台，替换当前占位文案。
- [ ] **AC-032** 新增管理端 Sidebar / 用户菜单组件放入 `src/web/src/shared/ui/` 或 `shared/templates/`，不在 `pages/` 内重复实现 DS 能力。
- [ ] **AC-033** 样式使用 semantic token（`bg-page`、`text-brand-gold`、`border-border-default` 等），**禁止**在 TSX 中硬编码 `#18160F`、`#C8A055` 等（HTML 原型除外）。
- [ ] **AC-034** 视觉还原策略在 OpenSpec `design.md` 中声明（推荐 CSS Port 或 Tailwind + 原型对照，与登录页 fidelity 专项一致）。
- [ ] **AC-035** 补充前端布局与用户菜单交互测试（至少 smoke / 关键交互）。
- [ ] **AC-036** `/design-system` 预览页可展示新增管理端 Shell 组件（若新增复合组件）。

## 5. UI 与交互验收

- [ ] **AC-037** 视觉与 `prototype/web/admin-home.png` 并排验收通过（Golden Reference）。
- [ ] **AC-038** HTML 原型 `admin-home.html` 为最高优先级视觉参考。
- [ ] **AC-039** 圆角 2px–3px；分割线使用低透明白色 semantic border。
- [ ] **AC-040** 品牌金仅用于 Logo、激活态、关键数字和轻量强调。
- [ ] **AC-041** 用户菜单支持键盘可达性：`aria-expanded`、`role="menu"`、`role="menuitem"`。
- [ ] **AC-042** 响应式：`< 1024px` Sidebar 顶置、用户菜单隐藏；`< 640px` 网格单列、表格隐藏操作人列。

## 6. 异常场景验收

| 场景 | 期望表现 |
|---|---|
| 用户信息加载中 | Sidebar 用户区展示 skeleton 或 fallback，不阻塞整页 |
| 用户信息缺失 email | 邮箱行隐藏或展示占位，不破坏布局 |
| 退出登录失败 | 仍清除本地态并跳转登录页，或展示可理解错误提示 |
| 快捷操作目标未实现 | 占位提示，无 console 未捕获错误 |

## 7. 本期不包含（不作为验收阻塞项）

- 真实 Dashboard 统计 API 与缓存。
- 最近更新审计日志接口。
- SKU/品牌/类目/Banner 列表与表单页。
- 个人资料、密码修改完整流程。
- Sidebar 移动端抽屉与完整 touch 优化。
- 小程序管理端。

## 8. 验收通过条件

满足以下全部条件视为本需求验收通过：

1. 第 1 节 AC-001 ~ AC-029 全部通过。
2. 第 4 节技术验收 AC-030 ~ AC-036 通过。
3. 第 5 节 UI 验收 AC-037 ~ AC-042 通过，含 PNG 并排 checklist。
4. 第 6 节异常场景均可复现且表现符合预期。
