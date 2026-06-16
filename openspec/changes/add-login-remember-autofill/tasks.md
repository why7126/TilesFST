## 1. 凭证存储工具

- [ ] 1.1 新建 `src/web/src/features/auth/utils/login-credentials.ts`（key：`stonex_login_credentials`）
- [ ] 1.2 实现 `saveLoginCredentials` / `loadLoginCredentials` / `clearLoginCredentials`
- [ ] 1.3 处理 JSON 损坏与 localStorage 不可用时的静默降级

## 2. LoginForm 与登出

- [ ] 2.1 `LoginForm` mount：读取凭证并自动填充 username、password、rememberMe
- [ ] 2.2 登录成功：勾选记住 → save；未勾选 → clear；失败不更新
- [ ] 2.3 `auth-store` logout：调用 `clearLoginCredentials()`
- [ ] 2.4 密码显隐：`.password-wrap` + toggle 按钮，`type` 切换，保留输入值

## 3. 样式（CSS Port）

- [ ] 3.1 `login-page.css`：`.password-wrap`、`.password-toggle`、输入框右侧 padding
- [ ] 3.2 使用 `var(--color-*)` / login token，无裸 Hex

## 4. 测试

- [ ] 4.1 `login-credentials.test.ts`：save/load/clear/损坏数据
- [ ] 4.2 `LoginForm.test.tsx`：自动填充、显隐切换、登出清除（mock store）
- [ ] 4.3 运行 `cd src/web && npx vitest run src/features/auth`

## 5. 构建

- [ ] 5.1 `cd src/web && npm run build`

## 6. 验收与文档

- [ ] 6.1 手工冒烟：记住填充、未勾选清除、登出清除、显隐切换
- [ ] 6.2 填写 `openspec/changes/add-login-remember-autofill/trace.md` checklist
- [ ] 6.3 更新 `issues/requirements/REQ-0003-login-remember-autofill/trace.md`（status: proposed/applied）
- [ ] 6.4 回归确认左栏 `REQ-0003-login-left-panel-refine` 无变更

## 7. 归档准备

- [ ] 7.1 本文件全部 `[x]` 后执行 `/opsx-archive add-login-remember-autofill`
