---
bug_id: BUG-0026-change-password-cancel-confirm-redundant
title: 修改密码弹窗取消时出现多余浏览器二次确认
severity: low
status: draft
owner: product
discovered_at: 2026-06-28 12:49:31
environment: local|docker
related_requirement: REQ-0014-profile-page
related_change: null
related_bug: BUG-0024-change-password-error-wrong-field
---

# 缺陷说明

Web 管理端「修改密码」弹窗（`ChangePasswordModal`，由侧栏用户菜单、`AdminLayout` 或 REQ-0014 个人资料页入口打开）中，用户在表单已有输入时点击「取消」、按 Esc、点击右上角 × 或遮罩关闭，会弹出浏览器原生 `window.confirm`（「当前填写内容尚未保存，确认关闭吗？」）。用户需再次确认才能关闭，与「取消即放弃编辑」的预期及管理端其他表单弹窗行为不一致。

**不在本缺陷范围**：

- 新密码错误提示字段错位（BUG-0024）
- 显示/隐藏按钮垂直错位（BUG-0025）
- 密码校验规则、API 契约、改密成功后登出流程
- 将 `window.confirm` 替换为 Design System Confirm Modal（修复方向为移除多余确认，而非换壳）

**规格说明**：REQ-0015（`FR-003`、`AC-007`）与 `openspec/specs/admin-password-change`「关闭与脏确认」Scenario 曾要求脏表单二次确认；当前实现符合该规格。本缺陷主张与管理端 `BrandFormModal`、`UserFormModal`、`TileSkuFormModal` 等「直接关闭、无 dirty guard」模式对齐。修复时 **MUST** 通过 OpenSpec delta **MODIFIED** 更新 REQ-0015 / `admin-password-change` 相关 Scenario，并同步 `acceptance.md` AC-007、AC-040。

# 复现步骤

1. 以 `admin` 或 `employee` 登录 Web 管理端（`http://localhost:3000` 或 `http://localhost:5173`）。
2. 通过侧栏用户菜单「密码修改」打开「修改密码」弹窗（或个人资料页「修改密码」入口，同一弹窗实例）。
3. 在任意密码字段输入内容（原密码、新密码或确认新密码均可）。
4. 任选以下关闭方式：
   - 点击 footer「取消」
   - 点击右上角 ×
   - 按 Esc
   - 点击遮罩区域

**对照路径（无 confirm）**：

| 操作 | 表单状态 | 实际 | 期望 |
|---|---|---|---|
| 上述任一关闭方式 | 三字段均为空 | 直接关闭 | 直接关闭（正确） |
| 上述任一关闭方式 | 任一字段有输入 | 弹出 `window.confirm` | 直接关闭，无浏览器对话框 |

复现稳定性：**100%**（由 `isDirty` 与统一 `requestClose` 逻辑决定）。

# 期望结果

- 用户点击「取消」或采用其他关闭方式时，**MUST** 直接关闭修改密码弹窗，**MUST NOT** 弹出浏览器原生二次确认。
- 关闭后再次打开弹窗时，表单 **MUST** 重置为空（沿用现有 `open` 时 reset 逻辑）。
- 修复 **MUST NOT** 改变密码提交、校验、API 或成功后的登出流程。
- 修复 **SHOULD** 与管理端其他 CRUD 表单弹窗关闭行为一致。
- 若经评审批准修复，OpenSpec delta **MUST** 更新 REQ-0015 脏关闭相关验收与 spec Scenario。

# 实际结果

- `ChangePasswordModal.tsx` L101：`isDirty` 判定任一密码字段非空。
- L103–108：`requestClose` 在 `isDirty` 时调用 `window.confirm('当前填写内容尚未保存，确认关闭吗？')`，用户点「取消」则 `return`，弹窗保持打开。
- 「取消」、×、Esc、遮罩 **共用** 同一 `requestClose`，因此均触发 confirm。
- `submitting` 时 footer「取消」被 `disabled`，但 × / Esc / 遮罩仍可触发 confirm 后关闭。
- 全项目仅此处使用 `window.confirm`；删除用户等场景已采用应用内 Confirm Modal。
- `ChangePasswordModal.test.tsx` L62–70 断言 dirty 关闭 **必须** 调用 `window.confirm`（修复时需同步更新）。

# 影响范围

| 范围 | 影响 |
|---|---|
| Web 管理端修改密码弹窗 | 多余交互步骤；体验与品牌/用户/SKU 等表单弹窗不一致 |
| `admin` / `employee` | 均可打开改密弹窗，均受影响 |
| REQ-0014 | 个人资料页改密入口复用同一 modal，现象相同 |
| REQ-0015 | 原 AC-007 与修复目标冲突，fix change 须含 spec delta |
| 后端 / API / 数据库 / Orval | 无变更需求 |
| 店主端 / 小程序 | 无 |

**与关联项关系**

| 项 | 说明 |
|---|---|
| REQ-0014 | 个人资料页账号安全卡片改密入口；弹窗由 `AdminLayout` 全局挂载 |
| REQ-0015 | 改密弹窗规格归属；脏关闭 Scenario 需在 fix 中 MODIFIED |
| BUG-0024 | 同弹窗错误字段映射问题，可合并编排 |
| BUG-0025 | 同弹窗布局问题，可合并编排 |
| 建议 Change | `fix-change-password-modal-cancel-confirm` 或与 BUG-0024/0025 合并为 `fix-change-password-modal-ux` |

# 严重等级说明

严重程度为 **low**。

理由：

- **100% 稳定复现**，但仅增加一次点击，不阻断改密主流程。
- 无数据丢失风险（未提交密码不落库；关闭后 reopen 会 reset）。
- 无安全或权限影响。
- 修复面小（单组件 + 单测 + 可选 REQ-0015 / OpenSpec delta），可与同弹窗其他 UX 缺陷一并交付。
