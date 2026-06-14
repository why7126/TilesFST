# Change Trace — update-tilesfst-login-simplify

## 关联

| 项 | 值 |
|---|---|
| REQ | [REQ-0002-product-brand-login-simplify](../../../issues/requirements/REQ-0002-product-brand-login-simplify/) |
| Type | update（品牌）+ fix（登录结构/视口） |
| 实现模式 | 追溯补登（代码先于 OpenSpec） |

## 策略

- CSS Port 与 auth 逻辑冻结
- REQ-0002 覆盖 REQ-0001 原型中品牌名与企微冲突项

## 验收 Checklist

| # | 项 | 结果 |
|---|---|---|
| 1 | 浏览器标题 TilesFST | pass |
| 2 | 登录左栏 Logo/标题 TilesFST | pass |
| 3 | 管理端顶栏 TilesFST | pass |
| 4 | OpenAPI 标题 TilesFST API | pass |
| 5 | 无企微按钮 / 无第三方分割 | pass |
| 6 | `.login-shell` 视口锁定 | pass |
| 7 | validate-design-system.py | pass |
| 8 | LoginForm vitest | pass |

## 验证命令

```bash
python scripts/validate-design-system.py
cd src/web && ./node_modules/.bin/vitest run src/features/auth/components/LoginForm.test.tsx
```

## 已知偏差

- REQ-0001 原型 HTML/PNG 仍含 STONEX 与企微，以 REQ-0002 delta spec 为准，不更新原型文件。
