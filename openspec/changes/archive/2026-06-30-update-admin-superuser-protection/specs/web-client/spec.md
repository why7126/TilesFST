---
change_id: update-admin-superuser-protection
capability: web-client
created_at: 2026-06-30 18:26:13
updated_at: 2026-06-30 18:26:13
---

## MODIFIED Requirements

### Requirement: 管理端列表页操作反馈 Toast 布局统一

Web 客户端 MUST 在管理端以下四个列表页对「操作成功/失败且约 3.2 秒后自动消失」的全局反馈使用固定位置 toast（`.admin-toast-region` + `.admin-toast` 或等价共享组件），MUST NOT 在 `page-hero` 或主体内容上方插入文档流 `.admin-notice` 占位节点。toast 样式 MUST 来自管理端共享样式（如 `admin-home.css`），四页视觉与行为 MUST 一致。弹窗内 inline 表单错误 MAY 继续使用 inline 错误文案；`AdminLayout` 侧栏占位 notice 不在本 requirement 范围。修复 MUST NOT 回归品牌 Logo 展示、上传进度及四页 CRUD、筛选、分页、权限边界。受保护账号操作提示或失败反馈也 MUST 使用 fixed toast、title、tooltip 或等价不改变文档流布局的方式，MUST NOT 推挤用户管理页布局。

涵盖路由：

- `/admin/brands`（瓷砖品牌）
- `/admin/users`（用户管理）
- `/admin/tile-categories`（瓷砖类目）
- `/admin/tile-skus`（瓷砖 SKU）

#### Scenario: 用户管理列表操作反馈不推挤页面

- **WHEN** `admin` 在 `/admin/users` 执行冻结、解冻、删除、重置密码、新建/编辑用户成功或列表加载失败等会触发全局反馈的操作
- **THEN** 系统 MUST 展示 fixed toast 反馈
- **AND** 反馈出现和消失 MUST NOT 改变 page-hero、指标卡、筛选区、表格或分页的纵向位置
- **AND** MUST NOT 在列表页主体顶部使用文档流 `.admin-notice` 承载该反馈

#### Scenario: 受保护账号提示不推挤页面

- **WHEN** 用户管理列表展示受保护账号禁用原因
- **THEN** 提示 MUST 使用 `title`、tooltip、fixed toast 或等价方式
- **AND** MUST NOT 插入文档流 notice 推挤 page-hero、筛选区、表格或分页

#### Scenario: 四页 toast 视觉与行为一致

- **WHEN** 对比四页成功 toast（如「品牌已启用」「用户已冻结」「类目已启用」「SKU 已上架」）
- **THEN** 位置、圆角、边框、背景、字号、阴影 MUST 一致
- **AND** 自动消失时长 MUST 为 3200ms
- **AND** MUST 保留 `aria-live="polite"` 与 `role="status"` 可访问性语义

#### Scenario: Design System 约束

- **WHEN** 修复修改 Web UI 样式
- **THEN** MUST 使用既有管理端 CSS 变量与 semantic token
- **AND** MUST NOT 新增裸 Hex 或与 `rules/ui-design.md` 冲突的提示样式

### Requirement: 用户列表状态变更二次确认

Web 客户端 MUST 在 `/admin/users` 用户管理列表页为行内「冻结」「解冻」与「删除」操作提供二次确认，以降低误触风险。冻结/解冻确认 MUST 复用与同项目类目/品牌启停确认相同的 modal 结构（`modal-backdrop` + `modal-card` + head/body/footer）。删除确认 MUST 使用与同页/类目/品牌删除一致的 modal 结构，MUST NOT 使用 `window.confirm`。用户点击「冻结」「解冻」或「删除」时 MUST NOT 直接调用 status API；MUST 先展示确认弹窗，仅在用户点击确认主按钮后调用 API。重置密码 confirm 见「用户重置密码二次确认」requirement。本能力 MUST NOT 修改用户 API、数据库、权限边界或 Orval 生成接口。当目标用户 `is_protected=true` 时，冻结/解冻/删除按钮 MUST 置灰并展示 `protected_reason`，MUST NOT 打开确认弹窗或调用 status API。

#### Scenario: 受保护账号状态按钮置灰

- **GIVEN** 用户列表行 `is_protected=true`
- **WHEN** 管理员查看冻结、解冻或删除操作
- **THEN** 对应按钮 MUST 置灰但仍可见
- **AND** 禁用原因 MUST 来自 `protected_reason`
- **AND** 点击这些按钮 MUST NOT 展示 confirm modal
- **AND** MUST NOT 调用 `PATCH /api/v1/admin/users/{id}/status`

#### Scenario: 冻结须先确认

- **WHEN** `admin` 在普通用户列表行点击「冻结」
- **THEN** MUST 展示冻结确认弹窗，MUST NOT 直接调用 `PATCH /api/v1/admin/users/{id}/status`
- **AND** 弹窗标题 MUST 为「冻结用户」或等价文案
- **AND** 正文 MUST 含用户名及冻结后果（如禁止登录）

#### Scenario: 删除须使用 DS modal

- **WHEN** `admin` 对可删除普通用户点击「删除」
- **THEN** MUST 展示删除确认 modal，MUST NOT 使用 `window.confirm`
- **AND** 正文 MUST 含用户名及不可恢复提示

#### Scenario: 用户管理其他能力不回退

- **WHEN** `admin` 执行查询、分页、新建/编辑用户或重置密码
- **THEN** 既有功能 MUST 保持可用
- **AND** 仅 `admin` MUST 可访问用户管理写操作

### Requirement: 用户重置密码二次确认

Web 客户端 MUST 在 `/admin/users` 用户管理列表页为行内「重置密码」操作提供二次确认。确认 MUST 复用与同项目类目/品牌启停及同页冻结确认相同的 modal 结构（`modal-backdrop` + `modal-card` + head/body/footer）。用户点击「重置密码」时 MUST NOT 使用 `window.confirm`；MUST NOT 直接调用 `POST /api/v1/admin/users/{id}/reset-password`；MUST 先展示确认弹窗，仅在用户点击确认主按钮后调用 API。确认成功后 MUST 继续打开既有结果弹窗展示一次性随机密码（REQ-0005 AC-022）。当目标用户 `is_protected=true` 时，重置密码按钮 MUST 置灰并展示 `protected_reason`，MUST NOT 打开确认弹窗或调用 reset-password API。本能力 MUST NOT 修改数据库或权限边界；本 change 会通过 API schema 扩展 `is_protected` / `protected_reason` 并要求 Orval 同步。

#### Scenario: 受保护账号重置密码按钮置灰

- **GIVEN** 用户列表行 `is_protected=true`
- **WHEN** 管理员查看「重置密码」操作
- **THEN** 按钮 MUST 置灰但仍可见
- **AND** 禁用原因 MUST 来自 `protected_reason`
- **AND** 点击按钮 MUST NOT 展示重置密码确认弹窗
- **AND** MUST NOT 调用 `POST /api/v1/admin/users/{id}/reset-password`

#### Scenario: 重置密码须先确认

- **WHEN** `admin` 在普通用户列表行点击「重置密码」
- **THEN** MUST 展示重置密码确认弹窗，MUST NOT 直接调用 `POST /api/v1/admin/users/{id}/reset-password`
- **AND** MUST NOT 调用 `window.confirm`
- **AND** 弹窗标题 MUST 为「重置密码」或等价文案
- **AND** 正文 MUST 含用户名及重置后果（如将生成新随机密码）

#### Scenario: 用户管理其他 confirm 不回退

- **WHEN** 本修复已合并
- **THEN** 同页冻结/解冻/删除 confirm MUST 保持 BUG-0016 行为
- **AND** 品牌/类目启停 confirm MUST NOT 回归
