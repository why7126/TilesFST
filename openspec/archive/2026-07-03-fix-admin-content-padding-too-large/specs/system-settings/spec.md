## MODIFIED Requirements

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
