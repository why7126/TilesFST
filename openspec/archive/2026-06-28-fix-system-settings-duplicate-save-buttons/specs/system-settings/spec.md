## MODIFIED Requirements

### Requirement: 管理端系统设置页面与分组导航

Web 管理端 MUST 为 `role=admin` 用户提供系统设置能力，路由 MUST 包含 `/admin/settings`（默认重定向至 `/admin/settings/basic`）及子路由 `/admin/settings/basic`、`/admin/settings/security`、`/admin/settings/media`、`/admin/settings/notification`、`/admin/settings/audit`。页面 MUST 采用 Admin Shell（264px Sidebar + 主内容 max-width 1080px），结构 MUST 包含 `page-hero`、`summary-grid`、`settings-layout`（`settings-nav` | `settings-panel`）。`settings-nav` MUST 展示 5 个分组 Tab，当前 Tab MUST 品牌金 active 且与 URL 同步。表单 dirty 时 MUST 展示「有未保存修改」提示。MUST 仅在 `settings-panel-footer` 提供一处「保存设置」主 CTA（与「取消」「恢复默认」并列）；MUST NOT 在页头 `settings-hero-actions` 重复渲染「保存设置」。「取消」MUST 恢复 GET 快照；「恢复默认」MUST 二次确认后 reset。保存成功 MUST inline 提示（save-tip 风格，MUST NOT 仅用 toast）。视觉 MUST 高保真对齐 prototype CSS Port 策略。

#### Scenario: 单保存入口

- **WHEN** `admin` 访问任意 `/admin/settings/{tab}` 且表单 dirty
- **THEN** 全页 MUST 仅存在 **1** 个 accessible name 为「保存设置」的 button
- **AND** 该按钮 MUST 位于 `settings-panel-footer`
- **AND** 页头 MUST NOT 渲染「保存设置」

#### Scenario: 管理员访问系统设置

- **WHEN** 已登录 `admin` 访问 `/admin/settings`
- **THEN** 系统 MUST 重定向至 `/admin/settings/basic`
- **AND** 侧栏「系统设置」MUST 为 active

#### Scenario: Tab 切换与 dirty 提示

- **WHEN** 管理员修改可写字段但未保存
- **THEN** MUST 展示「有未保存修改」
