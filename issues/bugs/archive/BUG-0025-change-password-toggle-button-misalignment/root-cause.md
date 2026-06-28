---
bug_id: BUG-0025-change-password-toggle-button-misalignment
status: pending_review
created_at: 2026-06-28 12:57:00
updated_at: 2026-06-28 12:57:00
root_cause_type: code
---

# 根因分析

## 1. 直接原因

### 1.1 切换按钮绝对定位参照容器含 error 区域

`password-change-modal.css` 中：

```css
.admin-shell .password-field { position: relative; }
.admin-shell .toggle-pass { position: absolute; right: 8px; bottom: 8px; }
```

`PasswordField` DOM 结构（`ChangePasswordModal.tsx` L35–61）：

```text
.password-field          ← position: relative（定位参照）
  label
    .field-label
    input
  button.toggle-pass      ← absolute; bottom: 8px
  div.error-text          ← 有错误时撑高父容器
```

- **无错误时**：`.password-field` 高度 ≈ label + input，`bottom: 8px` 相对 input 底边，视觉居中。
- **有错误时**：`.error-text` 作为同级节点增加容器高度，`bottom: 8px` 锚定至「input + error」整体底部，按钮下沉。

### 1.2 原型 CSS Port 遗留相同结构

`issues/requirements/archive/REQ-0015-password-change/prototype/web/password-change-modal.html` 使用相同 DOM 顺序与 `bottom: 8px` 规则；确认字段带 `error-text` 的静态示例亦存在相同布局缺陷，实现阶段未在动态 error 场景下验收。

### 1.3 测试未覆盖布局

`ChangePasswordModal.test.tsx` 断言错误文案存在性，未断言 `toggle-pass` 相对 input 的垂直位置；缺陷未在 CI 中被捕获。

## 2. 根本原因

### 2.1 定位策略与 DOM 层级不匹配

「显示/隐藏」按钮语义上属于**输入框内嵌控件**，但实现将其与 `error-text` 并列置于 `.password-field` 下，且 CSS 以整段 field 为定位参照。错误提示本应在 input 行之外，却参与了 toggle 的定位计算。

### 2.2 未采用 input 行独立定位上下文

同类表单常见模式为 `input-wrap { position: relative }` 包裹 input + toggle，error 置于 wrap 外。当前实现缺少该包装层，导致 error 动态出现/消失时 toggle 位置漂移。

### 2.3 非回归：自 REQ-0015 CSS Port 起即存在

`ChangePasswordModal` 随 REQ-0014 / REQ-0015 交付；自实现起即采用上述 DOM/CSS，非近期变更引入的回归。

## 3. 触发条件

满足以下条件时可 **100% 稳定复现**：

1. 以 `admin` 或 `employee` 登录 Web 管理端。
2. 打开「修改密码」弹窗。
3. 使任一 `PasswordField` 渲染 `error-text`：
   - **路径 A**：提交触发服务端/客户端错误（当前多挂在原密码字段，见 BUG-0024）
   - **路径 B**：确认新密码不一致 → `confirmError` 挂在确认字段
4. 观察该字段「显示/隐藏」按钮相对 input 垂直位置下沉，与同弹窗无错误字段按钮不一致。

**与 BUG-0024 关系**：修复 BUG-0024 将错误移至新密码字段后，错位会出现在新密码字段；本缺陷独立于错误挂载字段，任意带 error 的字段均触发。

## 4. 分类结论

| 维度 | 结论 |
|---|---|
| 缺陷分类 | code / frontend-ui / css-layout |
| 是否接口缺陷 | 否 |
| 是否数据库缺陷 | 否 |
| 是否权限缺陷 | 否 |
| 是否回归 | 否 |
| 主要修复面 | `ChangePasswordModal.tsx`、`password-change-modal.css` |
| 关联 BUG | BUG-0024（同弹窗；错误字段映射独立） |
| 建议 Change | `fix-change-password-modal-errors` |

## 5. 后续修复建议

1. 为 input + `toggle-pass` 增加 `.password-input-wrap { position: relative }` 包装层；toggle 的 `absolute` 规则绑定至 wrap。
2. `error-text` 保持在 wrap 外、`.password-field` 内（或 field 末尾），不参与 toggle 定位。
3. 可选：将 `bottom: 8px` 改为 `top: 50%; transform: translateY(-50%)` 相对 wrap 垂直居中（input 高度 44px 时与现有视觉一致）。
4. 新增 Vitest 或 DOM 结构断言：有 error 时 toggle 仍在 input-wrap 内；或补充 E2E/截图验收 checklist。
5. 可与 BUG-0024、BUG-0026 合并为 `fix-change-password-modal-errors`，tasks 分列验收。
