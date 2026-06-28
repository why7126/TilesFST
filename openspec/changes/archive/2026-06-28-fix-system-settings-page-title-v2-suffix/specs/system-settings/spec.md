## MODIFIED Requirements

### Requirement: 管理端系统设置页面与分组导航

Web 管理端 MUST 为 `role=admin` 用户提供系统设置能力，路由 MUST 包含 `/admin/settings`（默认重定向至 `/admin/settings/basic`）及子路由 `/admin/settings/basic`、`/admin/settings/security`、`/admin/settings/media`、`/admin/settings/notification`、`/admin/settings/audit`。页面 MUST 采用 Admin Shell（264px Sidebar + 主内容 max-width 1080px），结构 MUST 包含 `page-hero`、`summary-grid`、`settings-layout`（`settings-nav` | `settings-panel`）。`page-hero` 眉标（eyebrow）MUST 为 `SYSTEM / SYSTEM SETTINGS`，MUST NOT 含 `/ V2` 或任意产品版本后缀。`settings-nav` MUST 展示 5 个分组 Tab，当前 Tab MUST 品牌金 active 且与 URL 同步。表单 dirty 时 MUST 展示「有未保存修改」提示。MUST 提供页头与底部两处「保存设置」、 「取消」（恢复 GET 快照）、 「恢复默认」（二次确认后 reset）。保存成功 MUST inline 提示（save-tip 风格，MUST NOT 仅用 toast）。视觉 MUST 高保真对齐 `issues/requirements/archive/REQ-0017-system-settings/prototype/web/system-settings-{group}.html` CSS Port 策略。

#### Scenario: 管理员访问系统设置

- **WHEN** 已登录 `admin` 访问 `/admin/settings`
- **THEN** 系统 MUST 重定向至 `/admin/settings/basic`
- **AND** 侧栏「系统设置」MUST 为 active
- **AND** `settings-nav` 中「基础信息」MUST 为 active
- **AND** 页头眉标 MUST 为 `SYSTEM / SYSTEM SETTINGS`

#### Scenario: 运营不可见系统设置

- **WHEN** 已登录 `employee` 查看 Sidebar SYSTEM 分组
- **THEN** MUST NOT 展示「系统设置」菜单项
- **AND** 直链 `/admin/settings/basic` MUST 返回 forbidden/403

#### Scenario: Tab 切换与 dirty 提示

- **WHEN** 管理员修改可写字段但未保存
- **THEN** MUST 展示「有未保存修改」
- **AND** 切换 Tab 前 MUST confirm 放弃未保存或阻止切换（以实现为准，design D5 为 confirm）
