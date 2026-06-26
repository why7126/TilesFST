---
title: Sprint 002 迭代说明
purpose: 记录 Sprint 002 目标、范围、Change、工作量与风险
content: 基于 REQ-0004 管理后台首页、REQ-0005 用户管理、REQ-0005-user-management-list-refine 用户管理列表页 UI 优化、REQ-0003 登录记住凭证与密码显隐、REQ-0005-brand-management 瓷砖品牌管理、REQ-0005-tile-category-management 瓷砖类目管理、REQ-0006-tile-sku-management 瓷砖 SKU 管理、BUG-0002 品牌管理 UI 一致性修复、BUG-0003 品牌图片显示与提示布局修复、BUG-0004 品牌 Logo 上传进度反馈修复、BUG-0005 服务重启后登录失败修复、BUG-0006 对象存储上传未写入 MinIO 修复、BUG-0007 对象存储修复后品牌 Logo 仍不显示修复、BUG-0008 对象存储 legacy uploads 双目录残留与历史数据清理及对应 OpenSpec Change 规划
source: AI 根据 issues/openspec 目录生成，项目团队确认
update_method: 迭代范围或状态变化时更新
owner: 项目负责人
status: in_progress
note: add-admin-home 已 archive；BUG-0001 / fix-tile-category-enable-action 已 archive；REQ-0007 / fix-tile-category-management-refine 纳入（2026-06-20）；BUG-0002 / fix-brand-ui-consistency 已 archive（2026-06-25）；BUG-0003 / fix-brand-image-display-layout-shift 已 archive（2026-06-26 08:43:24）；BUG-0004 / fix-brand-logo-upload-progress 已 apply（2026-06-26 09:47:15）；BUG-0006 / fix-object-storage-upload-not-minio 已 archive（2026-06-26 14:20:50）；BUG-0007 / fix-brand-logo-display-after-storage-fix 已 archive（2026-06-26 20:21:43）；BUG-0005 / fix-admin-login-service-restart 已 apply（2026-06-26 23:17:00）；REQ-0008 / fix-brand-status-confirm 已 req-opsx（2026-06-26 21:15:13，待 opsx-apply）；BUG-0008 / fix-object-storage-legacy-upload-residue 已纳入 sprint-002（2026-06-26 23:56:57，approved，待 bug-opsx）；其余 change 收尾进行中
---

# Sprint 002

## Sprint 目标

本迭代交付七项管理端能力：

1. **REQ-0004 管理后台首页 V5** — 登录后的 `/admin/dashboard` 从占位页升级为与原型一致的专业工作台。
2. **REQ-0005 管理后台用户管理** — `/admin/users` 列表、筛选、CRUD、冻结/解冻、软删除与重置密码；仅 `admin` 可访问。
3. **REQ-0005-user-management-list-refine 用户管理列表页 UI 优化** — 筛选区去搜索按钮、keyword 收窄、用户列两行、分页精简；依赖 REQ-0005 基线。
4. **REQ-0003-login-remember-autofill 登录页记住凭证与密码显隐** — `/admin/login` 勾选记住后自动填充用户名/密码；密码框显隐切换。
5. **REQ-0005-brand-management 瓷砖品牌管理** — `/admin/brands` 列表、筛选、新增/编辑、启停、条件删除与 Logo 上传；`admin` 与 `employee` 可访问。
6. **REQ-0005-tile-category-management 瓷砖类目管理** — `/admin/tile-categories` 类目树+列表联动、检索、新增/编辑、启停、条件删除；最多三级类目；`admin` 与 `employee` 可访问。
7. **REQ-0006-tile-sku-management 瓷砖 SKU 管理** — `/admin/tile-skus` 列表、五维筛选、新增/编辑（880px 弹窗）、多图主图、多视频、参考价格、上下架；依赖品牌与类目主数据。
8. **BUG-0001 瓷砖类目停用行缺少启用入口** — 修复 `/admin/tile-categories` 停用且 SKU=0 行无「启用」按钮；对齐 REQ-0005 AC-015 与品牌管理操作列模式。（**已修复并 archive**）
9. **REQ-0007-tile-category-management-refine 瓷砖类目管理页 UI 优化** — 启停二次确认；去掉检索/列表 section 标题；分页对齐用户管理 v2；依赖类目管理基线。
10. **BUG-0002 品牌管理 UI 一致性修复** — 修复 `/admin/brands` 底部分页与用户管理页不一致、品牌 Logo 选择文件控件与管理端表单风格不一致；仅 Web 管理端 UI，依赖品牌管理基线。
11. **BUG-0003 品牌图片显示失败与 Tips 布局波动修复** — 修复 `/admin/brands` 上传 Logo 后列表/编辑弹窗无法显示，以及状态提示插入页面顶部导致页面上下波动；涉及媒体访问链路与管理端提示布局策略。
12. **BUG-0004 品牌 Logo 上传进度反馈修复** — 修复编辑品牌弹窗更换 Logo 后缺少可感知上传、预览不更新的问题；要求上传过程中展示进度条或等价反馈。
13. **BUG-0006 对象存储上传未写入 MinIO 修复** — 修复业务上传链路仍写入本地 `UPLOAD_DIR` 而非 MinIO `tile-info-platform` 单桶的问题；要求图片/视频上传写入标准对象前缀并保持受控读取。
14. **BUG-0007 对象存储修复后品牌 Logo 仍不显示修复** — 修复品牌列表页与品牌编辑弹窗在对象存储链路修复后仍无法展示 Logo 的问题；要求品牌 Logo URL、对象 key、受控读取与前端回显闭环。
15. **BUG-0005 服务重启后正确账号密码无法登录修复** — 修复本地/Docker 持久化 SQLite 中已有 `admin` 时，默认管理员初始化与当前环境密码不一致导致重启后登录失败的问题；要求提供明确、可审计的初始化/恢复策略。
16. **REQ-0008-brand-status-confirm 品牌列表启停二次确认** — `/admin/brands` 点击「启用」「停用」须二次确认；停用正文含「停用后前台将不再展示该品牌。」；对齐删除弹窗与类目启停确认模式；依赖品牌管理基线。
17. **BUG-0008 对象存储 legacy uploads 双目录残留与历史数据清理** — BUG-0006 修复后清理 `data/uploads` 孤儿文件、澄清 `data/minio` vs `data/uploads` 职责、收敛 `UPLOAD_DIR` 挂载与配置；依赖对象存储 MinIO 写入基线。

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

### REQ-0006-tile-sku-management 要点

- SKU 列表：关键词/品牌/类目/状态/素材完整度筛选、四指标卡、分页（10/20/50/100，默认 20）
- 新增/编辑弹窗（880px、多图主图、多视频、参考价格（元））；无状态字段；默认草稿
- 「保存草稿」与「创建SKU」校验级别不同（design D8）；上下架/条件删除
- 后端 Admin Tile SKU API；扩展 `tiles` 表 + `tile_videos`；图片/视频 MinIO 上传
- CSS Port 对齐 `tile-sku-management-list.html` / `tile-sku-create-modal.html` v4
- OpenSpec `add-tile-sku-management`（proposed，待 `/opsx-apply`；**MUST** 在 brand + category 之后）

### BUG-0001-tile-category-enable-missing 要点

- **严重等级**：high（P0 BUG 优先）
- **现象**：停用 + SKU=0 类目行仅「编辑」「删除」，缺少「启用」
- **根因**：`TileCategoryManagementPage.tsx` 将 `canDeleteCategory` 与启停按钮展示错误绑定
- **修复**：对齐 `BrandManagementPage`；仅前端 + vitest；无 API/DB 变更
- OpenSpec `fix-tile-category-enable-action`（**archived** 2026-06-20）

### REQ-0007-tile-category-management-refine 要点

- 子需求：优化 `add-tile-category-management` 已落地列表页（O-01～O-04）
- 启停点击二次确认（复用删除 modal 结构）；取消不调用 API
- 删除「类目检索」「类目列表」外层 section 标题；保留 `cat-table-toolbar`
- 分页左「共 x 个类目」；右页码 +「每页显示」；对齐 `UserManagementPage` v2
- 仅前端 + vitest；无 API/DB/Orval 变更；BUG-0001 启停可见性 **不回归**
- OpenSpec `fix-tile-category-management-refine`（proposed，待 `/opsx-apply`）

### BUG-0002-brand-ui-inconsistency 要点

- **严重等级**：medium
- **现象**：`/admin/brands` 底部分页与 `/admin/users` 分页结构不一致；新增/编辑品牌弹窗「品牌Logo」选择文件控件与管理端整体表单风格不一致。
- **根因**：品牌管理页分页和 Logo 上传控件使用页面局部结构与样式，未对齐用户管理页的统一分页/上传控件模式。
- **修复范围**：仅 Web 管理端分页 DOM/CSS 与 `BrandFormModal` Logo 控件；无 API/DB/Orval/MinIO 策略变更。
- OpenSpec `fix-brand-ui-consistency`（proposed，待 `/opsx-apply`）。

### BUG-0003-brand-image-display-layout-shift 要点

- **严重等级**：high
- **现象**：`/admin/brands` 上传品牌 Logo 后，列表页和编辑弹窗均无法正常展示；品牌状态变更 Tips 在页面顶部临时插入/消失，导致页面上下波动。
- **根因**：品牌上传与列表接口返回 `/media/{object_key}`，但后端未挂载可访问媒体服务或受控代理；`admin-notice` 作为普通文档流节点条件渲染，自动消失时改变页面高度。
- **修复范围**：后端媒体访问 URL 策略、品牌 Logo 展示/回显、管理端 notice/toast 布局策略；如涉及 API 响应结构变化，需同步 OpenAPI 与 Orval。
- OpenSpec `fix-brand-image-display-layout-shift`（archived，2026-06-26 08:43:24）。

### BUG-0004-brand-logo-upload-progress-missing 要点

- **严重等级**：medium
- **现象**：编辑品牌弹窗点击「更换 Logo」并选择图片后，没有明显上传反馈，Logo 预览也没有更新。
- **根因**：品牌 Logo 上传控件缺少明确上传状态机、上传进度反馈和成功后预览状态同步；同文件重选与失败重试也需纳入修复验收。
- **修复范围**：Web 管理端品牌编辑弹窗 Logo 上传状态、进度条或等价反馈、预览更新、失败/重试体验；保持品牌管理既有功能和权限边界。
- OpenSpec `fix-brand-logo-upload-progress`（applied，待 `/opsx-archive`）。

### BUG-0006-object-storage-upload-not-minio 要点

- **严重等级**：high
- **现象**：MinIO 服务和 `tile-info-platform` 桶已初始化，但头像、品牌 Logo、SKU 图片、SKU 视频等业务上传仍写入本地 `UPLOAD_DIR`，MinIO Console 中无业务对象。
- **根因**：后端上传接口统一调用 `save_upload_file()`，当前实现使用 `settings.upload_dir` + `write_bytes()` 保存本地文件，未调用 MinIO client；`/media/{object_key}` 读取也绑定本地文件系统。
- **修复范围**：后端媒体存储适配、MinIO `put_object` 写入、受控读取或签名 URL 策略、错误码、集成测试与文档同步。
- OpenSpec `fix-object-storage-upload-not-minio`（archived，2026-06-26 14:20:50）。

### BUG-0007-brand-logo-not-displayed-after-storage-fix 要点

- **严重等级**：high
- **现象**：对象存储写入问题修复后，品牌列表页和品牌编辑弹窗仍无法显示品牌 Logo。
- **根因**：Web 层只反代 `/api`，品牌 Logo `logo_url` 使用 `/media/{object_key}` 相对地址时未被转发到后端媒体读取接口。
- **修复范围**：品牌列表 Logo 展示、品牌编辑弹窗 Logo 回显、新上传 Logo 可见、历史对象 key 兼容策略与回归测试。
- OpenSpec `fix-brand-logo-display-after-storage-fix`（archived，2026-06-26 20:21:43）。

### BUG-0005-login-fails-after-service-restart 要点

- **严重等级**：high
- **现象**：本地或 Docker 服务重启后，进入 `/admin/login` 使用正确管理员账号密码仍提示「账号或密码错误」。
- **根因**：默认管理员 seed 只在 `admin` 不存在时创建；持久化 SQLite 中已有 `admin` 时不会校验或恢复密码哈希，且根目录 `.env.example` 与后端示例环境变量对 `ADMIN_INITIAL_PASSWORD` 的说明不一致。
- **修复范围**：默认管理员初始化与恢复策略、根目录 `.env.example` / 部署文档 / 数据库说明、后端回归测试；保持登录接口统一凭证错误语义与权限边界。
- OpenSpec `fix-admin-login-service-restart`（applied，待 `/opsx-archive`）。

### REQ-0008-brand-status-confirm 要点

- 子需求：优化 `add-brand-management` 已落地品牌列表启停交互（O-01）
- 点击「启用」「停用」须二次确认；取消/遮罩/× 不调用 API
- 停用正文：「确认停用品牌「{name}」？停用后前台将不再展示该品牌。」
- 启用正文：「确认启用品牌「{name}」？」；复用删除 modal 结构
- 仅前端 + vitest；无 API/DB/Orval 变更；删除确认 **不回归**
- OpenSpec `fix-brand-status-confirm`（proposed，待 `/req-opsx` + `/opsx-apply`）

### BUG-0008-object-storage-legacy-upload-residue 要点

- **严重等级**：medium
- **现象**：BUG-0006 修复后 `data/uploads` 仍存本地上传孤儿文件，与 MinIO 持久化卷 `data/minio` 并存，缺少清理策略与文档澄清。
- **根因**：存储迁移缺少 post-migration cleanup；`UPLOAD_DIR` Docker 挂载与配置未收敛。
- **修复范围**：历史 uploads 清理脚本/步骤、`data/README.md` 与部署文档、可选移除无用 `UPLOAD_DIR` 挂载；MUST NOT 影响 MinIO 有效对象与品牌 Logo 展示。
- OpenSpec `fix-object-storage-legacy-upload-residue`（待 `/bug-opsx`）。

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
| REQ-0006-tile-sku-management | 瓷砖 SKU 管理 | P0 | Ready | 列表 + 880px 弹窗 + 多图/视频；依赖品牌 + 类目 |
| REQ-0007-tile-category-management-refine | 瓷砖类目管理页 UI 优化 | P1 | approved | fix-*；启停确认 + 去标题 + 分页 v2 |
| REQ-0008-brand-status-confirm | 品牌列表启停二次确认 | P1 | done | fix-* 已 archive |

### 包含 BUG

| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| BUG-0001-tile-category-enable-missing | 类目停用行缺少启用入口 | P0 | done | 已 archive fix-tile-category-enable-action |
| BUG-0002-brand-ui-inconsistency | 品牌管理分页与Logo选择文件控件UI不一致 | P1 | done | 已 archive fix-brand-ui-consistency |
| BUG-0003-brand-image-display-layout-shift | 品牌图片上传后不显示且状态提示导致页面上下波动 | P1 | done | 已归档 fix-brand-image-display-layout-shift |
| BUG-0004-brand-logo-upload-progress-missing | 编辑品牌弹窗更换Logo后未上传且缺少上传进度反馈 | P1 | applied | 已完成 fix-brand-logo-upload-progress apply |
| BUG-0005-login-fails-after-service-restart | 服务重启后正确账号密码无法登录 | P1 | applied | 已完成 fix-admin-login-service-restart apply |
| BUG-0006-object-storage-upload-not-minio | 上传链路未写入 MinIO 对象存储 | P1 | done | 已完成 fix-object-storage-upload-not-minio archive |
| BUG-0007-brand-logo-not-displayed-after-storage-fix | 对象存储修复后品牌Logo仍不显示 | P1 | done | 已完成 fix-brand-logo-display-after-storage-fix archive |
| BUG-0008-object-storage-legacy-upload-residue | 对象存储修复后本地uploads双目录残留与历史数据清理缺失 | P2 | done | 已 archive fix-object-storage-legacy-upload-residue |

### 包含 Change

| Change ID | 关联需求 | 状态 | Sprint 目标 |
|---|---|---|---|
| `add-admin-home` | REQ-0004 | archived | Admin Shell + Dashboard + PNG gate |
| `add-user-management` | REQ-0005 | applied | 用户管理 API + 页面 + PNG gate |
| `fix-user-management-list-refine` | REQ-0005-user-management-list-refine | proposed | 列表页 v2 UI + keyword 收窄 + PNG gate |
| `add-login-remember-autofill` | REQ-0003-login-remember-autofill | proposed | 登录凭证自动填充 + 密码显隐 |
| `add-brand-management` | REQ-0005-brand-management | proposed | 品牌管理 API + 页面 + HTML/PNG gate |
| `add-tile-category-management` | REQ-0005-tile-category-management | archived | 类目管理 API + 树/列表页 + HTML gate |
| `fix-tile-category-enable-action` | BUG-0001-tile-category-enable-missing | archived | 类目列表启停操作列修复 + vitest |
| `fix-tile-category-management-refine` | REQ-0007-tile-category-management-refine | proposed | 类目页 v2 UI：启停确认 + 分页对齐 |
| `fix-brand-ui-consistency` | BUG-0002-brand-ui-inconsistency | archived | 品牌页分页与 Logo 上传控件 UI 一致性修复 |
| `fix-brand-image-display-layout-shift` | BUG-0003-brand-image-display-layout-shift | archived | 品牌 Logo 媒体可访问与状态提示布局稳定性修复 |
| `fix-brand-logo-upload-progress` | BUG-0004-brand-logo-upload-progress-missing | applied | 品牌 Logo 上传进度反馈与预览更新修复 |
| `fix-object-storage-upload-not-minio` | BUG-0006-object-storage-upload-not-minio | archived | 上传链路写入 MinIO 单桶与受控读取修复 |
| `fix-brand-logo-display-after-storage-fix` | BUG-0007-brand-logo-not-displayed-after-storage-fix | archived | 对象存储修复后品牌 Logo 展示读取闭环修复 |
| `fix-admin-login-service-restart` | BUG-0005-login-fails-after-service-restart | applied | 默认管理员初始化与受控恢复策略修复 |
| `fix-brand-status-confirm` | REQ-0008-brand-status-confirm | archived | 品牌列表启停二次确认 + vitest |
| `add-tile-sku-management` | REQ-0006-tile-sku-management | in_progress | SKU 管理 API + 列表/弹窗 + 媒体上传 + HTML gate |
| `fix-object-storage-legacy-upload-residue` | BUG-0008-object-storage-legacy-upload-residue | archived | legacy uploads 清理 + 文档澄清 + UPLOAD_DIR 收敛 |

### 不包含（延后至后续 Sprint）

| 项目 | 延后原因 |
|---|---|
| Dashboard 真实统计 / 审计 API | PRD 明确本期 mock |
| Banner 管理页 | 独立 REQ |
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
| **BUG-0001-tile-category-enable-missing** | | | | | |
| 列表启停按钮修复 + vitest | S | 0.5 | — | 0.5 | 1 |
| trace / 归档 | XS | 0.25 | — | 0.25 | 0.5 |
| **REQ-0007-tile-category-management-refine** | | | | | |
| 启停确认 + 去 section 标题 + 分页 v2 | M | 1.5 | — | — | 1.5 |
| vitest + context 验收 + 归档 | S | 0.25 | — | 0.75 | 1 |
| **BUG-0002-brand-ui-inconsistency** | | | | | |
| 品牌分页与 Logo 上传控件一致性修复 | S | 1 | — | — | 1 |
| vitest + 视觉验收 + trace | S | 0.5 | — | 0.5 | 1 |
| **BUG-0003-brand-image-display-layout-shift** | | | | | |
| 品牌 Logo 媒体访问链路修复 | M | 0.5 | 1 | — | 1.5 |
| 品牌页 Tips 非占位提示布局修复 | S | 0.75 | — | — | 0.75 |
| 回归测试 + trace | S | 0.25 | — | 0.5 | 0.75 |
| **BUG-0004-brand-logo-upload-progress-missing** | | | | | |
| 品牌 Logo 上传状态机 + 进度反馈 | S | 1 | — | — | 1 |
| 预览更新、失败重试与同文件重选 | S | 0.5 | — | — | 0.5 |
| 回归测试 + trace | S | 0.25 | — | 0.25 | 0.5 |
| **BUG-0005-login-fails-after-service-restart** | | | | | |
| 默认管理员初始化/恢复策略 | S | — | 1.25 | — | 1.25 |
| 环境变量、部署与数据库说明同步 | S | — | 0.25 | — | 0.25 |
| 后端回归测试 + trace | S | — | — | 1 | 1 |
| **BUG-0006-object-storage-upload-not-minio** | | | | | |
| MinIO 存储适配与上传写入 | M | — | 1 | — | 1 |
| 受控读取 / URL 策略与错误处理 | M | — | 0.75 | — | 0.75 |
| 集成测试、Docker 验证与文档同步 | M | 0.25 | 0.25 | 0.75 | 1.25 |
| **BUG-0007-brand-logo-not-displayed-after-storage-fix** | | | | |
| 品牌 Logo 展示读取闭环修复 | S | 1 | 0.5 | 0.5 | 2 |
| **BUG-0008-object-storage-legacy-upload-residue** | | | | | |
| legacy uploads 清理脚本与文档澄清 | S | — | 0.5 | — | 0.5 |
| Docker / UPLOAD_DIR 配置收敛 + 回归 | S | — | 0.25 | 0.25 | 0.5 |
| 可选一致性检查工具 + trace | XS | — | 0.25 | 0.25 | 0.5 |
| **REQ-0008-brand-status-confirm** | | | | | |
| 启停确认弹窗 + vitest | S | 0.75 | — | 0.25 | 1 |
| **REQ-0006-tile-sku-management** | | | | | |
| `tiles` 扩展 + `tile_videos` + Admin SKU API | XL | — | 5 | — | 5 |
| SKU 管理页 CSS Port + 880px 弹窗 + 媒体上传 UI | XL | 5 | — | — | 5 |
| publish/unpublish + save_mode + Orval | M | 1 | 1 | — | 2 |
| 多图主图/多视频 + 素材完整度筛选 | M | 1 | 0.5 | — | 1.5 |
| SKU 管理测试 + HTML 验收 | M | 1 | — | 2 | 3 |
| 文档 / trace / 归档 | S | 0.25 | 0.25 | — | 0.5 |
| **合计** | | **46.75** | **25.5** | **17** | **73.75**（Story Points: 121） |

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
| M9b fix-tile-category-enable-action（BUG-0001） | BUG-0001-tile-category-enable-missing | 2026-06-28（**done**） |
| M9c fix-tile-category-management-refine | REQ-0007-tile-category-management-refine | 2026-06-28 |
| M9d fix-brand-ui-consistency | BUG-0002-brand-ui-inconsistency | 2026-06-28 |
| M9e fix-brand-image-display-layout-shift | BUG-0003-brand-image-display-layout-shift | 2026-06-28 |
| M9f fix-brand-logo-upload-progress-missing | BUG-0004-brand-logo-upload-progress-missing | 2026-06-28 |
| M9g fix-object-storage-upload-not-minio | BUG-0006-object-storage-upload-not-minio | 2026-06-28 |
| M9h fix-brand-logo-not-displayed-after-storage-fix | BUG-0007-brand-logo-not-displayed-after-storage-fix | 2026-06-28 |
| M9i fix-admin-login-service-restart | BUG-0005-login-fails-after-service-restart | 2026-06-28 |
| M9j fix-brand-status-confirm | REQ-0008-brand-status-confirm | 2026-06-28 |
| M9k fix-object-storage-legacy-upload-residue | BUG-0008-object-storage-legacy-upload-residue | 2026-06-28 |
| M10 add-tile-sku-management 实现 + 测试 + HTML 验收 | REQ-0006-tile-sku-management | 2026-06-28（依赖 M8/M9） |

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
| R-12 | Sprint 容量追加 SKU 管理 | **超容量风险** | SKU ~13 人天；**MUST** 在 brand + category apply 后启动；可与收尾并行或延至 sprint 末 |
| R-13 | SKU 依赖品牌/类目 API 与下拉数据 | 阻塞 SKU 表单 | apply 顺序：brand → category → sku |
| R-14 | BUG-0003 需要媒体访问链路闭环 | 品牌 Logo 与后续 SKU/前台媒体展示可能继续失败 | bug-opsx 中明确 `/media` 代理或签名 URL 策略；同步 OpenAPI/Orval（若响应结构变化） |
| R-14 | BUG-0001 类目启停 UI 缺陷 | 运营无法 UI 启用停用类目 | **已修复并 archive** |
| R-15 | REQ-0007 类目页 UI refine | 误操作 / 分页不一致 | 纳入 sprint-002；`/opsx-apply fix-tile-category-management-refine` |
| R-16 | BUG-0002 品牌管理 UI 一致性 | 品牌页与用户管理页控件体验割裂 | 纳入 sprint-002；`/opsx-apply fix-brand-ui-consistency` |
| R-17 | BUG-0004 品牌 Logo 上传进度缺失 | 运营无法确认 Logo 是否正在上传或已成功替换 | 已完成 `/opsx-apply fix-brand-logo-upload-progress`；待归档 |
| R-18 | BUG-0006 对象存储上传未写入 MinIO | 媒体上传与对象存储验收割裂，影响 SKU/品牌/头像素材持久化 | 已完成 `/opsx-archive fix-object-storage-upload-not-minio` |
| R-19 | BUG-0007 对象存储修复后品牌 Logo 仍不显示 | 品牌管理 Logo 展示验收继续失败，影响运营识别品牌 | 已完成 `fix-brand-logo-display-after-storage-fix` archive |
| R-20 | BUG-0005 服务重启后登录失败 | 持久化 SQLite 中已有 admin 与当前环境密码不一致时，管理端登录和演示验收被阻断 | 已完成 `fix-admin-login-service-restart` apply；待 `/opsx-archive` |
| R-21 | REQ-0008 品牌启停二次确认 | 误触直接启停品牌 | 已纳入 sprint-002；`/req-opsx` + `/opsx-apply fix-brand-status-confirm` |
| R-22 | BUG-0008 legacy uploads 双目录残留 | 本地磁盘占用与媒体存储排查误导 | 已纳入 sprint-002；依赖 BUG-0006 基线；`/bug-opsx` + `/opsx-apply fix-object-storage-legacy-upload-residue` |

## 依赖

```text
REQ-0001（已 resolved）
  └── auth / ProtectedRoute / logout / LoginForm
        ├── add-login-remember-autofill（REQ-0003-login-remember-autofill）
        ├── fix-admin-login-service-restart（BUG-0005）
        ├── add-admin-home（REQ-0004）
        │     └── Admin Shell 基座
        └── add-user-management（REQ-0005）
              ├── fix-user-management-list-refine（REQ-0005-user-management-list-refine）
              ├── add-brand-management（REQ-0005-brand-management）
              │     ├── fix-brand-ui-consistency（BUG-0002-brand-ui-inconsistency）
              │     ├── fix-brand-logo-upload-progress（BUG-0004）
              │     ├── fix-brand-logo-display-after-storage-fix（BUG-0007）
              │     └── fix-brand-status-confirm（REQ-0008-brand-status-confirm）
              ├── add-tile-category-management（REQ-0005-tile-category-management）
              │     ├── fix-tile-category-enable-action（BUG-0001）✓ archived
              │     ├── fix-tile-category-management-refine（REQ-0007-tile-category-management-refine）
              │     └── add-tile-sku-management（REQ-0006-tile-sku-management）
              ├── fix-object-storage-upload-not-minio（BUG-0006）
              ├── fix-object-storage-legacy-upload-residue（BUG-0008）
              └── [后续] Banner REQ
```

## 发布计划

- 开发环境：`./scripts/docker-up.sh` 验证 `/admin/login`、`/admin/dashboard`、`/admin/users`、`/admin/brands`、`/admin/tile-categories` 与 `/admin/tile-skus`
- REQ-0004：无后端 / DB / API 变更；无需 Orval
- REQ-0005：需 DB 迁移、OpenAPI 更新与 Orval 重新生成
- REQ-0005-user-management-list-refine：无 DB 迁移；后端 keyword 行为变更；无需 Orval（无新端点）
- REQ-0003-login-remember-autofill：仅 Web 前端；无需 Orval / DB
- REQ-0005-brand-management：需 `brands` 表迁移、OpenAPI 更新与 Orval 重新生成
- REQ-0005-tile-category-management：需 `tile_categories` 表扩展、OpenAPI 更新与 Orval 重新生成
- REQ-0007-tile-category-management-refine：仅 Web 前端；无需 Orval / DB
- BUG-0002-brand-ui-inconsistency：仅 Web 前端 UI；无需 Orval / DB / Docker Compose 必选验证
- BUG-0004-brand-logo-upload-progress-missing：仅 Web 管理端 UI + 前端上传封装进度回调；无 API schema / DB / Orval 变更
- BUG-0006-object-storage-upload-not-minio：已完成后端媒体存储策略修复、MinIO 写入与读取闭环、Docker Compose 验证；上传响应 schema 不变，无需 Orval
- BUG-0007-brand-logo-not-displayed-after-storage-fix：预计涉及 Web 管理端品牌 Logo 展示与后端媒体读取/URL；若 API 响应字段变化需同步 OpenAPI 与 Orval
- BUG-0005-login-fails-after-service-restart：已完成后端默认管理员初始化/显式恢复策略、`.env.example` 与部署/数据库文档；未改变登录接口响应 schema，无需 Orval；后端认证回归测试通过
- BUG-0008-object-storage-legacy-upload-residue：清理脚本、data/部署文档、Docker 挂载收敛；无 API schema 变更，无需 Orval；MUST 回归 BUG-0006/BUG-0007 媒体上传与品牌 Logo 展示
- REQ-0008-brand-status-confirm：仅 Web 前端；无需 Orval / DB
- REQ-0006-tile-sku-management：需 `tiles` 表扩展、`tile_videos` 表、OpenAPI 更新与 Orval 重新生成
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
| 缺陷记录（品牌 UI 一致性） | `issues/bugs/BUG-0002-brand-ui-inconsistency/` |
| OpenSpec Change（品牌 UI 一致性修复） | `openspec/changes/fix-brand-ui-consistency/` |
| 缺陷记录（品牌 Logo 上传进度反馈） | `issues/bugs/BUG-0004-brand-logo-upload-progress-missing/` |
| OpenSpec Change（品牌 Logo 上传进度反馈修复） | `openspec/changes/fix-brand-logo-upload-progress/` |
| 缺陷记录（对象存储上传未写入 MinIO） | `issues/bugs/BUG-0006-object-storage-upload-not-minio/` |
| OpenSpec Change（对象存储上传未写入 MinIO 修复） | `openspec/changes/archive/2026-06-26-fix-object-storage-upload-not-minio/` |
| 缺陷记录（对象存储修复后品牌 Logo 仍不显示） | `issues/bugs/BUG-0007-brand-logo-not-displayed-after-storage-fix/` |
| OpenSpec Change（对象存储修复后品牌 Logo 仍不显示修复） | `openspec/changes/archive/2026-06-26-fix-brand-logo-display-after-storage-fix/` |
| 缺陷记录（服务重启后登录失败） | `issues/bugs/BUG-0005-login-fails-after-service-restart/` |
| OpenSpec Change（服务重启后登录失败修复） | `openspec/changes/fix-admin-login-service-restart/` |
| 缺陷记录（对象存储 legacy uploads 残留） | `issues/bugs/BUG-0008-object-storage-legacy-upload-residue/` |
| OpenSpec Change（对象存储 legacy uploads 清理） | `openspec/changes/archive/2026-06-26-fix-object-storage-legacy-upload-residue/` |
| 需求 PRD（类目管理） | `issues/requirements/REQ-0005-tile-category-management/requirement.md` |
| 验收标准（类目管理） | `issues/requirements/REQ-0005-tile-category-management/acceptance.md` |
| OpenSpec Change（类目管理） | `openspec/changes/archive/2026-06-20-add-tile-category-management/` |
| HTML 原型（类目管理） | `issues/requirements/REQ-0005-tile-category-management/prototype/web/tile-category-management.html` |
| 缺陷记录（类目启用） | `issues/bugs/BUG-0001-tile-category-enable-missing/` |
| OpenSpec Change（类目启用修复） | `openspec/changes/archive/2026-06-20-fix-tile-category-enable-action/` |
| 需求 PRD（类目 UI 优化） | `issues/requirements/REQ-0007-tile-category-management-refine/requirement.md` |
| 验收标准（类目 UI 优化） | `issues/requirements/REQ-0007-tile-category-management-refine/acceptance.md` |
| OpenSpec Change（类目 UI 优化） | `openspec/changes/fix-tile-category-management-refine/` |
| v2 context（类目列表） | `issues/requirements/REQ-0007-tile-category-management-refine/prototype/web/tile-category-management-list-refine-context.md` |
| 需求 PRD（品牌启停确认） | `issues/requirements/REQ-0008-brand-status-confirm/requirement.md` |
| 验收标准（品牌启停确认） | `issues/requirements/REQ-0008-brand-status-confirm/acceptance.md` |
| OpenSpec Change（品牌启停确认） | `openspec/changes/fix-brand-status-confirm/` |
| 启停确认 context | `issues/requirements/REQ-0008-brand-status-confirm/prototype/web/brand-status-confirm-context.md` |
| 需求 PRD（SKU 管理） | `issues/requirements/REQ-0006-tile-sku-management/requirement.md` |
| 验收标准（SKU 管理） | `issues/requirements/REQ-0006-tile-sku-management/acceptance.md` |
| OpenSpec Change（SKU 管理） | `openspec/changes/add-tile-sku-management/` |
| HTML 原型（SKU 管理） | `issues/requirements/REQ-0006-tile-sku-management/prototype/web/tile-sku-management-list.html` |
