---
created_at: 2026-06-28 10:03:15
updated_at: 2026-06-28 19:40:42
title: Sprint 003 发布说明
purpose: 记录 Sprint 003 交付能力与发布注意事项（初稿）
content: 基于 REQ-0014、REQ-0015、REQ-0009、REQ-0012、REQ-0016、REQ-0017、BUG-0021～0029、BUG-0030～0041、BUG-0042～0047、BUG-0048
source: AI 根据迭代范围生成，项目团队确认
update_method: Sprint 完成或范围变更时更新
owner: 项目负责人
status: published
note: workflow-sync — Sprint completed；23/23 Change archived
---

# Sprint 003 发布说明

## 版本信息

| 字段 | 内容 |
|---|---|
| Sprint | sprint-003 |
| 关联需求 | REQ-0014-profile-page、REQ-0015-password-change、REQ-0009-tile-spec-management、REQ-0012-object-storage-key-layout、REQ-0016-banner-management、REQ-0017-system-settings |
| 关联 BUG | BUG-0021-sidebar-menu-icons-indistinguishable、BUG-0022-profile-basic-info-redundant-role-status、BUG-0023-profile-duplicate-save-buttons、BUG-0024-change-password-error-wrong-field、BUG-0025-change-password-toggle-button-misalignment、BUG-0026-change-password-cancel-confirm-redundant、BUG-0027-tile-spec-list-ui-inconsistency、BUG-0028-tile-spec-modal-form-layout、BUG-0029-tile-spec-list-not-refresh-after-create、BUG-0030-banner-list-ui-inconsistency、BUG-0031-banner-modal-image-section-label、BUG-0032-banner-modal-upload-button-label、BUG-0033-banner-modal-form-layout-overflow、BUG-0034-banner-modal-link-selector-combined、BUG-0035-banner-modal-sku-hero-image-no-effect、BUG-0036-banner-modal-datetime-picker、BUG-0037-tile-spec-status-confirm-ui-inconsistency、BUG-0038-tile-sku-modal-spec-hint-styling、BUG-0039-banner-list-display-position-column、BUG-0040-banner-modal-width-too-narrow、BUG-0041-sidebar-user-menu-avatar-missing、BUG-0042-system-settings-page-title-v2-suffix、BUG-0043-system-settings-duplicate-save-buttons、BUG-0045-system-settings-media-format-options-limited、BUG-0046-system-settings-reset-confirm-ui-inconsistency、BUG-0047-system-settings-save-tip-layout-shift、BUG-0048-banner-modal-width-css-cascade-overridden |
| 关联 Change | add-admin-profile-page、add-admin-password-change、add-tile-spec-management、update-object-storage-key-layout、add-banner-management、fix-banner-admin-ui、add-system-settings、fix-sidebar-menu-icons-indistinguishable、fix-profile-basic-info-redundant-role-status、fix-profile-duplicate-save-buttons、fix-change-password-modal-errors、fix-tile-spec-admin-ui、fix-tile-spec-status-confirm-ui、fix-tile-sku-modal-spec-hint-styling、fix-banner-list-and-modal-ui、fix-sidebar-user-menu-avatar、fix-banner-modal-width-css-cascade、fix-profile-activities-display-limit、fix-system-settings-page-title-v2-suffix、fix-system-settings-duplicate-save-buttons、fix-system-settings-media-format-options、fix-system-settings-reset-confirm-ui、fix-system-settings-save-tip-layout-shift |
| 计划周期 | 2026-06-28 10:03:15 ~ 2026-07-12 23:59:59 |

<!-- workflow-sync:release-status:start -->
| 发布状态 | **已发布（Published）** |
<!-- workflow-sync:release-status:end -->

## 计划新增功能

### Web 管理端 — 个人资料（REQ-0014）

- 侧栏「个人资料」进入 `/admin/profile`
- 查看/编辑头像、昵称、邮箱、手机、备注（用户名只读；角色/状态见账号安全卡片）
- 账号安全摘要 + 最近 **5** 条操作记录 timeline（REQ-0014 v1.1）
- inline「资料已更新」保存反馈
- 「修改密码」打开改密弹窗（REQ-0015）

### Web 管理端 — 个人资料操作记录上限（REQ-0014 v1.1）

- `GET /api/v1/profile/me/activities` 默认返回最近 **5** 条（原 20 条）
- 侧栏「最近操作记录」timeline 最多展示 5 条；审计表仍全量写入
- change `fix-profile-activities-display-limit`（已 apply，待 archive）

### Web 管理端 — 修改密码（REQ-0015）

- 侧栏「密码修改」+ profile 页入口打开 520px 居中弹窗
- 原密码 / 新密码 / 确认新密码；改密成功后全端 token 失效

### Web 管理端 — 修改密码弹窗错误字段（BUG-0024）

- 新密码相关校验/API 错误（如「新密码过于常见」）显示在「新密码」字段下方
- 原密码错误仍显示在原密码字段下方；确认不一致行为不变
- 无 API/DB 变更

### Web 管理端 — 修改密码弹窗显隐按钮布局（BUG-0025）

- 字段出现错误提示后，「显示/隐藏」按钮仍相对输入框垂直居中
- 三字段 toggle 视觉对齐一致；显示/隐藏功能无回归
- 与 BUG-0024 同 change `fix-change-password-modal-errors`；无 API/DB 变更

### Web 管理端 — 修改密码弹窗取消确认（BUG-0026）

- 表单有输入时点击「取消」/ × / Esc / 遮罩直接关闭，无浏览器二次确认
- 与管理端 Brand/User/TileSku 表单弹窗关闭行为一致
- 与 BUG-0024/0025 同 change `fix-change-password-modal-errors`；OpenSpec delta MODIFIED 脏关闭 Scenario

### Web 管理端 — 瓷砖规格（REQ-0009）

- OPERATIONS「瓷砖规格」→ `/admin/tile-specs` 主数据页
- 规格 CRUD、启停二次确认、条件删除（对齐品牌页）
- SKU 表单「规格尺寸」改为下拉选择已启用规格
- 历史 SKU `size` 自动匹配 `spec_id`（失败项需运营手动选择）

### Web 管理端 — 瓷砖规格 UX 修复（BUG-0027/0028/0029）

- **BUG-0027**：列表分页对齐用户管理页；尺寸名称列字号与同表协调
- **BUG-0028**：弹窗字段顺序对齐 REQ-0009（宽/长 → 只读尺寸名称 → 厚度/排序 → 备注）；备注 textarea 占满整行；保留 `600×1200mm` 格式
- **BUG-0029**：新增/编辑保存后自动刷新列表与统计卡片，无需 F5
- 合并 change `fix-tile-spec-admin-ui`；无 API/DB 变更

### Web 管理端 — 瓷砖规格 confirm 对齐（BUG-0037）

- 启停/删除二次确认弹窗对齐类目/品牌页 DS modal（× 关闭、`page-desc`、语义化主按钮）
- 停用 confirm 含「停用后前台将不再展示该规格。」；删除主按钮「删除规格」
- change `fix-tile-spec-status-confirm-ui`；无 API/DB 变更

### Web 管理端 — SKU 规格未匹配提示样式（BUG-0038）

- 编辑无 `spec_id` 历史 SKU 时，规格字段下方提示改用 `form-help`（11px `--admin-weak`）
- 提示文案与显隐逻辑不变；选择规格后提示消失
- change `fix-tile-sku-modal-spec-hint-styling`；无 API/DB 变更

### Web 管理端 — Banner 列表展示位置列（BUG-0039）

- Banner 列表第一列仅显示缩略图 + 标题
- 新增独立「展示位置」列（如「首页顶部轮播」）
- 与 `banner-management-list.png` 第一列结构 delta；change `fix-banner-list-and-modal-ui`；无 API/DB 变更

### Web 管理端 — Banner 弹窗宽度对齐 SKU（BUG-0040）

- Banner 新增/编辑弹窗宽度由 640px 调整为 880px，与瓷砖 SKU 弹窗一致
- 保留弹窗纵向滚动与运营备注整行（BUG-0033 无回归）
- MODIFIED `web-client` Banner 弹窗宽度 spec；与 BUG-0039 同 change `fix-banner-list-and-modal-ui`；无 API/DB 变更

### 基础设施 — 对象存储 Key 布局（REQ-0012）

- 图片类前缀 `original/` → `images/`；视频保持 `videos/`
- Key 形态：`{prefix}/{tenant}/{resource_type}/{uuid}.{ext}`（移除 `{YYYY}/{MM}`）
- 4 个 admin uploads API 映射调整；响应形态不变
- 一次性迁移脚本 `scripts/migrate_object_keys.py`（dry-run + apply）
- 同步 `rules/object-storage.md`、`docs/07-object-storage-strategy.md`、`.env.example`

### Web 管理端 — Banner 弹窗 CSS 层叠修复（BUG-0048）

- Banner 弹窗运行时 Computed width 真正为 880px（非仅源 CSS 声明）
- 移除 `BannerFormModal` 冗余 `modal-card` 类，消除 `.admin-shell .modal-card { 520px }` 覆盖
- Vitest 覆盖完整 admin CSS 冲突栈；DevTools Computed 验收
- change `fix-banner-modal-width-css-cascade`；闭环 BUG-0040 回归；须在 `fix-banner-list-and-modal-ui` archive 前 apply；无 API/DB 变更

### Web 管理端 — 侧栏用户菜单头像（BUG-0041）

- 侧栏 `AdminUserMenu` 在有 `avatar_url` 时展示头像图片；无 URL 或加载失败回退 initials
- Profile 页上传头像后，侧栏即时更新（无需硬刷新）
- change `fix-sidebar-user-menu-avatar`；复用 `GET /profile/me`；无 API/Orval 变更

### Web 管理端 — 侧栏菜单图标（BUG-0021）

- collapsed 侧栏各菜单配置 Lucide 语义图标（首页、SKU、品牌、类目、Banner、用户、设置）
- 收起态可仅凭图标形状识别目标菜单
- 无 API/DB 变更；不影响 REQ-0011 折叠/展开行为

### Web 管理端 — 个人资料表单去重（BUG-0022）

- `/admin/profile`「基础资料」表单不再重复展示「所属角色」「账号状态」
- 角色与账号状态仅在「账号安全」卡片展示（AC-011 MODIFIED）
- 无 API/DB 变更

### Web 管理端 — 个人资料保存按钮 UX（BUG-0023）

- `/admin/profile` 仅保留表单底部一处「保存修改」主按钮
- 移除页头重复 CTA；保存、重置、inline save-tip 行为不变
- 无 API/DB 变更

### Web 管理端 — Banner 列表/弹窗 UI 修复（BUG-0030～0036）

合并 change `fix-banner-admin-ui`（`add-banner-management` 之后 apply）：

- **BUG-0030**：Banner 列表移除多余 section 标题与 toolbar；分页对齐用户管理页
- **BUG-0031**：弹窗图片区移除冗余「自定义上传/SKU 主图」首行标题
- **BUG-0032**：上传按钮「选择/更换/上传中」；`hidden` file input
- **BUG-0033**：弹窗 body 可滚动；运营备注 textarea 整行宽度
- **BUG-0034**：SKU/专题关联合并为可搜索 Combobox（`SearchableSelect`）
- **BUG-0035**：「使用 SKU 主图」正确回填预览与 object_key
- **BUG-0036**：有效期改为区间控件，支持精确起止时间
- 无 API schema 变更（0035 可能 touch 列表媒体映射）

### Web 管理端 — Banner 管理（REQ-0016）

- OPERATIONS「Banner 管理」→ `/admin/banners` 列表页（筛选、指标卡、上线下线、删除）
- 新增/编辑弹窗按跳转类型分化：SKU 详情、外部链接、专题页、无跳转
- `banners` + `topics` 种子表；Banner 图 MinIO 上传；SKU 图库引用
- Dashboard「新增 Banner」快捷入口落地
- **不含** 店主端/小程序 Banner 展示消费端

### Web 管理端 — 系统设置（REQ-0017）

- SYSTEM「系统设置」→ `/admin/settings`（5 Tab：基础/安全/媒体/通知/审计）
- P0：平台基础信息 + 媒体上传限制（runtime effective，无需重启）
- P1：密码策略 + JWT 超时（联动改密/建用户）
- P2：`audit_logs` + 审计 Tab（与 profile audit 统一）
- P3：通知开关与阈值（**不含**真实发信引擎）
- 仅 `admin` 可访问；桶/Key 路径只读展示

### Web 管理端 — 系统设置 UI polish（BUG-0042～0047）

`add-system-settings` apply 后或并行 apply 以下 fix changes：

- **BUG-0042**：页眉标 `SYSTEM / SYSTEM SETTINGS`，去除多余 `/ V2`
- **BUG-0043**：仅保留表单底部一处「保存设置」；移除页头重复 CTA（对齐 REQ AC-009）
- **BUG-0045**：媒体 Tab 图片/视频 MIME 选项扩展至 8/7 种；同步 `.env.example`、后端 `_validate_media` 与 pytest
- **BUG-0046**：「恢复默认」确认改用管理端 `modal-backdrop` 样式，替代 `window.confirm`
- **BUG-0047**：保存成功提示改用 `AdminToast`，消除 inline tip 布局抖动

## 数据库变更（计划）

- `users.remark` TEXT NULL
- `profile_activity_logs` 审计表
- `users.token_version`（REQ-0015）
- `tile_specs` 表（REQ-0009）
- `tiles.spec_id` INTEGER FK（REQ-0009）
- `banners` 表、`topics` 种子表（REQ-0016）
- `system_settings` KV 表（REQ-0017）；P2 `audit_logs`（REQ-0017，与 profile audit 协调）

## API 变更（计划）

- `GET/PATCH /api/v1/profile/me`
- `GET /api/v1/profile/me/activities`
- `POST /api/v1/admin/profile/password`
- `GET/POST/PUT/DELETE /api/v1/admin/tile-specs` + enable/disable
- SKU create/update payload 含 `spec_id`（MODIFIED）
- `GET/POST/PUT/DELETE /api/v1/admin/banners` + online/offline + upload-image
- `GET /api/v1/admin/topics`（只读，专题下拉）
- `GET/PATCH/POST reset /api/v1/admin/system-settings/{group}`（REQ-0017）
- 头像 upload 权限放宽至 admin + employee
- 上传 API 生成新 object_key 前缀（REQ-0012；无 schema 变更）
- Orval 重生成（profile/规格相关；0012 通常无需 Orval）

## 部署注意事项

- 需执行 DB migration（remark、audit、token_version、tile_specs、spec_id）
- 改密后对应用户所有 session 失效
- 规格迁移脚本：部署前 backup SQLite；`python scripts/migrate_tile_spec_ids.py --dry-run` 查看匹配结果后再 `--apply`
- **对象 Key 迁移**：部署前 backup SQLite + MinIO；`migrate_object_keys.py --dry-run` 后再 `--apply`；迁移后验证 Logo/头像/SKU/Banner 媒体无 404
- MinIO 单桶策略不变

## 不在本 Sprint

- 忘记密码
- 管理员 reset-password 流程变更
- 店主端个人资料
- 规格 PNG Golden Reference 导出（非阻塞，apply 前补齐）
- `files/`、`audios/` 实际上传 API（REQ-0012 仅规范预留）
- REQ-0011 折叠/展开交互变更（BUG-0021 仅补图标）
- 店主端/小程序 Banner 展示（REQ-0016 Out of Scope）
- 系统设置通知真实发信、审计导出下载（REQ-0017 Out of Scope）
