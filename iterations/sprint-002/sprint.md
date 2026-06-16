---
title: Sprint 002 迭代说明
purpose: 记录 Sprint 002 目标、范围、Change、工作量与风险
content: 基于 REQ-0004 管理后台首页、REQ-0005 用户管理、REQ-0005-user-management-list-refine 用户管理列表页 UI 优化、REQ-0003 登录记住凭证与密码显隐、REQ-0005-brand-management 瓷砖品牌管理、REQ-0005-tile-category-management 瓷砖类目管理及对应 OpenSpec Change 规划
source: AI 根据 issues/openspec 目录生成，项目团队确认
update_method: 迭代范围或状态变化时更新
owner: 项目负责人
status: in_progress
note: add-admin-home 已 archive；add-user-management 实现中；REQ-0005-user-management-list-refine / fix-user-management-list-refine 已纳入；REQ-0003-login-remember-autofill 已纳入；REQ-0005-brand-management 已纳入；REQ-0005-tile-category-management 已纳入
---

# Sprint 002

## Sprint 目标

本迭代交付六项管理端能力：

1. **REQ-0004 管理后台首页 V5** — 登录后的 `/admin/dashboard` 从占位页升级为与原型一致的专业工作台。
2. **REQ-0005 管理后台用户管理** — `/admin/users` 列表、筛选、CRUD、冻结/解冻、软删除与重置密码；仅 `admin` 可访问。
3. **REQ-0005-user-management-list-refine 用户管理列表页 UI 优化** — 筛选区去搜索按钮、keyword 收窄、用户列两行、分页精简；依赖 REQ-0005 基线。
4. **REQ-0003-login-remember-autofill 登录页记住凭证与密码显隐** — `/admin/login` 勾选记住后自动填充用户名/密码；密码框显隐切换。
5. **REQ-0005-brand-management 瓷砖品牌管理** — `/admin/brands` 列表、筛选、新增/编辑、启停、条件删除与 Logo 上传；`admin` 与 `employee` 可访问。
6. **REQ-0005-tile-category-management 瓷砖类目管理** — `/admin/tile-categories` 类目树+列表联动、检索、新增/编辑、启停、条件删除；最多三级类目；`admin` 与 `employee` 可访问。

### REQ-0004 要点

- 264px 固定 Sidebar（100vh）+ 右侧独立滚动内容区
- OPERATIONS / SYSTEM 导航分组、底部用户菜单与下拉框（退出收纳至下拉）
- Dashboard 三模块：数据概览、快捷操作（4 项）、最近更新（mock 数据）
- CSS Port 视觉对齐 `admin-home.html` / `admin-home.png`
- OpenSpec `add-admin-home` 实现、测试、PNG 验收与归档

### REQ-0005 要点

- 用户列表：搜索、筛选、分页、统计指标卡
- 添加/编辑弹窗（用户名 4–32 位、头像、昵称、角色）
- 重置密码（一次性展示）、冻结/解冻、软删除（仅从未登录）
- 后端 Admin Users API + `users` 表扩展 + 头像 MinIO 上传
- CSS Port 对齐 `user-management-list.png` / `user-management-modal.png`
- OpenSpec `add-user-management`（实现中）

### REQ-0005-user-management-list-refine 要点

- 子需求：优化 `add-user-management` 已落地列表页（O-01～O-06）
- 删除「搜索」按钮；筛选 5 列；placeholder「搜索用户名/昵称」；自动查询（防抖/回车/筛选项变更）
- 删除 `section-head`、`table-toolbar`；用户列用户名/昵称两行；分页左「共 x 个用户」
- 后端 `keyword` 仅匹配 `username`、`display_name`（移除 email/phone）
- 弹窗、指标卡、行操作、权限 **不回归**
- OpenSpec `fix-user-management-list-refine`（proposed，待 `/opsx-apply`）

### REQ-0003-login-remember-autofill 要点

- 勾选「记住登录状态」且登录成功 → `localStorage` 保存用户名/密码，下次自动填充
- 未勾选成功 / 登出 → 清除本地凭证（`stonex_login_credentials`）
- 密码输入框显隐切换（`.password-wrap` + 眼睛图标）
- 仅前端变更；不改后端 API / DB / Orval
- OpenSpec `add-login-remember-autofill`（proposed，待 `/opsx-apply`）

### REQ-0005-brand-management 要点

- 品牌列表：关键词/状态筛选、四指标卡、分页（含每页 20/50/100）
- 新增/编辑弹窗（720px、固定字段顺序）；无导出、无批量操作
- 启用/停用；删除仅 `sku_count=0` 且停用时可执行
- 后端 Admin Brands API + `brands` 表 + Logo MinIO 上传
- CSS Port 对齐 `brand-management.html` / `brand-management-modal.html`
- OpenSpec `add-brand-management`（proposed，待 `/opsx-apply`）

### REQ-0005-tile-category-management 要点

- 类目树（280px）+ 列表联动；四指标卡；检索（名称/编码、状态、层级）
- 新增/编辑弹窗（560px、单列六字段）；无导出；工具栏仅「调整排序」（本期占位）
- 启用/停用；删除仅 `sku_count=0` 且停用时可执行；最多三级类目
- 后端 Admin Tile Categories API + 扩展 `tile_categories` 表
- CSS Port 对齐 `tile-category-management.html` / `tile-category-management-add.html`
- OpenSpec `add-tile-category-management`（proposed，待 `/opsx-apply`）

本迭代为后续 SKU / Banner 管理模块提供统一 Admin Shell、用户体系、品牌与类目主数据基座，并优化登录表单体验。

## Scope

### 包含需求

| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| REQ-0004 | 管理后台首页 | P0 | Ready | V5 精简工作台；依赖 REQ-0001 认证 |
| REQ-0005 | 管理后台用户管理 | P0 | Ready | 列表 + 弹窗 + 权限；依赖 REQ-0004 Admin Shell |
| REQ-0005-user-management-list-refine | 用户管理列表页 UI 优化 | P1 | Ready | fix-* 专项；依赖 REQ-0005 基线 |
| REQ-0003-login-remember-autofill | 登录记住凭证与密码显隐 | P1 | Ready | 仅前端；依赖 REQ-0001 登录页 CSS Port |
| REQ-0005-brand-management | 瓷砖品牌管理 | P0 | Ready | 列表 + 弹窗 + 启停/删除；依赖 REQ-0004 Admin Shell |
| REQ-0005-tile-category-management | 瓷砖类目管理 | P0 | Partially Ready | 类目树+列表 + 弹窗 + 启停/删除；依赖 REQ-0004 Admin Shell |

### 包含 BUG

无。

### 包含 Change

| Change ID | 关联需求 | 状态 | Sprint 目标 |
|---|---|---|---|
| `add-admin-home` | REQ-0004 | archived | Admin Shell + Dashboard + PNG gate |
| `add-user-management` | REQ-0005 | applied | 用户管理 API + 页面 + PNG gate |
| `fix-user-management-list-refine` | REQ-0005-user-management-list-refine | proposed | 列表页 v2 UI + keyword 收窄 + PNG gate |
| `add-login-remember-autofill` | REQ-0003-login-remember-autofill | proposed | 登录凭证自动填充 + 密码显隐 |
| `add-brand-management` | REQ-0005-brand-management | proposed | 品牌管理 API + 页面 + HTML/PNG gate |
| `add-tile-category-management` | REQ-0005-tile-category-management | proposed | 类目管理 API + 树/列表页 + HTML gate |

### 不包含（延后至后续 Sprint）

| 项目 | 延后原因 |
|---|---|
| Dashboard 真实统计 / 审计 API | PRD 明确本期 mock |
| SKU / Banner 业务页 | 独立 REQ |
| 个人资料 / 密码修改完整流程 | 占位即可 |
| 用户自助注册 / 细粒度 RBAC | REQ-0005 Out of Scope |
| 瓷砖目录（店主端） | 产品管理域后续迭代 |
| 忘记密码页实现 | `add-forgot-password` 未纳入本 Sprint |

## 工作量估算

| 工作包 | 规模 | 前端 | 后端 | 测试 | 合计人天 |
|---|---|---|---|---|---|
| **REQ-0004** | | | | | |
| CSS Port `admin-home.css` | M | 3 | — | — | 3 |
| AdminSidebar + UserMenu | L | 5 | — | — | 5 |
| DashboardPage 三模块 + mock | M | 2 | — | — | 2 |
| 响应式降级 | S | 1 | — | — | 1 |
| 单元 / smoke 测试 | S | — | — | 1 | 1 |
| PNG 并排视觉验收 | M | 2 | — | 1 | 3 |
| 文档 / trace / 归档 | S | 0.5 | — | 0.5 | 1 |
| **REQ-0005** | | | | | |
| `users` schema + Admin Users API | L | — | 4 | — | 4 |
| 用户管理页 CSS Port + 弹窗 | L | 4 | — | — | 4 |
| 头像上传 + Orval | M | 1 | 1 | — | 2 |
| 权限（仅 admin）前后端 | S | 0.5 | 0.5 | — | 1 |
| 用户管理测试 + PNG 验收 | M | 1 | — | 2 | 3 |
| 文档 / trace / 归档 | S | 0.5 | 0.5 | — | 1 |
| **REQ-0005-user-management-list-refine** | | | | | |
| 列表页 v2 CSS Port + 交互 | M | 1.5 | — | — | 1.5 |
| keyword 收窄 + repository 测试 | S | — | 0.5 | 0.5 | 1 |
| vitest + v2 PNG 验收 + 归档 | S | 0.5 | — | 1 | 1.5 |
| **REQ-0003-login-remember-autofill** | | | | | |
| `login-credentials.ts` + LoginForm | M | 1.5 | — | — | 1.5 |
| 密码显隐 CSS Port | S | 0.5 | — | — | 0.5 |
| auth vitest + 构建 | S | — | — | 0.5 | 0.5 |
| trace / 归档 | S | 0.25 | — | 0.25 | 0.5 |
| **REQ-0005-brand-management** | | | | | |
| `brands` schema + Admin Brands API | L | — | 3 | — | 3 |
| 品牌管理页 CSS Port + 弹窗 | L | 3.5 | — | — | 3.5 |
| Logo 上传 + Orval | M | 0.5 | 1 | — | 1.5 |
| 删除/启停规则前后端 | M | 0.5 | 0.5 | — | 1 |
| 品牌管理测试 + HTML/PNG 验收 | M | 1 | — | 1.5 | 2.5 |
| 文档 / trace / 归档 | S | 0.25 | 0.25 | — | 0.5 |
| **REQ-0005-tile-category-management** | | | | | |
| `tile_categories` 扩展 + Admin Categories API | L | — | 4 | — | 4 |
| 类目管理页 CSS Port + 树 + 弹窗 | L | 4.5 | — | — | 4.5 |
| 树/列表联动 + Orval | M | 1 | 0.5 | — | 1.5 |
| 删除/深度/启停规则前后端 | M | 0.5 | 0.5 | — | 1 |
| 类目管理测试 + HTML 验收 | M | 1 | — | 2 | 3 |
| 文档 / trace / 归档 | S | 0.25 | 0.25 | — | 0.5 |
| **合计** | | **30.25** | **13** | **9.25** | **41**（Story Points: 67） |

## 里程碑

| 阶段 | 交付 | 目标日期 |
|---|---|---|
| M1 CSS Port + 模块骨架 | add-admin-home tasks §1 | 2026-06-18 |
| M2 AdminLayout + Dashboard | add-admin-home tasks §2–3 | 2026-06-22 |
| M3 add-admin-home 测试 + 构建 | tasks §5–6 | 2026-06-24 |
| M4 admin-home PNG 验收 + archive | tasks §7–9 | 2026-06-26 |
| M5 requirement-to-opsx + add-user-management 实现 | REQ-0005 / opsx apply | 2026-06-27 |
| M6 用户管理测试 + PNG 验收 | REQ-0005 acceptance | 2026-06-28 |
| M6b fix-user-management-list-refine 实现 + v2 PNG 验收 | REQ-0005-user-management-list-refine | 2026-06-28 |
| M7 add-login-remember-autofill 实现 + 测试 + archive | REQ-0003-login-remember-autofill | 2026-06-28 |
| M8 add-brand-management 实现 + 测试 + HTML 验收 | REQ-0005-brand-management | 2026-06-28 |
| M9 add-tile-category-management 实现 + 测试 + HTML 验收 | REQ-0005-tile-category-management | 2026-06-28 |

## 风险

| 编号 | 风险 | 影响 | 缓解 |
|---|---|---|---|
| R-01 | CSS Port fidelity 不足 | 视觉验收失败 | 严格 HTML > PNG 优先级；1280×1024 checklist |
| R-02 | 误复用 catalog `Sidebar` | 架构混乱 | 新建 `AdminNavSidebar`，design D2 已约束 |
| R-03 | REQ-0001 退出入口变更 | 回归认知冲突 | delta spec MODIFIED「退出登录」；acceptance 注明 |
| R-04 | `auth/me` 无 email 字段 | 用户菜单展示异常 | fallback `{username}@tilesfst.com` |
| R-05 | 容量偏紧（22 人天 / 2 周，含 REQ-0005） | 延期 | 先完成 add-admin-home archive；REQ-0005 并行 opsx |
| R-06 | 角色/状态与 auth spec 不一致 | API 返工 | opsx design 定稿映射；MODIFIED auth spec |
| R-07 | 用户管理依赖 Admin Shell | 阻塞前端 | REQ-0004 先验收 Sidebar 再开用户管理页 |
| R-08 | Sprint 容量追加 REQ-0003 | 延期风险 | 登录增强仅前端 ~2 人天；可与 REQ-0005 收尾并行 |
| R-09 | Sprint 容量追加品牌管理 | 延期风险 | 品牌管理 ~6 人天；与用户管理/登录增强并行；`sku_count` 本期默认 0 |
| R-10 | Sprint 容量追加类目管理 | 延期风险 | 类目管理 ~8 人天；含树+表联动；与品牌管理并行；PNG 待补齐可先 HTML 并排 |
| R-11 | 列表 refine 与 add-user-management 归档顺序 | archive 失败 | 先完成 add-user-management 或同批 archive；MODIFIED 标题对齐 user-management capability |

## 依赖

```text
REQ-0001（已 resolved）
  └── auth / ProtectedRoute / logout / LoginForm
        ├── add-login-remember-autofill（REQ-0003-login-remember-autofill）
        ├── add-admin-home（REQ-0004）
        │     └── Admin Shell 基座
        └── add-user-management（REQ-0005）
              ├── fix-user-management-list-refine（REQ-0005-user-management-list-refine）
              ├── add-brand-management（REQ-0005-brand-management）
              ├── add-tile-category-management（REQ-0005-tile-category-management）
              └── [后续] SKU / Banner REQ
```

## 发布计划

- 开发环境：`./scripts/docker-up.sh` 验证 `/admin/login`、`/admin/dashboard`、`/admin/users`、`/admin/brands` 与 `/admin/tile-categories`
- REQ-0004：无后端 / DB / API 变更；无需 Orval
- REQ-0005：需 DB 迁移、OpenAPI 更新与 Orval 重新生成
- REQ-0005-user-management-list-refine：无 DB 迁移；后端 keyword 行为变更；无需 Orval（无新端点）
- REQ-0003-login-remember-autofill：仅 Web 前端；无需 Orval / DB
- REQ-0005-brand-management：需 `brands` 表迁移、OpenAPI 更新与 Orval 重新生成
- REQ-0005-tile-category-management：需 `tile_categories` 表扩展、OpenAPI 更新与 Orval 重新生成
- Sprint 结束：`/opsx-archive` 各 change + 更新 `acceptance-report.md`

## 关联文档

| 文档 | 路径 |
|---|---|
| Sprint 索引 | `iterations/sprint-002/sprint.yaml` |
| 需求 PRD（首页） | `issues/requirements/REQ-0004-admin-home/requirement.md` |
| 验收标准（首页） | `issues/requirements/REQ-0004-admin-home/acceptance.md` |
| OpenSpec Change（首页） | `openspec/changes/add-admin-home/` |
| PNG Golden（首页） | `issues/requirements/REQ-0004-admin-home/prototype/web/admin-home.png` |
| 需求 PRD（用户管理） | `issues/requirements/REQ-0005-user-management/requirement.md` |
| 验收标准（用户管理） | `issues/requirements/REQ-0005-user-management/acceptance.md` |
| OpenSpec Change（用户管理） | `openspec/changes/add-user-management/`（待创建） |
| PNG Golden（用户管理 v1） | `issues/requirements/REQ-0005-user-management/prototype/web/user-management-list.png` |
| 需求 PRD（列表 UI 优化） | `issues/requirements/REQ-0005-user-management-list-refine/requirement.md` |
| 验收标准（列表 UI 优化） | `issues/requirements/REQ-0005-user-management-list-refine/acceptance.md` |
| OpenSpec Change（列表 UI 优化） | `openspec/changes/fix-user-management-list-refine/` |
| HTML/PNG Golden（列表 v2） | `issues/requirements/REQ-0005-user-management-list-refine/prototype/web/user-management-list.html` |
| 需求 PRD（登录增强） | `issues/requirements/REQ-0003-login-remember-autofill/requirement.md` |
| 验收标准（登录增强） | `issues/requirements/REQ-0003-login-remember-autofill/acceptance.md` |
| OpenSpec Change（登录增强） | `openspec/changes/add-login-remember-autofill/` |
| 需求 PRD（品牌管理） | `issues/requirements/REQ-0005-brand-management/requirement.md` |
| 验收标准（品牌管理） | `issues/requirements/REQ-0005-brand-management/acceptance.md` |
| OpenSpec Change（品牌管理） | `openspec/changes/add-brand-management/` |
| HTML 原型（品牌管理） | `issues/requirements/REQ-0005-brand-management/prototype/web/brand-management.html` |
| 需求 PRD（类目管理） | `issues/requirements/REQ-0005-tile-category-management/requirement.md` |
| 验收标准（类目管理） | `issues/requirements/REQ-0005-tile-category-management/acceptance.md` |
| OpenSpec Change（类目管理） | `openspec/changes/add-tile-category-management/` |
| HTML 原型（类目管理） | `issues/requirements/REQ-0005-tile-category-management/prototype/web/tile-category-management.html` |
