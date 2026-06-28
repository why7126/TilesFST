## MODIFIED Requirements

### Requirement: 管理端系统设置页面与分组导航

Web 管理端 MUST 为 `role=admin` 用户提供系统设置能力（路由与 Shell 结构同既有 spec）。保存成功与恢复默认成功反馈 MUST 使用与管理端列表页一致的 fixed toast（`AdminLayout` `.admin-toast-region` + `.admin-toast` 或等价），MUST NOT 在 `summary-grid` 与 `settings-layout` 之间插入文档流条件块导致主内容 layout shift。成功文案 MUST 保持「设置已保存并立即生效」「已恢复默认配置」或等价语义。

#### Scenario: 保存成功无 layout shift

- **WHEN** `admin` 修改字段并点击「保存设置」成功
- **THEN** MUST 展示 fixed toast 成功反馈
- **AND** `settings-layout` MUST NOT 因反馈出现/消失发生垂直位移

#### Scenario: 恢复默认成功无 layout shift

- **WHEN** 恢复默认成功
- **THEN** MUST 满足保存成功无推挤要求

#### Scenario: toast 可访问性

- **WHEN** 成功 toast 展示
- **THEN** MUST 使用 `aria-live="polite"` 与 `role="status"`（与列表页一致）

#### Scenario: 管理员访问系统设置

- **WHEN** 已登录 `admin` 访问 `/admin/settings`
- **THEN** 系统 MUST 重定向至 `/admin/settings/basic`
