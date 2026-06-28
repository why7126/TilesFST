## MODIFIED Requirements

### Requirement: 管理端个人资料页面

Web 客户端 MUST 提供 `/admin/profile` 页面，视觉 MUST 高保真对齐 `issues/requirements/archive/REQ-0014-profile-page/prototype/web/profile-page.html` 与 `profile-page.png` 的 CSS Port 策略。页面 MUST 复用 `AdminLayout`。`admin` 与 `employee` MUST 可访问；`store_owner` MUST NOT 访问。页面 MUST 仅保留 **一处**「保存修改」主 CTA，MUST 位于「基础资料」卡片底部 `profile-form-actions` 与「重置」并列；MUST NOT 在页头 `profile-page-head` 与表单底部重复渲染相同主按钮。

#### Scenario: 访问个人资料页

- **WHEN** 已登录 `admin` 或 `employee` 访问 `/admin/profile`
- **THEN** MUST 展示眉标 `SYSTEM / PROFILE`、标题「个人资料」、两列 layout（主卡片 + 侧栏卡片）
- **AND** 样式 MUST 主要来自 port CSS（如 `profile-page.css`）

#### Scenario: 单保存入口

- **WHEN** 用户查看 `/admin/profile` 页面
- **THEN** 全页 MUST 仅存在 **1** 个 accessible name 为「保存修改」的主按钮
- **AND** 该按钮 MUST 位于「基础资料」卡片底部 `profile-form-actions`
- **AND** 页头 `profile-page-head` MUST NOT 渲染「保存修改」主按钮

#### Scenario: 表单字段与只读规则

- **WHEN** 用户查看主卡片表单
- **THEN** MUST 按顺序展示：用户名（只读）、昵称、联系邮箱、手机、备注
- **AND** MUST NOT 在主卡片表单内展示所属角色、账号状态（二者仅在账号安全卡片展示）
- **AND** 昵称 MUST 必填 2–32 字符

#### Scenario: 保存 inline 成功提示

- **WHEN** 用户点击「保存修改」并成功
- **THEN** MUST 在表单底部 inline 展示「资料已更新」及时间戳
- **AND** MUST NOT 使用全局 toast 承载该成功反馈

#### Scenario: 重置表单

- **WHEN** 用户点击「重置」
- **THEN** MUST 恢复最近一次 GET profile 快照

#### Scenario: 修改密码入口

- **WHEN** 用户点击账号安全卡片「修改密码」
- **THEN** MUST 打开 REQ-0015 密码修改弹窗（共用 hook）
- **AND** MUST NOT 导航至独立改密路由

#### Scenario: 操作记录 timeline

- **WHEN** 页面加载
- **THEN** MUST 展示最近 20 条 activities timeline（标题、时间、摘要）
- **AND** 无数据时 MUST 展示空态文案
