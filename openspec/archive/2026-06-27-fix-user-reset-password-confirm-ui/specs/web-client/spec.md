## ADDED Requirements

### Requirement: 用户重置密码二次确认

Web 客户端 MUST 在 `/admin/users` 用户管理列表页为行内「重置密码」操作提供二次确认。确认 MUST 复用与同项目类目/品牌启停及同页冻结确认相同的 modal 结构（`modal-backdrop` + `modal-card` + head/body/footer）。用户点击「重置密码」时 MUST NOT 使用 `window.confirm`；MUST NOT 直接调用 `POST /api/v1/admin/users/{id}/reset-password`；MUST 先展示确认弹窗，仅在用户点击确认主按钮后调用 API。确认成功后 MUST 继续打开既有结果弹窗展示一次性随机密码（REQ-0005 AC-022）。本能力 MUST NOT 修改用户 API、数据库、权限边界或 Orval 生成接口。

#### Scenario: 重置密码须先确认

- **WHEN** `admin` 在用户列表行点击「重置密码」
- **THEN** MUST 展示重置密码确认弹窗，MUST NOT 直接调用 `POST /api/v1/admin/users/{id}/reset-password`
- **AND** MUST NOT 调用 `window.confirm`
- **AND** 弹窗标题 MUST 为「重置密码」或等价文案
- **AND** 正文 MUST 含用户名及重置后果（如将生成新随机密码）

#### Scenario: 确认弹窗按钮与取消

- **WHEN** 重置密码确认弹窗展示
- **THEN** 底部 MUST 含「取消」与主按钮「确认重置」（或等价）
- **WHEN** 用户点击「取消」、遮罩或 ×
- **THEN** MUST 关闭弹窗且 MUST NOT 调用 reset-password API
- **AND** MUST NOT 打开结果密码展示弹窗

#### Scenario: 确认后调用 API 并展示结果

- **WHEN** 用户在重置密码确认弹窗点击「确认重置」
- **THEN** MUST 调用 reset-password API
- **AND** MUST Toast「密码已重置」（或等价）
- **AND** MUST 打开结果弹窗展示一次性密码与复制按钮
- **AND** 关闭结果弹窗后 MUST NOT 再次展示同一密码

#### Scenario: 无障碍与样式

- **WHEN** 重置密码确认弹窗展示
- **THEN** MUST 设置 `role="dialog"`、`aria-modal="true"`，标题 MUST 有 `aria-labelledby`
- **AND** 正文 MUST 使用 `page-desc`（或等价 semantic class）
- **AND** TSX MUST NOT 包含裸 Hex；样式 MUST 复用既有 modal 与 user-management CSS

#### Scenario: 用户管理其他 confirm 不回退

- **WHEN** 本修复已合并
- **THEN** 同页冻结/解冻/删除 confirm MUST 保持 BUG-0016 行为
- **AND** 品牌/类目启停 confirm MUST NOT 回归
