---
created_at: 2026-06-27 08:42:28
title: Sprint 002 验收报告
purpose: 记录 Sprint 002 验收结果与遗留项（模板）
content: 基于 REQ-0004、REQ-0005、REQ-0005-user-management-list-refine、REQ-0003-login-remember-autofill、REQ-0005-brand-management、REQ-0005-tile-category-management、REQ-0006-tile-sku-management、REQ-0007-tile-category-management-refine、REQ-0008-brand-status-confirm、BUG-0002-brand-ui-inconsistency、BUG-0003-brand-image-display-layout-shift、BUG-0004-brand-logo-upload-progress-missing、BUG-0005-login-fails-after-service-restart、BUG-0006-object-storage-upload-not-minio、BUG-0007-brand-logo-not-displayed-after-storage-fix、BUG-0008-object-storage-legacy-upload-residue acceptance.md 及对应 OpenSpec Change
source: AI 根据迭代范围生成，Sprint 结束时由团队填写
update_method: Sprint 验收完成后更新
owner: 产品负责人
status: completed
note: workflow-sync — 30/30 Change 已 archive；0 applied；待人工 sign-off
updated_at: 2026-06-27 15:52:00
---

# Sprint 002 验收报告

## 验收概况

| 字段 | 内容 |
|---|---|
| Sprint | sprint-002 |
| 关联需求 | REQ-0004-admin-home、REQ-0005-user-management、REQ-0005-user-management-list-refine、REQ-0003-login-remember-autofill、REQ-0005-brand-management、REQ-0005-tile-category-management、REQ-0006-tile-sku-management、REQ-0007-tile-category-management-refine、REQ-0008-brand-status-confirm、REQ-0010-product-version-display、REQ-0011-admin-sidebar-expand-collapse |
| 关联 BUG | BUG-0001-tile-category-enable-missing、BUG-0002-brand-ui-inconsistency、BUG-0003-brand-image-display-layout-shift、BUG-0004-brand-logo-upload-progress-missing、BUG-0005-login-fails-after-service-restart、BUG-0006-object-storage-upload-not-minio、BUG-0007-brand-logo-not-displayed-after-storage-fix、BUG-0008-object-storage-legacy-upload-residue、BUG-0009-tile-sku-list-ui-inconsistency、BUG-0011-tile-sku-modal-content-overflow、BUG-0012-tile-sku-modal-form-field-rules、BUG-0014-tile-sku-publish-action-missing、BUG-0015-admin-list-status-tips-layout-shift、BUG-0016-admin-list-status-action-confirm-missing、BUG-0017-user-reset-password-confirm-ui-inconsistency、BUG-0018-tile-sku-modal-video-upload-display、BUG-0019-user-modal-avatar-upload-display、BUG-0020-tile-sku-modal-video-upload-413 |
| 关联 Change | add-admin-home、add-user-management、fix-user-management-list-refine、add-login-remember-autofill、add-brand-management、add-tile-category-management、fix-tile-category-enable-action、fix-tile-category-management-refine、fix-brand-ui-consistency、fix-brand-image-display-layout-shift、fix-brand-logo-upload-progress、fix-object-storage-upload-not-minio、fix-brand-logo-display-after-storage-fix、fix-admin-login-service-restart、fix-brand-status-confirm、fix-object-storage-legacy-upload-residue、add-tile-sku-management、fix-tile-sku-modal-content-overflow、fix-tile-sku-list-ui-inconsistency、add-product-version-display、add-admin-sidebar-collapse、fix-tile-sku-modal-form-field-rules、fix-tile-sku-publish-action-missing、fix-admin-list-status-toast-layout、fix-admin-list-status-action-confirm、fix-user-modal-avatar-upload-display |
| 计划验收日期 | 2026-06-28 |
| 验收结论 | **实现完成，Sprint 已关闭（30/30 Change archived）；细项 AC 待人工勾选 sign-off** |
| 验收人 | _待填写_ |
| 归档日期 | 2026-06-27 16:00:00 |

## 功能验收

> 来源：`issues/requirements/archive/REQ-0004-admin-home/acceptance.md`  
> 状态：**done，已归档（`add-admin-home` archived 2026-06-15 00:00:00）**

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

> 来源：`issues/requirements/archive/REQ-0005-user-management/acceptance.md`  
> 状态：**done，已归档（`add-user-management` archived 2026-06-20 00:00:00）**

### 2.1 访问与权限

- [x] AC-001 ~ AC-005 路由、角色菜单、403/重定向（vitest + API 403）

### 2.2 列表、弹窗与操作

- [x] AC-006 ~ AC-028 筛选、列表、弹窗、重置密码、冻结/删除（实现 + pytest）

### 2.3 布局与视觉

- [x] AC-029 ~ AC-031 Sidebar 激活、布局、HTML v1 结构对照（trace checklist pass）
- [ ] AC-043 ~ AC-045 弹窗 PNG golden、design-system 预览（6.1 可选跳过）

### 2.4 接口与数据

- [x] AC-032 ~ AC-038 Admin Users API、Orval、DB（MinIO 上传由 BUG-0006 修复覆盖）

### 2.5 技术

- [x] AC-039 ~ AC-042 CSS Port、测试覆盖

## REQ-0005-user-management-list-refine 功能验收

> 来源：`issues/requirements/archive/REQ-0005-user-management-list-refine/acceptance.md`  
> 状态：**done，已归档（`fix-user-management-list-refine` archived 2026-06-20 00:00:00）**

### 筛选区与 keyword

- [ ] AC-001 ~ AC-006 无搜索按钮、自动查询、placeholder、keyword 仅 username/display_name

### 列表标题、用户列与分页

- [ ] AC-007 ~ AC-020 section-head/toolbar 移除、用户两行、分页精简

### 回归与技术

- [ ] AC-021 ~ AC-027 弹窗/指标卡/权限无回归；pytest/vitest/build；v2 PNG 并排

## REQ-0003-login-remember-autofill 功能验收

> 来源：`issues/requirements/archive/REQ-0003-login-remember-autofill/acceptance.md`  
> 状态：**done，已归档（`add-login-remember-autofill` archived 2026-06-20 00:00:00）**

### 记住凭证与自动填充

- [x] AC-001 ~ AC-007 本地存储、自动填充、JWT 行为无回归

### 登出与密码显隐

- [x] AC-008 ~ AC-014 登出清除、显隐切换、a11y、CSS Port

### 安全与回归

- [x] AC-015 ~ AC-019 vitest、build、左栏 refine 无回归

## REQ-0005-brand-management 功能验收

> 来源：`issues/requirements/archive/REQ-0005-brand-management/acceptance.md`  
> 状态：**done，已归档（`add-brand-management` archived 2026-06-26 00:00:00）**

### 访问、列表与删除

- [ ] AC-001 ~ AC-016 布局、指标卡、筛选、表格、删除规则、分页

### 弹窗与接口

- [ ] AC-020 ~ AC-029 弹窗字段、校验、Admin Brands API、Orval

### 技术与视觉

- [ ] AC-033 ~ AC-039 CSS Port、测试、HTML 原型并排（PNG 待补）

## BUG-0002 品牌管理 UI 一致性验收

> 来源：`issues/bugs/archive/BUG-0002-brand-ui-inconsistency/acceptance.md`
> 状态：**done，已归档（`fix-brand-ui-consistency` archived 2026-06-27 08:14:56）**

- [x] AC-001 品牌列表分页与用户管理页分页保持一致
- [x] AC-002 品牌分页不再使用割裂的局部视觉结构
- [x] AC-003 品牌 Logo 选择文件控件符合管理端表单风格
- [x] AC-004 Logo 空态、预览态和帮助文案一致
- [x] AC-005 品牌查询、分页、新增/编辑、Logo 上传和保存功能不回退
- [x] AC-006 满足 Design System 约束，无裸 Hex 或未登记局部色值
- [x] AC-007 补充回归测试与验收记录

## BUG-0003 品牌图片显示与提示布局验收

> 来源：`issues/bugs/archive/BUG-0003-brand-image-display-layout-shift/acceptance.md`
> 状态：**done，已归档（`fix-brand-image-display-layout-shift` archived 2026-06-27 08:14:56）**

- [x] AC-001 品牌 Logo 上传后返回可访问 URL
- [x] AC-002 品牌列表正常展示已上传 Logo，加载失败有稳定空态
- [x] AC-003 品牌编辑弹窗正常回显已上传 Logo，更换后即时更新
- [x] AC-004 品牌启用/停用提示不造成页面上下波动
- [x] AC-005 删除、创建、更新等提示不造成页面主体位移
- [x] AC-006 修复符合媒体与对象存储安全规范
- [x] AC-007 品牌查询、分页、新增/编辑、启停、删除等既有功能不回归
- [x] AC-008 测试覆盖图片展示与提示稳定性；必要时同步 OpenAPI 与 Orval
- [x] AC-009 满足 Design System 约束，无裸 Hex 或未登记局部色值

## BUG-0004 品牌 Logo 上传进度反馈验收

> 来源：`issues/bugs/archive/BUG-0004-brand-logo-upload-progress-missing/acceptance.md`
> 状态：**done，已归档（`fix-brand-logo-upload-progress` archived 2026-06-27 08:14:56）**

- [x] AC-001 选择 Logo 后必须触发上传
- [x] AC-002 上传过程中必须展示进度反馈
- [x] AC-003 上传成功后必须更新弹窗预览
- [x] AC-004 上传失败时必须展示错误和重试入口
- [x] AC-005 重新选择同一文件也应可触发上传
- [x] AC-006 修复不得破坏既有品牌管理功能
- [x] AC-007 修复必须符合媒体与安全规范
- [x] AC-008 测试必须覆盖上传进度与预览更新
- [x] AC-009 Design System 约束必须满足

## BUG-0005 服务重启后登录失败验收

> 来源：`issues/bugs/archive/BUG-0005-login-fails-after-service-restart/acceptance.md`
> 状态：**done，已归档（`fix-admin-login-service-restart` archived 2026-06-27 08:14:56）**

- [x] AC-001 首次启动空数据库时默认管理员可登录
- [x] AC-002 服务重启后已有管理员账号仍可按既有密码登录
- [x] AC-003 已存在 admin 且初始密码变化时必须有明确策略
- [x] AC-004 密码恢复不得绕过安全边界
- [x] AC-005 Docker Compose 环境变量说明必须一致
- [x] AC-006 错误提示保持一致但排障信息可定位
- [x] AC-007 必须补充回归测试
- [x] AC-008 不得破坏既有认证能力

## BUG-0006 对象存储上传未写入 MinIO 验收

> 来源：`issues/bugs/archive/BUG-0006-object-storage-upload-not-minio/acceptance.md`
> 状态：**done，已归档（`fix-object-storage-upload-not-minio` archived 2026-06-27 08:14:56）**

- [x] AC-001 上传成功后必须写入 MinIO 单桶
- [x] AC-002 对象 Key 必须使用标准前缀
- [x] AC-003 上传链路必须通过后端授权与校验
- [x] AC-004 上传响应必须保持 API 兼容
- [x] AC-005 媒体读取必须从 MinIO 受控读取
- [x] AC-006 Docker Compose 验证必须覆盖 MinIO
- [x] AC-007 测试必须覆盖对象存储写入
- [x] AC-008 不得破坏既有上传业务
- [x] AC-009 文档与规范必须同步

## BUG-0007 对象存储修复后品牌 Logo 仍不显示验收

> 来源：`issues/bugs/archive/BUG-0007-brand-logo-not-displayed-after-storage-fix/acceptance.md`
> 状态：**done，已归档（`fix-brand-logo-display-after-storage-fix` archived 2026-06-27 08:14:56）**

- [x] AC-001 品牌列表展示 Logo
- [x] AC-002 品牌编辑弹窗回显 Logo
- [x] AC-003 新上传 Logo 可见
- [x] AC-004 MinIO 对象读取闭环
- [x] AC-005 历史数据兼容
- [x] AC-006 回归品牌管理功能
- [x] AC-007 测试覆盖
- [x] AC-008 规范约束

## BUG-0008 对象存储 legacy uploads 双目录残留验收

> 来源：`issues/bugs/archive/BUG-0008-object-storage-legacy-upload-residue/acceptance.md`
> 状态：**done，已归档（`fix-object-storage-legacy-upload-residue` archived 2026-06-27 08:14:56）**

- [x] AC-001 历史 uploads 孤儿文件已清理或纳入脚本
- [x] AC-002 新上传不得再写入 data/uploads
- [x] AC-003 文档澄清 data/minio 与 data/uploads 职责
- [x] AC-004 UPLOAD_DIR 配置与挂载收敛
- [x] AC-005 品牌 Logo 展示无回归
- [x] AC-006 可选一致性检查工具
- [x] AC-007 测试与 CI

## BUG-0011 SKU 弹窗内容溢出验收

> 来源：`issues/bugs/archive/BUG-0011-tile-sku-modal-content-overflow/acceptance.md`  
> 状态：**done，已归档（`fix-tile-sku-modal-content-overflow` archived 2026-06-27 09:37:19）**

- [x] AC-001 弹窗主体 MUST 可垂直滚动
- [x] AC-002 页眉与页脚 MUST 保持可达
- [x] AC-003 全部字段 MUST 可操作
- [x] AC-006 修复范围 MUST 为纯前端布局
- [x] AC-007 Vitest 与 trace 记录

## BUG-0009 SKU 列表 UI 一致性验收

> 来源：`issues/bugs/archive/BUG-0009-tile-sku-list-ui-inconsistency/acceptance.md`  
> 状态：**done，已归档（`fix-tile-sku-list-ui-inconsistency` archived 2026-06-27 10:40:49）**

- [x] AC-001 SKU 列表分页 MUST 与用户管理页结构一致
- [x] AC-002 SKU 分页 MUST NOT 使用废弃 brand 局部结构
- [x] AC-003 表格卡片内 MUST NOT 有重复标题行
- [x] AC-004 分页功能 MUST 保持可用
- [x] AC-005 修复 MUST 对齐 REQ-0006 列表原型
- [x] AC-006～AC-008 纯前端范围、DS 约束、Vitest 与 trace

## BUG-0012 SKU 弹窗字段规则验收

> 来源：`issues/bugs/archive/BUG-0012-tile-sku-modal-form-field-rules/acceptance.md`  
> 状态：**done，已归档（`fix-tile-sku-modal-form-field-rules` archived 2026-06-27 00:00:00）**

- [ ] AC-001 表面工艺 MUST 为非必填
- [ ] AC-003 参考价格 MUST 为必填且新建默认 0
- [ ] AC-004 参考价格空值 MUST 被拦截
- [ ] AC-005 参考价格 0 MUST 合法且正确展示 `¥ 0.00`
- [ ] AC-007 上架 MUST NOT 因表面工艺留空而失败
- [ ] AC-009 后端 schema 与 Orval MUST 对齐
- [ ] AC-010 REQ-0006 文档 MUST 同步 delta
- [ ] AC-011～AC-012 测试补齐且不回退 BUG-0011

## BUG-0015 四列表页 Toast 布局验收

> 来源：`issues/bugs/archive/BUG-0015-admin-list-status-tips-layout-shift/acceptance.md`  
> 状态：**done，已归档（`fix-admin-list-status-toast-layout` archived 2026-06-27 12:59:21）**

- [ ] AC-001 四页 MUST 使用 fixed toast，禁止列表顶文档流 `.admin-notice`
- [ ] AC-002 Tips 出现/消失 MUST NOT 改变主体纵向位置
- [ ] AC-003 四页 toast 视觉与 3200ms 行为一致
- [ ] AC-004 品牌页 MUST NOT 回归 BUG-0003（含 Vitest）
- [ ] AC-005～AC-007 用户/类目/SKU 典型 notice 路径
- [ ] AC-008 共享样式 MUST 在 admin-home.css（或共享组件）
- [ ] AC-010 Vitest 补齐

## BUG-0016 用户/SKU 状态操作 confirm 验收

> 来源：`issues/bugs/archive/BUG-0016-admin-list-status-action-confirm-missing/acceptance.md`  
> 状态：**done，已归档（`fix-admin-list-status-action-confirm` archived 2026-06-27 00:00:00）**

- [x] AC-001～AC-003 用户冻结/解冻 confirm modal 与取消无副作用（Vitest）
- [x] AC-004 用户删除 DS modal（禁止 window.confirm）（Vitest）
- [x] AC-005～AC-007 SKU 上下架/恢复 confirm 与取消（Vitest）
- [x] AC-008 modal 对齐 Golden Reference（类目/品牌）（复用 brand-management.css modal 结构）
- [x] AC-009 品牌/类目/SKU 删除 MUST NOT 回归（Brand/Category Vitest 回归通过）
- [x] AC-010 重置密码 confirm 不在本 BUG scope（→ BUG-0017）
- [x] AC-011 Vitest 确认门禁（User + SKU + Brand + Category 21/21）
- [ ] AC-012～AC-014 纯前端、权限、部署冒烟（归档前 Docker 手工 confirm）

## BUG-0017 用户重置密码 confirm UI 验收

> 来源：`issues/bugs/archive/BUG-0017-user-reset-password-confirm-ui-inconsistency/acceptance.md`  
> 状态：**done，已归档（`fix-user-reset-password-confirm-ui` archived 2026-06-27 00:00:00）**

- [x] AC-001 重置密码 MUST 二次确认后再调 API（Vitest）
- [x] AC-002 MUST 禁止 `window.confirm`（Vitest spy）
- [x] AC-003 confirm modal 可取消且无副作用
- [x] AC-004 modal 视觉对齐 Golden Reference（类目启停 / 同页冻结 confirm）
- [x] AC-005 成功后 `ResetPasswordDialog` MUST NOT 回归
- [x] AC-006～AC-007 同页冻结/删除与品牌/类目启停 MUST NOT 回归（Vitest 17/17）
- [x] AC-008 Vitest 重置密码 confirm 门禁
- [x] AC-009 纯前端范围；AC-010 已删除用户按钮状态不回归
- [ ] Docker 手工冒烟（archive 前）

## BUG-0019 用户头像上传与回显验收

> 来源：`issues/bugs/archive/BUG-0019-user-modal-avatar-upload-display/acceptance.md`  
> 状态：**done，已归档（`fix-user-modal-avatar-upload-display` archived 2026-06-27 00:00:00）**

- [ ] AC-001 API 返回可访问 `avatar_url`
- [ ] AC-002 编辑弹窗回显已有头像
- [ ] AC-003～AC-006 上传触发、进度状态机、预览更新、失败重试
- [ ] AC-007～AC-008 列表头像与保存后一致
- [ ] AC-009～AC-012 回归、安全、测试、DS

## BUG-0018 SKU 弹窗商品视频上传即时回显验收

> 来源：`issues/bugs/archive/BUG-0018-tile-sku-modal-video-upload-display/acceptance.md`  
> 状态：**done，已归档（`fix-tile-sku-modal-video-upload-display` archived 2026-06-27 00:00:00）**

- [ ] AC-001 选择 MP4 后触发 `POST /api/v1/admin/uploads/tile-videos`
- [ ] AC-002 上传中展示可感知状态（idle → uploading → uploaded/failed）
- [ ] AC-003 上传成功后同一弹窗会话内即时出现文件卡片（核心）
- [ ] AC-004 失败时在视频区内展示错误（非仅顶部 notice）
- [ ] AC-005 支持继续添加多个视频
- [ ] AC-006 不回归 BUG-0011 滚动与 SKU 图片上传
- [ ] AC-007 Vitest mock 上传成功/失败
- [ ] AC-008 REQ-0006 AC-035 即时回显 + 上传状态对齐

## BUG-0020 SKU 弹窗视频上传 413 验收

> 来源：`issues/bugs/archive/BUG-0020-tile-sku-modal-video-upload-413/acceptance.md`  
> 状态：**done，已归档（`fix-tile-sku-modal-video-upload-413` archived 2026-06-27 00:00:00）**

- [ ] AC-001 Docker 路径 2MB～50MB MP4 经 `localhost:3000` 返回 200（非 413）
- [ ] AC-002 Nginx `client_max_body_size` ≥ `max(MAX_IMAGE_SIZE_MB, MAX_VIDEO_SIZE_MB)`
- [ ] AC-003 图片上传受 `MAX_IMAGE_SIZE_MB` / `ALLOWED_IMAGE_TYPES` 约束
- [ ] AC-004 视频上传受 `MAX_VIDEO_SIZE_MB` / `ALLOWED_VIDEO_TYPES` 约束
- [ ] AC-005 `.env.example` 与 Docker 后端 env 四类变量同步
- [ ] AC-006 小文件与其它上传端点无回归
- [ ] AC-007 pytest + Change trace Docker 大 MP4 手工验收（重建 Web 镜像）
- [ ] AC-008 REQ-0006 AC-035 Docker 路径可上传多个 MP4

## REQ-0008-brand-status-confirm 功能验收

> 来源：`issues/requirements/archive/REQ-0008-brand-status-confirm/acceptance.md`
> 状态：**done，已归档（`fix-brand-status-confirm` archived 2026-06-26 00:00:00）**

### 启停二次确认

- [x] AC-001 ~ AC-010 与 REQ-0008 §1 一致（vitest 覆盖启停确认流程）

### 无障碍、回归与自动化

- [x] AC-011 ~ AC-021 vitest 5/5 + build 通过
- [x] AC-023 OpenSpec archive 完成；web-client spec 已合并「品牌列表启停二次确认」
- [ ] AC-022 可选 PNG golden reference（非阻塞）

## REQ-0005-tile-category-management 功能验收

> 来源：`issues/requirements/archive/REQ-0005-tile-category-management/acceptance.md`  
> 状态：**done，已归档（`add-tile-category-management` archived 2026-06-20 00:00:00）**

### 访问、类目树与删除

- [ ] AC-001 ~ AC-019 布局、指标卡、检索、类目树联动、列表、删除规则、分页

### 弹窗与接口

- [ ] AC-023 ~ AC-033 弹窗字段、层级约束、Admin Tile Categories API、Orval

### 技术与视觉

- [ ] AC-037 ~ AC-043 CSS Port、测试、HTML 原型并排（PNG 待补）

## REQ-0006-tile-sku-management 功能验收

> 来源：`issues/requirements/archive/REQ-0006-tile-sku-management/acceptance.md`  
> 状态：**done，已归档（`add-tile-sku-management` archived 2026-06-27 00:00:00）**

### 访问、列表与筛选

- [x] AC-001 ~ AC-021 布局、指标卡、五维筛选、表格列、价格格式、分页（页码 UI 简化，见 trace §12 partial）

### 弹窗、媒体与上下架

- [x] AC-022 ~ AC-039 880px 弹窗、多图主图、多视频、save_mode、publish/unpublish、删除规则

### 接口、数据与技术

- [x] AC-042 ~ AC-053 Admin Tile SKU API、schema 扩展、Orval、测试（10 pytest passed）

### 视觉

- [x] AC-054 ~ AC-056 HTML 原型结构对照（trace.md checklist）；PNG 已复制至 `prototype/images/`（可选 golden）

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
- [x] 头像上传经 MinIO 授权链路（由 BUG-0006 修复覆盖）

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
- [x] Logo 上传经 MinIO 授权链路（由 BUG-0006 修复覆盖）

### BUG-0002-brand-ui-inconsistency

- [x] 无 API / DB / Orval / MinIO 策略变更
- [x] 品牌管理页分页与用户管理页分页并排验收
- [x] 品牌 Logo 控件与用户头像上传控件并排验收

### BUG-0003-brand-image-display-layout-shift

- [x] 品牌 Logo 上传 URL 可被浏览器加载
- [x] 品牌列表与编辑弹窗 Logo 展示/回显正常
- [x] 品牌状态提示不推挤页面主体
- [x] 媒体访问策略符合 MinIO 单桶与后端授权规范

### BUG-0004-brand-logo-upload-progress-missing

- [x] 更换 Logo 后触发上传并展示进度反馈
- [x] 上传成功后弹窗预览更新，保存后回显最新 Logo
- [x] 上传失败展示错误与重试入口
- [x] 同文件重选可重试

### BUG-0006-object-storage-upload-not-minio

- [x] 上传后对象写入 `MINIO_BUCKET=tile-info-platform`
- [x] 图片与视频对象使用标准前缀（`original/`、`videos/`、`videos/covers/`）
- [x] `/media/{object_key}` 或等价 URL 可受控读取 MinIO 对象
- [x] Docker Compose 环境可完成上传到 MinIO 的闭环验证

### REQ-0005-tile-category-management

- [ ] Admin Tile Categories CRUD + tree API 可用
- [ ] `tile_categories` 表扩展迁移已应用
- [ ] Orval 客户端已重新生成

### REQ-0006-tile-sku-management

- [x] Admin Tile SKU CRUD + publish/unpublish API 可用（`test_admin_tile_skus.py` 10 passed）
- [x] `tiles` 表扩展 + `tile_videos` 迁移已应用
- [x] Orval 客户端已重新生成
- [x] 图片/视频上传 API 端点（MinIO 完整链路由 BUG-0006 修复覆盖）

## 测试验收

- [x] `npx vitest run src/features/admin src/pages/admin` — 8 passed
- [x] `cd src/web && ./node_modules/.bin/vitest run src/features/admin/components/BrandFormModal.test.tsx src/pages/admin/BrandManagementPage.test.tsx` — 7 passed
- [x] `cd src/web && ./node_modules/.bin/vite build` — success（存在既有 Tailwind at-rule minify warning）
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
| §9 归档准备 | 1 | 1 | ✓ archived 2026-06-15 |
| **add-admin-home 合计** | **25** | **25** | **100%** |

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
| §10 文档与归档 | 4 | 4 | ✓ archived 2026-06-26（10.3 PNG 可选跳过） |

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
| §8 HTML 视觉 gate | 4 | 4 | trace checklist pass（2 partial 已记录）；PNG 已复制至 `prototype/images/` |
| §9 文档 | 3 | 3 | ✓ |
| §9.4 archive | 1 | 0 | 待 `/opsx-archive` |

### fix-tile-category-management-refine（REQ-0007）

| 任务组 | 总数 | 完成 | 状态 |
|---|---|---|---|
| §1 启停确认 | 3 | 3 | ✓ 完成 |
| §2 布局精简 | 3 | 3 | ✓ 完成 |
| §3 分页 v2 | 3 | 3 | ✓ 完成 |
| §4 测试 | 5 | 5 | ✓ vitest + build pass |
| §5 冒烟与视觉 | 3 | 2 | 5.3 PNG 可选跳过 |
| §6 追溯与归档 | 2 | 2 | ✓ archived 2026-06-22 |

### fix-tile-category-enable-action（BUG-0001）

| 任务组 | 总数 | 完成 | 状态 |
|---|---|---|---|
| §1 前端修复 | 2 | 2 | 完成 |
| §2 测试 | 3 | 3 | 完成 |
| §3 冒烟 | 2 | 2 | 完成 |
| §4 追溯与归档 | 3 | 3 | 已 archive（--skip-specs） |

### fix-brand-logo-upload-progress（BUG-0004）

| 任务组 | 总数 | 完成 | 状态 |
|---|---|---|---|
| §1 准备与门禁 | 4 | 4 | 完成 |
| §2 Web 上传状态与进度反馈 | 5 | 5 | 完成 |
| §3 预览、失败与重试 | 5 | 5 | 完成 |
| §4 API 封装与兼容性 | 4 | 4 | 完成；无 schema / DB 变更 |
| §5 测试 | 7 | 7 | Vitest 7 passed；Web build success |
| §6 验收与追溯 | 5 | 5 | ✓ archived 2026-06-26 |

### fix-brand-status-confirm（REQ-0008）

| 任务组 | 总数 | 完成 | 状态 |
|---|---|---|---|
| §1 启停确认弹窗 | 4 | 4 | ✓ archived 2026-06-26 |
| §2 测试与归档 | 2 | 2 | ✓ archived |

### fix-object-storage-upload-not-minio（BUG-0006）

> 已完成 OpenSpec Change apply 与 archive，正式 spec 已同步。

| 任务组 | 总数 | 完成 | 状态 |
|---|---|---|---|
| §1 准备与门禁 | 5 | 5 | 完成 |
| §2 MinIO 存储适配 | 6 | 6 | 完成 |
| §3 受控读取 / URL 策略 | 5 | 5 | 完成 |
| §4 API、配置与文档同步 | 6 | 6 | 完成 |
| §5 测试 | 7 | 7 | 完成 |
| §6 验收与追溯 | 5 | 5 | 完成 |

### fix-admin-login-service-restart（BUG-0005）

| 任务组 | 总数 | 完成 | 状态 |
|---|---|---|---|
| §1 准备与门禁 | 4 | 4 | 完成 |
| §2 后端初始化与恢复策略 | 6 | 6 | 完成 |
| §3 环境变量与文档 | 5 | 5 | 完成；无 API schema 变更，无需 Orval |
| §4 测试 | 6 | 6 | pytest 30 passed；ruff passed |
| §5 验收与追溯 | 4 | 4 | ✓ archived 2026-06-26 |

## REQ-0010-product-version-display 功能验收

> 来源：`issues/requirements/archive/REQ-0010-product-version-display/acceptance.md`  
> 状态：**done，已归档（`add-product-version-display` archived 2026-06-27 00:00:00）**

### 10.1 版本维护

- [ ] AC-001 ~ AC-003 `src/shared/` 单一常量；发版 checklist

### 10.2 管理端 / 店主端展示

- [ ] AC-004 ~ AC-012 双端侧边栏 brand-head + 同一版本值

### 10.3 视觉、测试与流程

- [ ] AC-013 ~ AC-023 semantic token、vitest、build、OpenSpec archive

## REQ-0011-admin-sidebar-expand-collapse 功能验收

> 来源：`issues/requirements/archive/REQ-0011-admin-sidebar-expand-collapse/acceptance.md`  
> 状态：**done，已归档（`add-admin-sidebar-collapse` archived 2026-06-27 00:00:00）**

### 11.1 折叠状态与持久化

- [ ] AC-001 ~ AC-003 expanded/collapsed 双态；localStorage；AdminLayout 统一管理

### 11.2 宽度、Chevron 与 collapsed 裁剪

- [ ] AC-004 ~ AC-017 264/72px、chevron、`aria-*`、collapsed 隐藏/保留项

### 11.3 回归、测试与视觉

- [ ] AC-018 ~ AC-023 nav 回归、≤1023px 不变、vitest、HTML 原型并排

## 问题清单

| 编号 | 描述 | 严重程度 | 状态 |
|---|---|---|---|
| I-01 | BUG-0001 类目停用行无「启用」按钮 | high | 已修复并 archive |
| I-02 | REQ-0007 类目页 UI refine | medium | **已 archive** `fix-tile-category-management-refine`（2026-06-22） |
| I-03 | BUG-0004 品牌 Logo 更换缺少上传进度与预览更新 | medium | **已 archive** `fix-brand-logo-upload-progress`（2026-06-26） |
| I-04 | BUG-0005 服务重启后正确账号密码无法登录 | high | **已 archive** `fix-admin-login-service-restart`（2026-06-26） |
| I-05 | BUG-0006 上传链路未写入 MinIO 对象存储 | high | 已完成 `fix-object-storage-upload-not-minio` archive |
| I-06 | BUG-0007 对象存储修复后品牌 Logo 仍不显示 | high | 已完成 `fix-brand-logo-display-after-storage-fix` archive |
| I-07 | REQ-0008 品牌启停二次确认 | medium | 已 archive `2026-06-26-fix-brand-status-confirm` |
| I-08 | BUG-0008 legacy uploads 双目录残留 | medium | 已完成 `fix-object-storage-legacy-upload-residue` archive |

## 遗留风险

| 编号 | 描述 | 优先级 | 状态 |
|---|---|---|---|
| L-01 | PNG 视觉 sign-off | P0 | 待关闭 |
| L-02 | `add-admin-home` 归档 | P0 | **archived** 2026-06-15 |
| L-03 | REQ-0001 退出入口文档同步 | P1 | 待确认 |
| L-04 | `add-user-management` 实现与归档 | P0 | **archived** 2026-06-20 |
| L-05 | 用户管理 list/modal PNG sign-off | P0 | 待关闭 |
| L-05b | fix-user-management-list-refine 实现与 v2 PNG sign-off | P1 | **archived**；主 spec 仍为 v1 baseline，v2 MODIFIED 待合入 |
| L-06 | add-login-remember-autofill 实现与归档 | P1 | **archived** 2026-06-20 |
| L-07 | add-brand-management 实现与归档 | P0 | **archived** 2026-06-26 |
| L-08 | 品牌管理 HTML/PNG sign-off | P1 | HTML trace pass；PNG 可选 |
| L-09 | add-tile-category-management 实现与归档 | P0 | **archived** 2026-06-20；specs synced |
| L-10 | 类目管理 HTML/PNG sign-off | P1 | HTML trace pass；PNG 待补 |
| L-11 | add-tile-sku-management 实现与归档 | P0 | **34/35 apply 完成**；待 `/opsx-archive` |
| L-12 | SKU 管理 HTML/PNG sign-off | P1 | HTML trace pass；PNG 可选 |
| L-13 | Sprint-002 容量超支（69 人天 / 2 周） | P1 | 监控；含 REQ-0007 +2 人天、BUG-0002 +2 人天、BUG-0006 +3 人天、BUG-0007 +2 人天 |
| L-14 | BUG-0001 类目启用 UI 缺陷 | P0 | 已修复并 archive |
| L-15 | fix-tile-category-management-refine 实现与归档 | P1 | **archived** 2026-06-22 |
| L-16 | BUG-0004 品牌 Logo 上传进度反馈修复 | P1 | **archived** 2026-06-26 |
| L-17 | BUG-0005 服务重启后登录失败修复 | P1 | **archived** 2026-06-26 |
| L-18 | BUG-0006 对象存储上传未写入 MinIO 修复 | P1 | **archived** 2026-06-26 14:20:50 |
| L-19 | BUG-0007 对象存储修复后品牌 Logo 仍不显示修复 | P1 | **archived** 2026-06-26 20:21:43 |
| L-20 | fix-brand-status-confirm 实现与归档 | P1 | **archived** 2026-06-26 21:24:30 |
| L-21 | add-product-version-display 实现与归档 | P2 | applied 17/17；待 `/opsx-archive` |
| L-22 | add-admin-sidebar-collapse 实现与归档 | P1 | proposed；依赖 REQ-0010 brand-head |

## 验收结论

- **结论**：_待 Sprint 结束填写_
- **日期**：_
- **备注**：_
