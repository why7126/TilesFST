## ADDED Requirements

### Requirement: 用户列表状态变更二次确认

Web 客户端 MUST 在 `/admin/users` 用户管理列表页为行内「冻结」「解冻」与「删除」操作提供二次确认，以降低误触风险。冻结/解冻确认 MUST 复用与同项目类目/品牌启停确认相同的 modal 结构（`modal-backdrop` + `modal-card` + head/body/footer）。删除确认 MUST 使用与同页/类目/品牌删除一致的 modal 结构，MUST NOT 使用 `window.confirm`。用户点击「冻结」「解冻」或「删除」时 MUST NOT 直接调用 status API；MUST 先展示确认弹窗，仅在用户点击确认主按钮后调用 API。重置密码操作的 confirm UI 不在本 requirement 范围（见 BUG-0017）。本能力 MUST NOT 修改用户 API、数据库、权限边界或 Orval 生成接口。

#### Scenario: 冻结须先确认

- **WHEN** `admin` 在用户列表行点击「冻结」
- **THEN** MUST 展示冻结确认弹窗，MUST NOT 直接调用 `PATCH /api/v1/admin/users/{id}/status`
- **AND** 弹窗标题 MUST 为「冻结用户」或等价文案
- **AND** 正文 MUST 含用户名及冻结后果（如禁止登录）

#### Scenario: 解冻须先确认

- **WHEN** `admin` 在用户列表行点击「解冻」
- **THEN** MUST 展示解冻确认弹窗，MUST NOT 直接调用 status API
- **AND** 正文 MUST 含用户名

#### Scenario: 删除须使用 DS modal

- **WHEN** `admin` 对可删除用户点击「删除」
- **THEN** MUST 展示删除确认 modal，MUST NOT 使用 `window.confirm`
- **AND** 正文 MUST 含用户名及不可恢复提示

#### Scenario: 确认弹窗按钮与取消

- **WHEN** 用户状态变更确认弹窗展示
- **THEN** 底部 MUST 含「取消」与确认主按钮（如「确认冻结」「确认解冻」「删除用户」）
- **WHEN** 用户点击「取消」、遮罩或 ×
- **THEN** MUST 关闭弹窗且 MUST NOT 调用 API 或改变用户状态

#### Scenario: 确认后调用 API 并刷新

- **WHEN** 用户在冻结确认弹窗点击确认
- **THEN** MUST 调用 status API 将用户设为 `disabled` 并 Toast「用户已冻结」，刷新列表
- **WHEN** 用户在解冻确认弹窗点击确认
- **THEN** MUST 调用 status API 将用户设为 `active` 并 Toast「用户已恢复正常」，刷新列表
- **WHEN** 用户在删除确认弹窗点击确认
- **THEN** MUST 软删除用户并 Toast「用户已删除」，刷新列表

#### Scenario: 无障碍与样式

- **WHEN** 用户状态变更确认弹窗展示
- **THEN** MUST 设置 `role="dialog"`、`aria-modal="true"`，标题 MUST 有 `aria-labelledby`
- **AND** TSX MUST NOT 包含裸 Hex；样式 MUST 复用既有 modal 与 user-management CSS

#### Scenario: 用户管理其他能力不回退

- **WHEN** `admin` 执行查询、分页、新建/编辑用户或重置密码
- **THEN** 既有功能 MUST 保持可用
- **AND** 仅 `admin` MUST 可访问用户管理写操作

### Requirement: SKU 列表上下架二次确认

Web 客户端 MUST 在 `/admin/tile-skus` 瓷砖 SKU 列表页为行内「上架」「下架」与「恢复」（或等价上架文案）操作提供二次确认。确认 MUST 复用与同页「删除 SKU」确认框相同的 modal 结构。用户点击上述操作时 MUST NOT 直接调用 publish/unpublish API；MUST 先展示确认弹窗，仅在用户点击确认主按钮后调用 API。本能力 MUST NOT 修改 SKU API、数据库、权限边界或 Orval 生成接口。

#### Scenario: 下架须先确认

- **WHEN** `admin` 或 `employee` 在已上架 SKU 行点击「下架」
- **THEN** MUST 展示下架确认弹窗，MUST NOT 直接调用 `POST /api/v1/admin/tile-skus/{id}/unpublish`
- **AND** 正文 MUST 含 SKU 名称

#### Scenario: 上架或恢复须先确认

- **WHEN** 用户在草稿/待完善/已停用 SKU 行点击「上架」或「恢复」
- **THEN** MUST 展示上架确认弹窗，MUST NOT 直接调用 `POST /api/v1/admin/tile-skus/{id}/publish`
- **AND** 正文 MUST 含 SKU 名称

#### Scenario: SKU 上下架确认弹窗按钮与取消

- **WHEN** SKU 上下架确认弹窗展示
- **THEN** 底部 MUST 含「取消」与确认主按钮
- **WHEN** 用户点击「取消」、遮罩或 ×
- **THEN** MUST 关闭弹窗且 MUST NOT 调用 publish/unpublish API

#### Scenario: 确认后调用 API 并刷新

- **WHEN** 用户在下架确认弹窗点击确认
- **THEN** MUST 调用 unpublish API 并 Toast「SKU 已下架」，刷新列表
- **WHEN** 用户在上架/恢复确认弹窗点击确认
- **THEN** MUST 调用 publish API 并 Toast「SKU 已上架」（或等价），刷新列表

#### Scenario: SKU 删除确认独立

- **WHEN** 用户点击行内「删除」
- **THEN** MUST 仍使用独立「删除 SKU」确认弹窗
- **AND** 上下架 confirm state MUST NOT 与删除 confirm state 共用

#### Scenario: SKU 管理其他能力不回退

- **WHEN** 用户执行查询、分页、新增/编辑 SKU 或删除 SKU
- **THEN** 既有功能 MUST 保持可用
- **AND** BUG-0011 弹窗滚动、BUG-0014 恢复按钮可见性 MUST NOT 回归
