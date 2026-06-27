## ADDED Requirements

### Requirement: 管理端 Sidebar 展开/收起

Web 客户端 MUST 在管理端 `AdminLayout` 包裹的全部 `/admin/*`  authenticated 页面支持 Sidebar **expanded** 与 **collapsed** 两种状态。状态 MUST 由 `AdminLayout`（或等价 Context）统一管理并传入 `AdminSidebar`；首次访问 MUST 默认为 **expanded**。用户切换后 MUST 将偏好写入 `localStorage`（key：`admin-sidebar-collapsed`）；刷新或路由切换后 MUST 恢复一致。折叠交互 MUST 仅在视口宽度 **>1023px** 生效；≤1023px MUST 沿用现有 responsive 布局且 MUST NOT 展示或 MUST 禁用折叠 chevron。MUST NOT 变更店主端 `Sidebar` 筛选栏。切换 Sidebar 状态 MUST NOT 改变 nav 路由行为、卸载当前页面或丢失 `AdminLayout` 内 notice 等局部 UI 状态。

#### Scenario: 状态持久化

- **WHEN** 用户在桌面端收起 Sidebar 并刷新页面或导航至其他 `/admin/*` 路由
- **THEN** Sidebar MUST 保持 collapsed
- **AND** `localStorage['admin-sidebar-collapsed']` MUST 反映该偏好

#### Scenario: 默认 expanded

- **WHEN** 用户首次访问且无 localStorage 记录
- **THEN** Sidebar MUST 为 expanded（264px）

#### Scenario: 移动端不启用折叠

- **WHEN** 视口宽度 ≤1023px
- **THEN** MUST NOT 与桌面 collapsed 72px 模型冲突
- **AND** 折叠 chevron MUST 隐藏或禁用

#### Scenario: 导航行为无回归

- **WHEN** 用户在 collapsed 态点击 nav 项
- **THEN** MUST 与 expanded 态相同执行 `navigate` 或 placeholder 逻辑

#### Scenario: 自动化测试

- **WHEN** 运行 vitest 覆盖 AdminLayout 或 AdminSidebar
- **THEN** MUST 断言 chevron 切换 `data-sidebar-state` 或等价 class
- **AND** MUST 断言 `aria-expanded` 与 localStorage 读写
