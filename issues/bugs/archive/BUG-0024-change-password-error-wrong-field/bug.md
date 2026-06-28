---
bug_id: BUG-0024-change-password-error-wrong-field
title: 修改密码弹窗新密码错误提示显示在原密码字段下方
severity: medium
status: draft
owner: product
discovered_at: 2026-06-28 12:47:55
environment: local|docker
related_requirement: REQ-0014-profile-page
related_change: null
related_bug: BUG-0025-change-password-toggle-button-misalignment
---

# 缺陷说明

Web 管理端「修改密码」弹窗（`ChangePasswordModal`，由侧栏用户菜单或 `AdminLayout` 打开）中，**与新密码相关的**校验失败与服务端错误提示错误地渲染在「原密码」输入框下方，而非「新密码」输入框下方。用户无法直观判断应修改哪一项，且可能误以为原密码填写有误。

典型表现：提交过于常见的新密码后，服务端返回「新密码过于常见，请更换」，该文案出现在「原密码」字段下方（见截图）。

**不在本缺陷范围**：

- 「确认新密码」不一致提示（已正确使用 `confirmError` 绑定确认字段）
- 「显示/隐藏」按钮垂直错位（BUG-0025，可能因错误挂载位置连带触发，职责独立）
- 取消/Esc 多余浏览器二次确认（BUG-0026）
- 后端密码策略本身（常见密码检测逻辑正确，问题在前端错误字段映射）
- 密码修改成功后登出与重登流程

# 复现步骤

1. 以 `admin` 或 `employee` 登录 Web 管理端（`http://localhost:3000` 或 `http://localhost:5173`）。
2. 通过侧栏用户菜单打开「修改密码」弹窗。
3. 填写正确的原密码（如 `AdminPass123!`）。
4. 填写一个过于常见的新密码（如 `AdminPass123`），「确认新密码」保持一致。
5. 点击「保存修改」，触发服务端校验失败。
6. 观察错误提示位置。

**客户端校验路径（同样错位）**：

| 操作 | 触发文案 | 实际显示位置 | 期望显示位置 |
|---|---|---|---|
| 新密码不符合 8–32 位或缺字母/数字 | `新密码不符合安全策略` | 原密码下方 | 新密码下方 |
| 新密码与原密码相同 | `新密码不能与原密码相同` | 原密码下方 | 新密码下方 |
| 服务端：常见密码 | `新密码过于常见，请更换` | 原密码下方 | 新密码下方 |
| 原密码错误（API） | 服务端返回原密码相关错误 | 原密码下方 | 原密码下方（正确） |

复现稳定性：**100%**（由 `error` 单一状态仅绑定原密码 `PasswordField` 决定）。

# 期望结果

- 与新密码策略、格式、常见性、与原密码相同等相关的错误 **MUST** 显示在「新密码」字段下方（`role="alert"`）。
- 与原密码验证失败相关的错误 **MUST** 显示在「原密码」字段下方。
- 「确认新密码」不一致 **MUST** 继续显示在确认字段下方（现有行为保持）。
- 错误出现时对应输入框 **SHOULD** 应用 `error` 样式类；字段与 `aria-describedby` **SHOULD** 关联错误区域（若已有模式可沿用）。
- 修复 **MUST NOT** 改变 API 契约、密码策略或成功后的登出流程。

# 实际结果

- 组件使用单一 `error` 状态（`ChangePasswordModal.tsx` L77），同时承载：
  - 客户端新密码规则校验（L127–133）
  - 服务端/API 全部错误（L146，`getErrorMessage`）
- 该 `error` **仅**传入原密码 `PasswordField` 的 `error` prop（L186）；「新密码」字段未接收任何错误 prop（L189–195）。
- 因此所有新密码相关文案均出现在原密码输入框下方，与用户认知不符。
- 后端 `PasswordTooCommonError` 默认消息为「新密码过于常见，请更换」（`exceptions.py`），前端未按字段分流。

# 影响范围

| 范围 | 影响 |
|---|---|
| Web 管理端修改密码弹窗 | 错误提示字段错位，误导用户；功能可用，修改密码流程不阻断 |
| `admin` / `employee` | 均可打开修改密码弹窗，均受影响 |
| REQ-0014 | 个人资料/账号安全相关能力；验收需补充错误字段对齐 |
| 后端 / API / 数据库 / Orval | 无变更需求 |
| 店主端 / 小程序 | 无 |

**与关联项关系**

| 项 | 说明 |
|---|---|
| REQ-0014 | 个人资料页含修改密码入口；弹窗由 `AdminLayout` 全局挂载 |
| BUG-0025 | 错误挂在原密码字段下方可能导致该字段「显示/隐藏」按钮布局异常 |
| BUG-0026 | 同弹窗取消确认问题，fix change 可合并编排但 scope 独立 |
| 建议 Change | `fix-change-password-modal-errors`（可与 BUG-0025/0026 合并为同一 fix change） |

# 严重等级说明

严重程度为 **medium**。

理由：

- **100% 稳定复现**：任意新密码校验失败或服务端新密码类错误均可触发。
- **误导用户**：错误文案明确指向「新密码」，却显示在「原密码」下，增加修正成本与困惑。
- **非功能阻断**：密码修改 API 与策略正常；用户反复尝试仍可能成功。
- **修复面小**：预计仅改 `ChangePasswordModal.tsx` 及对应 Vitest；无 API/DB 变更。
- **非安全漏洞**：不涉及权限绕过或信息泄露。

# 代码线索

| 线索 | 路径 |
|---|---|
| 错误状态与提交逻辑 | `src/web/src/features/admin/components/ChangePasswordModal.tsx`（L77–78、L123–149、L180–217） |
| 原密码字段错误绑定 | 同文件 L186 `error={error}` |
| 新密码字段（无 error） | 同文件 L189–195 |
| 确认字段错误（正确范例） | 同文件 L216 `error={confirmError}` |
| 单元测试 | `src/web/src/features/admin/components/ChangePasswordModal.test.tsx` |
| 样式 | `src/web/src/features/admin/styles/password-change-modal.css` |
| 后端常见密码异常 | `src/backend/app/core/exceptions.py` |
| 截图 | `issues/bugs/archive/BUG-0024-change-password-error-wrong-field/screenshots/change-password-error-wrong-field.png` |

# 分类结论

| 判断 | 结论 |
|---|---|
| 需求 vs 缺陷 | 缺陷（表单错误字段映射错误，非新能力 REQ） |
| 根因类型 | 前端状态设计：单一 `error` 误绑原密码字段 |
| 是否回归 | 待 bug-complete 核对 `add-admin-profile-page` 交付历史；自实现起即存在 |
| 建议修复 Change | `fix-change-password-modal-errors` |
