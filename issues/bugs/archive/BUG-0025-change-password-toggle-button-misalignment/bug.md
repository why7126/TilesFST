---
bug_id: BUG-0025-change-password-toggle-button-misalignment
title: 修改密码弹窗错误提示出现后显示/隐藏按钮垂直错位
severity: medium
status: draft
owner: product
discovered_at: 2026-06-28 12:47:55
environment: local|docker
related_requirement: REQ-0014-profile-page
related_change: null
related_bug: BUG-0024-change-password-error-wrong-field
---

# 缺陷说明

Web 管理端「修改密码」弹窗（`ChangePasswordModal`）中，当某个密码字段下方出现错误提示（`error-text`）后，该字段右侧「显示/隐藏」切换按钮（`toggle-pass`）**垂直位置下沉**，不再相对输入框垂直居中；同弹窗内无错误提示的字段按钮仍保持正常位置，形成视觉不一致。

典型表现：原密码字段下方出现「新密码过于常见，请更换」等服务端/校验错误后，该字段「隐藏」按钮明显低于新密码、确认新密码字段的按钮（见截图）。

**不在本缺陷范围**：

- 错误提示挂载在哪一字段（BUG-0024，状态绑定问题）
- 取消/Esc 多余浏览器二次确认（BUG-0026）
- 密码策略、API 契约或成功后登出流程
- 密码规则列表（`rule-list`）布局

# 复现步骤

1. 以 `admin` 或 `employee` 登录 Web 管理端（`http://localhost:3000` 或 `http://localhost:5173`）。
2. 通过侧栏用户菜单或个人资料页打开「修改密码」弹窗。
3. 触发任一密码字段下方出现错误提示，例如：
   - **路径 A**：原密码正确 + 新密码过于常见 → 提交（服务端错误，当前挂在原密码字段）
   - **路径 B**：新密码不符合规则 → 提交（客户端 `setError`）
   - **路径 C**：确认新密码不一致 → 提交（`confirmError` 挂在确认字段）
4. 对比有错误字段与无错误字段右侧「显示/隐藏」按钮的垂直位置。

| 触发路径 | 错位字段 |
|---|---|
| 服务端/客户端新密码类错误（当前实现） | 原密码 |
| 确认新密码不一致 | 确认新密码 |

复现稳定性：**100%**（只要对应 `PasswordField` 渲染 `error-text` 即触发）。

# 期望结果

- 无论字段下方是否显示错误提示，「显示/隐藏」按钮 **MUST** 始终相对**输入框**垂直居中（与同弹窗无错误字段一致）。
- 错误提示 **MUST** 显示在输入框下方，**MUST NOT** 参与切换按钮的定位参照。
- 修复 **MUST NOT** 改变 API、密码策略或弹窗交互逻辑（除布局 DOM/CSS 外）。

# 实际结果

- `PasswordField` 结构：`label`（含 input）、`toggle-pass`、`error-text` 均为 `.password-field` 直接子节点（`ChangePasswordModal.tsx` L35–61）。
- `.password-field` 设 `position: relative`；`.toggle-pass` 使用 `position: absolute; bottom: 8px`（`password-change-modal.css` L23–46）。
- **无错误时**：容器高度 ≈ label + input，`bottom: 8px` 相对 input 底部，视觉正常。
- **有错误时**：`error-text` 撑高 `.password-field`，`bottom: 8px` 锚定至含错误区的容器底部，按钮下沉。
- 原型 `password-change-modal.html` 使用相同 DOM 与 CSS，属 CSS Port 遗留，非近期回归。

# 影响范围

| 范围 | 影响 |
|---|---|
| Web 管理端修改密码弹窗 | 有错误时切换按钮错位，视觉不一致；按钮仍可点击，功能不阻断 |
| `admin` / `employee` | 均可打开弹窗，均受影响 |
| REQ-0014 / REQ-0015 | 个人资料与改密弹窗验收需补充布局对齐 |
| 后端 / API / 数据库 / Orval | 无变更需求 |
| 店主端 / 小程序 | 无 |

**与关联项关系**

| 项 | 说明 |
|---|---|
| REQ-0014 | 个人资料页修改密码入口；弹窗全局挂载于 `AdminLayout` |
| REQ-0015-password-change | 弹窗实现与验收归属 |
| BUG-0024 | 同弹窗；修复错误字段映射后，错位仍会在「有错误的字段」上出现 |
| BUG-0026 | 同弹窗取消确认问题，fix change 可合并编排但 scope 独立 |
| 建议 Change | `fix-change-password-modal-errors`（可与 BUG-0024/0026 合并为同一 fix change） |

# 严重等级说明

严重程度为 **medium**。

理由：

- **100% 稳定复现**：任意带 `error-text` 的密码字段均触发。
- **视觉/UX 问题**：按钮错位易让用户误判界面异常，降低改密流程信任感。
- **非功能阻断**：切换按钮仍可操作，密码修改流程不受影响。
- **修复面小**：预计调整 `PasswordField` DOM 包装层与 CSS（如 input + toggle 相对定位容器）；无 API/DB 变更。
- **非安全漏洞**：不涉及权限或数据泄露。

# 代码线索

| 线索 | 路径 |
|---|---|
| `PasswordField` 结构与 error 渲染 | `src/web/src/features/admin/components/ChangePasswordModal.tsx`（L15–63、L180–217） |
| toggle 绝对定位 `bottom: 8px` | `src/web/src/features/admin/styles/password-change-modal.css`（L23–46） |
| 单元测试（未覆盖布局） | `src/web/src/features/admin/components/ChangePasswordModal.test.tsx` |
| 原型（同结构遗留） | `issues/requirements/archive/REQ-0015-password-change/prototype/web/password-change-modal.html` |
| 截图 | `issues/bugs/archive/BUG-0025-change-password-toggle-button-misalignment/screenshots/change-password-toggle-misalignment.png` |

**建议修复方向**：为 input + `toggle-pass` 增加 `position: relative` 包装层，将 `error-text` 置于包装层外，使 toggle 定位参照 input 行而非整段 field。

# 分类结论

| 判断 | 结论 |
|---|---|
| 需求 vs 缺陷 | 缺陷（布局/CSS 参照容器错误，非新能力 REQ） |
| 根因类型 | 前端 CSS：绝对定位锚定含 error 的父容器 |
| 是否回归 | 否；自 REQ-0015 CSS Port 起即存在 |
| 建议修复 Change | `fix-change-password-modal-errors` |
