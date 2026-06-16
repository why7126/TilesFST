---
title: Sprint 002 发布说明
purpose: 记录 Sprint 002 交付能力与发布注意事项（初稿）
content: 基于 REQ-0004、REQ-0005、REQ-0005-user-management-list-refine、REQ-0003-login-remember-autofill、REQ-0005-brand-management、REQ-0005-tile-category-management 及对应 OpenSpec Change
source: AI 根据迭代范围生成，项目团队确认
update_method: Sprint 完成或范围变更时更新
owner: 项目负责人
status: draft
note: Sprint 002 规划中；实现完成后更新为 published
---

# Sprint 002 发布说明

## 版本信息

| 字段 | 内容 |
|---|---|
| Sprint | sprint-002 |
| 关联需求 | REQ-0004-admin-home、REQ-0005-user-management、REQ-0005-user-management-list-refine、REQ-0003-login-remember-autofill、REQ-0005-brand-management、REQ-0005-tile-category-management |
| 关联 Change | add-admin-home、add-user-management、fix-user-management-list-refine、add-login-remember-autofill、add-brand-management、add-tile-category-management |
| 计划周期 | 2026-06-15 ~ 2026-06-28 |
| 发布状态 | **规划中（Draft）** |

## 新增功能（计划）

### Web 管理端工作台首页

- `/admin/dashboard` 管理后台首页 V5
- 264px 固定 Sidebar（100vh）+ 右侧独立滚动工作台
- 品牌 **TILESFST**；OPERATIONS / SYSTEM 导航分组
- Sidebar 底部用户菜单与下拉框（个人资料、密码修改、退出登录）
- 数据概览（4 指标卡）、快捷操作（4 项新建入口）、最近更新（表格）
- 本期使用 mock 数据；Sidebar 非首页链接与快捷操作为占位

### Admin Shell 基座

- CSS Port：`features/admin/styles/admin-home.css`
- 组件：`AdminSidebar`、`AdminUserMenu`、Dashboard 子模块
- `/design-system` 可选 Admin Shell 预览

### Web 管理端用户管理（计划）

- `/admin/users` 用户列表：搜索、筛选、分页、统计指标卡
- 添加/编辑用户弹窗（用户名 4–32 位、头像、昵称、角色）
- 重置密码（一次性展示）、冻结/解冻、软删除（仅从未登录用户）
- 仅 `admin` 角色可见用户管理菜单并可操作
- CSS Port：`features/admin/styles/user-management.css`（或等价路径）
- 后端 Admin Users API；`users` 表扩展（头像、软删除状态等）

### Web 管理端用户管理列表页 UI 优化（计划）

- `/admin/users` 列表区 v2：无「搜索」按钮；筛选 5 列；关键词 placeholder「搜索用户名/昵称」
- 用户列用户名/昵称两行；删除标题行与 toolbar；分页左「共 x 个用户」
- 后端 `keyword` 仅匹配用户名与昵称（不含邮箱/手机号）
- 弹窗、指标卡、行操作无变更

### Web 管理端登录页增强（计划）

- `/admin/login` 勾选「记住登录状态」且登录成功后，下次进入自动填充用户名与密码
- 退出登录清除本地保存的凭证
- 密码输入框支持显示/隐藏切换（眼睛图标）
- 仅前端变更；`remember_me` JWT 行为不变

### Web 管理端瓷砖品牌管理（计划）

- `/admin/brands` 品牌列表：搜索、状态筛选、四指标卡、分页（20/50/100）
- 新增/编辑品牌弹窗（720px）；启用/停用；条件删除（未关联 SKU 且已停用）
- `admin` 与 `employee` 可维护品牌主数据
- CSS Port：`features/admin/styles/brand-management.css`
- 后端 Admin Brands API；`brands` 表；Logo MinIO 上传

### Web 管理端瓷砖类目管理（计划）

- `/admin/tile-categories` 类目树（280px）+ 列表联动；四指标卡；检索（名称/编码、状态、层级）
- 新增/编辑类目弹窗（560px）；启用/停用；条件删除（未绑定 SKU 且已停用）；最多三级类目
- `admin` 与 `employee` 可维护类目主数据；无导出；「调整排序」本期占位
- CSS Port：`features/admin/styles/tile-category-management.css`
- 后端 Admin Tile Categories API；扩展 `tile_categories` 表

## 优化项（计划）

- 移除 `AdminLayout` 顶栏外露退出按钮，退出收纳至用户菜单下拉（**BREAKING** UI 相对 Sprint 001）
- 用户管理列表页筛选与分页信息层级收紧（REQ-0005-user-management-list-refine）
- 登录后工作台视觉与登录页暗色旗舰风统一

## BUG 修复

无（本 Sprint 无 BUG 范围）。

## 兼容性影响

| 影响面 | 说明 |
|---|---|
| 后端 API | REQ-0005 新增 Admin Users API；REQ-0005-brand-management 新增 Admin Brands API；REQ-0005-tile-category-management 新增 Admin Tile Categories API |
| 数据库 | REQ-0005 需 `users` 表迁移；REQ-0005-brand-management 需 `brands` 表；REQ-0005-tile-category-management 需扩展 `tile_categories` 表 |
| Orval | REQ-0005、REQ-0005-brand-management、REQ-0005-tile-category-management 完成后需重新生成 |
| REQ-0005-user-management-list-refine | 无 API 端点变更；keyword 查询范围收窄 |
| REQ-0003-login-remember-autofill | 无 API/DB 变更 |
| Docker | Web + Backend 镜像重建 |
| REQ-0001 | 退出登录入口位置变更（行为不变）；冻结用户登录拒绝 |

## 升级说明（计划）

1. `./scripts/docker-up.sh`
2. 使用已有 admin 账号登录 `http://localhost:3000/admin/login`（可验证记住凭证与密码显隐）
3. 登录成功后访问 `http://localhost:3000/admin/dashboard`
4. 使用 `admin` 账号访问 `http://localhost:3000/admin/users` 验证用户管理（含列表 v2 筛选/分页）
5. 使用 `admin` 或 `employee` 访问 `http://localhost:3000/admin/brands` 验证品牌管理
6. 使用 `admin` 或 `employee` 访问 `http://localhost:3000/admin/tile-categories` 验证类目管理
7. 视觉验收：1280×1024 并排 `admin-home.png`、`user-management-list.png`（v2 refine）、`user-management-modal.png`、`brand-management.html`、`tile-category-management.html`

## 已知限制（计划保留）

- Dashboard 指标与最近更新为 mock 数据
- SKU / Banner 管理页未实现
- 个人资料、密码修改为占位
- 用户自助注册、细粒度 RBAC 未实现
- 移动端 Sidebar 仅基础降级（桌面为主验收视口）

## 关联验收

- `iterations/sprint-002/acceptance-report.md`（Sprint 结束时填写）
- `openspec/changes/add-admin-home/trace.md`（PNG checklist）
- `openspec/changes/add-user-management/trace.md`
- `openspec/changes/fix-user-management-list-refine/trace.md`
- `openspec/changes/add-login-remember-autofill/trace.md`
- `openspec/changes/add-brand-management/trace.md`
- `openspec/changes/add-tile-category-management/trace.md`
