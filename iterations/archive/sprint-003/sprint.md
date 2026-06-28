---
created_at: 2026-06-28 10:03:15
updated_at: 2026-06-28 19:40:42
title: Sprint 003 迭代说明
purpose: 记录 Sprint 003 目标、范围、Change、工作量与风险
content: 管理端个人资料 + 修改密码 + 瓷砖规格 + 对象存储 Key + Banner + 系统设置 + 侧栏菜单图标 + 个人资料/改密/规格 UX 修复 + Banner 列表/弹窗 UI 修复 BUG-0030～0036 + SKU 规格提示 BUG-0038 + Banner 列表列/弹窗宽度 BUG-0039/0040 + Banner 弹窗 CSS 层叠 BUG-0048 + 侧栏用户头像 BUG-0041 + 系统设置页 UI/媒体格式 BUG-0042/0043/0045/0046/0047（REQ-0014/0015/0009/0012/0016/0017 + BUG-0021~0029 + BUG-0030~0041 + BUG-0042~0048）
source: AI 根据 issues/openspec 目录生成，项目团队确认
update_method: 迭代范围或状态变化时更新
owner: 项目负责人
status: planning
note: workflow-sync — workflow-sync 自动同步 — 23/23 Change archived；0 applied；Sprint `completed`
---

# Sprint 003

## Sprint 目标

本迭代交付 **6 项需求 + 27 项缺陷修复 + REQ-0014 v1.1 修订**：

1. **REQ-0014-profile-page 管理端个人资料** — `/admin/profile` 页面；self-service API；`users.remark` + `profile_activity_logs` 完整审计；侧栏「个人资料」入口落地。
2. **REQ-0015-password-change 管理端修改密码** — 侧栏「密码修改」+ profile 页账号安全卡片入口；520px 居中弹窗；改密 API 与 token 失效；`AdminLayout` 托管共用 `ChangePasswordModal`。
3. **REQ-0009-tile-spec-management 瓷砖规格管理** — `/admin/tile-specs` 主数据 CRUD/启停/条件删除；导航入口；SKU 表单规格下拉 + `spec_id` 联动；历史 SKU 迁移。
4. **REQ-0012-object-storage-key-layout 对象存储 Key 布局优化** — `images`/`videos` 语义前缀；简化 Key 形态（去 `{YYYY}/{MM}`）；4 上传 API 映射调整；一次性迁移脚本（dry-run + apply）；文档与 pytest 同步。
5. **REQ-0016-banner-management Banner 管理** — `/admin/banners` 列表 + 按跳转类型分化弹窗（SKU 详情/外部链接/专题页/无跳转）；`banners` + `topics` 种子；MinIO Banner 上传；Dashboard 快捷入口落地。
6. **REQ-0017-system-settings 管理端系统设置** — `/admin/settings` 5 Tab（基础/安全/媒体/通知/审计）；`system_settings` + effective merge；侧栏占位闭环；P0–P3 分 Phase apply（P1 与改密联动）。
7. **BUG-0021-sidebar-menu-icons-indistinguishable 侧栏菜单图标无法区分** — collapsed 态各菜单配置 Lucide 语义图标；`admin-nav.ts` + `AdminSidebar.tsx`；无 API/DB 变更。
8. **BUG-0022-profile-basic-info-redundant-role-status 个人资料基础资料区角色/状态重复** — 移除表单内「所属角色」「账号状态」只读字段；仅在账号安全卡片展示；REQ-0014 AC-011 MODIFIED；无 API/DB 变更。
9. **BUG-0023-profile-duplicate-save-buttons 个人资料页重复保存修改按钮** — 移除页头重复「保存修改」，保留表单底单 CTA；`ProfilePage.tsx` + vitest；无 API/DB 变更。
10. **BUG-0024-change-password-error-wrong-field 修改密码弹窗错误提示字段错位** — 新密码相关错误显示在新密码字段下；拆分 `oldPasswordError`/`newPasswordError`；按 API error_code 分流；`ChangePasswordModal.tsx` + vitest；无 API/DB 变更。
11. **BUG-0025-change-password-toggle-button-misalignment 修改密码弹窗显隐按钮垂直错位** — 字段出现 error 后「显示/隐藏」按钮下沉；input + toggle 独立定位包装层；`password-change-modal.css`；与 BUG-0024 同 change `fix-change-password-modal-errors`；无 API/DB 变更。
12. **BUG-0026-change-password-cancel-confirm-redundant 修改密码弹窗取消多余浏览器二次确认** — 移除 `isDirty` + `window.confirm`；取消/×/Esc/遮罩直接关闭；MODIFIED spec 脏关闭 Scenario；与 BUG-0024/0025 同 change；无 API/DB 变更。
13. **BUG-0027-tile-spec-list-ui-inconsistency 瓷砖规格列表分页与字号不一致** — 分页 DOM 对齐用户管理页；`.size-name` 字号协调；`TileSpecManagementPage.tsx` + CSS；无 API/DB 变更。
14. **BUG-0028-tile-spec-modal-form-layout 瓷砖规格弹窗字段顺序与备注宽度** — 宽/长 → 只读尺寸名称 → 厚度/排序 → 备注；备注 textarea 整行；保留 `{w}×{l}mm`；`TileSpecFormModal.tsx` + CSS。
15. **BUG-0029-tile-spec-list-not-refresh-after-create 瓷砖规格保存后列表未刷新** — `onSuccess` 补 `loadSpecs()`；新增/编辑后列表与 summary 即时更新；纯前端逻辑修复。
16. **BUG-0030-banner-list-ui-inconsistency Banner 列表分页与表头与用户管理页不一致** — 移除 section-head/table-toolbar；标准 `.pagination` DOM；`BannerManagementPage.tsx` + CSS；无 API/DB 变更。
17. **BUG-0031-banner-modal-image-section-label Banner 弹窗图片区首行来源文案冗余** — 移除 `.banner-upload-title` 动态「自定义上传/SKU 主图」首行；保留字段 Label + 操作按钮；无 API/DB 变更。
18. **BUG-0032-banner-modal-upload-button-label Banner 弹窗上传按钮文案不一致** — 「选择/更换/上传中」+ `hidden` file input；对齐 `BrandFormModal`；无 API/DB 变更。
19. **BUG-0033-banner-modal-form-layout-overflow Banner 弹窗备注宽度不足且底部按钮溢出** — modal-body scroll；textarea 100% 宽；placeholder 12px；`banner-management.css`；无 API/DB 变更。
20. **BUG-0034-banner-modal-link-selector-combined Banner 弹窗 SKU/专题搜索与下拉应合并** — 单控件 `SearchableSelect` Combobox；`BannerFormModal.tsx`；无 API/DB 变更。
21. **BUG-0035-banner-modal-sku-hero-image-no-effect Banner 弹窗「使用 SKU 主图」无效果** — `fetchTileSku` 回填主图；`extractSkuMainImage`；列表 API 媒体映射修复；无 schema 变更。
22. **BUG-0036-banner-modal-datetime-picker Banner 弹窗有效期无法选时分秒** — 单字段有效期区间控件 `BannerValidityField`；支持精确起止时间；替换 `datetime-local` 双字段；无 API/DB 变更。
23. **BUG-0037-tile-spec-status-confirm-ui-inconsistency 瓷砖规格启停/删除 confirm 与类目页不一致** — 启停/删除 confirm markup 对齐 `TileCategoryManagementPage`；语义化主按钮、停用后果说明、× 关闭；`TileSpecManagementPage.tsx` + vitest；无 API/DB 变更。
24. **BUG-0038-tile-sku-modal-spec-hint-styling SKU 弹窗规格未匹配提示样式不当** — 历史 SKU `spec_id` 为空时规格字段下方提示 `form-hint` → `form-help`；对齐用户/品牌弹窗 11px `--admin-weak`；`TileSkuFormModal.tsx` + vitest；无 API/DB 变更。
25. **BUG-0039-banner-list-display-position-column Banner 列表展示位置未独立成列** — 第一列仅 Banner 标题；新增「展示位置」列；`BannerManagementPage.tsx`；与 list PNG 第一列 delta；无 API/DB 变更。
26. **BUG-0040-banner-modal-width-too-narrow Banner 弹窗宽度未对齐 SKU** — `.banner-modal-card` 640px → 880px；对齐 `.sku-modal-card`；MODIFIED web-client spec；回归 BUG-0033 滚动；无 API/DB 变更。
27. **BUG-0041-sidebar-user-menu-avatar-missing 侧栏用户菜单未显示头像** — `AdminLayout` 传递 `profile/me` 的 `avatar_url`；`AdminUserMenu` img + initials fallback；Profile 上传后侧栏即时刷新；纯前端；无 API/Orval 变更。
28. **BUG-0048-banner-modal-width-css-cascade-overridden Banner 弹窗 880px CSS 层叠未生效** — 移除 `BannerFormModal` 冗余 `modal-card` 类；运行时 Computed 880px；Vitest 完整 CSS 栈断言；闭环 BUG-0040 回归；无 API/DB 变更。
29. **REQ-0014 v1.1 个人资料操作记录展示上限 5 条** — activities API/UI 默认 limit 20→5；`fix-profile-activities-display-limit`（已 archive 2026-06-28 19:04:00）。
30. **BUG-0042-system-settings-page-title-v2-suffix 系统设置页眉标多余 V2** — 眉标改为 `SYSTEM / SYSTEM SETTINGS`；单行 TSX + prototype HTML；无 API/DB 变更。
31. **BUG-0043-system-settings-duplicate-save-buttons 系统设置页重复保存设置按钮** — 移除页头「保存设置」，保留 footer 单 CTA；对齐 BUG-0023；MODIFIED AC-009。
32. **BUG-0045-system-settings-media-format-options-limited 媒体格式选项过少** — 扩展图片 8 / 视频 7 MIME；前后端 + `.env.example` 对齐；upload effective 校验。
33. **BUG-0046-system-settings-reset-confirm-ui-inconsistency 恢复默认 confirm UI 不一致** — `window.confirm` → DS modal；含 dirty Tab 切换 confirm；对齐 BUG-0037。
34. **BUG-0047-system-settings-save-tip-layout-shift 保存 tip 导致页面位移** — inline tip → `AdminToast`；对齐 BUG-0015；MODIFIED AC-012。

### BUG-0042-system-settings-page-title-v2-suffix 要点

- **严重等级**：low
- **现象**：页头眉标 `SYSTEM / SYSTEM SETTINGS / V2` 多余版本后缀
- **根因**：prototype CSS port 硬编码；侧栏已有 `ProductVersionBadge`
- **修复范围**：`SystemSettingsPage.tsx` L798；5 份 prototype HTML eyebrow
- **父需求**：REQ-0017-system-settings
- **OpenSpec**：`fix-system-settings-page-title-v2-suffix`（已 `/bug-opsx`，proposed）

### BUG-0043-system-settings-duplicate-save-buttons 要点

- **严重等级**：low
- **现象**：页头与 footer 双「保存设置」按钮
- **根因**：`add-system-settings` AC-009 双入口；与用户反馈及 Profile fix 模式冲突
- **修复范围**：移除 `settings-hero-actions` 保存按钮；vitest 单按钮断言
- **父需求**：REQ-0017-system-settings；关联 BUG-0023
- **OpenSpec**：`fix-system-settings-duplicate-save-buttons`（已 `/bug-opsx`，proposed）

### BUG-0045-system-settings-media-format-options-limited 要点

- **严重等级**：medium
- **现象**：media Tab 图片/视频格式各仅 3 种 chip
- **根因**：前端常量 + env/后端校验子集过窄
- **修复范围**：`IMAGE_MIME_OPTIONS`/`VIDEO_MIME_OPTIONS`；`.env.example`；`_validate_media`；pytest upload
- **父需求**：REQ-0017-system-settings
- **OpenSpec**：`fix-system-settings-media-format-options`（已 `/bug-opsx`，proposed；**独立 apply**）

### BUG-0046-system-settings-reset-confirm-ui-inconsistency 要点

- **严重等级**：medium
- **现象**：恢复默认 / dirty Tab 切换使用浏览器原生 confirm
- **根因**：快捷实现未 port DS modal（参考 TileSpecManagementPage）
- **修复范围**：modal-backdrop + dialog state；移除 `window.confirm`
- **父需求**：REQ-0017-system-settings；关联 BUG-0037
- **OpenSpec**：`fix-system-settings-reset-confirm-ui`（已 `/bug-opsx`，proposed）

### BUG-0047-system-settings-save-tip-layout-shift 要点

- **严重等级**：medium
- **现象**：`settings-save-tip` 条件渲染推挤下方 Tab 内容
- **根因**：inline 文档流 tip vs 列表页 AdminToast 模式
- **修复范围**：`AdminLayout` toast；移除 layout shift；MODIFIED AC-012
- **父需求**：REQ-0017-system-settings；关联 BUG-0015
- **OpenSpec**：`fix-system-settings-save-tip-layout-shift`（已 `/bug-opsx`，proposed）

### fix-profile-activities-display-limit 要点

- **类型**：REQ-0014 v1.1 需求修订（BUG-0049 已驳回）
- **现象**：操作记录 timeline 展示 20 条信息密度过高
- **定稿**：API 与页面 **最多 5** 条；不足 5 时展示实际条数
- **修复范围**：`profile_service` / repository limit=5；pytest + vitest；`docs/03-api-index.md`
- **父需求**：REQ-0014-profile-page（`add-admin-profile-page` 已 archived）
- **OpenSpec**：`fix-profile-activities-display-limit`（archived 2026-06-28 19:04:00）

### BUG-0048-banner-modal-width-css-cascade-overridden 要点

- **严重等级**：medium
- **现象**：源 CSS 已 880px，浏览器 Computed width 仍约 520px，窄于 SKU 弹窗
- **根因**：`modal-card` + `banner-modal-card` 双类名；`.admin-shell .modal-card { 520px }` 在 bundle 中覆盖 880px
- **修复范围**：`BannerFormModal.tsx` 移除 `modal-card`；Vitest import 冲突 CSS 栈；DevTools Computed 验收
- **父 BUG**：BUG-0040-banner-modal-width-too-narrow
- **OpenSpec**：`fix-banner-modal-width-css-cascade`（已 `/bug-opsx`，proposed）；**须在** `fix-banner-list-and-modal-ui` archive **前** apply

### BUG-0041-sidebar-user-menu-avatar-missing 要点

- **严重等级**：medium
- **现象**：侧栏底部用户菜单始终 initials，不展示已上传头像图片
- **根因**：`AdminUserMenu` 未渲染 `<img>`；Layout 预取 profile 仅传 email；REQ-0014 未同步侧栏
- **修复范围**：`AdminLayout.tsx`、`AdminUserMenu.tsx`、`admin-home.css`、vitest；可选 Profile refetch hook
- **父需求**：REQ-0014-profile-page
- **OpenSpec**：`fix-sidebar-user-menu-avatar`（已 `/bug-opsx`，proposed）

### BUG-0040-banner-modal-width-too-narrow 要点

- **严重等级**：medium
- **现象**：Banner 弹窗 640px 明显窄于 SKU 880px，表单拥挤
- **根因**：REQ-0016 原型/spec 有意 640px；产品确认对齐 SKU 大表单档位
- **修复范围**：`banner-management.css` 宽度 + delta spec；验收以 SKU 并排为准
- **父需求**：REQ-0016-banner-management
- **OpenSpec**：`fix-banner-list-and-modal-ui`（与 BUG-0039 合并；已 `/bug-opsx`，proposed）

### BUG-0039-banner-list-display-position-column 要点

- **严重等级**：medium
- **现象**：第一列标题与展示位置（`banner-sub`）挤在同一单元格
- **根因**：列表原型 port 将 position 作副标题
- **修复范围**：独立「展示位置」列；第一列仅缩略图 + 标题；colSpan 9
- **父需求**：REQ-0016-banner-management
- **OpenSpec**：`fix-banner-list-and-modal-ui`（与 BUG-0040 合并；已 `/bug-opsx`，proposed）

### BUG-0038-tile-sku-modal-spec-hint-styling 要点

- **严重等级**：low
- **现象**：编辑无 `spec_id` 历史 SKU 时，规格下拉下方提示字号偏大、颜色过亮
- **根因**：误用未定义 `form-hint`；应复用 `form-help`（11px `--admin-weak`）
- **修复范围**：`TileSkuFormModal.tsx` 单行类名 + vitest
- **父需求**：REQ-0006-tile-sku-management；REQ-0009 迁移失败补选场景
- **OpenSpec**：`fix-tile-sku-modal-spec-hint-styling`（已 `/bug-opsx`，proposed）

### BUG-0030-banner-list-ui-inconsistency 要点

- **严重等级**：medium
- **现象**：Banner 列表多余「Banner 列表」标题、table-toolbar 范围行、非标准分页 DOM
- **根因**：CSS Port 未对齐用户管理页基准（同 BUG-0009/0027）
- **修复范围**：标准 pagination + 移除 section-head/toolbar
- **OpenSpec**：`fix-banner-admin-ui`（已 archived）

### BUG-0031-banner-modal-image-section-label 要点

- **严重等级**：low
- **现象**：图片 upload 区首行显示「自定义上传 / SKU 主图」冗余标题
- **根因**：`.banner-upload-title` 动态来源文案与字段 Label 重复
- **修复范围**：移除首行 title，保留 desc 与操作按钮
- **OpenSpec**：`fix-banner-admin-ui`（已 archived）

### BUG-0032-banner-modal-upload-button-label 要点

- **严重等级**：low
- **现象**：Banner 弹窗上传按钮显示「自定义上传 浏览…」，未对齐 `BrandFormModal`
- **根因**：硬编码文案 + `sr-only` 未完全隐藏原生 file input；上传中状态未绑定按钮
- **修复范围**：动态「选择/更换/上传中」+ `hidden` input + 上传中 disabled
- **父需求**：REQ-0016-banner-management（AC-032 自定义上传能力无回归）
- **OpenSpec**：`fix-banner-admin-ui`（与 BUG-0030～0036 合并；已 `/bug-opsx` + archived）

### BUG-0033-banner-modal-form-layout-overflow 要点

- **严重等级**：high
- **现象**：运营备注 textarea 宽度不足；弹窗无 scroll 导致底部按钮被裁切
- **根因**：未 port 原型 `.textarea` 与 `.modal-body { overflow: auto }`
- **修复范围**：flex column modal + scroll body + textarea 100%
- **OpenSpec**：`fix-banner-admin-ui`（已 archived）

### BUG-0034-banner-modal-link-selector-combined 要点

- **严重等级**：medium
- **现象**：SKU/专题关联为搜索框 + 下拉两控件，操作割裂
- **根因**：未实现单控件 Combobox
- **修复范围**：`SearchableSelect` 合并搜索与选择
- **OpenSpec**：`fix-banner-admin-ui`（已 archived）

### BUG-0035-banner-modal-sku-hero-image-no-effect 要点

- **严重等级**：high
- **现象**：「使用 SKU 主图」点击无预览/Key 回填
- **根因**：列表 API 未带 `images`；按钮仅依赖空 `mainImageKey`
- **修复范围**：SKU 详情 fetch 或媒体字段映射 + 按钮 handler
- **OpenSpec**：`fix-banner-admin-ui`（已 archived）

### BUG-0036-banner-modal-datetime-picker 要点

- **严重等级**：medium
- **现象**：`datetime-local` 无法选秒；双字段与原型单区间不符
- **根因**：原生控件精度与暗色主题交互限制
- **修复范围**：`BannerValidityField` 区间控件；精确起止时间
- **OpenSpec**：`fix-banner-admin-ui`（已 archived）

### BUG-0037-tile-spec-status-confirm-ui-inconsistency 要点

- **严重等级**：medium
- **现象**：规格页启停/删除 confirm 使用简化 `confirm-card` 模板，无 × 关闭、泛化「确认」主按钮、停用无前台影响说明
- **根因**：`add-tile-spec-management` 初版遗漏；`fix-tile-spec-admin-ui` scope 未含 confirm
- **修复范围**：对齐类目/品牌 DS modal 结构；补 Vitest 停用 confirm 门禁
- **父需求**：REQ-0009-tile-spec-management（AC-013/AC-018）
- **OpenSpec**：`fix-tile-spec-status-confirm-ui`（已 `/bug-opsx`，proposed；**独立**于已 archived `fix-tile-spec-admin-ui`）

### BUG-0027-tile-spec-list-ui-inconsistency 要点

- **严重等级**：medium
- **现象**：规格列表分页使用 `pagination-bar`/`page-indicator`，与用户管理页不一致；尺寸名称列字号偏大
- **根因**：CSS Port 未复用标准分页 DOM；`.size-name` 13px 偏离同表 12px
- **修复范围**：分页对齐 `UserManagementPage`；调整 `.size-name` rhythm
- **父需求**：REQ-0009-tile-spec-management（`add-tile-spec-management` 已 archived）
- **OpenSpec**：`fix-tile-spec-admin-ui`（与 BUG-0028/0029 合并；已 archived）

### BUG-0028-tile-spec-modal-form-layout 要点

- **严重等级**：medium
- **现象**：弹窗尺寸名称位于厚度/排序之后；备注 textarea 未占满整行
- **根因**：JSX 字段顺序错误；CSS 未 port textarea 宽度/高度
- **修复范围**：字段重排 + `.textarea { width:100% }`；**不**去掉 `mm` 后缀
- **父需求**：REQ-0009-tile-spec-management
- **OpenSpec**：`fix-tile-spec-admin-ui`（与 BUG-0027/0029 合并）

### BUG-0029-tile-spec-list-not-refresh-after-create 要点

- **严重等级**：high
- **现象**：新增/编辑保存成功但列表与指标卡 stale，须 F5 刷新
- **根因**：`onSuccess={setNotice}` 未调用 `loadSpecs()`；启停/删除路径已正确刷新
- **修复范围**：`onSuccess` 同时 Toast + `loadSpecs()`；对齐品牌/SKU 页
- **父需求**：REQ-0009-tile-spec-management
- **OpenSpec**：`fix-tile-spec-admin-ui`（与 BUG-0027/0028 合并）

### REQ-0014-profile-page 要点

- **优先级**：P1
- **入口**：`AdminUserMenu`「个人资料」→ `/admin/profile`（替换 `onPlaceholder`）
- **UI**：两列 layout（主卡片 + 账号安全/操作记录）；CSS Port `profile-page.html` / PNG；inline save-tip
- **后端**：`GET/PATCH /api/v1/profile/me`；`GET .../activities`（**5** 条，v1.1）；login/profile/avatar audit
- **DB**：`users.remark`；`profile_activity_logs`
- **协作**：「修改密码」打开 REQ-0015 弹窗（共用 hook）
- **OpenSpec**：`add-admin-profile-page`（已 archive）；v1.1 → `fix-profile-activities-display-limit`（archived）

### REQ-0015-password-change 要点

- **优先级**：P1
- **入口**：用户菜单 + profile 账号安全卡片 → 打开弹窗
- **UI**：520px 居中弹窗；显隐切换；成功后 Toast + logout + 跳转登录
- **后端**：`POST /api/v1/admin/profile/password`；`token_version`；限流
- **OpenSpec**：`add-admin-password-change`（**待 `/req-opsx REQ-0015`**）

### REQ-0009-tile-spec-management 要点

- **优先级**：P1
- **入口**：OPERATIONS「瓷砖规格」→ `/admin/tile-specs`（类目与 Banner 之间）
- **UI**：对齐品牌页（指标卡、状态筛选、启停确认、条件删除、分页）；弹窗系统生成 `display_name`
- **后端**：`tile_specs` 表；Admin CRUD + enable/disable；`tiles.spec_id` + `sku_count`；历史 `size` 迁移
- **SKU MODIFIED**：`TileSkuFormModal` 规格改下拉（仅 ENABLED）；`size` 冗余同步
- **OpenSpec**：`add-tile-spec-management`（**待 `/req-opsx REQ-0009`**）

### REQ-0012-object-storage-key-layout 要点

- **优先级**：P1
- **范围**：基础设施 / 对象存储；无 UI 变更
- **Key 形态**：`{prefix}/{tenant}/{resource_type}/{uuid}.{ext}`；禁止 `original/` 与新对象 `{YYYY}/{MM}`
- **前缀**：`images`（头像/Logo/SKU 图）、`videos`（SKU 视频）；`files`/`audios` 规范预留
- **resource_type**：`user/avatars`、`brands/logos`、`tiles/{id|pending}` 等
- **上传 API**：4 个 admin uploads 端点映射调整；响应形态不变
- **迁移**：方案 A — `scripts/migrate_object_keys.py`（dry-run + apply）；更新 DB 四处 `object_key` 引用
- **文档**：`rules/object-storage.md`、`docs/07-object-storage-strategy.md`、`.env.example`
- **OpenSpec**：`update-object-storage-key-layout`（已 req-opsx）

### REQ-0016-banner-management 要点

- **优先级**：P1
- **父需求**：REQ-0004-admin-home（导航占位 + Dashboard「新增 Banner」快捷）
- **入口**：OPERATIONS「Banner 管理」→ `/admin/banners`；`admin-nav.ts` 配置 path
- **UI**：列表对齐用户管理/品牌页；640px 弹窗按 `jump_type` 分化（4 套 HTML/PNG）；弹窗 **不含** 状态字段
- **跳转类型**：SKU 详情（SKU 图库选图 + `image_source`）、外部链接（HTTPS）、专题页（`topics` 种子）、无跳转
- **后端**：`banners` + `topics` migration；Admin CRUD + online/offline；Banner 图 MinIO 上传
- **Out**：消费端展示、类目页跳转创建、专题 CRUD、外链白名单引擎
- **OpenSpec**：`add-banner-management`（**待 `/req-opsx REQ-0016`**）

### BUG-0021-sidebar-menu-icons-indistinguishable 要点

- **严重等级**：medium
- **现象**：collapsed 侧栏 7 个菜单项共用相同 `.nav-icon` CSS 占位，无法凭图标识别
- **根因**：`admin-nav.ts` 无 per-item icon；`AdminSidebar.tsx` 统一渲染 `<span className="nav-icon" />`
- **修复范围**：Lucide outline 语义图标（LayoutDashboard、Package、Building2 等）；expanded/collapsed 无布局回归
- **父需求**：REQ-0011-admin-sidebar-expand-collapse（已归档；折叠能力落地后暴露 UX 缺口）
- **OpenSpec**：`fix-sidebar-menu-icons-indistinguishable`（已 `/bug-opsx`，proposed）

### BUG-0022-profile-basic-info-redundant-role-status 要点

- **严重等级**：low
- **现象**：`/admin/profile`「基础资料」表单内「所属角色」「账号状态」与「账号安全」卡片重复
- **根因**：REQ-0014 原 AC-011 / 原型双区展示；`add-admin-profile-page` 按 spec 交付
- **修复范围**：移除 `profile-form-grid` 内 role/status 只读 field；保留账号安全卡片 AC-022；同步 REQ/prototype/OpenSpec delta
- **父需求**：REQ-0014-profile-page（`add-admin-profile-page` 已 archived）
- **OpenSpec**：`fix-profile-basic-info-redundant-role-status`（已 `/bug-opsx`，proposed）

### BUG-0023-profile-duplicate-save-buttons 要点

- **严重等级**：low
- **现象**：`/admin/profile` 页头与表单底部各有一个「保存修改」按钮，功能相同、视觉重复
- **根因**：REQ-0014 原型/AC-017 允许双 CTA；`add-admin-profile-page` 按原型交付
- **修复范围**：移除页头按钮，保留表单底与「重置」、inline save-tip 同区；更新 vitest 单按钮断言
- **父需求**：REQ-0014-profile-page（`add-admin-profile-page` 已 archived）
- **OpenSpec**：`fix-profile-duplicate-save-buttons`（已 `/bug-opsx`，proposed）

### BUG-0024-change-password-error-wrong-field 要点

- **严重等级**：medium
- **现象**：修改密码弹窗中「新密码过于常见」等新密码相关错误显示在「原密码」字段下方
- **根因**：单一 `error` 状态误绑原密码 `PasswordField`；API 错误码未按字段分流
- **修复范围**：拆分 per-field 错误；40020→原密码，40021/40022/40023→新密码；Vitest 字段位置断言
- **父需求**：REQ-0014-profile-page（改密弹窗入口）；依赖 REQ-0015 `add-admin-password-change` 已交付
- **OpenSpec**：`fix-change-password-modal-errors`（已 `/bug-opsx`，proposed；与 BUG-0025 合并 scope）

### BUG-0025-change-password-toggle-button-misalignment 要点

- **严重等级**：medium
- **现象**：密码字段下方出现 error 后「显示/隐藏」按钮垂直下沉，未相对 input 居中
- **根因**：`toggle-pass` 的 `bottom: 8px` 相对含 `error-text` 的 `.password-field` 定位
- **修复范围**：`.password-input-wrap` 包裹 input + toggle；error 不参与 toggle 定位；CSS + vitest/DOM 断言
- **父需求**：REQ-0014-profile-page；姊妹 REQ-0015-password-change
- **OpenSpec**：`fix-change-password-modal-errors`（与 BUG-0024 同一 change；tasks §3 分列验收）

### BUG-0026-change-password-cancel-confirm-redundant 要点

- **严重等级**：low
- **现象**：表单有输入时点击「取消」/ × / Esc / 遮罩弹出浏览器原生 `window.confirm`
- **根因**：`requestClose` 在 `isDirty` 时调用 `window.confirm`（REQ-0015 原规格交付）；与管理端其它表单弹窗不一致
- **修复范围**：删除 dirty guard；`requestClose` 直接 `onClose()`；Vitest 更新；OpenSpec delta MODIFIED 关闭 Scenario
- **父需求**：REQ-0014-profile-page；姊妹 REQ-0015-password-change
- **OpenSpec**：`fix-change-password-modal-errors`（与 BUG-0024/0025 同一 change；tasks §5 分列验收）

### REQ-0017-system-settings 要点

- **优先级**：P1
- **父需求**：REQ-0004-admin-home（SYSTEM「系统设置」占位 → `/admin/settings`）
- **权限**：仅 `admin`（`require_system_admin`）；`employee` 隐藏菜单 + 403
- **UI**：5 Tab Shell（`settings-nav` + `settings-panel`）；CSS Port `system-settings-*.html`；1080px max-width
- **Phase**：P0 basic+media → P1 security（联动 REQ-0015）→ P2 audit_logs → P3 notification（无发信）
- **后端**：`system_settings` KV；effective merge env；upload 读 runtime limits（MODIFIED object-storage）
- **协作**：P2 `audit_logs` 与 REQ-0014 profile audit 统一；P1 密码规则 enforcement 改密/建用户
- **OpenSpec**：`add-system-settings`（已 req-opsx，proposed）

## Scope

### 包含需求

<!-- workflow-sync:scope-requirements:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| REQ-0014 | 管理后台个人资料页面 | P1 | done | archived `add-admin-profile-page`（2026-06-28 12:15:00） |
| REQ-0015 | 管理端修改密码（侧栏入口 + 居中弹窗） | P1 | done | archived `add-admin-password-change`（2026-06-28 12:52:00） |
| REQ-0009 | 管理后台 - 瓷砖规格管理 | P1 | done | archived `add-tile-spec-management`（2026-06-28 13:30:00） |
| REQ-0012 | 对象存储前缀与 Object Key 生成规则优化 | P1 | done | archived `update-object-storage-key-layout`（2026-06-28 10:32:00） |
| REQ-0016 | 管理后台 - Banner 管理 | P1 | done | archived `add-banner-management`（2026-06-28 15:50:00） |
| REQ-0017 | 管理后台系统设置页面 | P1 | done | archived `add-system-settings`（2026-06-28 17:10:00） |
<!-- workflow-sync:scope-requirements:end -->

### 包含 BUG

<!-- workflow-sync:scope-bugs:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| BUG-0021 | 侧边栏收起后各菜单图标相同无法区分 | medium | in_sprint | status `in_sprint` |
| BUG-0022 | 个人资料基础资料区所属角色与账号状态与账号安全卡片重复 | low | done | archived `fix-profile-basic-info-redundant-role-status`（2026-06-28 13:40:00） |
| BUG-0023 | 个人资料页页头与表单底部重复保存修改按钮 | low | done | archived `fix-profile-duplicate-save-buttons`（2026-06-28 13:40:00） |
| BUG-0024 | 修改密码弹窗新密码错误提示显示在原密码字段下方 | medium | done | archived `fix-change-password-modal-errors`（2026-06-28 15:16:00） |
| BUG-0025 | 修改密码弹窗错误提示出现后显示/隐藏按钮垂直错位 | medium | done | archived `fix-change-password-modal-errors`（2026-06-28 15:16:00） |
| BUG-0026 | 修改密码弹窗取消时出现多余浏览器二次确认 | low | done | archived `fix-change-password-modal-errors`（2026-06-28 15:16:00） |
| BUG-0027 | 瓷砖规格列表分页与尺寸名称列字号与用户管理页不一致 | medium | done | archived `fix-tile-spec-admin-ui`（2026-06-28 15:28:00） |
| BUG-0028 | 瓷砖规格弹窗表单字段顺序与备注宽度不符合 REQ-0009 规范 | medium | done | archived `fix-tile-spec-admin-ui`（2026-06-28 15:28:00） |
| BUG-0029 | 瓷砖规格新增/编辑保存后列表未自动刷新 | high | done | archived `fix-tile-spec-admin-ui`（2026-06-28 15:28:00） |
| BUG-0030 | Banner列表分页与用户管理页不一致且表头上方多余标题行 | medium | done | archived `fix-banner-admin-ui`（2026-06-28 16:35:00） |
| BUG-0031 | Banner弹窗图片模块首行自定义上传/SKU主图文案冗余 | low | done | archived `fix-banner-admin-ui`（2026-06-28 16:35:00） |
| BUG-0032 | Banner弹窗图片上传按钮文案应为选择或更换 | low | done | archived `fix-banner-admin-ui`（2026-06-28 16:35:00） |
| BUG-0033 | Banner 弹窗运营备注宽度不足且底部按钮超出弹窗无滚动 | high | done | archived `fix-banner-admin-ui`（2026-06-28 16:35:00） |
| BUG-0034 | Banner弹窗关联专题/SKU搜索框与下拉框应合并 | medium | done | archived `fix-banner-admin-ui`（2026-06-28 16:35:00） |
| BUG-0035 | Banner弹窗点击使用SKU主图无任何效果 | high | done | archived `fix-banner-admin-ui`（2026-06-28 16:35:00） |
| BUG-0036 | Banner弹窗有效期DateTime选择器无法选择时分秒 | medium | done | archived `fix-banner-admin-ui`（2026-06-28 16:35:00） |
| BUG-0037 | 瓷砖规格页启用/停用/删除确认弹窗与类目页 UI/UE 不一致 | medium | done | archived `fix-tile-spec-status-confirm-ui`（2026-06-28 16:48:07） |
| BUG-0038 | SKU弹窗规格字段下方提示字号过大且颜色不当 | low | done | archived `fix-tile-sku-modal-spec-hint-styling`（2026-06-28 17:20:00） |
| BUG-0039 | Banner列表第一列标题与展示位置挤在同一列 | medium | done | archived `fix-banner-list-and-modal-ui`（2026-06-28 18:57:34） |
| BUG-0040 | Banner弹窗宽度偏小未对齐SKU弹窗 | medium | done | archived `fix-banner-list-and-modal-ui`（2026-06-28 18:57:34） |
| BUG-0041 | 侧边栏底部用户菜单未显示用户头像 | medium | done | archived `fix-sidebar-user-menu-avatar`（2026-06-28 18:49:06） |
| BUG-0048 | Banner弹窗880px样式被modal-card全局规则层叠覆盖 | medium | done | archived `fix-banner-modal-width-css-cascade`（2026-06-28 18:56:51） |
| BUG-0042 | 系统设置页眉标多余 V2 后缀 | low | done | archived `fix-system-settings-page-title-v2-suffix`（2026-06-28 19:13:52） |
| BUG-0043 | 系统设置页页头与底部重复保存设置按钮 | low | done | archived `fix-system-settings-duplicate-save-buttons`（2026-06-28 19:13:52） |
| BUG-0045 | 系统设置媒体与存储图片/视频格式各仅 3 种 | medium | done | archived `fix-system-settings-media-format-options`（2026-06-28 19:36:12） |
| BUG-0046 | 系统设置恢复默认二次确认弹窗 UI 不一致 | medium | done | archived `fix-system-settings-reset-confirm-ui`（2026-06-28 19:36:12） |
| BUG-0047 | 系统设置保存成功提示导致下方内容位移 | medium | done | archived `fix-system-settings-save-tip-layout-shift`（2026-06-28 19:36:12） |
<!-- workflow-sync:scope-bugs:end -->

### 包含 Change

<!-- workflow-sync:scope-changes:start -->
| Change ID | 关联需求 | 状态 | Sprint 目标 |
|---|---|---|---|
| `add-admin-profile-page` | REQ-0014-profile-page | archived | archived `add-admin-profile-page`（2026-06-28 12:15:00） |
| `add-admin-password-change` | REQ-0015-password-change | archived | archived `add-admin-password-change`（2026-06-28 12:52:00） |
| `add-tile-spec-management` | REQ-0009-tile-spec-management | archived | archived `add-tile-spec-management`（2026-06-28 13:30:00） |
| `update-object-storage-key-layout` | REQ-0012-object-storage-key-layout | archived | archived `update-object-storage-key-layout`（2026-06-28 10:32:00） |
| `fix-sidebar-menu-icons-indistinguishable` | REQ-0011-admin-sidebar-expand-collapse | archived | archived `fix-sidebar-menu-icons-indistinguishable`（2026-06-28 12:05:00） |
| `fix-profile-basic-info-redundant-role-status` | REQ-0014-profile-page | archived | archived `fix-profile-basic-info-redundant-role-status`（2026-06-28 13:40:00） |
| `fix-profile-duplicate-save-buttons` | REQ-0014-profile-page | archived | archived `fix-profile-duplicate-save-buttons`（2026-06-28 13:40:00） |
| `fix-change-password-modal-errors` | REQ-0014-profile-page | archived | archived `fix-change-password-modal-errors`（2026-06-28 15:16:00） |
| `fix-tile-spec-admin-ui` | REQ-0009-tile-spec-management | archived | archived `fix-tile-spec-admin-ui`（2026-06-28 15:28:00） |
| `fix-tile-spec-status-confirm-ui` | BUG-0037-tile-spec-status-confirm-ui-inconsistency | archived | archived `fix-tile-spec-status-confirm-ui`（2026-06-28 16:48:07） |
| `add-banner-management` | REQ-0016-banner-management | archived | archived `add-banner-management`（2026-06-28 15:50:00） |
| `fix-banner-admin-ui` | REQ-0016-banner-management | archived | archived `fix-banner-admin-ui`（2026-06-28 16:35:00） |
| `add-system-settings` | REQ-0017-system-settings | archived | archived `add-system-settings`（2026-06-28 17:10:00） |
| `fix-tile-sku-modal-spec-hint-styling` | REQ-0006-tile-sku-management | archived | archived `fix-tile-sku-modal-spec-hint-styling`（2026-06-28 17:20:00） |
| `fix-banner-list-and-modal-ui` | REQ-0016-banner-management | archived | archived `fix-banner-list-and-modal-ui`（2026-06-28 18:57:34） |
| `fix-sidebar-user-menu-avatar` | REQ-0014-profile-page | archived | archived `fix-sidebar-user-menu-avatar`（2026-06-28 18:49:06） |
| `fix-banner-modal-width-css-cascade` | BUG-0048-banner-modal-width-css-cascade-overridden | archived | archived `fix-banner-modal-width-css-cascade`（2026-06-28 18:56:51） |
| `fix-profile-activities-display-limit` | REQ-0014-profile-page | archived | archived `fix-profile-activities-display-limit`（2026-06-28 19:04:00） |
| `fix-system-settings-page-title-v2-suffix` | REQ-0017-system-settings | archived | archived `fix-system-settings-page-title-v2-suffix`（2026-06-28 19:13:52） |
| `fix-system-settings-duplicate-save-buttons` | REQ-0017-system-settings | archived | archived `fix-system-settings-duplicate-save-buttons`（2026-06-28 19:13:52） |
| `fix-system-settings-media-format-options` | REQ-0017-system-settings | archived | archived `fix-system-settings-media-format-options`（2026-06-28 19:36:12） |
| `fix-system-settings-reset-confirm-ui` | REQ-0017-system-settings | archived | archived `fix-system-settings-reset-confirm-ui`（2026-06-28 19:36:12） |
| `fix-system-settings-save-tip-layout-shift` | REQ-0017-system-settings | archived | archived `fix-system-settings-save-tip-layout-shift`（2026-06-28 19:36:12） |
<!-- workflow-sync:scope-changes:end -->

> **Note：** `update-object-storage-key-layout` 已通过 `/req-opsx REQ-0012` 创建并写入 `sprint.yaml` `changes[]`。

### 延后项（待评审 / 未纳入本 Sprint）

| 项目 | 状态 | 延后原因 |
|---|---|---|
| REQ-0013-admin-shell-padding-refine | pending_review | 未评审，不得纳入正式规划 |
| 忘记密码 / 店主端改密 | — | REQ-0015 Out of Scope |

## 工作量估算

| 工作包 | 规模 | 前端 | 后端 | 测试 | 合计人天 |
|---|---|---|---|---|---|
| REQ-0014 OpenSpec（已完成）+ apply | M | 1.5 | 2 | 0.5 | 4 |
| REQ-0015 req-opsx + apply | M | 1 | 1.5 | 0.5 | 3 |
| AdminUserMenu 联调（0014+0015 共用） | S | 0.5 | — | — | 0.5 |
| REQ-0009 req-opsx + apply | L | 3 | 4 | 1 | 8 |
| REQ-0012 req-opsx + apply | M | — | 3.5 | 1 | 4.5 |
| REQ-0016 req-opsx + apply | L | 3.5 | 3 | 1.5 | 8 |
| REQ-0017 add-system-settings apply（P0–P3） | XL | 4 | 5 | 2 | 11 |
| BUG-0021 bug-opsx + apply | XS | 0.5 | — | 0.5 | 1 |
| BUG-0022 bug-opsx + apply | XS | 0.25 | — | 0.25 | 0.5 |
| BUG-0023 bug-opsx + apply | XS | 0.25 | — | 0.25 | 0.5 |
| BUG-0024 bug-opsx + apply（含 BUG-0025 toggle + BUG-0026 取消 confirm） | XS | 0.5 | — | 0.5 | 1 |
| BUG-0027/0028/0029 bug-opsx + apply（`fix-tile-spec-admin-ui` 合并） | S | 0.75 | — | 0.5 | 1.25 |
| BUG-0037 bug-opsx + apply（`fix-tile-spec-status-confirm-ui`） | XS | 0.5 | — | 0.25 | 0.75 |
| BUG-0030～0036 bug-opsx + apply（`fix-banner-admin-ui` 合并） | S | 1.25 | 0.25 | 0.75 | 2.25 |
| BUG-0038 bug-opsx + apply（`fix-tile-sku-modal-spec-hint-styling`） | XS | 0.25 | — | 0.25 | 0.5 |
| BUG-0039/0040 bug-opsx + apply（`fix-banner-list-and-modal-ui` 合并） | XS | 0.5 | — | 0.25 | 0.75 |
| BUG-0041 bug-opsx + apply（`fix-sidebar-user-menu-avatar`） | XS | 0.5 | — | 0.25 | 0.75 |
| BUG-0048 bug-opsx + apply（`fix-banner-modal-width-css-cascade`） | XS | 0.25 | — | 0.25 | 0.5 |
| BUG-0042 bug-opsx + apply（`fix-system-settings-page-title-v2-suffix`） | XS | 0.25 | — | 0.25 | 0.5 |
| BUG-0043 bug-opsx + apply（`fix-system-settings-duplicate-save-buttons`） | XS | 0.25 | — | 0.25 | 0.5 |
| BUG-0045 bug-opsx + apply（`fix-system-settings-media-format-options`） | S | 0.5 | 0.75 | 0.25 | 1.5 |
| BUG-0046 bug-opsx + apply（`fix-system-settings-reset-confirm-ui`） | XS | 0.5 | — | 0.25 | 0.75 |
| BUG-0047 bug-opsx + apply（`fix-system-settings-save-tip-layout-shift`） | XS | 0.5 | — | 0.25 | 0.75 |
| **合计** | **XXL+** | **21** | **20** | **11.5** | **54** |

> 容量：2 开发者 × 2 周 ≈ 20 人天；本 Sprint 估算 **54 人天**，**显著超容量 34 人天**（纳入 BUG-0042～0047 后 +3.5 人天）。**BUG-0042/0043/0046/0047 可合并一次 touch `SystemSettingsPage.tsx`**（建议在 `add-system-settings` P0 apply 后或并行）。**BUG-0045 独立 apply**（后端 + env）。

## 里程碑

| 阶段 | 交付 | 目标日期 |
|---|---|---|
| M1 REQ-0014 opsx 完成 + REQ-0015/0009/0012 req-opsx | changes proposed | 2026-06-29 23:59:59 |
| M1b REQ-0012 Key 生成 + 上传 API + pytest | object_keys / uploads | 2026-07-02 23:59:59 |
| M2 Profile 后端 + migration + audit | profile API、DB | 2026-07-03 23:59:59 |
| M3 Profile 前端 + 菜单入口 | `/admin/profile`、PNG 验收 | 2026-07-06 23:59:59 |
| M4 改密 API + ChangePasswordModal | REQ-0015 全链路 | 2026-07-08 23:59:59 |
| M5 规格 API + migration + SKU spec_id | REQ-0009 后端 | 2026-07-10 23:59:59 |
| M6 规格页 + SKU 下拉 + 集成测试 | REQ-0009 前端 + AC | 2026-07-11 23:59:59 |
| M6b REQ-0012 迁移脚本 dry-run + apply + 冒烟 | migrate_object_keys.py | 2026-07-11 23:59:59 |
| M6c BUG-0021 侧栏语义图标 + vitest | fix-sidebar-menu-icons-indistinguishable | 2026-07-11 23:59:59 |
| M6d BUG-0022 个人资料表单去重 role/status + vitest | fix-profile-basic-info-redundant-role-status | 2026-07-11 23:59:59 |
| M6e BUG-0023 个人资料单保存 CTA + vitest | fix-profile-duplicate-save-buttons | 2026-07-11 23:59:59 |
| M6f BUG-0024/0025/0026 改密弹窗错误字段 + toggle 布局 + 取消 confirm + vitest | fix-change-password-modal-errors | 2026-07-11 23:59:59 |
| M6g BUG-0027/0028/0029 瓷砖规格列表分页/弹窗布局/保存刷新 + vitest | fix-tile-spec-admin-ui | 2026-07-11 23:59:59 |
| M6h BUG-0037 瓷砖规格启停/删除 confirm 对齐类目页 + vitest | fix-tile-spec-status-confirm-ui | 2026-07-11 23:59:59 |
| M6i BUG-0030～0036 Banner 列表/弹窗 UI 修复 + vitest | fix-banner-admin-ui | 2026-07-11 23:59:59 |
| M6j BUG-0038 SKU 弹窗规格未匹配提示 form-help + vitest | fix-tile-sku-modal-spec-hint-styling | 2026-07-11 23:59:59 |
| M6k BUG-0039/0040 Banner 列表展示位置列 + 弹窗 880px + vitest | fix-banner-list-and-modal-ui | 2026-06-28 17:47:30 |
| M6k2 BUG-0048 Banner 弹窗 CSS 层叠修复 + Computed 880px + vitest | fix-banner-modal-width-css-cascade | 2026-07-12 23:59:59 |
| M6l BUG-0041 侧栏用户菜单头像 img + fallback + Profile 刷新 + vitest | fix-sidebar-user-menu-avatar | 2026-07-12 23:59:59 |
| M7 REQ-0016 Banner API + migration + topics 种子 | banners/topics 表 | 2026-07-12 23:59:59 |
| M7b REQ-0016 Banner 列表 + 四套弹窗 + Dashboard 入口 | `/admin/banners`、PNG 验收 | 2026-07-12 23:59:59 |
| M8 REQ-0017 P0 系统设置 basic+media + nav | `/admin/settings`、effective upload | 2026-07-12 23:59:59 |
| M8b REQ-0017 P1–P3 security/audit/notification | 五 Tab 全量或部分 spill | 2026-07-12 23:59:59 |
| M8c BUG-0042/0043/0046/0047 系统设置页 UI polish（眉标/单 CTA/confirm/toast） | fix-system-settings-* UI fixes | 2026-07-12 23:59:59 |
| M8d BUG-0045 媒体 MIME 扩展（8 图 + 7 视频）+ env + pytest | fix-system-settings-media-format-options | 2026-07-12 23:59:59 |
| M9 六 REQ + 27 BUG archive + release | AC 勾选、release note | 2026-07-12 23:59:59 |

## 风险

| 编号 | 风险 | 影响 | 缓解 |
|---|---|---|---|
| R-01 | REQ-0015 change 未创建 | 无法 apply 0015 | Sprint 启动前 `/req-opsx REQ-0015` |
| R-02 | AdminUserMenu 双 REQ 耦合 | 入口分叉 | 同一 PR 改菜单；0014 提供 `openChangePasswordModal` hook |
| R-03 | `token_version` 迁移 | 改密后全端 re-login | release note 说明 |
| R-04 | profile audit 表增长 | 存储 | 本期仅展示 20 条 |
| R-05 | REQ-0009 change 未创建 | 无法 apply 0009 | M1 前 `/req-opsx REQ-0009` |
| R-07 | 历史 SKU 迁移失败 | 上架阻塞 | acceptance AC-032~035；运营手动选规格 |
| R-08 | REQ-0012 change 未创建 | 无法 apply 0012 | M1 前 `/req-opsx REQ-0012` |
| R-09 | 对象 Key 迁移误删/404 | 媒体不可访问 | dry-run 先行；AC-021~022；备份 MinIO + SQLite |
| R-10 | Sprint 容量四 REQ 满负荷 | 延期 | 21/20 人天；0012 可与 0014 后端并行 |
| R-11 | BUG-0021 change 未创建 | 无法 apply | Sprint 启动前 `/bug-opsx BUG-0021`；可与 0014 前端并行 |
| R-12 | REQ-0016 change 未创建 | 无法 apply 0016 | M1 前 `/req-opsx REQ-0016` |
| R-13 | Sprint 容量纳入 0016 后严重超支 | 延期 M7/M8 | 29/20 人天；或 0016 移至 sprint-004 |
| R-14 | SKU 图库选图 UI 复杂 | 0016 前端延期 | 依赖 REQ-0006 tile_images；可与 0009 并行开发 |
| R-15 | REQ-0017 纳入后容量翻倍 | M8/M9 延期 | 40/20 人天；优先 P0；P2 audit 依赖 0014；P1 依赖 0015 |
| R-16 | effective settings 与 0012 迁移时序 | upload 校验不一致 | 0012 apply 后再调 media 限制；或 P0 与 0012 联调冒烟 |
| R-17 | BUG-0023 与 profile 页并行 touch | merge 冲突 | 与 0014 已 archive 代码小 diff；建议 profile apply 后立即 apply 0023 fix |
| R-18 | BUG-0022/0023 同 touch ProfilePage | merge 冲突 | **先** apply `fix-profile-basic-info-redundant-role-status`，**再** apply `fix-profile-duplicate-save-buttons` |
| R-19 | BUG-0024/0025/0026 与改密弹窗并行 touch | merge 冲突 | 在 `add-admin-password-change` archived 后一次 apply `fix-change-password-modal-errors`（含 toggle + 取消 confirm） |
| R-20 | BUG-0027/0028/0029 与规格页并行 touch | merge 冲突 | 在 `add-tile-spec-management` archived 后一次 apply `fix-tile-spec-admin-ui`；0029 优先（high） |
| R-21 | REQ-0009 视觉 AC 未全关 | archive 后仍缺 PNG | BUG-0027/0028 fix 后补 AC-045/046 并排验收 |
| R-22 | BUG-0037 与规格页 confirm 块 touch | merge 冲突 | 在 `fix-tile-spec-admin-ui` archived 后 apply；仅改 confirm JSX（L329–382），与分页/表单无交叉 |
| R-23 | BUG-0038 与 SKU 弹窗 touch | merge 冲突 | 在 `add-tile-spec-management` archived 后 apply；单行 className，与 0010/0011/0012 无交叉 |
| R-24 | BUG-0039/0040 与 Banner 页 touch | merge 冲突 | 在 `fix-banner-admin-ui` archived 后 apply `fix-banner-list-and-modal-ui`；列表列 + CSS 宽度 |
| R-25 | BUG-0041 与 AdminLayout/Profile touch | merge 冲突 | 在 `add-admin-profile-page` archived 后 apply；与 0022/0023 profile 页无交叉（侧栏 shell） |
| R-26 | BUG-0048 与 BUG-0040 层叠未闭环即 archive | 880px 验收假 pass | **禁止** archive `fix-banner-list-and-modal-ui` 直至 BUG-0048 pass；DevTools Computed 为准 |
| R-27 | REQ-0014 v1.1 与 profile 活动 limit | 文档/实现漂移 | 以 v1.1 acceptance AC-024 为准；archive `fix-profile-activities-display-limit` 合并 spec |
| R-28 | BUG-0042～0047 与 `SystemSettingsPage` 并行 touch | merge 冲突 | 0042/0043/0046/0047 建议同一 PR 顺序 apply；0045 独立 |
| R-29 | BUG-0045 env 与 Docker 默认 MIME 漂移 | upload 校验不一致 | 同步 `.env.docker` + 文档；pytest upload 冒烟 |

## 依赖

```text
REQ-0001-user-login（archived）
  └── auth / JWT / PasswordInput
REQ-0004-admin-home（archived）
  └── AdminLayout / AdminSidebar / AdminUserMenu
        ├── BUG-0021-sidebar-menu-icons-indistinguishable（本 Sprint）
        │     └── fix-sidebar-menu-icons-indistinguishable（proposed）
        │           └── per-menu Lucide icons（collapsed 可区分）
        ├── REQ-0014-profile-page（本 Sprint）
        │     ├── add-admin-profile-page（archived）
        │     ├── BUG-0022-profile-basic-info-redundant-role-status（本 Sprint）
        │     │     └── fix-profile-basic-info-redundant-role-status（proposed）
        │     │           └── 表单移除 role/status 重复字段
        │     └── BUG-0023-profile-duplicate-save-buttons（本 Sprint）
        │           └── fix-profile-duplicate-save-buttons（proposed）
        │                 └── 单「保存修改」CTA（表单 actions 区）
        │     └── BUG-0041-sidebar-user-menu-avatar-missing（本 Sprint）
        │           └── fix-sidebar-user-menu-avatar（archived）
        │                 └── 侧栏 avatar_url img + fallback；Profile 上传后刷新
        │     └── REQ-0014 v1.1 操作记录 limit 5（本 Sprint）
        │           └── fix-profile-activities-display-limit（archived）
        └── REQ-0015-password-change（本 Sprint）
              ├── add-admin-password-change（archived）
              ├── 共用 ChangePasswordModal ← profile 页「修改密码」
              └── BUG-0024-change-password-error-wrong-field（本 Sprint）
              └── BUG-0025-change-password-toggle-button-misalignment（本 Sprint）
              └── BUG-0026-change-password-cancel-confirm-redundant（本 Sprint）
                    └── fix-change-password-modal-errors（proposed）
                          ├── 改密弹窗错误按字段挂载（新密码错误→新密码字段）
                          ├── 显隐切换按钮相对 input 垂直居中（不受 error 影响）
                          └── 关闭弹窗直接关闭、无浏览器二次确认
REQ-0005-brand-management（archived）
  └── Logo upload object_key
REQ-0005-user-management（archived）
  └── 头像 upload object_key
REQ-0006-tile-sku-management（archived）
  └── SKU 图/视频 upload object_key
        ├── REQ-0012-object-storage-key-layout（本 Sprint）
        │     └── update-object-storage-key-layout（待 req-opsx）
        │           └── 影响 avatar / logo / SKU 图视频 Key 形态
        └── TileSkuFormModal（本 Sprint MODIFIED by REQ-0009）
              ├── REQ-0009-tile-spec-management（本 Sprint，archived add）
                    ├── add-tile-spec-management（archived）
                    └── BUG-0027-tile-spec-list-ui-inconsistency（本 Sprint）
                    └── BUG-0028-tile-spec-modal-form-layout（本 Sprint）
                    └── BUG-0029-tile-spec-list-not-refresh-after-create（本 Sprint）
                          └── fix-tile-spec-admin-ui（archived）
                    └── BUG-0037-tile-spec-status-confirm-ui-inconsistency（本 Sprint）
                          └── fix-tile-spec-status-confirm-ui（archived）
                    └── BUG-0038-tile-sku-modal-spec-hint-styling（本 Sprint）
                          └── fix-tile-sku-modal-spec-hint-styling（proposed）
                                └── 规格未匹配提示 form-hint → form-help
REQ-0004-admin-home（archived）
  └── Banner 管理占位 + Dashboard 快捷「新增 Banner」
        └── REQ-0016-banner-management（本 Sprint）
              ├── add-banner-management（archived）
              ├── BUG-0030-banner-list-ui-inconsistency（本 Sprint）
              ├── BUG-0031-banner-modal-image-section-label（本 Sprint）
              ├── BUG-0032-banner-modal-upload-button-label（本 Sprint）
              ├── BUG-0033-banner-modal-form-layout-overflow（本 Sprint）
              ├── BUG-0034-banner-modal-link-selector-combined（本 Sprint）
              ├── BUG-0035-banner-modal-sku-hero-image-no-effect（本 Sprint）
              ├── BUG-0036-banner-modal-datetime-picker（本 Sprint）
              │     └── fix-banner-admin-ui（archived；合并 BUG-0030～0036）
              │           ├── 列表标准分页 + 移除 section-head
              │           ├── 弹窗 scroll / 备注 / Combobox / SKU 主图 / 有效期区间
              │           └── 上传按钮选择/更换/上传中
              ├── BUG-0039-banner-list-display-position-column（本 Sprint）
              ├── BUG-0040-banner-modal-width-too-narrow（本 Sprint）
              │     └── fix-banner-list-and-modal-ui（proposed）
              │           ├── 列表独立「展示位置」列
              │           └── 弹窗 880px 源 CSS（待 BUG-0048 运行时闭环）
              ├── BUG-0048-banner-modal-width-css-cascade-overridden（本 Sprint）
              │     └── fix-banner-modal-width-css-cascade（proposed）
              │           ├── 移除 modal-card 双类名
              │           ├── 运行时 Computed 880px
              │           └── Vitest 完整 CSS 栈断言
              └── 依赖 REQ-0006 tile_images（SKU 详情跳转/图库）
REQ-0004-admin-home（archived）
  └── SYSTEM「系统设置」占位
        └── REQ-0017-system-settings（本 Sprint）
              ├── add-system-settings（in_progress 41/44）
              ├── BUG-0042-system-settings-page-title-v2-suffix（本 Sprint）
              │     └── fix-system-settings-page-title-v2-suffix（proposed）
              ├── BUG-0043-system-settings-duplicate-save-buttons（本 Sprint）
              │     └── fix-system-settings-duplicate-save-buttons（proposed）
              ├── BUG-0045-system-settings-media-format-options-limited（本 Sprint）
              │     └── fix-system-settings-media-format-options（proposed）
              ├── BUG-0046-system-settings-reset-confirm-ui-inconsistency（本 Sprint）
              │     └── fix-system-settings-reset-confirm-ui（proposed）
              ├── BUG-0047-system-settings-save-tip-layout-shift（本 Sprint）
              │     └── fix-system-settings-save-tip-layout-shift（proposed）
              ├── P0 basic+media → effective upload（依赖/联动 REQ-0012）
              ├── P1 security → 联动 REQ-0015-password-change
              └── P2 audit_logs → 联动 REQ-0014-profile-page
```

## 发布计划

- `/sprint-apply sprint-003` 建议编排：`update-object-storage-key-layout` → `fix-sidebar-menu-icons-indistinguishable`（可与 profile 并行）→ `add-admin-profile-page` → `fix-profile-basic-info-redundant-role-status` → `fix-profile-duplicate-save-buttons` → **`fix-sidebar-user-menu-avatar`（BUG-0041）** → **`fix-profile-activities-display-limit`（REQ-0014 v1.1，已 apply）** → `add-admin-password-change` → `fix-change-password-modal-errors` → `add-tile-spec-management` → **`fix-tile-spec-admin-ui`（BUG-0027/0028/0029）** → **`fix-tile-spec-status-confirm-ui`（BUG-0037）** → **`fix-tile-sku-modal-spec-hint-styling`（BUG-0038）** → `add-banner-management` → **`fix-banner-admin-ui`（BUG-0030～0036）** → **`fix-banner-list-and-modal-ui`（BUG-0039/0040）** → **`fix-banner-modal-width-css-cascade`（BUG-0048，须在 list-and-modal archive 前）** → `add-system-settings`（P0 优先，P1–P3 紧随其后或 spill）→ **`fix-system-settings-page-title-v2-suffix`（BUG-0042）** → **`fix-system-settings-duplicate-save-buttons`（BUG-0043）** → **`fix-system-settings-reset-confirm-ui`（BUG-0046）** → **`fix-system-settings-save-tip-layout-shift`（BUG-0047）**（0042/0043/0046/0047 可合并单 PR）→ **`fix-system-settings-media-format-options`（BUG-0045，独立）**
- 完成后 `/sprint-archive sprint-003`
- Docker Compose：profile、改密 token 失效、规格 CRUD、SKU 规格下拉、**规格页 UI/confirm/刷新修复**、**对象 Key 迁移脚本**、Banner CRUD/上线下线、**系统设置 P0+**、迁移后媒体冒烟

## 关联文档

- `issues/bugs/archive/BUG-0021-sidebar-menu-icons-indistinguishable/acceptance.md`
- `issues/bugs/archive/BUG-0022-profile-basic-info-redundant-role-status/acceptance.md`
- `issues/bugs/archive/BUG-0023-profile-duplicate-save-buttons/acceptance.md`
- `issues/bugs/archive/BUG-0024-change-password-error-wrong-field/acceptance.md`
- `issues/bugs/archive/BUG-0025-change-password-toggle-button-misalignment/acceptance.md`
- `issues/bugs/archive/BUG-0026-change-password-cancel-confirm-redundant/acceptance.md`
- `issues/bugs/archive/BUG-0027-tile-spec-list-ui-inconsistency/acceptance.md`
- `issues/bugs/archive/BUG-0028-tile-spec-modal-form-layout/acceptance.md`
- `issues/bugs/archive/BUG-0029-tile-spec-list-not-refresh-after-create/acceptance.md`
- `issues/bugs/archive/BUG-0030-banner-list-ui-inconsistency/acceptance.md`
- `issues/bugs/archive/BUG-0031-banner-modal-image-section-label/acceptance.md`
- `issues/bugs/archive/BUG-0032-banner-modal-upload-button-label/acceptance.md`
- `issues/bugs/archive/BUG-0033-banner-modal-form-layout-overflow/acceptance.md`
- `issues/bugs/archive/BUG-0034-banner-modal-link-selector-combined/acceptance.md`
- `issues/bugs/archive/BUG-0035-banner-modal-sku-hero-image-no-effect/acceptance.md`
- `issues/bugs/archive/BUG-0036-banner-modal-datetime-picker/acceptance.md`
- `issues/bugs/archive/BUG-0037-tile-spec-status-confirm-ui-inconsistency/acceptance.md`
- `issues/bugs/archive/BUG-0038-tile-sku-modal-spec-hint-styling/acceptance.md`
- `issues/bugs/archive/BUG-0039-banner-list-display-position-column/acceptance.md`
- `issues/bugs/archive/BUG-0040-banner-modal-width-too-narrow/acceptance.md`
- `issues/bugs/archive/BUG-0048-banner-modal-width-css-cascade-overridden/acceptance.md`
- `issues/bugs/archive/BUG-0041-sidebar-user-menu-avatar-missing/acceptance.md`
- `issues/bugs/archive/BUG-0042-system-settings-page-title-v2-suffix/acceptance.md`
- `issues/bugs/archive/BUG-0043-system-settings-duplicate-save-buttons/acceptance.md`
- `issues/bugs/archive/BUG-0045-system-settings-media-format-options-limited/acceptance.md`
- `issues/bugs/archive/BUG-0046-system-settings-reset-confirm-ui-inconsistency/acceptance.md`
- `issues/bugs/archive/BUG-0047-system-settings-save-tip-layout-shift/acceptance.md`
- `issues/requirements/archive/REQ-0014-profile-page/requirement.md`
- `issues/requirements/archive/REQ-0015-password-change/requirement.md`
- `issues/requirements/archive/REQ-0009-tile-spec-management/requirement.md`
- `issues/requirements/archive/REQ-0009-tile-spec-management/acceptance.md`
- `issues/requirements/archive/REQ-0009-tile-spec-management/prototype/web/tile-size-management.html`
- `issues/requirements/archive/REQ-0012-object-storage-key-layout/requirement.md`
- `issues/requirements/archive/REQ-0012-object-storage-key-layout/acceptance.md`
- `issues/requirements/archive/REQ-0016-banner-management/requirement.md`
- `issues/requirements/archive/REQ-0016-banner-management/acceptance.md`
- `issues/requirements/archive/REQ-0016-banner-management/prototype/web/banner-management-list.html`
- `issues/requirements/archive/REQ-0017-system-settings/requirement.md`
- `issues/requirements/archive/REQ-0017-system-settings/acceptance.md`
- `issues/requirements/archive/REQ-0017-system-settings/prototype/web/system-settings-basic.html`
- `rules/object-storage.md`
- `docs/07-object-storage-strategy.md`

## 变更记录

| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-06-28 19:08:30 | `/sprint-propose` | 纳入 BUG-0042/0043/0045/0046/0047 + 5 fix-system-settings-* changes；SP 80 / 54 人天 |
| 2026-06-28 19:02:00 | `/sprint-propose` | 纳入 REQ-0014 v1.1 + `fix-profile-activities-display-limit`；SP 75 / 50.5 人天 |
| 2026-06-28 18:49:11 | `/sprint-propose` | 纳入 BUG-0048 + `fix-banner-modal-width-css-cascade`；SP 74 / 50 人天 |
| 2026-06-28 18:41:41 | `/sprint-propose` | 纳入 BUG-0041 + `fix-sidebar-user-menu-avatar`；SP 73 / 49.5 人天 |
| 2026-06-28 17:47:30 | `/sprint-propose` | 纳入 BUG-0039/0040 + `fix-banner-list-and-modal-ui`；SP 72 / 49 人天 |
| 2026-06-28 17:16:29 | `/sprint-propose` | 纳入 BUG-0038 + `fix-tile-sku-modal-spec-hint-styling`；SP 71 / 48.25 人天 |
| 2026-06-28 17:05:08 | `/sprint-propose` | 纳入 BUG-0030/0031/0033～0036；SP 70 / 47.75 人天 |
| 2026-06-28 17:03:05 | `/sprint-propose` | 纳入 BUG-0032 + `fix-banner-admin-ui`；SP 68 / 45.75 人天 |
| 2026-06-28 16:21:17 | `/sprint-propose` | 纳入 BUG-0037 + `fix-tile-spec-status-confirm-ui`；SP 67 / 45.5 人天 |
| 2026-06-28 13:26:21 | `/sprint-propose` | 纳入 BUG-0027/0028/0029 + `fix-tile-spec-admin-ui`；SP 66 / 44.75 人天 |
| 2026-06-28 13:16:02 | `/sprint-propose` | 纳入 BUG-0026（与 BUG-0024/0025 同 change）；SP 64 / 43.5 人天 |
| 2026-06-28 13:06:48 | `/sprint-propose` | 纳入 BUG-0025（与 BUG-0024 同 change）；SP 63 / 43 人天 |
| 2026-06-28 13:00:49 | `/sprint-propose` | 纳入 BUG-0024 + fix-change-password-modal-errors；SP 62 / 42.5 人天 |
| 2026-06-28 12:59:29 | `/sprint-propose` | 纳入 BUG-0022 + fix-profile-basic-info-redundant-role-status；SP 61 / 42 人天 |
| 2026-06-28 12:58:39 | `/sprint-propose` | 纳入 BUG-0023-profile-duplicate-save-buttons + fix-profile-duplicate-save-buttons；SP 60 / 41 人天 |
| 2026-06-28 11:40:00 | `/sprint-propose` | 纳入 REQ-0017-system-settings + add-system-settings；SP 59 / 40 人天 |
| 2026-06-28 11:18:03 | `/sprint-propose` | 纳入 REQ-0016-banner-management；SP 46 / 29 人天 |
| 2026-06-28 10:40:00 | `/bug-opsx` | 创建 fix-sidebar-menu-icons-indistinguishable |
| 2026-06-28 10:35:00 | `/sprint-propose` | 纳入 BUG-0021-sidebar-menu-icons-indistinguishable |
| 2026-06-28 10:27:18 | `/sprint-propose` | 纳入 REQ-0012-object-storage-key-layout |
| 2026-06-28 10:15:31 | `/sprint-propose` | 纳入 REQ-0009-tile-spec-management |
| 2026-06-28 10:04:56 | `/sprint-propose` | 纳入 REQ-0014-profile-page + change add-admin-profile-page |
| 2026-06-28 10:03:15 | `/sprint-propose` | 创建 sprint-003；纳入 REQ-0015-password-change |

## 经验复盘

- 文档：[`docs/knowledge-base/retrospectives/sprint-003-retrospective.md`](../../docs/knowledge-base/retrospectives/sprint-003-retrospective.md)
- 生成：2026-06-28 19:42:56（`/sprint-exps sprint-003`）
