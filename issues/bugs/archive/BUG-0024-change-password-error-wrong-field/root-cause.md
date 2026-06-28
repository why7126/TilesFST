---
bug_id: BUG-0024-change-password-error-wrong-field
status: pending_review
created_at: 2026-06-28 12:55:16
updated_at: 2026-06-28 12:55:16
root_cause_type: code
---

# 根因分析

## 1. 直接原因

### 1.1 单一 `error` 状态误绑原密码字段

`ChangePasswordModal.tsx` 使用单一 `error` 状态（L77），同时承载：

- 客户端新密码规则校验（L127–133）：`新密码不符合安全策略`、`新密码不能与原密码相同`
- 服务端/API 全部 catch 错误（L146）：`getErrorMessage(err, '密码修改失败')`

该 `error` **仅**传入原密码 `PasswordField` 的 `error` prop（L186）：

```tsx
<PasswordField id="pwd-old" label="原密码" ... error={error} />
<PasswordField id="pwd-new" label="新密码" ... />  {/* 无 error prop */}
<PasswordField id="pwd-confirm" label="确认新密码" ... error={confirmError} />
```

因此所有写入 `error` 的文案均渲染在原密码输入框下方，与新密码字段无关。

### 1.2 确认字段已正确分流，形成对照

「确认新密码」不一致使用独立 `confirmError` 状态（L78、L135–137、L216），错误正确显示在确认字段下方。原密码/新密码未采用相同 per-field 模式。

### 1.3 测试未覆盖错误字段位置

`ChangePasswordModal.test.tsx` 仅断言确认密码不一致文案；无新密码客户端校验或服务端错误字段位置用例，缺陷未在 CI 中被捕获。

## 2. 根本原因

### 2.1 实现阶段未按字段拆分错误状态

`PasswordField` 组件已支持 `error` prop 与 `role="alert"` 渲染，但 `ChangePasswordModal` 提交逻辑将所有非确认类错误汇入单一 `error`，并在 JSX 中默认绑定到第一个密码字段（原密码），未区分错误语义所属字段。

### 2.2 服务端错误码可字段化，前端未利用

后端已按场景抛出细分异常与错误码（`error_codes.py`）：

| 错误码 | 异常 | 默认消息 | 应属字段 |
|---|---|---|---|
| 40020 | `PasswordOldIncorrectError` | 原密码不正确 | 原密码 |
| 40021 | `PasswordPolicyError` | 新密码不符合安全策略 | 新密码 |
| 40022 | `PasswordWeakError` | 新密码过于常见，请更换 | 新密码 |
| 40023 | `PasswordSameAsOldError` | 新密码不能与原密码相同 | 新密码 |
| 42901 | `PasswordChangeRateLimitError` | 改密操作过于频繁，请稍后再试 | 表单级/新密码（任选，MUST 不绑原密码） |

前端 catch 块未按 `error_code` 或消息分流，一律 `setError(...)`。

### 2.3 非回归：自交付起即存在

`ChangePasswordModal` 随 REQ-0014 / `add-admin-profile-page` 引入；自实现起即采用单一 `error` 绑定原密码，非近期变更引入的回归。

## 3. 触发条件

满足以下条件时可 **100% 稳定复现**：

1. 以 `admin` 或 `employee` 登录 Web 管理端。
2. 打开「修改密码」弹窗。
3. 触发以下任一错误路径并点击「保存修改」：
   - 新密码长度/字符集不符 → 客户端 `新密码不符合安全策略`
   - 新密码与原密码相同 → 客户端 `新密码不能与原密码相同`
   - 新密码过于常见 → 服务端 `新密码过于常见，请更换`（需原密码正确）
4. 观察错误提示出现在「原密码」字段下方。

**原密码错误路径（当前行为正确）：** 原密码填写错误 → API 返回 40020「原密码不正确」→ 显示在原密码下方（符合预期，修复后 MUST 保持）。

## 4. 分类结论

| 维度 | 结论 |
|---|---|
| 缺陷分类 | code / frontend-ui |
| 是否接口缺陷 | 否（API 与错误码正确） |
| 是否数据库缺陷 | 否 |
| 是否权限缺陷 | 否 |
| 是否回归 | 否 |
| 主要修复面 | `ChangePasswordModal.tsx`、`ChangePasswordModal.test.tsx` |
| 关联 BUG | BUG-0025（错误挂错字段可能连带触发布局问题） |
| 建议 Change | `fix-change-password-modal-errors` |

## 5. 后续修复建议

1. 拆分状态为 `oldPasswordError` 与 `newPasswordError`（或等价命名）；客户端新密码校验写入 `newPasswordError`。
2. API catch 中按 `error_code` 分流：40020 → 原密码；40021/40022/40023 → 新密码；42901 → 新密码或表单 intro 区（MUST NOT 仅绑原密码）。
3. 将 `newPasswordError` 传入新密码 `PasswordField`；提交前 `setOldPasswordError(null); setNewPasswordError(null)`。
4. 新增 Vitest：客户端策略失败、服务端 weak 错误 MUST 出现在新密码字段 DOM 邻域，MUST NOT 出现在原密码字段下。
5. 可选与 BUG-0025、BUG-0026 合并为同一 `fix-change-password-modal-errors` change，scope 在 tasks 中分列。
