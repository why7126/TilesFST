---
title: Change 追踪
purpose: fix-login-left-panel-refine 与 REQ-0003 追溯
source: requirement-to-opsx
---

# Change 追踪

## 基本信息

```yaml
change_id: fix-login-left-panel-refine
requirement_id: REQ-0003-login-left-panel-refine
change_type: fix
priority: P1
status: implemented
iteration: sprint-001
strategy: css-port
created_at: 2026-06-14
implemented_at: 2026-06-14
```

## 策略

**CSS Port 延续** — 仅改 `AuthBrandPanel`、`LoginForm`、`login-page.css`；auth 逻辑冻结。

## 冲突决议（相对 REQ-0002）

| 项 | REQ-0002 | REQ-0003 | 本 change |
|---|---|---|---|
| `.logo` | TilesFST | TilesFST | 不变 |
| `.brand-title` | TilesFST | 瓷砖信息管理后台 | MODIFIED |
| 忘记密码 | 占位可见 | 隐藏 | MODIFIED |

## PNG / 目视 Checklist（1440×1024）

| # | 检查项 | Pass |
|---|---|---|
| 1 | Logo TilesFST 金色 | [x] |
| 2 | 主标题「瓷砖信息管理后台」 | [x] |
| 3 | Logo-眉标间距紧凑 | [x] |
| 4 | 统计三格可读（126 不遮挡） | [x] |
| 5 | 无「忘记密码？」 | [x] |
| 6 | 记住我 + 登录按钮正常 | [x] |
| 7 | 无企微入口 | [x] |
| 8 | 无页面级纵向滚动 | [x] |

> 实现验证：Vitest 23/23、validate-design-system pass、vite build pass。团队目视 sign-off 可选复验。

## 验证命令

```bash
cd src/web && pnpm test && pnpm build
python scripts/validate-design-system.py
```

## 目标文件

- `src/web/src/features/auth/components/AuthBrandPanel.tsx`
- `src/web/src/features/auth/components/LoginForm.tsx`
- `src/web/src/features/auth/styles/login-page.css`
- `src/web/src/features/auth/components/LoginPage.test.tsx`
- `src/web/src/features/auth/components/LoginForm.test.tsx`
