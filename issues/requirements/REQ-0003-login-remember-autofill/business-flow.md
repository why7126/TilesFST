---
title: 业务流程
purpose: 登录页记住凭证与密码显隐交互流程
content: 基于 requirement.md 提炼
source: AI 根据 PRD 生成，项目团队确认
update_method: PRD 变更时同步更新
owner: product
status: draft
note: REQ-0003-login-remember-autofill
---

# 业务流程

## 1. 流程总览

```text
进入 /admin/login
  ↓
读取本地凭证（若有且 remember=true）→ 自动填充用户名、密码、勾选记住
  ↓
用户输入/修改 → 可选切换密码显隐
  ↓
提交登录
  ↓
成功 + 勾选记住 → 保存凭证 + remember_me JWT（localStorage）
成功 + 未勾选   → 清除凭证 + 短效 JWT（sessionStorage）
失败            → 不更新凭证
  ↓
退出登录 → 清除 JWT + 清除本地凭证
```

## 2. 页面加载 · 自动填充

```text
LoginForm mount
  ↓
readLoginCredentials() from localStorage
  ↓
存在且 remember === true ?
  ├─ 是 → setUsername / setPassword / setRememberMe(true)
  └─ 否 → 空表单，rememberMe=false
```

## 3. 登录成功 · 凭证持久化

```text
POST /api/v1/auth/login { username, password, remember_me }
  ↓
200 OK
  ↓
remember_me === true ?
  ├─ 是 → saveLoginCredentials({ username, password, remember: true })
  └─ 否 → clearLoginCredentials()
  ↓
setStoredToken(token, remember_me)  // 现有逻辑
  ↓
跳转 /admin/dashboard
```

## 4. 登出

```text
POST /api/v1/auth/logout（或客户端登出）
  ↓
clearStoredToken()  // 现有
  ↓
clearLoginCredentials()  // 新增
  ↓
跳转 /admin/login
```

## 5. 密码显隐

```text
密码框默认 type=password，showPassword=false
  ↓
用户点击显隐按钮
  ↓
toggle showPassword
  ├─ true  → type=text，aria-label「隐藏密码」
  └─ false → type=password，aria-label「显示密码」
```

## 6. 与 REQ-0001 的差异

| 维度 | REQ-0001 / 现网 | REQ-0003-login-remember-autofill |
|---|---|---|
| 记住登录状态 | 仅延长 JWT，刷新保持会话 | **额外** 保存并自动填充用户名、密码 |
| 密码框 | 仅 password 类型 | 增加显隐切换 |
| 登出 | 清除 token | 清除 token **+** 本地凭证 |

## 7. 预期实现触点

| 模块 | 路径 |
|---|---|
| 登录表单 | `src/web/src/features/auth/components/LoginForm.tsx` |
| 凭证读写 | `src/web/src/features/auth/utils/login-credentials.ts`（建议新建） |
| Token 存储 | `src/web/src/features/auth/utils/auth-token.ts` |
| 登出 | `src/web/src/features/auth/store/auth-store.ts` |
| 样式 | `src/web/src/features/auth/styles/login-page.css` |

## 8. 异常流程

| 场景 | 期望 |
|---|---|
| localStorage 不可用 / 配额满 | 静默降级：不保存、不自动填充，登录主流程可用 |
| 保存数据 JSON 损坏 | 清除坏数据，空表单展示 |
| 自动填充后密码错误 | 正常登录失败提示，不更新凭证 |
