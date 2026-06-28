## Why

[BUG-0024-change-password-error-wrong-field](issues/bugs/archive/BUG-0024-change-password-error-wrong-field/)、[BUG-0025-change-password-toggle-button-misalignment](issues/bugs/archive/BUG-0025-change-password-toggle-button-misalignment/) 与 [BUG-0026-change-password-cancel-confirm-redundant](issues/bugs/archive/BUG-0026-change-password-cancel-confirm-redundant/) 已评审通过，同属 `ChangePasswordModal` 表单 UX 缺陷：

1. **BUG-0024**：新密码相关校验/API 错误错误显示在「原密码」字段下方，误导用户。
2. **BUG-0025**：字段下方出现 `error-text` 后，「显示/隐藏」按钮因 `bottom: 8px` 相对含 error 的 `.password-field` 定位而垂直下沉。
3. **BUG-0026**：表单有输入时点击「取消」/ × / Esc / 遮罩弹出浏览器原生 `window.confirm`，与管理端其它表单弹窗不一致。

根据项目规则，已交付能力上的缺陷 MUST 使用 `fix-*` change 修复；三 BUG 共享同一组件与 CSS，合并于本 change 以减少重复 touch。

## What Changes

- 拆分 `ChangePasswordModal` 错误状态：`oldPasswordError` 与 `newPasswordError`（或等价命名）。
- 客户端新密码规则校验与服务端新密码类错误（40021/40022/40023）写入新密码字段；原密码错误（40020）写入原密码字段。
- 确认新密码不一致继续使用 `confirmError`（无回归）。
- 更新 `ChangePasswordModal.test.tsx`：断言错误文案出现在对应字段容器内。
- **BUG-0025**：为 input + `toggle-pass` 增加相对定位包装层；`error-text` 不参与 toggle 定位；更新 `password-change-modal.css`。
- **BUG-0026**：移除 `isDirty` + `window.confirm`；`requestClose` 直接 `onClose()`；MODIFIED spec 脏关闭 Scenario。
- **不** 变更 API 契约、密码策略、后端错误码、Orval、Docker、成功改密登出流程。

## Capabilities

### New Capabilities

（无新 capability 目录。）

### Modified Capabilities

- `admin-password-change`：MODIFIED「管理端修改密码弹窗」— 校验/API 错误 MUST 按字段挂载；显隐切换按钮 MUST 始终相对输入框垂直居中（不受 error 影响）；关闭 MUST 直接关闭、无浏览器二次确认。

## Impact

| 影响面 | 说明 |
|---|---|
| Web 管理端 | `ChangePasswordModal.tsx`、`password-change-modal.css`、`ChangePasswordModal.test.tsx` |
| 店主端 / 小程序 | 无 |
| 后端 / API / DB / Orval | 无 |
| 父需求 | REQ-0014-profile-page（改密弹窗入口） |
| 关联 BUG | BUG-0024（错误字段映射）、BUG-0025（toggle 布局）、BUG-0026（取消 confirm） |
| 测试 | vitest ChangePasswordModal；BUG-0024 AC-001～AC-010；BUG-0025 AC-001～AC-010；BUG-0026 AC-001～AC-011 |

## Rollback Plan

若字段分流导致回归或测试失败，可回滚本 change 的前端改动：

1. 恢复 `ChangePasswordModal.tsx`、`password-change-modal.css`、`ChangePasswordModal.test.tsx` 至 fix 前版本。
2. 运行 `cd src/web && pnpm vitest run src/features/admin/components/ChangePasswordModal && pnpm build` 确认通过。

回滚不涉及 API、数据库或部署配置。
