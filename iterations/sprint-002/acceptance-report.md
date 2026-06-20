---
title: Sprint 002 验收报告
purpose: 记录 Sprint 002 验收结果与遗留项（模板）
content: 基于 REQ-0004、REQ-0005、REQ-0005-user-management-list-refine、REQ-0003-login-remember-autofill、REQ-0005-brand-management、REQ-0005-tile-category-management、REQ-0006-tile-sku-management acceptance.md 及对应 OpenSpec Change
source: AI 根据迭代范围生成，Sprint 结束时由团队填写
update_method: Sprint 验收完成后更新
owner: 产品负责人
status: pending
note: Sprint 002 未开始验收；实现完成后逐项勾选
---

# Sprint 002 验收报告

## 验收概况

| 字段 | 内容 |
|---|---|
| Sprint | sprint-002 |
| 关联需求 | REQ-0004-admin-home、REQ-0005-user-management、REQ-0005-user-management-list-refine、REQ-0003-login-remember-autofill、REQ-0005-brand-management、REQ-0005-tile-category-management、REQ-0006-tile-sku-management、REQ-0007-tile-category-management-refine |
| 关联 BUG | BUG-0001-tile-category-enable-missing |
| 关联 Change | add-admin-home、add-user-management、fix-user-management-list-refine、add-login-remember-autofill、add-brand-management、add-tile-category-management、fix-tile-category-enable-action、fix-tile-category-management-refine、add-tile-sku-management |
| 计划验收日期 | 2026-06-28 |
| 验收结论 | **实现完成，待验收（Pending sign-off）** |
| 验收人 | _待填写_ |

## 功能验收

> 来源：`issues/requirements/REQ-0004-admin-home/acceptance.md`

### 1.1 页面访问与布局

- [ ] AC-001 已登录用户可访问 `/admin/dashboard`
- [ ] AC-002 左右布局 264px Sidebar + 独立滚动内容区
- [ ] AC-003 Sidebar 100vh sticky
- [ ] AC-004 右侧 100vh overflow auto，主内容 max-width 1080px
- [ ] AC-005 未登录跳转 `/admin/login`

### 1.2 品牌与 Sidebar 导航

- [ ] AC-006 品牌 TILESFST，无 STONEX
- [ ] AC-007 OPERATIONS 五 nav
- [ ] AC-008 SYSTEM 两 nav
- [ ] AC-009 首页 active 态
- [ ] AC-010 非首页占位反馈

### 1.3 用户菜单

- [ ] AC-011 ~ AC-018 用户菜单、下拉、退出、占位

### 1.4 ~ 1.7 工作台内容

- [ ] AC-019 ~ AC-029 数据概览、快捷操作、最近更新、删除项验证

## REQ-0005 功能验收

> 来源：`issues/requirements/REQ-0005-user-management/acceptance.md`  
> 状态：**apply 完成**（34/36 tasks；6.1 DS 可选跳过；待 `/opsx-archive`）

### 2.1 访问与权限

- [x] AC-001 ~ AC-005 路由、角色菜单、403/重定向（vitest + API 403）

### 2.2 列表、弹窗与操作

- [x] AC-006 ~ AC-028 筛选、列表、弹窗、重置密码、冻结/删除（实现 + pytest）

### 2.3 布局与视觉

- [x] AC-029 ~ AC-031 Sidebar 激活、布局、HTML v1 结构对照（trace checklist pass）
- [ ] AC-043 ~ AC-045 弹窗 PNG golden、design-system 预览（6.1 可选跳过）

### 2.4 接口与数据

- [x] AC-032 ~ AC-038 Admin Users API、Orval、DB（MinIO 上传为桩）

### 2.5 技术

- [x] AC-039 ~ AC-042 CSS Port、测试覆盖

## REQ-0005-user-management-list-refine 功能验收

> 来源：`issues/requirements/REQ-0005-user-management-list-refine/acceptance.md`  
> 状态：**未开始**（待 `fix-user-management-list-refine` opsx-apply）

### 筛选区与 keyword

- [ ] AC-001 ~ AC-006 无搜索按钮、自动查询、placeholder、keyword 仅 username/display_name

### 列表标题、用户列与分页

- [ ] AC-007 ~ AC-020 section-head/toolbar 移除、用户两行、分页精简

### 回归与技术

- [ ] AC-021 ~ AC-027 弹窗/指标卡/权限无回归；pytest/vitest/build；v2 PNG 并排

## REQ-0003-login-remember-autofill 功能验收

> 来源：`issues/requirements/REQ-0003-login-remember-autofill/acceptance.md`  
> 状态：**apply 完成**（17/18；vitest + trace checklist；待 archive）

### 记住凭证与自动填充

- [x] AC-001 ~ AC-007 本地存储、自动填充、JWT 行为无回归

### 登出与密码显隐

- [x] AC-008 ~ AC-014 登出清除、显隐切换、a11y、CSS Port

### 安全与回归

- [x] AC-015 ~ AC-019 vitest、build、左栏 refine 无回归

## REQ-0005-brand-management 功能验收

> 来源：`issues/requirements/REQ-0005-brand-management/acceptance.md`  
> 状态：**未开始**（待 `add-brand-management` opsx-apply）

### 访问、列表与删除

- [ ] AC-001 ~ AC-016 布局、指标卡、筛选、表格、删除规则、分页

### 弹窗与接口

- [ ] AC-020 ~ AC-029 弹窗字段、校验、Admin Brands API、Orval

### 技术与视觉

- [ ] AC-033 ~ AC-039 CSS Port、测试、HTML 原型并排（PNG 待补）

## REQ-0005-tile-category-management 功能验收

> 来源：`issues/requirements/REQ-0005-tile-category-management/acceptance.md`  
> 状态：**未开始**（待 `add-tile-category-management` opsx-apply）

### 访问、类目树与删除

- [ ] AC-001 ~ AC-019 布局、指标卡、检索、类目树联动、列表、删除规则、分页

### 弹窗与接口

- [ ] AC-023 ~ AC-033 弹窗字段、层级约束、Admin Tile Categories API、Orval

### 技术与视觉

- [ ] AC-037 ~ AC-043 CSS Port、测试、HTML 原型并排（PNG 待补）

## REQ-0006-tile-sku-management 功能验收

> 来源：`issues/requirements/REQ-0006-tile-sku-management/acceptance.md`  
> 状态：**apply 完成**（32/35 tasks；待 `/opsx-archive`；HTML gate 结构对照 pass）

### 访问、列表与筛选

- [x] AC-001 ~ AC-021 布局、指标卡、五维筛选、表格列、价格格式、分页（页码 UI 简化，见 trace §12 partial）

### 弹窗、媒体与上下架

- [x] AC-022 ~ AC-039 880px 弹窗、多图主图、多视频、save_mode、publish/unpublish、删除规则

### 接口、数据与技术

- [x] AC-042 ~ AC-053 Admin Tile SKU API、schema 扩展、Orval、测试（10 pytest passed）

### 视觉

- [x] AC-054 ~ AC-056 HTML 原型结构对照（trace.md checklist）；PNG 可选未导出

## 技术验收（REQ-0004）

- [ ] AC-030 ~ AC-036 AdminLayout 重构、组件位置、semantic token、测试、design-system 预览

## UI 与 PNG 验收

- [ ] AC-037 ~ AC-042 视觉与 PNG 并排、响应式
- [ ] `openspec/changes/add-admin-home/trace.md` PNG checklist ≥18 项 pass

## 接口与数据验收

### REQ-0004

- [ ] 无新 API；复用 auth/me、logout
- [ ] 无 DB 迁移
- [ ] mock 数据集中定义

### REQ-0005

- [x] Admin Users CRUD API 可用（`test_admin_users.py` 8 passed）
- [x] `users` 表迁移已应用
- [x] Orval 客户端已重新生成
- [ ] 头像上传经 MinIO 授权链路（桩实现，待完整 MinIO change）

### REQ-0005-user-management-list-refine

- [ ] keyword 仅匹配 username、display_name（pytest）
- [ ] 无 DB / Orval 变更
- [ ] v2 `user-management-list.png` 1280×1024 并排验收

### REQ-0003-login-remember-autofill

- [ ] 无后端 / DB / Orval 变更
- [ ] `stonex_login_credentials` 读写与登出清除
- [ ] `npx vitest run src/features/auth` 通过

### REQ-0005-brand-management

- [ ] Admin Brands CRUD API 可用
- [ ] `brands` 表迁移已应用
- [ ] Orval 客户端已重新生成
- [ ] Logo 上传经 MinIO 授权链路

### REQ-0005-tile-category-management

- [ ] Admin Tile Categories CRUD + tree API 可用
- [ ] `tile_categories` 表扩展迁移已应用
- [ ] Orval 客户端已重新生成

### REQ-0006-tile-sku-management

- [x] Admin Tile SKU CRUD + publish/unpublish API 可用（`test_admin_tile_skus.py` 10 passed）
- [x] `tiles` 表扩展 + `tile_videos` 迁移已应用
- [x] Orval 客户端已重新生成
- [x] 图片/视频上传 API 端点（桩 object_key；MinIO 完整链路待后续 change）

## 测试验收

- [x] `npx vitest run src/features/admin src/pages/admin` — 8 passed
- [x] `cd src/backend && uv run pytest tests/test_admin_users.py` — 8 passed
- [x] `npm run build` — success
- [x] `docker compose build web` — success
- [ ] Docker 运行时 `/admin/dashboard` 人工登录验证
- [ ] 1280×1024 PNG 并排人工 sign-off

## OpenSpec Tasks 完成度

> 来源：`openspec/changes/add-admin-home/tasks.md`

| 任务组 | 总数 | 完成 | 状态 |
|---|---|---|---|
| §1 CSS Port 与模块结构 | 4 | 4 | ✓ 完成 |
| §2 布局与页面重构 | 6 | 6 | ✓ 完成 |
| §3 响应式 | 2 | 2 | ✓ 完成 |
| §4 Design System 预览 | 1 | 1 | ✓ 完成 |
| §5 测试 | 3 | 3 | ✓ 完成 |
| §6 构建与部署 | 2 | 2 | ✓ 完成 |
| §7 视觉验收 | 3 | 3 | ✓ 完成（CSS port + checklist；PNG 人工复核待 Sprint 验收） |
| §8 文档与追溯 | 3 | 3 | ✓ 完成 |
| §9 归档准备 | 1 | 0 | 待 `/opsx-archive` |
| **add-admin-home 合计** | **25** | **24** | **96%** |

### add-user-management

| 任务组 | 总数 | 完成 | 状态 |
|---|---|---|---|
| §1–§7 实现与测试 | 31 | 31 | ✓ 完成 |
| §8 Docker | 1 | 1 | ✓ Web 200 / API 401 |
| §9 HTML/PNG gate | 3 | 3 | trace checklist pass |
| §10 文档 | 3 | 3 | ✓ |
| §6 DS（可选） | 1 | 0 | 跳过 |
| §11 archive | 1 | 1 | ✓ archived 2026-06-20 |

### fix-user-management-list-refine

| 任务组 | 总数 | 完成 | 状态 |
|---|---|---|---|
| §1–§2 后端 + 前端 v2 UI | 8 | 8 | ✓ 完成 |
| §3–§4 测试与构建 | 5 | 5 | ✓ pytest 9 / vitest pass / build |
| §5 HTML 视觉 gate | 4 | 3 | trace pass；5.3 PNG 可选 |
| §6 文档与归档 | 3 | 3 | ✓ archived 2026-06-20 |

### add-login-remember-autofill

| 任务组 | 总数 | 完成 | 状态 |
|---|---|---|---|
| §1–§5 实现与测试 | 16 | 16 | ✓ 完成 |
| §6–§7 冒烟与归档 | 5 | 5 | ✓ archived 2026-06-20 |

### add-brand-management

| 任务组 | 总数 | 完成 | 状态 |
|---|---|---|---|
| §1–§5 后端 + 前端实现 | 26 | 26 | ✓ 完成 |
| §6 DS 预览（可选） | 1 | 0 | 跳过 |
| §7–§8 测试与构建 | 3 | 3 | ✓ Docker 200/401 |
| §9 HTML 视觉 gate | 3 | 3 | trace checklist pass |
| §10 文档与归档 | 3 | 2 | 10.3 PNG 可选；10.4 待 archive |

### add-tile-category-management

| 任务组 | 总数 | 完成 | 状态 |
|---|---|---|---|
| §1–§5 后端 + 前端实现 | 26 | 26 | ✓ 完成 |
| §6 DS 预览（可选） | 1 | 0 | 跳过 |
| §7–§8 测试与构建 | 3 | 3 | ✓ Docker 200/401 |
| §9 HTML 视觉 gate | 3 | 2 | 9.1–9.2 pass；9.3 PNG 待补 |
| §10 文档 | 3 | 3 | ✓ archived 2026-06-20 |

### add-tile-sku-management

| 任务组 | 总数 | 完成 | 状态 |
|---|---|---|---|
| §1–§6 后端 + 前端 + 测试 | 28 | 28 | ✓ 完成 |
| §7 Docker | 1 | 1 | ✓ Web 200 / API 401 |
| §8 HTML 视觉 gate | 3 | 3 | trace checklist pass（2 partial 已记录） |
| §9 文档 | 2 | 2 | ✓ |
| §9.3 PNG（可选） | 1 | 0 | 跳过 |
| §9.4 archive | 1 | 0 | 待 `/opsx-archive` |

### fix-tile-category-management-refine（REQ-0007）

| 任务组 | 总数 | 完成 | 状态 |
|---|---|---|---|
| §1 启停确认 | 3 | 0 | 待 `/opsx-apply` |
| §2 布局精简 | 3 | 0 | 待 apply |
| §3 分页 v2 | 3 | 0 | 待 apply |
| §4 测试 | 5 | 0 | 待 apply |
| §5 冒烟与视觉 | 3 | 0 | 待 apply |
| §6 追溯与归档 | 2 | 0 | 待 apply + archive |

### fix-tile-category-enable-action（BUG-0001）

| 任务组 | 总数 | 完成 | 状态 |
|---|---|---|---|
| §1 前端修复 | 2 | 2 | 完成 |
| §2 测试 | 3 | 3 | 完成 |
| §3 冒烟 | 2 | 2 | 完成 |
| §4 追溯与归档 | 3 | 3 | 已 archive（--skip-specs） |

## 问题清单

| 编号 | 描述 | 严重程度 | 状态 |
|---|---|---|---|
| I-01 | BUG-0001 类目停用行无「启用」按钮 | high | 已修复并 archive |
| I-02 | REQ-0007 类目页 UI refine 待实现 | medium | 已纳入 sprint-002；待 fix change apply |

## 遗留风险

| 编号 | 描述 | 优先级 | 状态 |
|---|---|---|---|
| L-01 | PNG 视觉 sign-off | P0 | 待关闭 |
| L-02 | `add-admin-home` 归档 | P0 | 待关闭 |
| L-03 | REQ-0001 退出入口文档同步 | P1 | 待确认 |
| L-04 | `add-user-management` 实现与归档 | P0 | **archived** 2026-06-20 |
| L-05 | 用户管理 list/modal PNG sign-off | P0 | 待关闭 |
| L-05b | fix-user-management-list-refine 实现与 v2 PNG sign-off | P1 | **archived**；主 spec 仍为 v1 baseline，v2 MODIFIED 待合入 |
| L-06 | add-login-remember-autofill 实现与归档 | P1 | **archived** 2026-06-20 |
| L-07 | add-brand-management 实现与归档 | P0 | **32/35 apply 完成**；待 archive |
| L-08 | 品牌管理 HTML/PNG sign-off | P1 | HTML trace pass；PNG 可选 |
| L-09 | add-tile-category-management 实现与归档 | P0 | **archived** 2026-06-20；specs synced |
| L-10 | 类目管理 HTML/PNG sign-off | P1 | HTML trace pass；PNG 待补 |
| L-11 | add-tile-sku-management 实现与归档 | P0 | **32/35 apply 完成**；待 archive |
| L-12 | SKU 管理 HTML/PNG sign-off | P1 | HTML trace pass；PNG 可选 |
| L-13 | Sprint-002 容量超支（57 人天 / 2 周） | P1 | 监控；含 REQ-0007 +2 人天 |
| L-14 | BUG-0001 类目启用 UI 缺陷 | P0 | 已修复并 archive |
| L-15 | fix-tile-category-management-refine 实现与归档 | P1 | 已纳入 sprint-002；待 apply |

## 验收结论

- **结论**：_待 Sprint 结束填写_
- **日期**：_
- **备注**：_
