# 系统设置规范

## Purpose
定义管理端系统设置五 Tab 页面、分组 API、effective 配置、审计与视觉验收 gate；覆盖 BUG-0042～0047 fix 合并后的 UI/媒体格式行为。
## Requirements
### Requirement: 管理端系统设置页面与分组导航

Web 管理端 MUST 为 `role=admin` 用户提供系统设置能力，路由 MUST 包含 `/admin/settings`（默认重定向至 `/admin/settings/basic`）及子路由 `/admin/settings/basic`、`/admin/settings/security`、`/admin/settings/media`、`/admin/settings/notification`、`/admin/settings/audit`。页面 MUST 采用 Admin Shell（264px Sidebar + 主内容宽度跟随全局 Admin Shell `content-inner` 策略，MUST NOT 通过 `settings-content-inner` 将页面重新锁定为 1080px），结构 MUST 包含 `page-hero`、`summary-grid`、`settings-layout`（`settings-nav` | `settings-panel`）。`page-hero` 眉标（eyebrow）MUST 为 `SYSTEM / SYSTEM SETTINGS`，MUST NOT 含 `/ V2` 或任意产品版本后缀。`settings-nav` MUST 展示 5 个分组 Tab，当前 Tab MUST 品牌金 active 且与 URL 同步。表单 dirty 时 MUST 展示「有未保存修改」提示。MUST 仅在 `settings-panel-footer` 提供一处「保存设置」主 CTA（与「取消」「恢复默认」并列）；MUST NOT 在页头 `settings-hero-actions` 重复渲染「保存设置」。「取消」MUST 恢复 GET 快照。「恢复默认」与 dirty 态 Tab 切换放弃未保存修改 MUST 使用页面内 Design System 确认弹窗（`role="dialog"`、`modal-backdrop`），MUST NOT 使用 `window.confirm` 或 `window.alert`；确认后 reset MUST 调用 `POST .../reset`。保存成功与恢复默认成功反馈 MUST 使用与管理端列表页一致的 fixed toast（`AdminLayout` `.admin-toast-region` + `.admin-toast` 或等价），MUST NOT 在 `summary-grid` 与 `settings-layout` 之间插入文档流条件块导致主内容 layout shift。成功文案 MUST 保持「设置已保存并立即生效」「已恢复默认配置」或等价语义。视觉 MUST 高保真对齐 `issues/requirements/archive/REQ-0017-system-settings/prototype/web/system-settings-{group}.html` CSS Port 策略。

#### Scenario: 系统设置页布局

- **WHEN** `role=admin` 用户访问 `/admin/settings/basic`
- **THEN** 页面 MUST 展示系统设置 page-hero、summary-grid、settings-nav 和 settings-panel
- **AND** 当前 Tab MUST 与 URL 同步
- **AND** 页面内容宽度 MUST 跟随全局 Admin Shell 策略
- **AND** `settings-content-inner` 或等价页面级容器 MUST NOT 将页面重新限制为 1080px。

#### Scenario: 系统设置页操作反馈不推挤布局

- **WHEN** 用户保存设置或恢复默认
- **THEN** 成功反馈 MUST 使用 fixed toast 或等价不改变文档流的反馈方式
- **AND** MUST NOT 在 summary-grid 与 settings-layout 之间插入条件提示块导致 layout shift。

### Requirement: 系统设置分组 API 与持久化

后端 MUST 提供 `/api/v1/admin/system-settings/{group}`，其中 `group` MUST 为 `basic` | `security` | `media` | `notification` | `audit`。GET MUST 返回该分组 **effective** 配置（SQLite `system_settings` 覆盖值 merge env/代码默认值）及只读字段（如 MinIO bucket、Key 规则文案）。PATCH MUST 部分更新可写字段并校验。POST `/api/v1/admin/system-settings/{group}/reset` MUST 恢复该分组默认值。全部接口 MUST 使用 `require_system_admin`。响应 MUST 使用统一 `ApiResponse` 包装。

#### Scenario: 读取基础信息分组

- **WHEN** `admin` 调用 `GET /api/v1/admin/system-settings/basic`
- **THEN** MUST 返回平台名称、语言、时区等 effective 值
- **AND** `employee` 调用 MUST 返回 403

#### Scenario: 更新媒体限制并生效

- **WHEN** `admin` PATCH `media` 分组修改 `max_image_size_mb`
- **THEN** 值 MUST 写入 `system_settings`
- **AND** 后续 `POST /api/v1/admin/uploads/*` MUST 按新上限校验，MUST NOT 要求重启 backend

#### Scenario: 恢复默认

- **WHEN** `admin` POST reset `media` 分组
- **THEN** DB 中该分组覆盖 key MUST 清除或恢复 seed
- **AND** GET MUST 返回 env 默认值

### Requirement: 系统设置分组字段范围

**basic（P0）** MUST 支持：平台名称（2–64 字）、默认语言、默认时区、数据刷新周期、客服邮箱、维护窗口、系统公告（≤500 字）、首页指标卡开关、维护公告开关。**media（P0）** 可写：图片/视频最大 MB、允许 MIME 列表；UI MUST 提供以下可勾选 MIME catalog：**图片** `image/jpeg`、`image/png`、`image/webp`、`image/gif`、`image/svg+xml`、`image/bmp`、`image/tiff`、`image/heic`；**视频** `video/mp4`、`video/quicktime`、`video/x-msvideo`、`video/webm`、`video/x-matroska`、`video/mpeg`、`video/3gpp`。后端 PATCH 校验子集 MUST 与 env `ALLOWED_IMAGE_TYPES` / `ALLOWED_VIDEO_TYPES` 及前端 catalog 对齐。只读：存储桶、Key 生成规则（对齐 REQ-0012 / object-storage spec 文案）。**security（P1）** MUST 支持：密码最小长度 8–32、四项复杂度开关、密码有效期、会话超时（映射 JWT access expire）、首次登录强制改密；P1b 可选登录失败锁定。**notification（P3）** MUST 持久化开关与容量阈值（50–95%）；模板 MUST 只读 + 查看入口；MUST NOT 要求真实发信。**audit（P2）** 可写：日志保留天数 30–3650、导出权限、敏感操作强制记录、脱敏展示；只读：审计范围说明、最近变更列表。

#### Scenario: 媒体 Tab MIME chip 扩展

- **WHEN** `admin` 访问 `/admin/settings/media`
- **THEN** UI MUST 展示至少 8 个图片格式 chip 与 7 个视频格式 chip
- **AND** PATCH 所选 MIME MUST 被 `_validate_media` 接受

#### Scenario: 媒体 Tab 桶路径只读

- **WHEN** `admin` PATCH `media` 分组尝试修改 bucket 或 key 规则字段
- **THEN** 服务端 MUST 忽略或拒绝
- **AND** GET 只读块 MUST 展示当前 `MINIO_BUCKET` 与 Key 规则说明

#### Scenario: PATCH 后 upload 生效

- **WHEN** `admin` PATCH 启用 `image/gif` 并上传 gif 文件
- **THEN** upload MUST 成功（在大小限制内）

#### Scenario: 通知 Tab 无发信

- **WHEN** `admin` 开启「账号冻结通知」并保存
- **THEN** 开关 MUST 持久化
- **AND** 系统 MUST NOT 因此触发邮件或短信

### Requirement: 系统设置变更审计

自 Phase P2 起，每次 system-settings PATCH 或 reset MUST 写入 `audit_logs`（`domain=system_settings`，`action_type` 为 `settings_update` 或 `settings_reset`）。审计 Tab MUST 通过 `GET /api/v1/admin/system-settings/audit/recent` 展示最近变更（默认 10 条：修改人、时间、摘要）。P0/P1 MAY 写最小变更日志或为 P2 预留。

#### Scenario: 保存写入审计

- **WHEN** P2 已启用且 `admin` PATCH `basic` 成功
- **THEN** MUST 插入 `audit_logs` 含 actor、summary、metadata diff
- **AND** 审计 Tab 最近列表 MUST 包含该条目

### Requirement: 系统设置 PNG 视觉验收 Gate

系统设置页视觉对齐 MUST 通过 HTML/PNG golden reference 验收 gate（5 分组）。

#### Scenario: 基础信息 Tab 并排验收

- **WHEN** 团队在 1440×1024 并排对比 `/admin/settings/basic` 与 `system-settings-basic.png`（或 HTML 截图）
- **THEN** Shell、settings-nav、summary-grid、表单、底部操作条 checklist MUST pass
- **AND** 结果 MUST 记录在 change `trace.md`

#### Scenario: 五 Tab checklist

- **WHEN** `/opsx-apply` 完成 P0–P3
- **THEN** 5 分组 HTML/PNG checklist MUST 在 change `trace.md` 逐项记录

