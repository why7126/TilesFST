## MODIFIED Requirements

### Requirement: 管理端用户表单弹窗

Web 客户端 MUST 提供添加/编辑用户弹窗，视觉对齐 `user-management-modal.html` / `user-management-modal.png`。弹窗字段 MUST 为单列，顺序固定为：用户名、头像、昵称、角色。弹窗 MUST NOT 展示状态字段。头像区 MUST 支持选择文件后立即上传、上传进度反馈、上传成功预览更新与失败重试，行为 MUST 对齐已修复的品牌 Logo 弹窗（`idle → uploading → uploaded / failed` 状态机）。编辑时 MUST 回显已有头像图片。添加用户成功且 API 返回 `initial_password` 时，Web 客户端 MUST 展示一次性密码结果弹窗，并 MUST 提供可靠复制、成功反馈和剪贴板失败 fallback。

#### Scenario: 添加用户弹窗

- **WHEN** 用户点击「添加用户」
- **THEN** MUST 打开弹窗，用户名可编辑且必填
- **AND** 提交成功后 MUST Toast「用户已创建」
- **AND** 若 API 返回 `initial_password` MUST 展示一次性密码弹窗与复制按钮

#### Scenario: 创建用户后复制初始密码成功

- **GIVEN** `admin` 在 `/admin/users` 创建新用户成功
- **AND** API 返回 `data.initial_password`
- **WHEN** 一次性密码结果弹窗展示，管理员点击「复制密码」
- **THEN** Web 客户端 MUST 调用 Clipboard API 将当前弹窗展示的完整 `initial_password` 写入剪贴板
- **AND** MUST 展示复制成功反馈
- **AND** 粘贴内容 MUST 与弹窗展示密码一致

#### Scenario: 创建用户后剪贴板不可用 fallback

- **GIVEN** 一次性初始密码弹窗已展示
- **AND** 当前浏览器不支持 Clipboard API、剪贴板权限被拒绝，或 `writeText` 失败
- **WHEN** 管理员点击「复制密码」
- **THEN** Web 客户端 MUST NOT 静默失败
- **AND** MUST 展示失败提示或手动复制指引
- **AND** SHOULD focus/select 当前一次性密码文本，帮助管理员手动复制

#### Scenario: 编辑用户弹窗

- **WHEN** 用户点击「编辑」
- **THEN** 用户名字段 MUST 只读
- **AND** 已有头像 MUST 展示图片预览
- **AND** 提交成功后 MUST Toast「用户信息已更新」

#### Scenario: 更换头像上传与预览

- **WHEN** admin 在弹窗点击「更换头像」并选择合法 JPG/PNG/WebP
- **THEN** 系统 MUST 立即触发上传并进入 uploading 状态
- **AND** MUST 展示进度条或等价进度反馈
- **AND** 上传成功后 MUST 更新弹窗头像预览与待保存的 `avatar_object_key`
- **AND** 上传中 MUST 禁止提交保存
- **AND** 上传失败 MUST 展示错误并允许重试

#### Scenario: 保存后头像持久可见

- **WHEN** admin 更换头像并保存用户
- **THEN** 再次打开编辑弹窗 MUST 回显最新头像
- **AND** 用户列表 MUST 展示最新头像图片

### Requirement: 管理端用户列表行操作

用户列表操作列 MUST 提供：编辑、重置密码、冻结/解冻、删除。已冻结用户 MUST 显示「解冻」；仅 `last_login_at` 为空的用户 MUST 启用「删除」，否则删除按钮 MUST 置灰。当 `user.is_protected=true` 时，编辑、重置密码、冻结/解冻、删除按钮 MUST 保留但置灰，MUST 使用 `protected_reason` 作为 title、tooltip 或等价原因提示，且 MUST NOT 打开确认弹窗或调用对应 API。前端 MUST NOT 通过硬编码 `admin` 或 role 判断保护状态。重置密码成功且 API 返回 `data.password` 时，Web 客户端 MUST 展示一次性密码结果弹窗，并 MUST 提供可靠复制、成功反馈和剪贴板失败 fallback。一次性密码关闭后 MUST NOT 再次展示同一密码。

#### Scenario: 重置密码交互

- **WHEN** 用户确认重置密码且 API 成功
- **THEN** MUST 在二次弹窗展示一次性密码与复制按钮
- **AND** 关闭后 MUST NOT 再次展示同一密码

#### Scenario: 重置密码后复制新随机密码成功

- **GIVEN** `admin` 对非受保护用户确认重置密码成功
- **AND** API 返回 `data.password`
- **WHEN** 一次性密码结果弹窗展示，管理员点击「复制密码」
- **THEN** Web 客户端 MUST 调用 Clipboard API 将当前弹窗展示的完整 `password` 写入剪贴板
- **AND** MUST 展示复制成功反馈
- **AND** 粘贴内容 MUST 与弹窗展示密码一致

#### Scenario: 重置密码后剪贴板不可用 fallback

- **GIVEN** 一次性随机密码弹窗已展示
- **AND** 当前浏览器不支持 Clipboard API、剪贴板权限被拒绝，或 `writeText` 失败
- **WHEN** 管理员点击「复制密码」
- **THEN** Web 客户端 MUST NOT 静默失败
- **AND** MUST 展示失败提示或手动复制指引
- **AND** SHOULD focus/select 当前一次性密码文本，帮助管理员手动复制

#### Scenario: 一次性密码安全边界

- **WHEN** Web 客户端展示创建用户或重置密码后的一次性密码结果弹窗
- **THEN** 弹窗 MUST 继续提示「关闭后不可再次查看」或等价风险说明
- **AND** Web 客户端 MUST NOT 新增再次查询一次性明文密码的接口或入口
- **AND** Web 客户端 MUST NOT 将一次性明文密码写入 localStorage、sessionStorage、URL、日志、审计事件或长期文档

#### Scenario: 冻结解冻 Toast

- **WHEN** 冻结或解冻成功
- **THEN** MUST 分别 Toast「用户已冻结」「用户已恢复正常」

#### Scenario: 删除 Toast

- **WHEN** 软删除成功
- **THEN** MUST Toast「用户已删除」
