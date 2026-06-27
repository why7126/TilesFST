---
created_at: 2026-06-27 08:42:28
title: Sprint 002 发布说明
purpose: 记录 Sprint 002 交付能力与发布注意事项（初稿）
content: 基于 REQ-0004、REQ-0005、REQ-0005-user-management-list-refine、REQ-0003-login-remember-autofill、REQ-0005-brand-management、REQ-0005-tile-category-management、REQ-0006-tile-sku-management、REQ-0007-tile-category-management-refine、REQ-0008-brand-status-confirm、BUG-0002-brand-ui-inconsistency、BUG-0003-brand-image-display-layout-shift、BUG-0004-brand-logo-upload-progress-missing、BUG-0005-login-fails-after-service-restart、BUG-0006-object-storage-upload-not-minio、BUG-0007-brand-logo-not-displayed-after-storage-fix、BUG-0008-object-storage-legacy-upload-residue 及对应 OpenSpec Change
source: AI 根据迭代范围生成，项目团队确认
update_method: Sprint 完成或范围变更时更新
owner: 项目负责人
status: published
note: workflow-sync — Sprint completed；30/30 Change archived
updated_at: 2026-06-27 15:52:00
---

# Sprint 002 发布说明

## 版本信息

| 字段 | 内容 |
|---|---|
| Sprint | sprint-002 |
| 关联需求 | REQ-0004-admin-home、REQ-0005-user-management、REQ-0005-user-management-list-refine、REQ-0003-login-remember-autofill、REQ-0005-brand-management、REQ-0005-tile-category-management、REQ-0006-tile-sku-management、REQ-0007-tile-category-management-refine、REQ-0008-brand-status-confirm、REQ-0010-product-version-display、REQ-0011-admin-sidebar-expand-collapse |
| 关联 BUG | BUG-0001-tile-category-enable-missing、BUG-0002-brand-ui-inconsistency、BUG-0003-brand-image-display-layout-shift、BUG-0004-brand-logo-upload-progress-missing、BUG-0005-login-fails-after-service-restart、BUG-0006-object-storage-upload-not-minio、BUG-0007-brand-logo-not-displayed-after-storage-fix、BUG-0008-object-storage-legacy-upload-residue、BUG-0009-tile-sku-list-ui-inconsistency、BUG-0011-tile-sku-modal-content-overflow、BUG-0012-tile-sku-modal-form-field-rules、BUG-0014-tile-sku-publish-action-missing、BUG-0015-admin-list-status-tips-layout-shift、BUG-0016-admin-list-status-action-confirm-missing、BUG-0017-user-reset-password-confirm-ui-inconsistency、BUG-0018-tile-sku-modal-video-upload-display、BUG-0019-user-modal-avatar-upload-display、BUG-0020-tile-sku-modal-video-upload-413 |
| 关联 Change | add-admin-home、add-user-management、fix-user-management-list-refine、add-login-remember-autofill、add-brand-management、add-tile-category-management、fix-tile-category-enable-action、fix-tile-category-management-refine、fix-brand-ui-consistency、fix-brand-image-display-layout-shift、fix-brand-logo-upload-progress、fix-object-storage-upload-not-minio、fix-brand-logo-display-after-storage-fix、fix-admin-login-service-restart、fix-brand-status-confirm、fix-object-storage-legacy-upload-residue、add-tile-sku-management、fix-tile-sku-modal-content-overflow、fix-tile-sku-list-ui-inconsistency、add-product-version-display、add-admin-sidebar-collapse、fix-tile-sku-modal-form-field-rules、fix-tile-sku-publish-action-missing、fix-admin-list-status-toast-layout、fix-admin-list-status-action-confirm、fix-user-reset-password-confirm-ui、fix-user-modal-avatar-upload-display |
| 计划周期 | 2026-06-15 ~ 2026-06-28 |

<!-- workflow-sync:release-status:start -->
| 发布状态 | **已发布（Published）** |
<!-- workflow-sync:release-status:end -->
| 发布状态 | **实现完成，待 sign-off（Ready for sign-off）** |

## 新增功能（已交付）

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

### Web 管理端瓷砖 SKU 管理（计划）

- `/admin/tile-skus` SKU 列表：五维筛选、四指标卡、分页（10/20/50/100，默认 20）
- 新增/编辑 SKU 弹窗（880px）；多图主图、多视频；参考价格（元）；无状态字段、默认草稿
- 「保存草稿」与「创建SKU」双按钮；上下架/条件删除
- `admin` 与 `employee` 可维护 SKU 主数据
- CSS Port：`features/admin/styles/tile-sku-management.css`
- 后端 Admin Tile SKU API；扩展 `tiles` 表 + `tile_videos`；图片/视频 MinIO 上传

### Web 端产品版本号展示（计划）

- 管理端侧边栏顶部 `TILESFST` + 产品版本 pill（如 `v0.0.1`）
- 店主端筛选侧栏顶部品牌名 + 同一版本 pill
- 版本由 `src/shared/` 单一常量人工维护；不展示 API 版本
- 仅 Web 前端；无 API / DB / Orval 变更

## 优化项（已交付）

- 移除 `AdminLayout` 顶栏外露退出按钮，退出收纳至用户菜单下拉（**BREAKING** UI 相对 Sprint 001）
- 用户管理列表页筛选与分页信息层级收紧（REQ-0005-user-management-list-refine）
- 瓷砖类目管理页启停确认、去 section 标题、分页对齐用户管理 v2（REQ-0007-tile-category-management-refine）
- 品牌列表页启停操作二次确认（REQ-0008-brand-status-confirm）
- 品牌管理页分页与 Logo 文件选择控件对齐用户管理页/管理端表单模式（BUG-0002）
- 登录后工作台视觉与登录页暗色旗舰风统一

## BUG 修复

### BUG-0001 瓷砖类目停用行缺少「启用」入口

- **问题**：`/admin/tile-categories` 停用且 SKU=0 的行无法通过 UI 重新启用
- **修复**：操作列对齐品牌管理页；停用行始终展示「启用」；删除规则不变
- **影响**：仅 Web 前端 + vitest；无 API/DB 变更
- OpenSpec：已归档 `2026-06-20-fix-tile-category-enable-action`

### BUG-0002 品牌管理 UI 一致性修复

- **问题**：`/admin/brands` 底部分页与用户管理页分页不一致；新增/编辑品牌弹窗 Logo 选择文件控件与管理端整体表单风格不一致
- **修复结果**：分页对齐用户管理页；Logo 文件选择控件对齐管理端图片上传控件模式
- **影响**：仅 Web 管理端 UI；无 API/DB/Orval/MinIO 策略变更
- OpenSpec：`fix-brand-ui-consistency`（archived，2026-06-25）

### BUG-0003 品牌图片显示失败与 Tips 布局波动

- **问题**：`/admin/brands` 上传品牌 Logo 后，列表页和编辑弹窗无法正常展示；状态变更 Tips 临时插入页面顶部导致上下波动
- **修复结果**：补齐品牌 Logo 可访问媒体 URL/代理策略；品牌页状态提示改为不推挤页面主体的固定 toast
- **影响**：Web 管理端品牌页、品牌弹窗、媒体访问链路；API 响应结构未变化，无需同步 OpenAPI 与 Orval
- OpenSpec：`fix-brand-image-display-layout-shift`

### BUG-0004 品牌 Logo 上传进度反馈缺失

- **问题**：编辑品牌弹窗点击「更换 Logo」并选择图片后，缺少上传进度反馈，Logo 预览不更新
- **修复结果**：补齐品牌 Logo 上传状态机、进度条、成功后预览更新、失败重试和同文件重选能力
- **影响**：Web 管理端品牌弹窗；仅前端上传封装增加进度回调，无 API schema / DB / Orval 变更
- OpenSpec：`fix-brand-logo-upload-progress`（archived，2026-06-26）

### BUG-0005 服务重启后正确账号密码无法登录

- **问题**：本地或 Docker 服务重启后，进入 `/admin/login` 使用正确管理员账号密码仍提示「账号或密码错误」
- **修复结果**：默认管理员 seed 保持首次创建和重启不覆盖；新增显式 `ADMIN_RESET_PASSWORD_ON_STARTUP` 恢复策略；补齐根目录 `.env.example`、部署文档、数据库说明和后端认证回归测试
- **影响**：后端初始化/运行时数据治理与文档；登录接口响应 schema 未变化，无需 Orval
- OpenSpec：`fix-admin-login-service-restart`（archived，2026-06-26）

### BUG-0006 对象存储上传未写入 MinIO

- **问题**：MinIO 服务与 `tile-info-platform` 桶已初始化，但头像、品牌 Logo、SKU 图片、SKU 视频等业务上传仍写入本地 `UPLOAD_DIR`，MinIO Console 中无业务对象
- **修复结果**：后端上传已写入 `MINIO_BUCKET=tile-info-platform`，头像、品牌 Logo、SKU 图片、SKU 视频使用标准前缀，`/media/{object_key}` 从 MinIO 受控读取
- **影响**：后端媒体上传与读取链路；上传成功响应 schema 与 URL 语义不变，无需 Orval；已完成 Docker Compose 闭环验证
- OpenSpec：`fix-object-storage-upload-not-minio`（archived，2026-06-26 14:20:50）

### BUG-0007 对象存储修复后品牌 Logo 仍不显示

- **问题**：对象存储写入问题修复后，品牌列表页和品牌编辑弹窗仍无法显示品牌 Logo
- **修复结果**：Web 开发代理与 Docker Nginx 已补齐 `/media` 反代，品牌 Logo `logo_url` 可从后端受控读取并在列表页、编辑弹窗展示
- **影响**：Web 管理端品牌列表与品牌编辑弹窗；API 响应字段未变化，无需同步 OpenAPI 与 Orval
- OpenSpec：`fix-brand-logo-display-after-storage-fix`（archived，2026-06-26 20:21:43）

### BUG-0008 对象存储 legacy uploads 双目录残留

- **问题**：BUG-0006 修复后 `data/uploads` 仍存本地上传孤儿文件，与 MinIO 持久化卷并存
- **修复结果**：新增 `scripts/clean_legacy_uploads.py`；移除 `UPLOAD_DIR` 配置与 Docker uploads 挂载；更新 data/部署/对象存储文档；本地清理 6 个孤儿 PNG
- **影响**：本地 Docker 运维；无 API schema 变更，无需 Orval
- OpenSpec：`fix-object-storage-legacy-upload-residue`（archived，2026-06-27 00:11:29）

### BUG-0016 用户/SKU 列表状态操作缺少二次确认（计划）

- **问题**：用户冻结/解冻、SKU 上下架/恢复点击即生效；用户删除使用浏览器原生 confirm
- **修复计划**：用户 freeze/unfreeze/delete 与 SKU publish/unpublish 增加 DS modal 确认；对齐品牌/类目模式
- **影响**：仅 Web 管理端；无 API/DB/Orval
- OpenSpec：`fix-admin-list-status-action-confirm`（待 `/bug-opsx`）

### BUG-0019 用户弹窗头像上传后未回显（计划）

- **问题**：用户弹窗/列表头像始终 initials；更换头像无预览与上传进度（底层上传 200 且已入库）
- **修复计划**：补 `UserAdminItem.avatar_url`；`UserFormModal` 对齐品牌 Logo 状态机；列表头像 `<img>` 回显
- **影响**：Web 管理端用户管理；需 OpenAPI + Orval
- OpenSpec：`fix-user-modal-avatar-upload-display`（proposed；待 apply）

### BUG-0018 SKU 弹窗商品视频上传后未即时回显（计划）

- **问题**：SKU 弹窗「商品视频」上传 MP4 后无文件卡片/上传状态，用户无法确认成功
- **修复计划**：`TileSkuFormModal` 视频区上传状态机 + 区域级成功/失败反馈 + 即时 `.sku-video-card` 回显；对齐 REQ-0006 AC-035 与品牌 Logo 模式
- **影响**：仅 Web 管理端 SKU 弹窗；无 API schema/DB/Orval（可选上传进度回调）
- OpenSpec：`fix-tile-sku-modal-video-upload-display`（approved；待 `/bug-opsx` → `/opsx-apply`）

### BUG-0020 SKU 弹窗视频上传 413（计划）

- **问题**：经 `localhost:3000` 上传大体积 MP4 返回 413；Nginx 默认 body ~1MB；env 上传限制未对齐
- **修复计划**：`nginx.conf` `client_max_body_size`；`MAX_IMAGE/VIDEO_SIZE_MB` 与 `ALLOWED_*_TYPES` env 落地；文档与 pytest
- **影响**：Web Nginx + 后端配置；无 API schema/DB/Orval；**须重建 Web 镜像**
- OpenSpec：`fix-tile-sku-modal-video-upload-413`（approved；待 `/bug-opsx` → `/opsx-apply`）

## 兼容性影响

| 影响面 | 说明 |
|---|---|
| 后端 API | REQ-0005 新增 Admin Users API；REQ-0005-brand-management 新增 Admin Brands API；REQ-0005-tile-category-management 新增 Admin Tile Categories API；REQ-0006-tile-sku-management 新增 Admin Tile SKU API |
| 数据库 | REQ-0005 需 `users` 表迁移；REQ-0005-brand-management 需 `brands` 表；REQ-0005-tile-category-management 需扩展 `tile_categories` 表；REQ-0006-tile-sku-management 需扩展 `tiles` 表 + `tile_videos` |
| Orval | REQ-0005、REQ-0005-brand-management、REQ-0005-tile-category-management、REQ-0006-tile-sku-management 完成后需重新生成 |
| REQ-0005-user-management-list-refine | 无 API 端点变更；keyword 查询范围收窄 |
| REQ-0003-login-remember-autofill | 无 API/DB 变更 |
| REQ-0007-tile-category-management-refine | 无 API/DB 变更 |
| REQ-0008-brand-status-confirm | 无 API/DB/Orval 变更；仅 Web 管理端启停确认弹窗 |
| BUG-0002-brand-ui-inconsistency | 无 API/DB/Orval 变更；仅 Web 管理端 UI |
| BUG-0003-brand-image-display-layout-shift | 已补齐 `/media/{object_key}` 访问链路；上传与品牌响应 schema 未变化，无需 Orval |
| BUG-0004-brand-logo-upload-progress-missing | 仅 Web 管理端 UI + 前端上传封装进度回调；无 API schema / DB / Orval 变更 |
| BUG-0005-login-fails-after-service-restart | 已完成后端默认管理员初始化/显式恢复策略、根目录 `.env.example`、部署与数据库说明；登录接口 schema 未变化，无需 Orval |
| BUG-0006-object-storage-upload-not-minio | 后端媒体上传已写入 MinIO 单桶；Docker Compose 闭环通过；上传成功 schema 不变，无需 Orval；已同步 `.env.example`、媒体与部署文档 |
| BUG-0007-brand-logo-not-displayed-after-storage-fix | 已完成 `fix-brand-logo-display-after-storage-fix` archive；Web `/media` 反代闭环通过，API schema 未变化，无需 Orval |
| BUG-0008-object-storage-legacy-upload-residue | 已完成 legacy uploads 清理脚本、UPLOAD_DIR 收敛与文档；无 API schema 变更，无需 Orval |
| BUG-0016-admin-list-status-action-confirm-missing | 无 API/DB/Orval 变更；仅 Web 管理端 confirm modal |
| BUG-0018-tile-sku-modal-video-upload-display | 无 API schema/DB/Orval 变更；仅 Web SKU 弹窗视频上传 UI |
| BUG-0020-tile-sku-modal-video-upload-413 | Nginx `client_max_body_size` + 后端 env 上传限制；无 API schema/DB/Orval；须重建 Web 镜像 |
| Docker | Web + Backend 镜像重建 |
| REQ-0001 | 退出登录入口位置变更（行为不变）；冻结用户登录拒绝 |

## 升级说明

1. `./scripts/docker-up.sh`
2. 使用已有 admin 账号登录 `http://localhost:3000/admin/login`（可验证记住凭证与密码显隐）
3. 登录成功后访问 `http://localhost:3000/admin/dashboard`
4. 使用 `admin` 账号访问 `http://localhost:3000/admin/users` 验证用户管理（含列表 v2 筛选/分页）
5. 使用 `admin` 或 `employee` 访问 `http://localhost:3000/admin/brands` 验证品牌管理
6. 使用 `admin` 或 `employee` 访问 `http://localhost:3000/admin/tile-categories` 验证类目管理（含停用类目「启用」按钮）
7. 使用 `admin` 或 `employee` 访问 `http://localhost:3000/admin/tile-skus` 验证 SKU 管理
8. 视觉验收：1280×1024 并排 `admin-home.png`、`user-management-list.png`（v2 refine）、`user-management-modal.png`、`brand-management.html`、`tile-category-management.html`、`tile-sku-management-list.html`

## 已知限制

- Dashboard 指标与最近更新为 mock 数据
- Banner 管理页未实现
- 个人资料、密码修改为占位
- 用户自助注册、细粒度 RBAC 未实现
- 移动端 Sidebar 仅基础降级（桌面为主验收视口）

## 关联验收

- `iterations/sprint-002/acceptance-report.md`（待人工 sign-off）
- `openspec/changes/archive/2026-06-15-add-admin-home/trace.md`（PNG checklist）
- `openspec/changes/archive/2026-06-20-add-user-management/trace.md`
- `openspec/changes/archive/2026-06-20-fix-user-management-list-refine/trace.md`
- `openspec/changes/archive/2026-06-20-add-login-remember-autofill/trace.md`
- `openspec/changes/archive/2026-06-26-add-brand-management/trace.md`
- `openspec/changes/archive/2026-06-25-fix-brand-ui-consistency/trace.md`
- `issues/bugs/BUG-0003-brand-image-display-layout-shift/acceptance.md`
- `issues/bugs/BUG-0004-brand-logo-upload-progress-missing/acceptance.md`
- `issues/bugs/BUG-0005-login-fails-after-service-restart/acceptance.md`
- `issues/bugs/BUG-0006-object-storage-upload-not-minio/acceptance.md`
- `issues/bugs/BUG-0007-brand-logo-not-displayed-after-storage-fix/acceptance.md`
- `openspec/changes/archive/2026-06-26-fix-brand-logo-display-after-storage-fix/trace.md`
- `openspec/changes/archive/2026-06-26-fix-brand-logo-upload-progress/trace.md`
- `openspec/changes/archive/2026-06-20-add-tile-category-management/trace.md`
- `openspec/changes/archive/2026-06-22-fix-tile-category-management-refine/trace.md`
- `issues/requirements/REQ-0007-tile-category-management-refine/acceptance.md`
