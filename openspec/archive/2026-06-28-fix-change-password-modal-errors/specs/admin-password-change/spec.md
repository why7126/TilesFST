## MODIFIED Requirements

### Requirement: 管理端修改密码弹窗

Web 客户端 MUST 提供 `ChangePasswordModal`（520px 居中），含原密码、新密码、确认新密码三字段；每字段 MUST 支持显隐切换，且显隐切换按钮 MUST 始终相对该字段输入框垂直居中（不受字段下方错误提示影响）；MUST 展示新密码规则提示列表。弹窗 MUST 由 `AdminLayout` 挂载；侧栏 `AdminUserMenu`「密码修改」MUST 打开该弹窗，MUST NOT 使用 placeholder toast。校验失败与 API 错误 MUST 按字段挂载：与新密码相关的错误 MUST 显示在「新密码」字段下方；与原密码验证失败相关的错误 MUST 显示在「原密码」字段下方；确认新密码不一致 MUST 显示在「确认新密码」字段下方。各字段错误区域 MUST 含 `role="alert"`，且对应输入框 MUST 应用错误样式类。

#### Scenario: 菜单打开弹窗

- **WHEN** 用户点击侧栏用户菜单「密码修改」
- **THEN** MUST 打开居中弹窗，无路由跳转
- **AND** MUST 默认聚焦原密码
- **AND** 页面主体 MUST NOT 滚动

#### Scenario: 关闭弹窗无二次确认

- **WHEN** 用户点击 ×、取消、Esc 或遮罩关闭弹窗
- **THEN** MUST 直接关闭弹窗
- **AND** MUST NOT 弹出浏览器原生二次确认对话框（无论表单是否有输入）
- **AND** 再次打开时 MUST 重置表单字段为空

#### Scenario: 提交成功

- **WHEN** API 返回成功
- **THEN** MUST Toast「密码修改成功，请使用新密码重新登录。」
- **AND** MUST 调用 logout 并跳转 `/admin/login`

#### Scenario: openChangePasswordModal 复用

- **WHEN** `REQ-0014` profile 页或未来入口调用 `openChangePasswordModal`
- **THEN** MUST 打开同一弹窗实例
- **AND** MUST NOT 重复实现改密表单

#### Scenario: 新密码客户端校验错误字段位置

- **WHEN** 用户提交时新密码不符合 8–32 位、缺少字母或数字、或与新密码规则不符
- **THEN** MUST 在「新密码」字段下方展示对应错误文案（如「新密码不符合安全策略」）
- **AND** MUST NOT 在「原密码」字段下方展示该文案

#### Scenario: 新密码与原密码相同错误字段位置

- **WHEN** 用户提交时新密码与原密码相同
- **THEN** MUST 在「新密码」字段下方展示「新密码不能与原密码相同」（或等价文案）
- **AND** MUST NOT 在「原密码」字段下方展示该文案

#### Scenario: 服务端弱密码错误字段位置

- **WHEN** API 返回 HTTP 400 且错误码 `40022`（新密码过于常见）
- **THEN** MUST 在「新密码」字段下方展示「新密码过于常见，请更换」（或 API message）
- **AND** MUST NOT 在「原密码」字段下方展示该文案

#### Scenario: 原密码错误字段位置

- **WHEN** API 返回 HTTP 400 且错误码 `40020`（原密码不正确）
- **THEN** MUST 在「原密码」字段下方展示「原密码不正确」（或 API message）
- **AND** MUST NOT 在「新密码」字段下方展示该错误

#### Scenario: 确认新密码不一致字段位置

- **WHEN** 用户提交时「确认新密码」与「新密码」不一致
- **THEN** MUST 在「确认新密码」字段下方展示「两次输入的新密码不一致」
- **AND** MUST NOT 调用改密 API

#### Scenario: 显隐切换按钮不受错误提示影响

- **WHEN** 任一密码字段下方展示错误提示（`role="alert"`）
- **THEN** 该字段「显示/隐藏」切换按钮 MUST 仍相对该字段输入框垂直居中
- **AND** MUST 与同弹窗无错误字段的切换按钮垂直对齐一致
- **AND** 点击切换 MUST 仍可正常切换 input 的 password/text 类型
