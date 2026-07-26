## ADDED Requirements

### Requirement: 品牌列表启停二次确认

Web 客户端 MUST 在 `/admin/brands` 品牌列表页为行内「启用」与「停用」操作提供二次确认，以降低误触风险。启停确认 MUST 复用与同页「删除品牌」确认框相同的 modal 结构（`modal-backdrop` + `modal-card` + head/body/footer）。用户点击「启用」或「停用」时 MUST NOT 直接调用 enable/disable API；MUST 先展示确认弹窗，仅在用户点击「确认启用」或「确认停用」后调用 API。删除操作 MUST 仍使用独立「删除品牌」确认弹窗，MUST NOT 与启停确认合并。本能力 MUST NOT 修改品牌 API、数据库、权限边界或 Orval 生成接口。

#### Scenario: 停用须先确认

- **WHEN** 用户在品牌列表行点击「停用」
- **THEN** MUST 展示停用确认弹窗，MUST NOT 直接调用 `POST /api/v1/admin/brands/{id}/disable`
- **AND** 弹窗标题 MUST 为「停用品牌」
- **AND** 正文 MUST 为「确认停用品牌「{name}」？停用后前台将不再展示该品牌。」（`{name}` 为该行品牌名称）

#### Scenario: 启用须先确认

- **WHEN** 用户在品牌列表行点击「启用」
- **THEN** MUST 展示启用确认弹窗，MUST NOT 直接调用 `POST /api/v1/admin/brands/{id}/enable`
- **AND** 弹窗标题 MUST 为「启用品牌」
- **AND** 正文 MUST 为「确认启用品牌「{name}」？」

#### Scenario: 确认弹窗按钮与取消

- **WHEN** 启停确认弹窗展示
- **THEN** 底部 MUST 含「取消」与「确认停用」或「确认启用」（主按钮）
- **WHEN** 用户点击「取消」、遮罩、× 或 ESC
- **THEN** MUST 关闭弹窗且 MUST NOT 改变品牌状态或调用 API

#### Scenario: 确认后调用 API 并刷新

- **WHEN** 用户在停用确认弹窗点击「确认停用」
- **THEN** MUST 调用 disable API 并展示 Toast「品牌已停用」，并刷新列表与指标卡 summary
- **WHEN** 用户在启用确认弹窗点击「确认启用」
- **THEN** MUST 调用 enable API 并展示 Toast「品牌已启用」，并刷新列表与指标卡 summary

#### Scenario: 删除确认独立

- **WHEN** 用户点击行内「删除」
- **THEN** MUST 仍使用独立「删除品牌」确认弹窗
- **AND** 启停确认 state MUST NOT 与删除确认 state 共用

#### Scenario: 无障碍与样式

- **WHEN** 启停确认弹窗展示
- **THEN** MUST 设置 `role="dialog"`、`aria-modal="true"`，标题 MUST 有 `aria-labelledby`
- **AND** TSX MUST NOT 包含裸 Hex；样式 MUST 复用既有 modal 与 brand-management CSS Port

#### Scenario: 品牌管理其他能力不回退

- **WHEN** 用户执行查询、重置、分页、新增、编辑、删除品牌或上传 Logo
- **THEN** 既有功能 MUST 保持可用
- **AND** `admin` 与 `employee` MUST 可维护品牌
