# add-login-remember-autofill — Trace

## 变更摘要

- **REQ**: `REQ-0003-login-remember-autofill`
- **Change**: `add-login-remember-autofill`
- **Type**: add（登录体验增强）
- **Strategy**: 登录 CSS Port 扩展（`login-page.css`）
- **Status**: applied（待 archive）
- **Iteration**: sprint-002

## 关联文档

| 文档 | 路径 |
|---|---|
| PRD | `issues/requirements/archive/REQ-0003-login-remember-autofill/requirement.md` |
| 验收 | `issues/requirements/archive/REQ-0003-login-remember-autofill/acceptance.md` |
| 表单 context | `issues/requirements/archive/REQ-0003-login-remember-autofill/prototype/web/login-form-enhancements-context.md` |
| 登录基线 HTML | `issues/requirements/archive/REQ-0001-user-login/prototype/web/user-login.html` |

## Conflict Resolution 记录

| 项 | 决议 |
|---|---|
| 密码显隐 | 废除 web-client「禁止显隐」；以 REQ-0003 context 为准 |
| 记住我 | 扩展为 JWT + `stonex_login_credentials` 自动填充 |
| 左栏 | 不改 |

## 功能验收 Checklist（1280×1024 右栏表单区）

验收方式：2026-06-20 vitest 26 passed（`src/features/auth`）+ `npm run build`；行为由单元/组件测试覆盖。

| # | 检查项 | 结果 | 说明 |
|---|--------|------|------|
| 1 | 密码框右侧显隐图标 | pass | `LoginForm` + `.password-toggle` |
| 2 | 默认密文 | pass | `type=password` 默认 |
| 3 | 点击切换明文再恢复 | pass | `LoginForm.test.tsx` |
| 4 | 切换不清空密码 | pass | vitest |
| 5 | 显隐按钮 aria-label | pass | `aria-label` on toggle |
| 6 | 记住勾选+登录成功 | pass | `login-credentials.test.ts` |
| 7 | 重开 /admin/login 自动填充 | pass | mount 读取 localStorage |
| 8 | 复选框自动勾选 | pass | vitest |
| 9 | 未勾选成功登录后凭证清除 | pass | vitest |
| 10 | 登出后凭证清除 | pass | auth-store logout |
| 11 | 登录失败凭证不变 | pass | vitest |
| 12 | 左栏 TilesFST / 主标题无回归 | pass | 无左栏 DOM 变更 |
| 13 | 无忘记密码入口 | pass | |
| 14 | Tab 顺序含显隐按钮 | pass | DOM 顺序 |
| 15 | 无裸 Hex | pass | login-page.css tokens |

## Docker / 页面冒烟

| 检查 | 结果 |
|---|---|
| `GET http://localhost:3000/admin/login` | 200 |

## 验证命令

```bash
cd src/web && npx vitest run src/features/auth
cd src/web && npm run build
```
