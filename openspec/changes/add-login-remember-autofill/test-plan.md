# add-login-remember-autofill — Test Plan

## AC 映射

| AC | 描述 | unit | manual |
|---|---|:---:|:---:|
| AC-001 | 记住成功存 localStorage | ✓ | ✓ |
| AC-002 | 重开页面自动填充 | ✓ | ✓ |
| AC-003 | 未勾选清除凭证 | ✓ | ✓ |
| AC-004 | 修改后成功更新 | ✓ | ✓ |
| AC-005 | 失败不更新 | ✓ | — |
| AC-006 | remember_me JWT 7d | — | ✓ |
| AC-007 | sessionStorage token | — | ✓ |
| AC-008 | 登出清凭证 | ✓ | ✓ |
| AC-009 | 登出后表单空 | — | ✓ |
| AC-010~014 | 密码显隐 UI/a11y/CSS | ✓ | ✓ |
| AC-015~017 | 安全与回归 | — | ✓ |
| AC-018~019 | vitest + build | ✓ | ✓ |

## 命令

```bash
cd src/web && npx vitest run src/features/auth
cd src/web && npm run build
```
