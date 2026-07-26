---
change_id: fix-user-create-validation-message-unclear
capability: web-client
created_at: 2026-06-30 18:35:35
updated_at: 2026-06-30 18:35:35
---

## ADDED Requirements

### Requirement: 用户创建校验错误提示修复

Web 客户端 MUST 修复 `/admin/users` 添加用户弹窗的校验失败提示缺陷。创建用户失败时，弹窗或等价错误区域 MUST 优先展示后端统一错误响应中的 `message`，并 MUST 让管理员能够判断需要修改「用户名」字段。该修复 MUST 保持用户管理弹窗既有 CSS Port、Design System Token、头像上传、成功 Toast、一次性密码弹窗和列表刷新行为不回归。

#### Scenario: 用户名长度不足展示明确错误

- **WHEN** 管理员打开 `/admin/users` 添加用户弹窗
- **AND** 输入 `username="abc"` 与合法 role 后提交
- **THEN** 页面 MUST 展示来自 API 或等价映射的明确中文错误
- **AND** 错误文案 MUST 指向用户名长度不足
- **AND** 页面 MUST NOT 仅展示无法定位字段的泛化兜底失败文案

#### Scenario: 其他用户名格式错误展示明确错误

- **WHEN** 管理员分别提交 `username="1abc"`、`username="ab__cd"` 或保留字
- **THEN** 页面 MUST 展示对应用户名规则错误
- **AND** 管理员 MUST 能判断应修改用户名字段

#### Scenario: 错误修正后可成功创建

- **GIVEN** 添加用户弹窗已展示用户名校验错误
- **WHEN** 管理员将用户名改为合法且未重复的值并重新提交
- **THEN** 系统 MUST 创建用户成功
- **AND** MUST Toast「用户已创建」
- **AND** 若 API 返回 `initial_password`，一次性密码弹窗 MUST 正常展示

#### Scenario: 弹窗布局不回归

- **WHEN** 添加用户弹窗展示校验错误
- **THEN** 弹窗宽度、字段顺序、按钮区、头像上传区域和遮罩布局 MUST 保持用户管理弹窗既有视觉约束
- **AND** 新增或变更样式 MUST 使用 semantic token 或既有 CSS 变量，MUST NOT 新增裸 Hex
