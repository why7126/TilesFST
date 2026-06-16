# add-login-remember-autofill — Trace

## 变更摘要

- **REQ**: `REQ-0003-login-remember-autofill`
- **Change**: `add-login-remember-autofill`
- **Type**: add（登录体验增强）
- **Strategy**: 登录 CSS Port 扩展（`login-page.css`）
- **Status**: proposed

## 关联文档

| 文档 | 路径 |
|---|---|
| PRD | `issues/requirements/REQ-0003-login-remember-autofill/requirement.md` |
| 验收 | `issues/requirements/REQ-0003-login-remember-autofill/acceptance.md` |
| 表单 context | `issues/requirements/REQ-0003-login-remember-autofill/prototype/web/login-form-enhancements-context.md` |
| 登录基线 HTML | `issues/requirements/REQ-0001-user-login/prototype/web/user-login.html` |

## Conflict Resolution 记录

| 项 | 决议 |
|---|---|
| 密码显隐 | 废除 web-client「禁止显隐」；以 REQ-0003 context 为准 |
| 记住我 | 扩展为 JWT + `stonex_login_credentials` 自动填充 |
| 左栏 | 不改 |

## 功能验收 Checklist（1280×1024 右栏表单区）

| # | 检查项 | 结果 | 说明 |
|---|--------|------|------|
| 1 | 密码框右侧显隐图标 | | |
| 2 | 默认密文 | | |
| 3 | 点击切换明文再恢复 | | |
| 4 | 切换不清空密码 | | |
| 5 | 显隐按钮 aria-label | | |
| 6 | 记住勾选+登录成功 | | localStorage 有凭证 |
| 7 | 重开 /admin/login 自动填充 | | |
| 8 | 复选框自动勾选 | | |
| 9 | 未勾选成功登录后凭证清除 | | |
| 10 | 登出后凭证清除 | | |
| 11 | 登录失败凭证不变 | | |
| 12 | 左栏 TilesFST / 主标题无回归 | | |
| 13 | 无忘记密码入口 | | |
| 14 | Tab 顺序含显隐按钮 | | |
| 15 | 无裸 Hex | | |

## 验证命令

```bash
cd src/web && npx vitest run src/features/auth
cd src/web && npm run build
```
