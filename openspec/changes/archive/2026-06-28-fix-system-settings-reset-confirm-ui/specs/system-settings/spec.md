## MODIFIED Requirements

### Requirement: 管理端系统设置页面与分组导航

Web 管理端 MUST 为 `role=admin` 用户提供系统设置能力（路由与 Shell 结构同既有 spec）。「恢复默认」与 dirty 态 Tab 切换放弃未保存修改 MUST 使用页面内 Design System 确认弹窗（`role="dialog"`、`modal-backdrop`、`.btn` / `.btn.primary`），MUST NOT 使用 `window.confirm` 或 `window.alert`。确认后 reset MUST 调用 `POST .../reset`；取消 MUST 关闭 modal 且不调用 API。

#### Scenario: 恢复默认 DS 确认

- **WHEN** `admin` 点击「恢复默认」
- **THEN** MUST 展示 confirm modal（非浏览器原生对话框）
- **AND** 标题与正文 MUST 说明不可撤销
- **AND** MUST 含「取消」与「确认恢复」
- **WHEN** 点击「确认恢复」
- **THEN** MUST 调用 reset API 并刷新表单

#### Scenario: 取消恢复默认

- **WHEN** 恢复默认 modal 已打开且用户点击「取消」或遮罩
- **THEN** modal MUST 关闭且 MUST NOT 调用 reset API

#### Scenario: dirty Tab 切换确认

- **WHEN** 表单 dirty 且用户切换 Tab
- **THEN** MUST 展示 DS confirm modal 询问是否放弃未保存修改
- **AND** MUST NOT 使用 `window.confirm`

#### Scenario: 管理员访问系统设置

- **WHEN** 已登录 `admin` 访问 `/admin/settings`
- **THEN** 系统 MUST 重定向至 `/admin/settings/basic`
