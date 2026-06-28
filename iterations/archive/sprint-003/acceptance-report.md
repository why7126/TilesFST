---
created_at: 2026-06-28 10:03:15
updated_at: 2026-06-28 19:40:42
title: Sprint 003 验收报告
purpose: 记录 Sprint 003 验收结果与遗留项（模板）
content: 基于 REQ-0014、REQ-0015、REQ-0009、REQ-0012、REQ-0016、REQ-0017、BUG-0021～0029、BUG-0030～0041、BUG-0042～0047、BUG-0048 acceptance.md
source: AI 根据迭代范围生成，Sprint 结束时由团队填写
update_method: Sprint 验收完成后更新
owner: 产品负责人
status: completed
note: workflow-sync — 23/23 Change 已 archive；0 applied；待人工 sign-off
---

# Sprint 003 验收报告

## 验收概况

| 字段 | 内容 |
|---|---|
| Sprint | sprint-003 |
| 关联需求 | REQ-0014-profile-page、REQ-0015-password-change、REQ-0009-tile-spec-management、REQ-0012-object-storage-key-layout、REQ-0016-banner-management、REQ-0017-system-settings |
| 关联 BUG | BUG-0021-sidebar-menu-icons-indistinguishable、BUG-0022-profile-basic-info-redundant-role-status、BUG-0023-profile-duplicate-save-buttons、BUG-0024-change-password-error-wrong-field、BUG-0025-change-password-toggle-button-misalignment、BUG-0026-change-password-cancel-confirm-redundant、BUG-0027-tile-spec-list-ui-inconsistency、BUG-0028-tile-spec-modal-form-layout、BUG-0029-tile-spec-list-not-refresh-after-create、BUG-0030-banner-list-ui-inconsistency、BUG-0031-banner-modal-image-section-label、BUG-0032-banner-modal-upload-button-label、BUG-0033-banner-modal-form-layout-overflow、BUG-0034-banner-modal-link-selector-combined、BUG-0035-banner-modal-sku-hero-image-no-effect、BUG-0036-banner-modal-datetime-picker、BUG-0037-tile-spec-status-confirm-ui-inconsistency、BUG-0038-tile-sku-modal-spec-hint-styling、BUG-0039-banner-list-display-position-column、BUG-0040-banner-modal-width-too-narrow、BUG-0041-sidebar-user-menu-avatar-missing、BUG-0042-system-settings-page-title-v2-suffix、BUG-0043-system-settings-duplicate-save-buttons、BUG-0045-system-settings-media-format-options-limited、BUG-0046-system-settings-reset-confirm-ui-inconsistency、BUG-0047-system-settings-save-tip-layout-shift、BUG-0048-banner-modal-width-css-cascade-overridden |
| 关联 Change | add-admin-profile-page、add-admin-password-change、add-tile-spec-management、update-object-storage-key-layout、add-banner-management、fix-banner-admin-ui、add-system-settings、fix-sidebar-menu-icons-indistinguishable、fix-profile-basic-info-redundant-role-status、fix-profile-duplicate-save-buttons、fix-change-password-modal-errors、fix-tile-spec-admin-ui、fix-tile-spec-status-confirm-ui、fix-tile-sku-modal-spec-hint-styling、fix-banner-list-and-modal-ui、fix-sidebar-user-menu-avatar、fix-banner-modal-width-css-cascade、fix-profile-activities-display-limit、fix-system-settings-page-title-v2-suffix、fix-system-settings-duplicate-save-buttons、fix-system-settings-media-format-options、fix-system-settings-reset-confirm-ui、fix-system-settings-save-tip-layout-shift |
| 计划验收日期 | 2026-07-12 18:00:00 |
| 验收结论 | **实现完成，Sprint 已关闭（23/23 Change archived）；细项 AC 待人工勾选 sign-off** |
| 验收人 | _待填写_ |
| 归档日期 | 2026-06-28 19:39:54 |

## REQ-0014 功能验收

> 来源：`issues/requirements/archive/REQ-0014-profile-page/acceptance.md`  
> 状态：**done，已归档（`add-admin-profile-page` archived 2026-06-28 12:15:00）**

### 1. 访问与导航（AC-001～AC-005）

- [ ] AC-001～AC-005 路由、菜单、页头

### 2. 布局与视觉（AC-006～AC-009）

- [ ] AC-006～AC-009 PNG 并排、semantic token

### 3. 表单 / 头像 / 侧栏卡片（AC-010～AC-028）

- [ ] AC-010～AC-028 见 acceptance.md

### 4. 接口与数据（AC-029～AC-035）

- [ ] AC-029～AC-035 API、migration、audit

## REQ-0014 v1.1 功能验收（操作记录 limit 5）

> 来源：`issues/requirements/archive/REQ-0014-profile-page/acceptance.md` AC-024（v1.1）  
> 状态：**done，已归档（`fix-profile-activities-display-limit` archived 2026-06-28）**

- [ ] AC-024 activities API / timeline **最多 5** 条；不足 5 时展示实际条数
- [ ] 审计写入（login / profile_update / avatar_update）无回归

## REQ-0015 功能验收

> 来源：`issues/requirements/archive/REQ-0015-password-change/acceptance.md`  
> 状态：**done，已归档（`add-admin-password-change` archived 2026-06-28 12:52:00）**

### 1. 入口与弹窗（AC-001～AC-009）

- [ ] AC-001～AC-009 侧栏 + profile 页入口、弹窗 UI

### 2. 校验 / API / Token（AC-010～AC-026）

- [ ] AC-010～AC-026 见 acceptance.md

## REQ-0009 功能验收

> 来源：`issues/requirements/archive/REQ-0009-tile-spec-management/acceptance.md`  
> 状态：**done，已归档（`add-tile-spec-management` archived 2026-06-28 13:30:00）**

### 1. 规格管理页（AC-001～AC-025）

- [x] AC-001～AC-025 导航、列表、启停、删除、弹窗、分页（pytest/vitest + Docker 冒烟）

### 2. SKU 联动（AC-026～AC-031）

- [x] AC-026～AC-031 规格下拉、spec_id、上架校验

### 3. 迁移与 API（AC-032～AC-044）

- [x] AC-032～AC-044 migration、API、pytest、RBAC

### 4. 视觉（AC-045～AC-047）

- [x] AC-045～AC-047 HTML gate（`tile-spec-visual-checklist.test.ts` 12/12）；PNG Golden 见 prototype/web

## REQ-0012 功能验收

> 来源：`issues/requirements/archive/REQ-0012-object-storage-key-layout/acceptance.md`  
> 状态：**done，已归档（`update-object-storage-key-layout` archived 2026-06-28 10:32:00）**

### 1. Key 形态与前缀（AC-001～AC-008）

- [x] AC-001～AC-008 build_object_key、images/videos 前缀、deprecated original/

### 2. resource_type 映射（AC-009～AC-014）

- [x] AC-009～AC-014 头像/Logo/SKU 图视频 Key 形态、四上传 API 响应

### 3. 读取与安全（AC-015～AC-017）

- [x] AC-015～AC-017 /media 读取、路径校验、单桶策略

### 4. 存量迁移（AC-018～AC-022）

- [x] AC-018～AC-022 migrate_object_keys.py dry-run/apply、DB 与 MinIO 一致、无 404

### 5. 文档与测试（AC-023～AC-034）

- [x] AC-023～AC-034 规范文档、pytest、Docker 冒烟、OpenSpec archive

## BUG-0021 功能验收

> 来源：`issues/bugs/archive/BUG-0021-sidebar-menu-icons-indistinguishable/acceptance.md`  
> 状态：**in_sprint**

### 1. 语义图标（AC-001～AC-003）

- [x] AC-001 各菜单独立 Lucide 语义图标
- [x] AC-002 collapsed 态可仅凭图标识别并正确导航
- [x] AC-003 expanded 态图标与文案并存无布局回归

### 2. 角色 / a11y / 回归（AC-004～AC-008）

- [x] AC-004～AC-010 semantic token、a11y、角色过滤、REQ-0011 回归、vitest

## BUG-0022 功能验收

> 来源：`issues/bugs/archive/BUG-0022-profile-basic-info-redundant-role-status/acceptance.md`  
> 状态：**done，已归档（`fix-profile-basic-info-redundant-role-status` archived 2026-06-28 13:40:00）**

### 1. 表单去重（AC-001～AC-005）

- [ ] AC-001 表单 grid 无 role/status input；字段顺序正确
- [ ] AC-002 账号安全卡片仍展示 role/status badge
- [ ] AC-003～AC-005 PATCH/校验无回归；REQ AC-011 / prototype 对齐

### 2. 回归与测试（AC-006～AC-009）

- [ ] AC-006～AC-007 纯前端范围；无 API/DB 变更
- [ ] AC-008 vitest ProfilePage 通过
- [ ] AC-009 1440×1024 与 profile-page.html 并排验收

## BUG-0023 功能验收

> 来源：`issues/bugs/archive/BUG-0023-profile-duplicate-save-buttons/acceptance.md`  
> 状态：**done，已归档（`fix-profile-duplicate-save-buttons` archived 2026-06-28 13:40:00）**

### 1. 单 CTA（AC-001～AC-006）

- [ ] AC-001 全页仅一处「保存修改」；页头无重复按钮
- [ ] AC-002 保留按钮位于表单 actions 区
- [ ] AC-003～AC-006 保存/重置/disabled、页头 layout、semantic token

### 2. 回归与测试（AC-007～AC-011）

- [ ] AC-007～AC-008 REQ-0014 其他能力无回归；纯前端范围
- [ ] AC-009 vitest 单按钮断言
- [ ] AC-010～AC-011 视觉验收与 AC-017 delta

## BUG-0024 功能验收

> 来源：`issues/bugs/archive/BUG-0024-change-password-error-wrong-field/acceptance.md`  
> 状态：**done，已归档（`fix-change-password-modal-errors` archived 2026-06-28 15:16:00）**

### 1. 错误字段位置（AC-001～AC-004）

- [ ] AC-001 新密码客户端校验错误在新密码字段下
- [ ] AC-002 新密码与原密码相同错误在新密码字段下
- [ ] AC-003 服务端「过于常见」错误在新密码字段下
- [ ] AC-004 原密码不正确仍在原密码字段下

### 2. 回归与测试（AC-005～AC-010）

- [ ] AC-005 确认新密码不一致无回归
- [ ] AC-006 错误 input 样式
- [ ] AC-007 成功改密流程无回归
- [ ] AC-008 纯前端范围
- [ ] AC-009 vitest ChangePasswordModal 字段位置断言
- [ ] AC-010 常见密码失败截图场景视觉验收

## BUG-0025 功能验收

> 来源：`issues/bugs/archive/BUG-0025-change-password-toggle-button-misalignment/acceptance.md`  
> 状态：**done，已归档（`fix-change-password-modal-errors` archived 2026-06-28 15:16:00）**

### 1. Toggle 垂直居中（AC-001～AC-004）

- [ ] AC-001 原密码字段有 error 时 toggle 相对 input 居中
- [ ] AC-002 确认新密码不一致时 toggle 相对 input 居中
- [ ] AC-003 新密码字段有 error 时 toggle 居中（BUG-0024 修复后）
- [ ] AC-004 无 error 时 toggle 位置无回归

### 2. 功能与结构（AC-005～AC-010）

- [ ] AC-005 显示/隐藏功能无回归
- [ ] AC-006 error-text 不参与 toggle 定位
- [ ] AC-007 BUG-0024/0026 无回归
- [ ] AC-008 纯前端范围
- [ ] AC-009 vitest DOM/结构断言
- [ ] AC-010 与 `change-password-toggle-misalignment.png` 并排视觉验收

## BUG-0026 功能验收

> 来源：`issues/bugs/archive/BUG-0026-change-password-cancel-confirm-redundant/acceptance.md`  
> 状态：**done，已归档（`fix-change-password-modal-errors` archived 2026-06-28 15:16:00）**

### 1. 关闭无二次确认（AC-001～AC-004）

- [ ] AC-001 footer「取消」有输入时直接关闭，无 `window.confirm`
- [ ] AC-002 × / Esc / 遮罩关闭同样无 confirm
- [ ] AC-003 空表单关闭无回归
- [ ] AC-004 再次打开表单重置为空

### 2. 无回归与 spec（AC-005～AC-011）

- [ ] AC-005 成功改密流程无回归
- [ ] AC-006 客户端校验（确认不一致）无回归
- [ ] AC-007 与管理端其它表单弹窗行为一致
- [ ] AC-008 vitest 更新并通过
- [ ] AC-009 OpenSpec / REQ-0015 delta 同步
- [ ] AC-010 纯前端范围
- [ ] AC-011 与 `change-password-cancel-browser-confirm.png` 场景视觉验收

## BUG-0027 功能验收

> 来源：`issues/bugs/archive/BUG-0027-tile-spec-list-ui-inconsistency/acceptance.md`  
> 状态：**done，已归档（`fix-tile-spec-admin-ui` archived 2026-06-28 15:28:00）**

### 1. 列表分页与字号（AC-001～AC-009）

- [ ] AC-001 分页 DOM 与用户管理页一致
- [ ] AC-002 无 `pagination-bar` / `page-indicator`
- [ ] AC-003 尺寸名称列字号协调
- [ ] AC-004～AC-009 分页功能、纯前端、vitest、AC-042 对齐

## BUG-0028 功能验收

> 来源：`issues/bugs/archive/BUG-0028-tile-spec-modal-form-layout/acceptance.md`  
> 状态：**done，已归档（`fix-tile-spec-admin-ui` archived 2026-06-28 15:28:00）**

### 1. 弹窗布局（AC-001～AC-011）

- [ ] AC-001 字段顺序：宽/长 → 尺寸名称 → 厚度/排序 → 备注
- [ ] AC-002 只读 preview 保持 `{w}×{l}mm`
- [ ] AC-003 备注 textarea 整行 + 固定高度
- [ ] AC-004～AC-009 禁止字段、720px grid、CRUD 无回归、AC-046 并排
- [ ] AC-010 宽长冲突提示（可选，可延后）
- [ ] AC-011 vitest 字段顺序

## BUG-0029 功能验收

> 来源：`issues/bugs/archive/BUG-0029-tile-spec-list-not-refresh-after-create/acceptance.md`  
> 状态：**done，已归档（`fix-tile-spec-admin-ui` archived 2026-06-28 15:28:00）**

### 1. 保存后刷新（AC-001～AC-009）

- [ ] AC-001 新增保存后列表自动出现新记录
- [ ] AC-002 编辑保存后行内数据更新
- [ ] AC-003 summary 指标卡同步
- [ ] AC-004 onSuccess 含 `loadSpecs()`
- [ ] AC-005～AC-006 启停/删除/筛选无回归
- [ ] AC-007～AC-008 纯前端 + vitest

## BUG-0030 功能验收

> 来源：`issues/bugs/archive/BUG-0030-banner-list-ui-inconsistency/acceptance.md`  
> 状态：**done，已归档（`fix-banner-admin-ui` archived 2026-06-28 16:35:00）**

- [ ] 列表无 section-head / table-toolbar；标准 pagination DOM

## BUG-0031 功能验收

> 来源：`issues/bugs/archive/BUG-0031-banner-modal-image-section-label/acceptance.md`  
> 状态：**done，已归档（`fix-banner-admin-ui` archived 2026-06-28 16:35:00）**

- [ ] 图片 upload 区无 `.banner-upload-title` 冗余首行

## BUG-0032 功能验收

> 来源：`issues/bugs/archive/BUG-0032-banner-modal-upload-button-label/acceptance.md`  
> 状态：**done，已归档（`fix-banner-admin-ui` archived 2026-06-28 16:35:00）**

### 1. 上传按钮文案与隐藏（AC-001～AC-010）

- [ ] AC-001 未选图时按钮为「选择」
- [ ] AC-002 已有图时按钮为「更换」
- [ ] AC-003 上传中「上传中」且不可重复触发
- [ ] AC-004 file input 使用 `hidden`，无「浏览…」
- [ ] AC-005 自定义上传功能无回归（AC-032/AC-045）
- [ ] AC-006 重复选择同一文件可再次上传
- [ ] AC-007 与 BrandFormModal 结构一致
- [ ] AC-008 纯前端范围
- [ ] AC-009 Vitest 覆盖按钮文案
- [ ] AC-010 视觉并排验收（可选）

## BUG-0033 功能验收

> 来源：`issues/bugs/archive/BUG-0033-banner-modal-form-layout-overflow/acceptance.md`  
> 状态：**done，已归档（`fix-banner-admin-ui` archived 2026-06-28 16:35:00）**

- [ ] 弹窗 scroll；备注 textarea 100% 宽；底部按钮可见

## BUG-0034 功能验收

> 来源：`issues/bugs/archive/BUG-0034-banner-modal-link-selector-combined/acceptance.md`  
> 状态：**done，已归档（`fix-banner-admin-ui` archived 2026-06-28 16:35:00）**

- [ ] SKU/专题单控件 Combobox；搜索与选择合一

## BUG-0035 功能验收

> 来源：`issues/bugs/archive/BUG-0035-banner-modal-sku-hero-image-no-effect/acceptance.md`  
> 状态：**done，已归档（`fix-banner-admin-ui` archived 2026-06-28 16:35:00）**

- [ ] 「使用 SKU 主图」回填预览与 imageKey

## BUG-0036 功能验收

> 来源：`issues/bugs/archive/BUG-0036-banner-modal-datetime-picker/acceptance.md`  
> 状态：**done，已归档（`fix-banner-admin-ui` archived 2026-06-28 16:35:00）**

- [ ] 有效期区间控件；精确起止时间可选

## BUG-0037 功能验收

> 来源：`issues/bugs/archive/BUG-0037-tile-spec-status-confirm-ui-inconsistency/acceptance.md`  
> 状态：**done，已归档（`fix-tile-spec-status-confirm-ui` archived 2026-06-28 16:48:07）**

### 1. 启停/删除 confirm 对齐（AC-001～AC-011）

- [ ] AC-001 停用 confirm 文案/按钮/确认前不调 API
- [ ] AC-002 启用 confirm 对齐类目页
- [ ] AC-003 删除 confirm 对齐类目页（无 danger 变体）
- [ ] AC-004 取消/×/遮罩无副作用
- [ ] AC-005 modal 结构与 Golden Reference 并排
- [ ] AC-006～AC-007 0027/28/29 与类目/品牌 confirm 无回归
- [ ] AC-008 Vitest 停用 confirm 门禁
- [ ] AC-009～AC-010 纯前端 + REQ-0009 AC-013/AC-018

## BUG-0038 功能验收

> 来源：`issues/bugs/archive/BUG-0038-tile-sku-modal-spec-hint-styling/acceptance.md`  
> 状态：**done，已归档（`fix-tile-sku-modal-spec-hint-styling` archived 2026-06-28 17:20:00）**

### 1. 规格未匹配提示样式（AC-001～AC-006）

- [ ] AC-001 提示使用 `form-help`，非 `form-hint`
- [ ] AC-002 Typography 11px `--admin-weak`
- [ ] AC-003 文案与显隐逻辑不变
- [ ] AC-004 非触发场景不误展示
- [ ] AC-005 不回退 BUG-0010/0011/0012
- [ ] AC-006 Vitest 覆盖 `spec_id: null` 编辑模式

## BUG-0039 功能验收

> 来源：`issues/bugs/archive/BUG-0039-banner-list-display-position-column/acceptance.md`  
> 状态：**done，已归档（`fix-banner-list-and-modal-ui` archived 2026-06-28 18:57:34）**

### 1. 列表展示位置列（AC-001～AC-008）

- [ ] AC-001 第一列仅 Banner 标题
- [ ] AC-002 独立「展示位置」列
- [ ] AC-003 与展示端语义区分
- [ ] AC-004 空态/加载 colSpan 一致
- [ ] AC-005 列表功能无回归
- [ ] AC-006～AC-008 Design System / Vitest / delta

## BUG-0040 功能验收

> 来源：`issues/bugs/archive/BUG-0040-banner-modal-width-too-narrow/acceptance.md`  
> 状态：**done，已归档（`fix-banner-list-and-modal-ui` archived 2026-06-28 18:57:34）**

### 1. 弹窗 880px（AC-001～AC-010）

- [ ] AC-001 Banner 弹窗 880px
- [ ] AC-002 与 SKU 弹窗宽度一致
- [ ] AC-003 BUG-0033 滚动无回归
- [ ] AC-004 四套 jump_type 通过
- [ ] AC-005～AC-010 布局 / 纯前端 / OpenSpec delta / Vitest

## BUG-0041 功能验收

> 来源：`issues/bugs/archive/BUG-0041-sidebar-user-menu-avatar-missing/acceptance.md`  
> 状态：**done，已归档（`fix-sidebar-user-menu-avatar` archived 2026-06-28 18:49:06）**

### 1. 侧栏头像展示（AC-001～AC-011）

- [ ] AC-001 有 avatar_url 时侧栏显示头像图片
- [ ] AC-002 无 avatar_url 时 initials fallback
- [ ] AC-003 图片加载失败 fallback
- [ ] AC-004 Profile 上传后侧栏即时更新
- [ ] AC-005 collapsed 侧栏保留 avatar 图片
- [ ] AC-006 侧栏菜单行为无回归
- [ ] AC-007～AC-011 纯前端 / semantic token / vitest / tablet 回归 / 视觉一致

## BUG-0048 功能验收

> 来源：`issues/bugs/archive/BUG-0048-banner-modal-width-css-cascade-overridden/acceptance.md`  
> 状态：**done，已归档（`fix-banner-modal-width-css-cascade` archived 2026-06-28 18:56:51）**

### 1. 运行时 Computed 880px（AC-001～AC-010）

- [ ] AC-001 DevTools Computed width 880px（非 520px）
- [ ] AC-002 生效规则非 `.modal-card` 520px 覆盖
- [ ] AC-003 与 SKU 弹窗并排宽度一致
- [ ] AC-004 单一专属类 `banner-modal-card`（无冗余 `modal-card`）
- [ ] AC-005 BUG-0033 滚动无回归
- [ ] AC-006 四套 jump_type 通过
- [ ] AC-007 Vitest 完整 CSS 栈断言
- [ ] AC-008～AC-010 纯前端 / semantic token / change trace 记录

## BUG-0042 功能验收

> 来源：`issues/bugs/archive/BUG-0042-system-settings-page-title-v2-suffix/acceptance.md`  
> 状态：**done，已归档（`fix-system-settings-page-title-v2-suffix` archived 2026-06-28 19:13:52）**

- [ ] AC-001～AC-005 眉标去除 `/ V2`、五 Tab 一致、无回归

## BUG-0043 功能验收

> 来源：`issues/bugs/archive/BUG-0043-system-settings-duplicate-save-buttons/acceptance.md`  
> 状态：**done，已归档（`fix-system-settings-duplicate-save-buttons` archived 2026-06-28 19:13:52）**

- [ ] AC-001～AC-006 单 CTA、保存/脏态/dirty guard 无回归

## BUG-0045 功能验收

> 来源：`issues/bugs/archive/BUG-0045-system-settings-media-format-options-limited/acceptance.md`  
> 状态：**done，已归档（`fix-system-settings-media-format-options` archived 2026-06-28 19:36:12）**

- [ ] AC-001～AC-010 8 图 + 7 视频 MIME 选项、env、后端校验、upload 冒烟

## BUG-0046 功能验收

> 来源：`issues/bugs/archive/BUG-0046-system-settings-reset-confirm-ui-inconsistency/acceptance.md`  
> 状态：**done，已归档（`fix-system-settings-reset-confirm-ui` archived 2026-06-28 19:36:12）**

- [ ] AC-001～AC-007 modal-backdrop 确认、无 `window.confirm`、五 Tab 一致

## BUG-0047 功能验收

> 来源：`issues/bugs/archive/BUG-0047-system-settings-save-tip-layout-shift/acceptance.md`  
> 状态：**done，已归档（`fix-system-settings-save-tip-layout-shift` archived 2026-06-28 19:36:12）**

- [ ] AC-001～AC-006 AdminToast 提示、无 inline tip 布局抖动

## REQ-0016 功能验收

> 来源：`issues/requirements/archive/REQ-0016-banner-management/acceptance.md`  
> 状态：**done，已归档（`add-banner-management` archived 2026-06-28 15:50:00）**

### 1. Banner 列表页（AC-001～AC-023）

- [ ] AC-001～AC-023 路由、筛选、指标卡、表格、上线下线、删除、分页、Dashboard 入口

### 2. 弹窗公共与变体（AC-024～AC-039）

- [ ] AC-024～AC-030 弹窗结构、无状态块、jump_type 切换
- [ ] AC-031～AC-039 SKU 详情/外链/专题/无跳转四套变体

### 3. API / 数据 / 媒体（AC-040～AC-049）

- [ ] AC-040～AC-049 banners API、topics、MinIO、pytest

### 4. 视觉（AC-050～AC-052）

- [ ] AC-050～AC-052 列表 + 四套弹窗 HTML/PNG 并排

## REQ-0017 功能验收

> 来源：`issues/requirements/archive/REQ-0017-system-settings/acceptance.md`  
> 状态：**done，已归档（`add-system-settings` archived 2026-06-28 17:10:00）**

### 1. 访问与 Shell（AC-001～AC-013，P0）

- [ ] AC-001～AC-013 路由、RBAC、Shell、dirty、保存/取消/reset

### 2. 基础信息 + 媒体 Tab（AC-014～AC-022，P0）

- [ ] AC-014～AC-022 basic/media PATCH、effective upload、只读 bucket/Key

### 3. 安全 + 审计 + 通知（AC-023～AC-035，P1–P3）

- [ ] AC-023～AC-027 安全策略与 REQ-0015 联动
- [ ] AC-028～AC-031 审计 Tab + audit_logs
- [ ] AC-032～AC-035 通知开关（无发信）

### 4. API / 数据 / 测试（AC-036～AC-045）

- [ ] AC-036～AC-045 API、migration、pytest、vitest

## 视觉验收

- [ ] `/admin/profile` 与 `profile-page.png` 并排（1440×1024）
- [ ] `/admin/profile` 表单无 role/status input；账号安全卡片完整（BUG-0022）
- [ ] `/admin/profile` 页头无重复「保存修改」；表单底单 CTA（BUG-0023）
- [ ] 改密弹窗与 `password-change-modal.png` 并排
- [ ] 改密弹窗常见密码失败：错误在新密码字段下（BUG-0024）
- [ ] 改密弹窗有 error 时三字段 toggle 垂直对齐（BUG-0025）
- [ ] 改密弹窗 dirty 后点取消：直接关闭，无浏览器 confirm（BUG-0026）
- [x] `/admin/tile-specs` 与 `tile-size-management.html` 并排（HTML gate vitest 2026-06-28）
- [ ] `/admin/tile-specs` 分页与用户管理页一致（BUG-0027）
- [x] 规格弹窗与 `tile-size-management-modal.html` 并排（HTML gate vitest 2026-06-28）
- [ ] 规格新增/编辑保存后无需 F5（BUG-0029）
- [ ] 编辑无 spec_id SKU 时规格提示为次要文字样式（BUG-0038）
- [ ] Banner vs SKU 弹窗并排 Computed 880px（BUG-0040/0048）
- [ ] 侧栏用户菜单有头像时显示图片，与 Profile 页一致（BUG-0041）
- [x] collapsed 侧栏各菜单图标形状可区分（Vitest `AdminSidebar.icons.test.tsx`）
- [ ] `/admin/banners` 与 `banner-management-list.png` 并排
- [ ] 四套 Banner 弹窗与对应 modal PNG 并排
- [ ] `/admin/settings/basic` 与 `system-settings-basic.html` 并排（5 Tab checklist）
- [ ] 系统设置页眉标无 `/ V2`（BUG-0042）
- [ ] 系统设置页仅表单底一处「保存设置」（BUG-0043）
- [ ] 系统设置「恢复默认」为 modal-backdrop 确认（BUG-0046）
- [ ] 系统设置保存成功为 AdminToast，无布局抖动（BUG-0047）
- [ ] 系统设置媒体 Tab 8 图 + 7 视频 MIME 选项（BUG-0045）

## 遗留项

| 编号 | 描述 | 处理 |
|---|---|---|
| _待填写_ | — | — |
