---
created_at: 2026-06-27 08:42:28
title: Sprint 002 迭代说明
purpose: 记录 Sprint 002 目标、范围、Change、工作量与风险
content: 基于 REQ-0004 管理后台首页、REQ-0005 用户管理、REQ-0005-user-management-list-refine 用户管理列表页 UI 优化、REQ-0003 登录记住凭证与密码显隐、REQ-0005-brand-management 瓷砖品牌管理、REQ-0005-tile-category-management 瓷砖类目管理、REQ-0006-tile-sku-management 瓷砖 SKU 管理、BUG-0002 品牌管理 UI 一致性修复、BUG-0003 品牌图片显示与提示布局修复、BUG-0004 品牌 Logo 上传进度反馈修复、BUG-0005 服务重启后登录失败修复、BUG-0006 对象存储上传未写入 MinIO 修复、BUG-0007 对象存储修复后品牌 Logo 仍不显示修复、BUG-0008 对象存储 legacy uploads 双目录残留与历史数据清理及对应 OpenSpec Change 规划
source: AI 根据 issues/openspec 目录生成，项目团队确认
update_method: 迭代范围或状态变化时更新
owner: 项目负责人
status: completed
note: workflow-sync — workflow-sync 自动同步 — 30/30 Change archived；0 applied；Sprint `completed`
updated_at: 2026-06-27 16:00:00
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
18. **BUG-0011 SKU 新增/编辑弹窗内容溢出且无垂直滚动条** — 修复 `/admin/tile-skus` 880px 弹窗在矮视口下 body 不可滚动、底部字段不可达；`.sku-modal-card` 采用 flex 滚动布局；对齐 REQ-0006 AC-022。（**已修复并 archive**）
19. **BUG-0009 SKU 列表分页与用户管理页不一致且表头上方多余标题行** — 修复 `/admin/tile-skus` 底部分页 DOM 对齐用户管理页、移除 `table-card` 内重复「SKU 列表」标题行；对齐 REQ-0006 AC-051 / AC-054；依赖 SKU 管理基线。
20. **REQ-0010-product-version-display Web 端产品版本号展示** — 管理端 + 店主端侧边栏顶部产品名旁展示人工维护的产品版本 pill（如 `v0.0.1`）；单一 `src/shared/` 常量；无 API 变更；OpenSpec `add-product-version-display`（**applied**；待 archive）。
21. **REQ-0011-admin-sidebar-expand-collapse 管理端侧边栏展开/收起** — 桌面端 264px ↔ 72px chevron 切换；`localStorage` 持久化；collapsed 保留图标与 active accent；依赖 REQ-0010 brand-head；OpenSpec `add-admin-sidebar-collapse`（**proposed**）。
22. **BUG-0012 SKU 弹窗表面工艺/参考价格字段规则调整** — 表面工艺改非必填、参考价格改必填且新建默认 0 元；前后端校验与 `publish_sku` 策略对齐 UAT 产品规则；同步 REQ-0006 acceptance delta；OpenSpec `fix-tile-sku-modal-form-field-rules`（**proposed**；待 `/opsx-apply`）。
23. **BUG-0014 SKU 列表已下架行缺少上架操作** — 修复 `/admin/tile-skus` 已下架（`DISABLED`）行无「恢复/上架」入口，阻断下架后 UI 恢复上架；对齐 REQ-0006 AC-018/AC-037 与 BUG-0001 修复模式；OpenSpec `fix-tile-sku-publish-action-missing`（**proposed**；待 `/opsx-apply`）。
24. **BUG-0015 管理端四列表页状态 Tips 推挤页面** — 修复品牌/用户/类目/SKU 列表页操作反馈使用文档流 `.admin-notice` 导致 hero/表格上下波动；四页统一 fixed toast；品牌页迁移至共享样式且不回归 BUG-0003；OpenSpec `fix-admin-list-status-toast-layout`（**proposed**；待 `/opsx-apply`）。
25. **BUG-0019 用户弹窗头像上传后未回显且更换功能未生效** — 修复 `/admin/users` 用户弹窗与列表头像始终 initials、更换头像无预览/进度；对齐品牌 Logo 弹窗状态机；后端补 `avatar_url`；OpenSpec `fix-user-modal-avatar-upload-display`（**proposed**；待 `/opsx-apply`）。
26. **BUG-0016 管理端用户/SKU 列表状态变更缺少二次确认** — 用户冻结/解冻、删除（modal 化）与 SKU 上架/下架/恢复须 DS modal 确认；对齐 REQ-0007/0008 模式；品牌启停已交付不在 scope；OpenSpec `fix-admin-list-status-action-confirm`（**archived** 2026-06-27）。
27. **BUG-0017 用户重置密码确认弹窗 UI 不一致** — `/admin/users`「重置密码」须 DS confirm modal（禁止 `window.confirm`），对齐类目启停与同页冻结确认；**排除** `ResetPasswordDialog` 结果弹窗；OpenSpec `fix-user-reset-password-confirm-ui`（**待 `/bug-opsx`**；approved 2026-06-27）。
28. **BUG-0018 SKU 弹窗商品视频上传后未即时回显** — 修复 `/admin/tile-skus` 新增/编辑弹窗「商品视频」区上传 MP4 后无文件卡片/上传状态反馈；对齐 REQ-0006 AC-035 与 `BrandFormModal` Logo 状态机；OpenSpec `fix-tile-sku-modal-video-upload-display`（**approved**；待 `/bug-opsx` → `/opsx-apply`）。
29. **BUG-0020 SKU 弹窗视频上传 413 Request Entity Too Large** — 修复 Docker Web 入口（`localhost:3000`）上传大体积 MP4 时 Nginx 反代返回 413；对齐 `MAX_IMAGE/VIDEO_SIZE_MB` 与 `ALLOWED_*_TYPES` env 配置；`nginx.conf` `client_max_body_size` 与后端限制一致；OpenSpec `fix-tile-sku-modal-video-upload-413`（**approved**；待 `/bug-opsx` → `/opsx-apply`）。

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
- OpenSpec `add-user-management`（**archived** 2026-06-20）

### REQ-0005-user-management-list-refine 要点

- 子需求：优化 `add-user-management` 已落地列表页（O-01～O-06）
- 删除「搜索」按钮；筛选 5 列；placeholder「搜索用户名/昵称」；自动查询（防抖/回车/筛选项变更）
- 删除 `section-head`、`table-toolbar`；用户列用户名/昵称两行；分页左「共 x 个用户」
- 后端 `keyword` 仅匹配 `username`、`display_name`（移除 email/phone）
- 弹窗、指标卡、行操作、权限 **不回归**
- OpenSpec `fix-user-management-list-refine`（**archived** 2026-06-20）

### REQ-0003-login-remember-autofill 要点

- 勾选「记住登录状态」且登录成功 → `localStorage` 保存用户名/密码，下次自动填充
- 未勾选成功 / 登出 → 清除本地凭证（`stonex_login_credentials`）
- 密码输入框显隐切换（`.password-wrap` + 眼睛图标）
- 仅前端变更；不改后端 API / DB / Orval
- OpenSpec `add-login-remember-autofill`（**archived** 2026-06-20）

### REQ-0005-brand-management 要点

- 品牌列表：关键词/状态筛选、四指标卡、分页（含每页 20/50/100）
- 新增/编辑弹窗（720px、固定字段顺序）；无导出、无批量操作
- 启用/停用；删除仅 `sku_count=0` 且停用时可执行
- 后端 Admin Brands API + `brands` 表 + Logo MinIO 上传
- CSS Port 对齐 `brand-management.html` / `brand-management-modal.html`
- OpenSpec `add-brand-management`（**archived** 2026-06-26）

### REQ-0005-tile-category-management 要点

- 类目树（280px）+ 列表联动；四指标卡；检索（名称/编码、状态、层级）
- 新增/编辑弹窗（560px、单列六字段）；无导出；工具栏仅「调整排序」（本期占位）
- 启用/停用；删除仅 `sku_count=0` 且停用时可执行；最多三级类目
- 后端 Admin Tile Categories API + 扩展 `tile_categories` 表
- CSS Port 对齐 `tile-category-management.html` / `tile-category-management-add.html`
- OpenSpec `add-tile-category-management`（**archived** 2026-06-20）

### REQ-0006-tile-sku-management 要点

- SKU 列表：关键词/品牌/类目/状态/素材完整度筛选、四指标卡、分页（10/20/50/100，默认 20）
- 新增/编辑弹窗（880px、多图主图、多视频、参考价格（元））；无状态字段；默认草稿
- 「保存草稿」与「创建SKU」校验级别不同（design D8）；上下架/条件删除
- 后端 Admin Tile SKU API；扩展 `tiles` 表 + `tile_videos`；图片/视频 MinIO 上传
- CSS Port 对齐 `tile-sku-management-list.html` / `tile-sku-create-modal.html` v4
- OpenSpec `add-tile-sku-management`（**applied** 34/35；待 `/opsx-archive`；依赖 brand + category 已满足）

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
- OpenSpec `fix-tile-category-management-refine`（**archived** 2026-06-22）

### BUG-0002-brand-ui-inconsistency 要点

- **严重等级**：medium
- **现象**：`/admin/brands` 底部分页与 `/admin/users` 分页结构不一致；新增/编辑品牌弹窗「品牌Logo」选择文件控件与管理端整体表单风格不一致。
- **根因**：品牌管理页分页和 Logo 上传控件使用页面局部结构与样式，未对齐用户管理页的统一分页/上传控件模式。
- **修复范围**：仅 Web 管理端分页 DOM/CSS 与 `BrandFormModal` Logo 控件；无 API/DB/Orval/MinIO 策略变更。
- OpenSpec `fix-brand-ui-consistency`（**archived** 2026-06-25）。

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
- OpenSpec `fix-brand-logo-upload-progress`（**archived** 2026-06-26）。

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
- OpenSpec `fix-admin-login-service-restart`（**archived** 2026-06-26）。

### REQ-0008-brand-status-confirm 要点

- 子需求：优化 `add-brand-management` 已落地品牌列表启停交互（O-01）
- 点击「启用」「停用」须二次确认；取消/遮罩/× 不调用 API
- 停用正文：「确认停用品牌「{name}」？停用后前台将不再展示该品牌。」
- 启用正文：「确认启用品牌「{name}」？」；复用删除 modal 结构
- 仅前端 + vitest；无 API/DB/Orval 变更；删除确认 **不回归**
- OpenSpec `fix-brand-status-confirm`（**archived** 2026-06-26）

### BUG-0008-object-storage-legacy-upload-residue 要点

- **严重等级**：medium
- **现象**：BUG-0006 修复后 `data/uploads` 仍存本地上传孤儿文件，与 MinIO 持久化卷 `data/minio` 并存，缺少清理策略与文档澄清。
- **根因**：存储迁移缺少 post-migration cleanup；`UPLOAD_DIR` Docker 挂载与配置未收敛。
- **修复范围**：历史 uploads 清理脚本/步骤、`data/README.md` 与部署文档、可选移除无用 `UPLOAD_DIR` 挂载；MUST NOT 影响 MinIO 有效对象与品牌 Logo 展示。
- OpenSpec `fix-object-storage-legacy-upload-residue`（**archived** 2026-06-26）。

### BUG-0011-tile-sku-modal-content-overflow 要点

- **严重等级**：high
- **现象**：`/admin/tile-skus` 新增/编辑弹窗（880px）在常见或矮视口下，表单内容（含 SKU 图片/视频区、备注等）超出可视区域；`modal-body` 无垂直滚动，底部字段被裁切且滚轮无法访问，阻塞 SKU 创建/编辑。
- **根因**：`.sku-modal-card` 已设 `max-height` 与 `overflow: hidden`，但 `.modal-body` 未配置 `flex: 1; min-height: 0; overflow-y: auto`，flex 子项被父级裁切；实现未满足 REQ-0006 AC-022「主体可滚动」。
- **修复范围**：仅 Web 管理端 SKU 弹窗 CSS（`tile-sku-management.css`）与 Vitest 布局断言；无 API/DB/Orval 变更。
- OpenSpec `fix-tile-sku-modal-content-overflow`（**archived** 2026-06-27 09:37:19）。

### BUG-0009-tile-sku-list-ui-inconsistency 要点

- **严重等级**：medium
- **现象**：`/admin/tile-skus` 列表底部分页使用 `page-left` / `brand-pagination-right`，与用户管理页 `page-summary` / `page-right` 结构不一致；`table-card` 内存在多余 `table-head`「SKU 列表」标题行，与 `page-hero` 重复。
- **根因**：CSS Port 实现时复用 BUG-0002 修复前品牌页分页 DOM；表格卡片内局部臆造标题行，偏离 REQ-0006 原型 context 与 AC-051。
- **修复范围**：仅 Web 管理端 `TileSkuManagementPage.tsx` 分页 DOM + 移除 table-head；Vitest 分页结构断言；无 API/DB/Orval 变更。
- OpenSpec `fix-tile-sku-list-ui-inconsistency`（**archived** 2026-06-27 10:40:49）

### BUG-0010-tile-sku-modal-subtitle-inconsistency 要点

- **现象**：SKU 新增/编辑弹窗副标题使用无样式 `modal-subtitle`，与品牌弹窗 `brand-modal-desc` Typography 不一致。
- **根因**：SKU 弹窗未复用管理端共享副标题样式类。
- **修复范围**：`user-management.css` 抽取 `.modal-desc`；SKU/品牌弹窗统一 class；modal-head 自适应高度；Vitest 断言；无 API/DB/Orval 变更。
- OpenSpec `fix-tile-sku-modal-subtitle-inconsistency`（**applied** 2026-06-27 12:02:52）

### BUG-0012-tile-sku-modal-form-field-rules 要点

- **严重等级**：medium
- **现象**：SKU 新增/编辑弹窗表面工艺仍必填（Label `*` + 前后端拦截）；参考价格选填、新建默认空、未填存 `null` 列表显示「—」；与 UAT 产品规则（工艺非必填、价格必填默认 0）不符。
- **根因**：`add-tile-sku-management` 按 REQ-0006 v4 旧 spec 实现；UAT 规则变更未回写 acceptance/OpenSpec。
- **修复范围**：`TileSkuFormModal` 校验与默认值；`tile_sku_admin_service` create/update/publish；Orval；REQ-0006 `requirement.md` + `acceptance.md` AC-024/AC-015 delta；**不回归** BUG-0011 弹窗滚动。
- OpenSpec `fix-tile-sku-modal-form-field-rules`（**proposed**；待 `/opsx-apply`；依赖 `add-tile-sku-management` 基线）

### BUG-0014-tile-sku-publish-action-missing 要点

- **严重等级**：high（P0 BUG 优先）
- **现象**：`/admin/tile-skus` 已下架（`DISABLED`）SKU 行仅「编辑」「删除」，缺少「恢复/上架」；下架后无法从列表恢复上架。
- **根因**：`TileSkuManagementPage.tsx` L349–365 对 `status === 'DISABLED'` 显式渲染 `null`；`handlePublish` / publish API 已存在。
- **修复范围**：仅 Web 管理端操作列条件渲染 + Vitest；`DISABLED` 文案「恢复」；与 delete 独立；无 API/DB/Orval 变更。
- OpenSpec `fix-tile-sku-publish-action-missing`（**proposed**；待 `/opsx-apply`；依赖 `add-tile-sku-management` 基线；参考 `fix-tile-category-enable-action`）

### BUG-0015-admin-list-status-tips-layout-shift 要点

- **严重等级**：medium（P1）
- **现象**：用户/类目/SKU 三页状态变更、CRUD 成功或错误反馈在 `page-hero` 前插入 `.admin-notice`，3.2s 消失时整页上下跳动；品牌页已有 fixed toast 但未共享至其他页。
- **根因**：自动消失反馈误用文档流 notice；BUG-0003 品牌 toast 修复未推广。
- **修复范围**：共享 `.admin-toast-region` / `.admin-toast`（或 `AdminToast`）；四页 TSX + Vitest；**不回归**品牌 Logo/上传进度；无 API/DB/Orval。
- OpenSpec `fix-admin-list-status-toast-layout`（**proposed**；待 `/opsx-apply`；参考 `fix-brand-image-display-layout-shift`）

### BUG-0019-user-modal-avatar-upload-display 要点

- **严重等级**：high（P1 BUG）
- **现象**：用户弹窗/列表头像始终 initials；「更换头像」后无预览与进度；运行时上传 200 且 `avatar_object_key` 已入库
- **根因**：`UserFormModal` 未绑定预览 URL；缺上传状态机；API 缺 `avatar_url`；列表未渲染 `<img>`
- **修复范围**：`UserAdminItem.avatar_url`、`UserFormModal`（对齐 `BrandFormModal`）、`UserManagementPage` 列表、Orval + pytest/Vitest
- OpenSpec `fix-user-modal-avatar-upload-display`（**proposed**；待 `/opsx-apply`；参照 BUG-0004/0007）

### BUG-0016-admin-list-status-action-confirm-missing 要点

- **严重等级**：medium（P1）
- **现象**：用户列表冻结/解冻、SKU 上下架/恢复点击即 API；用户删除使用 `window.confirm` 非 modal
- **根因**：REQ-0007/0008 确认模式未横向推广；各页独立实现无共享 confirm 契约
- **修复范围**：`UserManagementPage` freeze/unfreeze/delete modal；`TileSkuManagementPage` publish/unpublish confirm；Vitest；**排除**品牌（已交付）、重置密码 UI（→ BUG-0017）
- OpenSpec `fix-admin-list-status-action-confirm`（**archived** 2026-06-27）

### BUG-0017-user-reset-password-confirm-ui-inconsistency 要点

- **严重等级**：medium（P1）
- **现象**：用户列表「重置密码」使用 `window.confirm`，与同页冻结/删除及类目启停 DS modal 不一致
- **根因**：`add-user-management` 遗留；BUG-0016 change 有意排除重置密码 confirm
- **修复范围**：`UserManagementPage` 重置前 confirm modal + Vitest；**排除** `ResetPasswordDialog` 结果弹窗；无 API/DB/Orval
- OpenSpec `fix-user-reset-password-confirm-ui`（**待 `/bug-opsx`**；approved 2026-06-27；MUST NOT 与 BUG-0016 change 混 scope）

### BUG-0018-tile-sku-modal-video-upload-display 要点

- **严重等级**：high（P1 BUG）
- **现象**：SKU 弹窗「商品视频」上传 MP4 后同一弹窗会话内无文件卡片/上传状态，用户无法确认成功
- **根因**：缺 AC-035 上传状态机；错误仅在弹窗顶部；成功回显显著性不足；未横向同步 BUG-0004 Logo 模式
- **修复范围**：`TileSkuFormModal` 视频区状态机 + 区域反馈 + Vitest；**不含**保存后重开/列表计数；无 API schema/DB 变更（除非 apply 发现独立问题）
- OpenSpec `fix-tile-sku-modal-video-upload-display`（**approved**；待 `/bug-opsx`；依赖 `add-tile-sku-management` + BUG-0011 滚动基线）

### BUG-0020-tile-sku-modal-video-upload-413 要点

- **严重等级**：high（P1 BUG）
- **现象**：经 `localhost:3000` 上传 SKU 商品视频返回 **413 Request Entity Too Large**；典型 MP4 > ~1MB 在 Nginx 层被拒
- **根因**：`nginx.conf` 缺 `client_max_body_size`（默认 ~1MB）；图片/视频上传大小与 MIME 白名单 env 未统一落地
- **修复范围**：`nginx.conf` body 限制；`config.py` + `uploads.py` 读取 `MAX_IMAGE/VIDEO_SIZE_MB`、`ALLOWED_*_TYPES`；`.env.example` 与文档；pytest；**须重建 Web 镜像**
- **与 BUG-0018**：0020 为上传失败（413），0018 为上传成功后的 UI 回显；须分别修复
- OpenSpec `fix-tile-sku-modal-video-upload-413`（**approved**；待 `/bug-opsx`；依赖 REQ-0006 视频上传链路 + BUG-0006 MinIO 基线）

### REQ-0010-product-version-display 要点

- **优先级**：P2
- **范围**：管理端 `AdminSidebar` + 店主端 `Sidebar` 顶部 brand-head；产品名 + version pill（参照 SoulKing 参考图）
- **版本维护**：`src/shared/` 单一常量（如 `PRODUCT_VERSION = 'v0.0.1'`）；发版人工更新；不读 package.json / API version
- **仅 Web 前端** + Vitest；无 API / DB / Orval 变更
- OpenSpec `add-product-version-display`（**applied** 17/17；待 `/opsx-archive`）

### REQ-0011-admin-sidebar-expand-collapse 要点

- **优先级**：P1
- **范围**：管理端 `AdminLayout` / `AdminSidebar`；expanded 264px ↔ collapsed 72px；头部右上 chevron（‹ / ›）
- **持久化**：`localStorage` key `admin-sidebar-collapsed`；跨 `/admin/*` 路由保持
- **collapsed**：隐藏产品名/版本 pill/分区标题/nav 文案/用户姓名邮箱；保留 logo 缩略、nav 图标、active accent、avatar 菜单
- **Out**：店主端 Sidebar、≤1023px responsive 变更、flyout 子菜单
- **依赖**：REQ-0010 brand-head（建议先 apply/archive REQ-0010 或并行）
- **仅 Web 前端** + Vitest + HTML 原型并排；无 API / DB / Orval
- OpenSpec `add-admin-sidebar-collapse`（**proposed**；待 `/opsx-apply`）

## Scope

### 包含需求

<!-- workflow-sync:scope-requirements:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| REQ-0004 | 管理后台首页 V5 | P0 | done | archived `add-admin-home`（2026-06-15 00:00:00） |
| REQ-0005 | 管理后台用户管理 | P1 | done | archived `add-user-management`（2026-06-20 00:00:00） |
| REQ-0005 | 管理后台用户管理列表页 UI 优化 | P1 | done | archived `fix-user-management-list-refine`（2026-06-20 00:00:00） |
| REQ-0003 | 登录页记住凭证与密码显隐 | P1 | done | archived `add-login-remember-autofill`（2026-06-20 00:00:00） |
| REQ-0005 | 管理后台 - 瓷砖品牌管理 | P0 | done | archived `add-brand-management`（2026-06-26 00:00:00） |
| REQ-0005 | 管理后台 - 瓷砖类目管理 | P0 | done | archived `add-tile-category-management`（2026-06-20 00:00:00） |
| REQ-0006 | 瓷砖SKU管理页面 | P1 | done | archived `add-tile-sku-management`（2026-06-27 00:00:00） |
| REQ-0007 | 管理后台瓷砖类目管理页 UI 优化 | P1 | done | archived `fix-tile-category-management-refine`（2026-06-22 00:00:00） |
| REQ-0008 | 管理后台品牌列表启停二次确认 | P1 | done | archived `fix-brand-status-confirm`（2026-06-26 00:00:00） |
| REQ-0010 | Web 端产品版本号展示（管理端 + 店主端侧边栏） | P2 | done | archived `add-product-version-display`（2026-06-27 00:00:00） |
| REQ-0011 | 管理端侧边栏展开/收起（参照 SoulKing 交互） | P1 | done | archived `add-admin-sidebar-collapse`（2026-06-27 00:00:00） |
<!-- workflow-sync:scope-requirements:end -->

### 包含 BUG

<!-- workflow-sync:scope-bugs:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| BUG-0001 | 瓷砖类目停用行缺少「启用」操作入口 | high | done | archived `fix-tile-category-enable-action`（2026-06-20 00:00:00） |
| BUG-0002 | 品牌管理分页与Logo选择文件控件UI不一致 | medium | done | archived `fix-brand-ui-consistency`（2026-06-27 08:14:56） |
| BUG-0003 | 品牌图片上传后不显示且状态提示导致页面上下波动 | high | done | archived `fix-brand-image-display-layout-shift`（2026-06-27 08:14:56） |
| BUG-0004 | 编辑品牌弹窗更换 Logo 后未上传且缺少上传进度反馈 | medium | done | archived `fix-brand-logo-upload-progress`（2026-06-27 08:14:56） |
| BUG-0005 | 服务重启后正确账号密码无法登录管理端 | high | done | archived `fix-admin-login-service-restart`（2026-06-27 08:14:56） |
| BUG-0006 | 业务上传未写入 MinIO 对象存储 | high | done | archived `fix-object-storage-upload-not-minio`（2026-06-27 08:14:56） |
| BUG-0007 | 对象存储修复后品牌 Logo 仍不显示 | high | done | archived `fix-brand-logo-display-after-storage-fix`（2026-06-27 08:14:56） |
| BUG-0008 | 对象存储修复后本地 uploads 双目录残留与历史数据清理缺失 | medium | done | archived `fix-object-storage-legacy-upload-residue`（2026-06-27 08:14:56） |
| BUG-0009 | SKU列表分页与用户管理页不一致且表头上方多余标题行 | medium | done | archived `fix-tile-sku-list-ui-inconsistency`（2026-06-27 10:40:49） |
| BUG-0011 | SKU新增/编辑弹窗内容溢出且无垂直滚动条 | high | done | archived `fix-tile-sku-modal-content-overflow`（2026-06-27 09:37:19） |
| BUG-0010 | SKU弹窗副标题与品牌弹窗样式不一致 | medium | done | archived `fix-tile-sku-modal-subtitle-inconsistency`（2026-06-27 00:00:00） |
| BUG-0012 | SKU弹窗表面工艺与参考价格字段规则不符合产品预期 | medium | done | archived `fix-tile-sku-modal-form-field-rules`（2026-06-27 00:00:00） |
| BUG-0014 | SKU 列表已下架行缺少「上架」操作入口 | high | done | archived `fix-tile-sku-publish-action-missing`（2026-06-27 12:29:15） |
| BUG-0015 | 管理端列表页状态变更 Tips 推挤页面导致上下布局波动 | medium | done | archived `fix-admin-list-status-toast-layout`（2026-06-27 12:59:21） |
| BUG-0016 | 管理端用户/SKU 列表状态变更操作缺少二次确认弹窗 | medium | done | archived `fix-admin-list-status-action-confirm`（2026-06-27 00:00:00） |
| BUG-0017 | 用户重置密码二次确认弹窗与类目启用停用确认弹窗 UI 不一致 | medium | done | archived `fix-user-reset-password-confirm-ui`（2026-06-27 00:00:00） |
| BUG-0019 | 用户弹窗与列表头像上传后未回显且更换功能未生效 | high | done | archived `fix-user-modal-avatar-upload-display`（2026-06-27 00:00:00） |
| BUG-0018 | SKU弹窗商品视频上传后未即时回显文件卡片 | high | done | archived `fix-tile-sku-modal-video-upload-display`（2026-06-27 00:00:00） |
| BUG-0020 | SKU弹窗视频上传返回413 Request Entity Too Large | high | done | archived `fix-tile-sku-modal-video-upload-413`（2026-06-27 00:00:00） |
<!-- workflow-sync:scope-bugs:end -->

### 包含 Change

<!-- workflow-sync:scope-changes:start -->
| Change ID | 关联需求 | 状态 | Sprint 目标 |
|---|---|---|---|
| `add-admin-home` | REQ-0004-admin-home | archived | archived `add-admin-home`（2026-06-15 00:00:00） |
| `add-user-management` | REQ-0005-user-management | archived | archived `add-user-management`（2026-06-20 00:00:00） |
| `fix-user-management-list-refine` | REQ-0005-user-management-list-refine | archived | archived `fix-user-management-list-refine`（2026-06-20 00:00:00） |
| `add-login-remember-autofill` | REQ-0003-login-remember-autofill | archived | archived `add-login-remember-autofill`（2026-06-20 00:00:00） |
| `add-brand-management` | REQ-0005-brand-management | archived | archived `add-brand-management`（2026-06-26 00:00:00） |
| `add-tile-category-management` | REQ-0005-tile-category-management | archived | archived `add-tile-category-management`（2026-06-20 00:00:00） |
| `fix-tile-category-enable-action` | BUG-0001-tile-category-enable-missing | archived | archived `fix-tile-category-enable-action`（2026-06-20 00:00:00） |
| `add-tile-sku-management` | REQ-0006-tile-sku-management | archived | archived `add-tile-sku-management`（2026-06-27 00:00:00） |
| `fix-tile-category-management-refine` | REQ-0007-tile-category-management-refine | archived | archived `fix-tile-category-management-refine`（2026-06-22 00:00:00） |
| `fix-brand-ui-consistency` | BUG-0002-brand-ui-inconsistency | archived | archived `fix-brand-ui-consistency`（2026-06-27 08:14:56） |
| `fix-brand-image-display-layout-shift` | REQ-0005-brand-management | archived | archived `fix-brand-image-display-layout-shift`（2026-06-27 08:14:56） |
| `fix-brand-logo-upload-progress` | REQ-0005-brand-management | archived | archived `fix-brand-logo-upload-progress`（2026-06-27 08:14:56） |
| `fix-object-storage-upload-not-minio` | BUG-0006-object-storage-upload-not-minio | archived | archived `fix-object-storage-upload-not-minio`（2026-06-27 08:14:56） |
| `fix-brand-logo-display-after-storage-fix` | REQ-0005-brand-management | archived | archived `fix-brand-logo-display-after-storage-fix`（2026-06-27 08:14:56） |
| `fix-brand-status-confirm` | REQ-0008-brand-status-confirm | archived | archived `fix-brand-status-confirm`（2026-06-26 00:00:00） |
| `fix-admin-login-service-restart` | REQ-0001-user-login | archived | archived `fix-admin-login-service-restart`（2026-06-27 08:14:56） |
| `fix-object-storage-legacy-upload-residue` | BUG-0008-object-storage-legacy-upload-residue | archived | archived `fix-object-storage-legacy-upload-residue`（2026-06-27 08:14:56） |
| `fix-tile-sku-modal-content-overflow` | REQ-0006-tile-sku-management | archived | archived `fix-tile-sku-modal-content-overflow`（2026-06-27 09:37:19） |
| `fix-tile-sku-list-ui-inconsistency` | REQ-0006-tile-sku-management | archived | archived `fix-tile-sku-list-ui-inconsistency`（2026-06-27 10:40:49） |
| `fix-tile-sku-modal-subtitle-inconsistency` | REQ-0006-tile-sku-management | archived | archived `fix-tile-sku-modal-subtitle-inconsistency`（2026-06-27 00:00:00） |
| `fix-tile-sku-modal-form-field-rules` | REQ-0006-tile-sku-management | archived | archived `fix-tile-sku-modal-form-field-rules`（2026-06-27 00:00:00） |
| `fix-tile-sku-publish-action-missing` | REQ-0006-tile-sku-management | archived | archived `fix-tile-sku-publish-action-missing`（2026-06-27 12:29:15） |
| `fix-tile-sku-modal-video-upload-display` | REQ-0006-tile-sku-management | archived | archived `fix-tile-sku-modal-video-upload-display`（2026-06-27 00:00:00） |
| `add-product-version-display` | REQ-0010-product-version-display | archived | archived `add-product-version-display`（2026-06-27 00:00:00） |
| `add-admin-sidebar-collapse` | REQ-0011-admin-sidebar-expand-collapse | archived | archived `add-admin-sidebar-collapse`（2026-06-27 00:00:00） |
| `fix-admin-list-status-toast-layout` | REQ-0005-brand-management | archived | archived `fix-admin-list-status-toast-layout`（2026-06-27 12:59:21） |
| `fix-admin-list-status-action-confirm` | REQ-0008-brand-status-confirm | archived | archived `fix-admin-list-status-action-confirm`（2026-06-27 00:00:00） |
| `fix-user-reset-password-confirm-ui` | REQ-0005-user-management | archived | archived `fix-user-reset-password-confirm-ui`（2026-06-27 00:00:00） |
| `fix-user-modal-avatar-upload-display` | REQ-0005-user-management | archived | archived `fix-user-modal-avatar-upload-display`（2026-06-27 00:00:00） |
| `fix-tile-sku-modal-video-upload-413` | REQ-0006-tile-sku-management | archived | archived `fix-tile-sku-modal-video-upload-413`（2026-06-27 00:00:00） |
<!-- workflow-sync:scope-changes:end -->

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
| **BUG-0011-tile-sku-modal-content-overflow** | | | | | |
| 弹窗 flex 滚动布局 + Vitest | S | 0.5 | — | 0.5 | 1 |
| **BUG-0009-tile-sku-list-ui-inconsistency** | | | | | |
| 列表分页 DOM 对齐 + 移除 table-head + Vitest | S | 0.5 | — | 0.5 | 1 |
| **BUG-0012-tile-sku-modal-form-field-rules** | | | | | |
| 表单校验/默认值 + 后端 API + publish 策略 | M | 1 | 1 | — | 2 |
| Orval + Vitest + REQ acceptance delta + trace | S | 0.25 | 0.25 | 0.5 | 1 |
| **BUG-0014-tile-sku-publish-action-missing** | | | | | |
| 列表 DISABLED 行恢复按钮 + Vitest | S | 0.5 | — | 0.5 | 1 |
| trace / 归档 | XS | 0.25 | — | 0.25 | 0.5 |
| **BUG-0015-admin-list-status-tips-layout-shift** | | | | | |
| 共享 toast CSS/组件 + 四页 TSX 改造 | M | 1.5 | — | — | 1.5 |
| Vitest（用户/类目/SKU + 品牌回归） | S | 0.5 | — | 0.5 | 1 |
| 手工布局稳定性冒烟 + trace / 归档 | XS | 0.25 | — | 0.25 | 0.5 |
| **BUG-0019-user-modal-avatar-upload-display** | | | | | |
| 后端 avatar_url + OpenAPI/Orval | S | 0.25 | 0.5 | — | 0.75 |
| UserFormModal 状态机/预览（对齐 BrandFormModal） | M | 1 | — | — | 1 |
| UserManagementPage 列表头像 + Vitest/pytest | S | 0.5 | — | 0.5 | 1 |
| trace / 归档 | XS | 0.25 | — | 0.25 | 0.5 |
| **BUG-0016-admin-list-status-action-confirm-missing** | | | | | |
| 用户/SKU 状态操作 confirm modal | M | 1.25 | — | 0.75 | 2 |
| trace / 归档 | XS | 0.25 | — | 0.25 | 0.5 |
| **BUG-0017-user-reset-password-confirm-ui-inconsistency** | | | | | |
| 重置密码 confirm modal + Vitest | S | 0.75 | — | 0.25 | 1 |
| trace / 归档 | XS | 0.25 | — | 0.25 | 0.5 |
| **BUG-0018-tile-sku-modal-video-upload-display** | | | | | |
| 视频上传状态机 + 区域反馈 + Vitest | S | 1 | — | 0.5 | 1.5 |
| trace / 归档 | XS | 0.25 | — | 0.25 | 0.5 |
| **BUG-0020-tile-sku-modal-video-upload-413** | | | | | |
| Nginx `client_max_body_size` + env 上传限制落地 | S | 0.25 | 0.75 | — | 1 |
| pytest + `.env.example` / 文档 + Docker 大 MP4 验收 | XS | 0.25 | — | 0.5 | 0.75 |
| trace / 归档（须重建 Web 镜像） | XS | 0.25 | — | 0.25 | 0.5 |
| **REQ-0010-product-version-display** | | | | | |
| `PRODUCT_VERSION` 常量 + 双端 brand-head 组件 | S | 1 | — | — | 1 |
| Vitest + HTML 原型验收 + trace / 归档 | S | 0.25 | — | 0.75 | 1 |
| **REQ-0011-admin-sidebar-expand-collapse** | | | | | |
| Layout state + localStorage + CSS var 宽度 | M | 1.5 | — | — | 1.5 |
| Chevron 头部 + collapsed 裁剪 CSS | M | 1 | — | — | 1 |
| Vitest + HTML 原型并排验收 + trace / 归档 | S | 0.25 | — | 0.75 | 1 |
| **合计** | | **62** | **28** | **24.75** | **98**（Story Points: 150） |

## 变更记录

| 2026-06-27 23:10:01 | lifecycle-stage-migrate | 迁入 `archive/`（status → stage 映射） |

## 里程碑

| 阶段 | 交付 | 目标日期 |
|---|---|---|
| M1 CSS Port + 模块骨架 | add-admin-home tasks §1 | 2026-06-18 00:00:00 |
| M2 AdminLayout + Dashboard | add-admin-home tasks §2–3 | 2026-06-22 00:00:00 |
| M3 add-admin-home 测试 + 构建 | tasks §5–6 | 2026-06-24 00:00:00 |
| M4 admin-home PNG 验收 + archive | tasks §7–9 | 2026-06-26 00:00:00 |
| M5 requirement-to-opsx + add-user-management 实现 | REQ-0005 / opsx apply | 2026-06-27 00:00:00 |
| M6 用户管理测试 + PNG 验收 | REQ-0005 acceptance | 2026-06-28 00:00:00 |
| M6b fix-user-management-list-refine 实现 + v2 PNG 验收 | REQ-0005-user-management-list-refine | 2026-06-28 00:00:00 |
| M7 add-login-remember-autofill 实现 + 测试 + archive | REQ-0003-login-remember-autofill | 2026-06-28 00:00:00 |
| M8 add-brand-management 实现 + 测试 + HTML 验收 | REQ-0005-brand-management | 2026-06-28 00:00:00 |
| M9 add-tile-category-management 实现 + 测试 + HTML 验收 | REQ-0005-tile-category-management | 2026-06-28 00:00:00 |
| M9b fix-tile-category-enable-action（BUG-0001） | BUG-0001-tile-category-enable-missing | 2026-06-28 00:00:00（**done**） |
| M9c fix-tile-category-management-refine | REQ-0007-tile-category-management-refine | 2026-06-28 00:00:00 |
| M9d fix-brand-ui-consistency | BUG-0002-brand-ui-inconsistency | 2026-06-28 00:00:00 |
| M9e fix-brand-image-display-layout-shift | BUG-0003-brand-image-display-layout-shift | 2026-06-28 00:00:00 |
| M9f fix-brand-logo-upload-progress-missing | BUG-0004-brand-logo-upload-progress-missing | 2026-06-28 00:00:00 |
| M9g fix-object-storage-upload-not-minio | BUG-0006-object-storage-upload-not-minio | 2026-06-28 00:00:00 |
| M9h fix-brand-logo-not-displayed-after-storage-fix | BUG-0007-brand-logo-not-displayed-after-storage-fix | 2026-06-28 00:00:00 |
| M9i fix-admin-login-service-restart | BUG-0005-login-fails-after-service-restart | 2026-06-28 00:00:00 |
| M9j fix-brand-status-confirm | REQ-0008-brand-status-confirm | 2026-06-28 00:00:00 |
| M9k fix-object-storage-legacy-upload-residue | BUG-0008-object-storage-legacy-upload-residue | 2026-06-28 00:00:00 |
| M10 add-tile-sku-management 实现 + 测试 + HTML 验收 | REQ-0006-tile-sku-management | 2026-06-28 00:00:00（依赖 M8/M9） |
| M11 add-product-version-display | REQ-0010-product-version-display | 2026-06-28 00:00:00（可与 SKU 收尾并行） |
| M12 add-admin-sidebar-collapse | REQ-0011-admin-sidebar-expand-collapse | 2026-06-28 00:00:00（依赖 REQ-0010 brand-head；可与 M11 并行） |
| M13 fix-tile-sku-modal-form-field-rules（BUG-0012） | BUG-0012-tile-sku-modal-form-field-rules | 2026-06-28 00:00:00（依赖 add-tile-sku-management；待 `/opsx-apply`） |
| M14 fix-tile-sku-publish-action-missing（BUG-0014） | BUG-0014-tile-sku-publish-action-missing | 2026-06-28 00:00:00（依赖 add-tile-sku-management；P0；待 `/opsx-apply`） |
| M15 fix-admin-list-status-toast-layout（BUG-0015） | BUG-0015-admin-list-status-tips-layout-shift | 2026-06-28 00:00:00（四列表页 toast 统一；medium；待 `/opsx-apply`） |
| M16 fix-user-modal-avatar-upload-display（BUG-0019） | BUG-0019-user-modal-avatar-upload-display | 2026-06-28 00:00:00（用户头像回显+上传进度；high；待 `/opsx-apply`） |
| M17 fix-admin-list-status-action-confirm（BUG-0016） | BUG-0016-admin-list-status-action-confirm-missing | 2026-06-28 00:00:00（用户冻结/SKU 上下架 confirm；medium；**archived** 2026-06-27） |
| M18 fix-user-reset-password-confirm-ui（BUG-0017） | BUG-0017-user-reset-password-confirm-ui-inconsistency | 2026-06-28 00:00:00（重置密码 confirm modal；medium；待 `/bug-opsx` → `/opsx-apply`） |
| M19 fix-tile-sku-modal-video-upload-display（BUG-0018） | BUG-0018-tile-sku-modal-video-upload-display | 2026-06-28 00:00:00（SKU 视频即时回显+上传状态；high P1；approved；待 `/bug-opsx`） |
| M20 fix-tile-sku-modal-video-upload-413（BUG-0020） | BUG-0020-tile-sku-modal-video-upload-413 | 2026-06-28 00:00:00（Docker 路径大 MP4 非 413；env 上传限制；high P1；approved；待 `/bug-opsx`） |

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
| R-15 | REQ-0007 类目页 UI refine | 误操作 / 分页不一致 | **已 archive** `fix-tile-category-management-refine`（2026-06-22） |
| R-16 | BUG-0002 品牌管理 UI 一致性 | 品牌页与用户管理页控件体验割裂 | **已 archive** `fix-brand-ui-consistency`（2026-06-25） |
| R-17 | BUG-0004 品牌 Logo 上传进度缺失 | 运营无法确认 Logo 是否正在上传或已成功替换 | **已 archive** `fix-brand-logo-upload-progress`（2026-06-26） |
| R-18 | BUG-0006 对象存储上传未写入 MinIO | 媒体上传与对象存储验收割裂，影响 SKU/品牌/头像素材持久化 | 已完成 `/opsx-archive fix-object-storage-upload-not-minio` |
| R-19 | BUG-0007 对象存储修复后品牌 Logo 仍不显示 | 品牌管理 Logo 展示验收继续失败，影响运营识别品牌 | 已完成 `fix-brand-logo-display-after-storage-fix` archive |
| R-20 | BUG-0005 服务重启后登录失败 | 持久化 SQLite 中已有 admin 与当前环境密码不一致时，管理端登录和演示验收被阻断 | **已 archive** `fix-admin-login-service-restart`（2026-06-26） |
| R-21 | REQ-0008 品牌启停二次确认 | 误触直接启停品牌 | **已 archive** `fix-brand-status-confirm`（2026-06-26） |
| R-22 | BUG-0008 legacy uploads 双目录残留 | 本地磁盘占用与媒体存储排查误导 | **已 archive** `fix-object-storage-legacy-upload-residue`（2026-06-27） |
| R-23 | Sprint 追加 REQ-0010 产品版本展示 | 容量略增；店主端 Sidebar 需新增 brand-head | P2 约 2 人天；`add-product-version-display` applied |
| R-24 | Sprint 追加 REQ-0011 侧栏折叠 | 与 REQ-0010 头部 DOM 耦合；超容量 | P1 约 3.5 人天；须 REQ-0010 apply 后或并行；`add-admin-sidebar-collapse` proposed |
| R-25 | BUG-0012 SKU 表单字段规则变更 | REQ-0006 acceptance delta 遗漏导致归档/验收失败 | `fix-tile-sku-modal-form-field-rules` 已 proposed；apply 时 MUST 同步 requirement/acceptance |
| R-26 | BUG-0014 已下架 SKU 无法 UI 恢复上架 | 运营上下架闭环中断 | **high** P0；`fix-tile-sku-publish-action-missing` proposed；优先于 medium UI 缺陷 apply |
| R-27 | BUG-0015 四页 toast 统一改造 | 品牌页 toast/Logo 回归；连续操作体验仍抖动直至 apply | medium；`fix-admin-list-status-toast-layout` proposed；MUST 保留 `BrandManagementPage.test.tsx` 断言 |
| R-28 | BUG-0019 用户头像展示链路未闭环 | 管理员无法确认头像上传结果；与品牌 Logo 体验不一致 | **high** P1；`fix-user-modal-avatar-upload-display` proposed；上传已通，修复面集中 UI+avatar_url |
| R-29 | BUG-0016 用户/SKU 状态操作无 confirm | 误触冻结/上下架；与品牌/类目交互不一致 | **已 archive** `fix-admin-list-status-action-confirm`（2026-06-27） |
| R-30 | BUG-0017 与 BUG-0016 change scope 混用 | 重置密码 confirm 与用户冻结 modal 同页耦合导致回归 | medium P1；`fix-user-reset-password-confirm-ui` 待 bug-opsx；MUST 独立 change；依赖 BUG-0016 已归档基线 |
| R-31 | BUG-0018 SKU 视频上传反馈未闭环 | 运营无法确认视频是否已加入待保存列表；阻塞 AC-035 即时回显验收 | **high** P1；`fix-tile-sku-modal-video-upload-display` approved 待 bug-opsx；MUST 视频区内反馈；**不回归** BUG-0011 滚动 |
| R-32 | BUG-0020 Docker 路径视频上传 413 | 典型 MP4 无法经 `localhost:3000` 上传；阻塞 AC-035 端到端可上传性 | **high** P1；`fix-tile-sku-modal-video-upload-413` approved 待 bug-opsx；MUST Nginx body ≥ env 上限；**须重建 Web 镜像**；与 BUG-0018 分层修复 |

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
              ├── fix-admin-list-status-action-confirm（BUG-0016；用户 freeze + SKU 上下架 confirm；✓ archived）
              ├── fix-user-reset-password-confirm-ui（BUG-0017；重置密码 confirm modal；待 bug-opsx）
              ├── fix-user-modal-avatar-upload-display（BUG-0019；proposed）
              ├── add-brand-management（REQ-0005-brand-management）
              │     ├── fix-brand-ui-consistency（BUG-0002-brand-ui-inconsistency）
              │     ├── fix-brand-image-display-layout-shift（BUG-0003；品牌 toast 先例）✓ archived
              │     ├── fix-brand-logo-upload-progress（BUG-0004）
              │     ├── fix-brand-logo-display-after-storage-fix（BUG-0007）
              │     └── fix-brand-status-confirm（REQ-0008-brand-status-confirm）
              ├── fix-admin-list-status-toast-layout（BUG-0015；四列表页 toast 统一；proposed）
              ├── add-tile-category-management（REQ-0005-tile-category-management）
              │     ├── fix-tile-category-enable-action（BUG-0001）✓ archived
              │     ├── fix-tile-category-management-refine（REQ-0007-tile-category-management-refine）
              │     └── add-tile-sku-management（REQ-0006-tile-sku-management）
              │           ├── fix-tile-sku-modal-content-overflow（BUG-0011）✓ archived
              │           ├── fix-tile-sku-list-ui-inconsistency（BUG-0009）✓ archived
              │           ├── fix-tile-sku-modal-form-field-rules（BUG-0012；proposed）
              │           ├── fix-tile-sku-publish-action-missing（BUG-0014；proposed；P0）
              │           ├── fix-tile-sku-modal-video-upload-display（BUG-0018；approved；待 bug-opsx）
              │           ├── fix-tile-sku-modal-video-upload-413（BUG-0020；approved；待 bug-opsx）
              │           └── fix-admin-list-status-action-confirm（BUG-0016；SKU 上下架 confirm；待 bug-opsx）
              ├── REQ-0010-product-version-display（P2；依赖 Admin Shell + 店主端 Sidebar 模板）
              │     ├── add-product-version-display（applied）
              │     └── REQ-0011-admin-sidebar-expand-collapse（P1；chevron 依附 brand-head）
              │           └── add-admin-sidebar-collapse（proposed）
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
- REQ-0010-product-version-display：仅 Web 前端 + `src/shared/` 常量；无需 Orval / DB；`add-product-version-display` applied
- REQ-0011-admin-sidebar-expand-collapse：仅 Web 管理端前端；无需 Orval / DB；依赖 REQ-0010 brand-head；`add-admin-sidebar-collapse` proposed
- BUG-0019-user-modal-avatar-upload-display：需 `UserAdminItem.avatar_url`、OpenAPI 更新与 Orval；弹窗/列表 Vitest + pytest
- BUG-0016-admin-list-status-action-confirm-missing：仅 Web 前端；用户 freeze/delete modal + SKU 上下架 confirm；无 API/DB/Orval；**archived** `fix-admin-list-status-action-confirm`
- BUG-0017-user-reset-password-confirm-ui-inconsistency：仅 Web 前端；重置密码 confirm modal；无 API/DB/Orval；待 `/bug-opsx fix-user-reset-password-confirm-ui`；MUST NOT 与 BUG-0016 change 混 scope
- BUG-0018-tile-sku-modal-video-upload-display：仅 Web 前端 SKU 弹窗视频区；上传状态机 + 即时文件卡片回显；无 API schema/DB/Orval（可选 `uploadTileVideo` 进度回调）；待 `/bug-opsx fix-tile-sku-modal-video-upload-display`
- BUG-0020-tile-sku-modal-video-upload-413：`nginx.conf` `client_max_body_size` + 后端 env 上传限制（`MAX_IMAGE/VIDEO_SIZE_MB`、`ALLOWED_*_TYPES`）；无 API schema/DB/Orval；修改 Nginx 后 **须重建 Web 镜像**；待 `/bug-opsx fix-tile-sku-modal-video-upload-413`
- Sprint 结束：`/opsx-archive` 各 change + 更新 `acceptance-report.md`

## 关联文档

| 文档 | 路径 |
|---|---|
| Sprint 索引 | `iterations/archive/sprint-002/sprint.yaml` |
| 需求 PRD（首页） | `issues/requirements/archive/REQ-0004-admin-home/requirement.md` |
| 验收标准（首页） | `issues/requirements/archive/REQ-0004-admin-home/acceptance.md` |
| OpenSpec Change（首页） | `openspec/changes/add-admin-home/` |
| PNG Golden（首页） | `issues/requirements/archive/REQ-0004-admin-home/prototype/web/admin-home.png` |
| 需求 PRD（用户管理） | `issues/requirements/archive/REQ-0005-user-management/requirement.md` |
| 验收标准（用户管理） | `issues/requirements/archive/REQ-0005-user-management/acceptance.md` |
| OpenSpec Change（用户管理） | `openspec/changes/add-user-management/`（待创建） |
| PNG Golden（用户管理 v1） | `issues/requirements/archive/REQ-0005-user-management/prototype/web/user-management-list.png` |
| 需求 PRD（列表 UI 优化） | `issues/requirements/archive/REQ-0005-user-management-list-refine/requirement.md` |
| 验收标准（列表 UI 优化） | `issues/requirements/archive/REQ-0005-user-management-list-refine/acceptance.md` |
| OpenSpec Change（列表 UI 优化） | `openspec/changes/fix-user-management-list-refine/` |
| HTML/PNG Golden（列表 v2） | `issues/requirements/archive/REQ-0005-user-management-list-refine/prototype/web/user-management-list.html` |
| 需求 PRD（登录增强） | `issues/requirements/archive/REQ-0003-login-remember-autofill/requirement.md` |
| 验收标准（登录增强） | `issues/requirements/archive/REQ-0003-login-remember-autofill/acceptance.md` |
| OpenSpec Change（登录增强） | `openspec/changes/add-login-remember-autofill/` |
| 需求 PRD（品牌管理） | `issues/requirements/archive/REQ-0005-brand-management/requirement.md` |
| 验收标准（品牌管理） | `issues/requirements/archive/REQ-0005-brand-management/acceptance.md` |
| OpenSpec Change（品牌管理） | `openspec/changes/add-brand-management/` |
| HTML 原型（品牌管理） | `issues/requirements/archive/REQ-0005-brand-management/prototype/web/brand-management.html` |
| 缺陷记录（品牌 UI 一致性） | `issues/bugs/archive/BUG-0002-brand-ui-inconsistency/` |
| OpenSpec Change（品牌 UI 一致性修复） | `openspec/changes/fix-brand-ui-consistency/` |
| 缺陷记录（品牌 Logo 上传进度反馈） | `issues/bugs/archive/BUG-0004-brand-logo-upload-progress-missing/` |
| OpenSpec Change（品牌 Logo 上传进度反馈修复） | `openspec/changes/fix-brand-logo-upload-progress/` |
| 缺陷记录（对象存储上传未写入 MinIO） | `issues/bugs/archive/BUG-0006-object-storage-upload-not-minio/` |
| OpenSpec Change（对象存储上传未写入 MinIO 修复） | `openspec/changes/archive/2026-06-26-fix-object-storage-upload-not-minio/` |
| 缺陷记录（对象存储修复后品牌 Logo 仍不显示） | `issues/bugs/archive/BUG-0007-brand-logo-not-displayed-after-storage-fix/` |
| OpenSpec Change（对象存储修复后品牌 Logo 仍不显示修复） | `openspec/changes/archive/2026-06-26-fix-brand-logo-display-after-storage-fix/` |
| 缺陷记录（服务重启后登录失败） | `issues/bugs/archive/BUG-0005-login-fails-after-service-restart/` |
| OpenSpec Change（服务重启后登录失败修复） | `openspec/changes/fix-admin-login-service-restart/` |
| 缺陷记录（对象存储 legacy uploads 残留） | `issues/bugs/archive/BUG-0008-object-storage-legacy-upload-residue/` |
| OpenSpec Change（对象存储 legacy uploads 清理） | `openspec/changes/archive/2026-06-26-fix-object-storage-legacy-upload-residue/` |
| 需求 PRD（类目管理） | `issues/requirements/archive/REQ-0005-tile-category-management/requirement.md` |
| 验收标准（类目管理） | `issues/requirements/archive/REQ-0005-tile-category-management/acceptance.md` |
| OpenSpec Change（类目管理） | `openspec/changes/archive/2026-06-20-add-tile-category-management/` |
| HTML 原型（类目管理） | `issues/requirements/archive/REQ-0005-tile-category-management/prototype/web/tile-category-management.html` |
| 缺陷记录（类目启用） | `issues/bugs/archive/BUG-0001-tile-category-enable-missing/` |
| OpenSpec Change（类目启用修复） | `openspec/changes/archive/2026-06-20-fix-tile-category-enable-action/` |
| 需求 PRD（类目 UI 优化） | `issues/requirements/archive/REQ-0007-tile-category-management-refine/requirement.md` |
| 验收标准（类目 UI 优化） | `issues/requirements/archive/REQ-0007-tile-category-management-refine/acceptance.md` |
| OpenSpec Change（类目 UI 优化） | `openspec/changes/fix-tile-category-management-refine/` |
| v2 context（类目列表） | `issues/requirements/archive/REQ-0007-tile-category-management-refine/prototype/web/tile-category-management-list-refine-context.md` |
| 需求 PRD（品牌启停确认） | `issues/requirements/archive/REQ-0008-brand-status-confirm/requirement.md` |
| 验收标准（品牌启停确认） | `issues/requirements/archive/REQ-0008-brand-status-confirm/acceptance.md` |
| OpenSpec Change（品牌启停确认） | `openspec/changes/fix-brand-status-confirm/` |
| 启停确认 context | `issues/requirements/archive/REQ-0008-brand-status-confirm/prototype/web/brand-status-confirm-context.md` |
| 需求 PRD（SKU 管理） | `issues/requirements/archive/REQ-0006-tile-sku-management/requirement.md` |
| 验收标准（SKU 管理） | `issues/requirements/archive/REQ-0006-tile-sku-management/acceptance.md` |
| OpenSpec Change（SKU 管理） | `openspec/changes/add-tile-sku-management/` |
| HTML 原型（SKU 管理） | `issues/requirements/archive/REQ-0006-tile-sku-management/prototype/web/tile-sku-management-list.html` |
| 需求 PRD（产品版本展示） | `issues/requirements/archive/REQ-0010-product-version-display/requirement.md` |
| 验收标准（产品版本展示） | `issues/requirements/archive/REQ-0010-product-version-display/acceptance.md` |
| OpenSpec Change（产品版本展示） | `openspec/changes/add-product-version-display/` |
| HTML 原型（版本展示 admin/catalog） | `issues/requirements/archive/REQ-0010-product-version-display/prototype/web/` |
| 需求 PRD（侧栏展开/收起） | `issues/requirements/archive/REQ-0011-admin-sidebar-expand-collapse/requirement.md` |
| 验收标准（侧栏展开/收起） | `issues/requirements/archive/REQ-0011-admin-sidebar-expand-collapse/acceptance.md` |
| OpenSpec Change（侧栏展开/收起） | `openspec/changes/add-admin-sidebar-collapse/` |
| 缺陷记录（用户头像回显） | `issues/bugs/archive/BUG-0019-user-modal-avatar-upload-display/` |
| OpenSpec Change（用户头像回显修复） | `openspec/changes/fix-user-modal-avatar-upload-display/` |
| 缺陷记录（状态操作 confirm 缺失） | `issues/bugs/archive/BUG-0016-admin-list-status-action-confirm-missing/` |
| 缺陷记录（重置密码 confirm UI） | `issues/bugs/archive/BUG-0017-user-reset-password-confirm-ui-inconsistency/` |
| 缺陷记录（SKU 视频上传即时回显） | `issues/bugs/archive/BUG-0018-tile-sku-modal-video-upload-display/` |
| 缺陷记录（SKU 视频上传 413） | `issues/bugs/archive/BUG-0020-tile-sku-modal-video-upload-413/` |
| OpenSpec Change（状态操作 confirm 修复） | `openspec/changes/archive/2026-06-27-fix-admin-list-status-action-confirm/` |

## 经验复盘

- 文档：[`docs/knowledge-base/retrospectives/sprint-002-retrospective.md`](../../docs/knowledge-base/retrospectives/sprint-002-retrospective.md)
- 生成：2026-06-27 16:15:00（`/sprint-exps`）
