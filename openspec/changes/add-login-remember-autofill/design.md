## Context

- **现状**：`LoginForm` 有「记住登录状态」复选框，仅影响 `remember_me` 与 token 存储；无凭证自动填充；密码无显隐。
- **依赖**：`REQ-0001-user-login` CSS Port、`REQ-0003-login-left-panel-refine` 左栏（本 change **不改** 左栏）。
- **原型来源**（优先级）：
  1. `issues/requirements/REQ-0003-login-remember-autofill/prototype/web/login-form-enhancements-context.md`
  2. `issues/requirements/REQ-0001-user-login/prototype/web/user-login.html`（布局壳层）
  3. `issues/requirements/REQ-0001-user-login/prototype/web/user-login.png`（左栏与整体；密码显隐以 context 为准）
  4. `issues/requirements/REQ-0003-login-remember-autofill/acceptance.md`
  5. `rules/ui-design.md`
  6. `openspec/specs/web-client/spec.md`

## Conflict Resolution

| 检查项 | user-login.html | user-login.png | acceptance / REQ-0003 | openspec/specs | 决议 |
|--------|-----------------|----------------|-------------------------|----------------|------|
| 密码显隐 icon | 无 | 无 | **必须有**（FR-004） | 禁止显隐（fix-login 遗留） | **MODIFIED** `管理端登录页`：以 REQ-0003 为准，增加 `.password-toggle` |
| 记住登录状态 | 仅复选框 UI | 同 | JWT + **自动填充凭证** | 仅 token 持久化 | **MODIFIED** `登录态保持`：叠加 `stonex_login_credentials` |
| Tab 顺序 | 无显隐项 | — | 密码 → 显隐 → 记住我 | 无显隐项 | **MODIFIED** `可访问性` |
| 左栏 / 忘记密码 | 已 refine | 同 | 不改 | 已归档 | 无变更 |

## Goals / Non-Goals

**Goals:**

- 勾选记住且登录成功 → 下次 `/admin/login` 自动填充用户名、密码，复选框勾选。
- 未勾选成功 / 登出 → 清除 `stonex_login_credentials`。
- 密码显隐：默认密文，眼睛图标切换，a11y 标签完整。
- vitest 覆盖凭证工具与表单行为；`npm run build` 通过。

**Non-Goals:**

- 后端、`remember_me` JWT 时长、auth API 契约变更。
- 左栏品牌区、忘记密码、企微入口。
- 加密凭证、Passkey、多账号历史。
- 更新 `user-login.png` golden（可选后续）；本 change checklist 以功能 + 局部 UI 为准。

## Decisions

### D1：实现策略 — 登录 CSS Port 扩展（路径 A 延续）

- **决策**：在现有 `login-page.css` 增加 `.password-wrap`、`.password-toggle`；不引入 shadcn Input。
- **理由**：与 `fix-login-css-port` 一致；局部 DOM 变更，不破坏左栏 fidelity。

### D2：凭证存储

```typescript
// localStorage key: stonex_login_credentials
interface StoredLoginCredentials {
  username: string;
  password: string;
  remember: true;
}
```

- 仅 `remember === true` 时写入；读取失败或 JSON 损坏 → `clearLoginCredentials()` + 空表单。
- `localStorage` 不可用时静默降级（不保存、不填充）。

### D3：与 token 存储正交

| 事件 | token（现有 `auth-token.ts`） | credentials（新增） |
|---|---|---|
| 记住 + 登录成功 | localStorage token | save credentials |
| 未记住 + 登录成功 | sessionStorage token | clear credentials |
| 登出 | clear token | clear credentials |
| 登录失败 | 不变 | 不更新 |

### D4：Auth 逻辑边界

- **允许**：`auth-store.logout` 调用 `clearLoginCredentials()`；`LoginForm` 在 `login()` 成功回调后 save/clear。
- **禁止**：修改 `POST /api/v1/auth/login` 请求体字段、token 过期策略、路由守卫、角色分流。

## 测试设计

见 `test-plan.md`；执行：

```bash
cd src/web && npx vitest run src/features/auth
cd src/web && npm run build
```

## 验收 Gate

- 功能：AC-001 ~ AC-019（`issues/.../acceptance.md`）。
- 视觉 checklist：见 `trace.md`（≥12 项，1280×1024 登录页右栏表单区）。
- 回归：`REQ-0003-login-left-panel-refine` 左栏无变更。
