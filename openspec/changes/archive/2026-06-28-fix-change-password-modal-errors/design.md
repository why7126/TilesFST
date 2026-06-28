## Context

- **BUG**: `BUG-0024-change-password-error-wrong-field`、`BUG-0025-change-password-toggle-button-misalignment`、`BUG-0026-change-password-cancel-confirm-redundant`
- **Severity**: medium（0024/0025）、low（0026）
- **Root cause type**: code / frontend-ui（0024 状态映射；0025 css-layout；0026 dirty-close guard）
- **Related REQ**: `REQ-0014-profile-page`
- **Parent capability**: `admin-password-change`（archive `add-admin-password-change`）
- **Target**: `ChangePasswordModal.tsx`、`password-change-modal.css`、`ChangePasswordModal.test.tsx`

### 原型 / 验收优先级（MUST）

```text
1. issues/bugs/archive/BUG-0024-change-password-error-wrong-field/acceptance.md
2. issues/bugs/archive/BUG-0025-change-password-toggle-button-misalignment/acceptance.md
3. issues/bugs/archive/BUG-0026-change-password-cancel-confirm-redundant/acceptance.md
4. issues/bugs/review/BUG-0024-.../screenshots/change-password-error-wrong-field.png
5. issues/bugs/review/BUG-0025-.../screenshots/change-password-toggle-misalignment.png
6. issues/bugs/review/BUG-0026-.../screenshots/change-password-cancel-browser-confirm.png
7. openspec/specs/admin-password-change/spec.md
8. rules/ui-design.md（semantic token、禁止裸 Hex）
```

## Bug Analysis Report

### 现象（BUG-0024）

修改密码弹窗中，新密码相关错误（客户端规则或服务端「过于常见」等）显示在「原密码」输入框下方。

### 现象（BUG-0025）

任一密码字段下方出现 `error-text` 后，该字段「显示/隐藏」按钮下沉，未相对 input 垂直居中；无 error 字段按钮正常。

### 现象（BUG-0026）

表单有输入时，点击「取消」、×、Esc 或遮罩会弹出浏览器原生 `window.confirm`（「当前填写内容尚未保存，确认关闭吗？」），需二次确认才能关闭；与管理端 Brand/User/TileSku 表单弹窗「直接关闭」不一致。

### 复现路径

1. `admin` 或 `employee` 登录，打开「修改密码」弹窗。
2. 填写正确原密码 + 过于常见新密码（或触发客户端新密码规则失败）。
3. 点击「保存修改」→ 错误出现在原密码字段下。

### 影响

- 误导用户修改错误字段；不阻断改密 API。
- BUG-0024 与 BUG-0025 叠加时改密体验更差（错误挂错字段 + 按钮错位）。
- BUG-0026 增加多余交互步骤；全项目唯一 `window.confirm` 用法。
- 无 API/DB/权限影响。

## Root Cause（摘要）

| ID | 结论 |
|---|---|
| RC-001 | 单一 `error` 状态同时承载新密码校验与 API 错误 |
| RC-002 | `error` 仅绑定原密码 `PasswordField`；新密码字段无 `error` prop |
| RC-003 | API catch 未按 `error_code`（40020–40023）分流 |
| RC-004 | Vitest 未覆盖错误字段 DOM 位置 |
| RC-005 | `toggle-pass` 使用 `bottom: 8px` 相对 `.password-field`，error 撑高容器后按钮下沉 |
| RC-006 | 缺少 input + toggle 独立定位包装层 |
| RC-007 | `requestClose` 在 `isDirty` 时调用 `window.confirm`（REQ-0015 原规格交付） |
| RC-008 | 取消/×/Esc/遮罩共用 `requestClose`，均触发 confirm |
| RC-009 | Vitest 断言 dirty 关闭须 confirm，固化错误行为 |

## Goals / Non-Goals

**Goals:**

- 新密码相关错误显示在新密码字段下方（含 `role="alert"`）。
- 原密码错误（40020）显示在原密码字段下方。
- 确认不一致保持 `confirmError` 行为。
- 成功改密、Orval 调用、登出流程无回归。
- Vitest 覆盖字段位置与 toggle DOM 结构。
- 有 error 时各字段 toggle 相对 input 垂直居中（BUG-0025 AC-001～AC-010）。
- 关闭弹窗直接 `onClose()`，无 `window.confirm`（BUG-0026 AC-001～AC-011）。

**Non-Goals:**

- 后端密码策略、错误码、API 路径变更。
- 修改 `admin-password-change` API requirement。
- 将 confirm 替换为 DS Confirm Modal（移除即可）。

## Decisions

### D1：按字段拆分错误状态

- **决策**：`oldPasswordError` + `newPasswordError` + 保留 `confirmError`。
- **理由**：与确认字段已有模式一致；改动面小。
- **备选**：单一 `formError` 顶部 banner — 拒绝（不符合 per-field 表单 UX 与 acceptance）。

### D2：API 错误分流策略

- **决策**：解析 Axios/API 响应 `error_code`：
  - `40020` → `oldPasswordError`
  - `40021` / `40022` / `40023` → `newPasswordError`
  - `42901` → `newPasswordError`（或 intro 区；MUST NOT 仅绑原密码）
  - 未知码 → `newPasswordError` 或 fallback 文案（MUST NOT 默认绑原密码 unless 40020）
- **理由**：与 `error_codes.py` 语义一致；后端已提供细分码。

### D3：客户端校验

- **决策**：`新密码不符合安全策略`、`新密码不能与原密码相同` → `setNewPasswordError`。
- **理由**：文案明确指向新密码。

### D4：测试策略

- 新增用例：客户端策略失败、mock API 40022 → 错误 MUST 在新密码 field 容器内，MUST NOT 在原密码 field 下。
- 更新用例：dirty 表单点击「取消」→ MUST NOT 调用 `window.confirm`；`onClose` MUST 被调用。
- 保留：确认不一致、成功提交用例。
- `cd src/web && pnpm vitest run src/features/admin/components/ChangePasswordModal`

### D5：Spec delta

- MODIFIED `admin-password-change` →「管理端修改密码弹窗」增加 per-field 错误 Scenario、toggle 居中 Scenario；**MODIFIED** 关闭 Scenario（移除脏确认，改为直接关闭）。

### D6：Toggle 定位包装层（BUG-0025）

- **决策**：新增 `.password-input-wrap { position: relative }` 包裹 input + `toggle-pass`；`error-text` 置于 wrap 外。
- **理由**：error 动态出现/消失时不改变 toggle 定位参照；与常见表单内嵌控件模式一致。
- **备选**：`top` 硬算 label 高度 — 拒绝（脆弱）；仅改 `bottom` 为固定 px — 拒绝（仍受 error 影响）。

### D7：移除脏关闭 confirm（BUG-0026）

- **决策**：删除 `isDirty` 与 `window.confirm`；`requestClose` 直接 `onClose()`。
- **理由**：改密无草稿持久化；「取消」即明确放弃；与 Brand/User/TileSku 弹窗一致；REQ-0015 原脏关闭要求通过 spec delta MODIFIED 消化。
- **备选**：仅「取消」直关、×/Esc 仍 confirm — 拒绝（capture 要求全部关闭路径无 confirm；与其它弹窗仍不一致）。

## Risks / Trade-offs

| 风险 | 缓解 |
|------|------|
| `getErrorMessage` 未暴露 error_code | 扩展解析或直接使用 API 响应 body；不改后端契约 |
| 42901 挂载字段争议 | acceptance 允许新密码或 intro；禁止原密码 |
| BUG-0024/0025/0026 同文件 touch | 同一 PR apply；tasks 分列验收 |
| REQ-0015 AC-007 与修复冲突 | delta MODIFIED 关闭 Scenario；tasks 同步 REQ-0015 acceptance 引用 |
| DOM 结构调整影响现有 CSS | 仅移动 toggle 定位上下文；保留 semantic token |

## Migration Plan

- 无数据迁移；前端 deploy 即生效。
- 回滚见 proposal Rollback Plan。

## Open Questions

- 无（BUG-0024/0025/0026 approved，acceptance 已明确）。
