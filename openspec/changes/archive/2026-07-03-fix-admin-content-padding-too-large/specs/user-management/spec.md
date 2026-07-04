## MODIFIED Requirements

### Requirement: 管理端用户管理页面

Web 客户端 MUST 提供 `/admin/users` 页面，视觉 MUST 高保真对齐 `user-management-list.html` / `user-management-list.png` 的 CSS Port 策略。页面 MUST 继承 `AdminLayout`（264px Sidebar、右侧独立滚动、主内容宽度跟随全局 Admin Shell `content-inner` 策略，MUST NOT 重新锁定为 1080px）。当前路由为用户管理时 SYSTEM「用户管理」导航 MUST 为 active。用户列表「用户」列 MUST 在有 `avatar_url` 时展示头像图片，无头像时 MUST 展示 initials 占位；图片加载失败 MUST 稳定回退 initials 且不引起布局跳动。

#### Scenario: 管理员访问用户管理页

- **WHEN** `role=admin` 用户访问 `/admin/users`
- **THEN** MUST 展示页面标题「用户管理」、筛选区、4 指标卡、用户表格与分页
- **AND** 样式 MUST 主要来自 port CSS（`user-management.css`）
- **AND** 页面内容宽度 MUST 跟随全局 Admin Shell 策略，不得通过页面级 max-width 退回 1080px。

#### Scenario: 筛选与搜索交互

- **WHEN** 用户输入关键词或筛选项并点击「搜索」或按回车
- **THEN** 系统 MUST 带 query 重新请求列表并重置到第 1 页
- **WHEN** 用户点击「重置」
- **THEN** MUST 清空筛选并重新加载默认列表。

#### Scenario: 列表字段与分页

- **WHEN** 用户查看表格
- **THEN** MUST 展示用户（头像+用户名+昵称/邮箱）、角色、状态、最后登录、创建时间、操作列
- **AND** 有 `avatar_url` 的用户 MUST 在头像位展示图片而非仅 initials。
