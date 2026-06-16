---
title: 测试计划
purpose: REQ-0003 验收标准到测试用例映射
content: AC → unit / integration / manual
source: acceptance.md + business-flow.md
owner: product
status: draft
note: 实现阶段由 /opsx-apply 执行
---

# 测试计划

## 1. 映射总览

| AC | 描述摘要 | unit | integration | manual |
|---|---|:---:|:---:|:---:|
| AC-001 | 勾选记住成功后 localStorage 存凭证 | ✓ | ✓ | ✓ |
| AC-002 | 重开页面自动填充 | ✓ | — | ✓ |
| AC-003 | 未勾选成功则清除凭证 | ✓ | ✓ | ✓ |
| AC-004 | 修改后成功登录更新凭证 | ✓ | — | ✓ |
| AC-005 | 登录失败不更新凭证 | ✓ | ✓ | — |
| AC-006 | remember_me JWT 7 天 | — | ✓ | — |
| AC-007 | 未勾选 sessionStorage token | — | ✓ | — |
| AC-008 | 登出清除凭证 | ✓ | ✓ | ✓ |
| AC-009 | 登出后表单空 | — | ✓ | ✓ |
| AC-010 | 显隐按钮存在 | ✓ | — | ✓ |
| AC-011 | 密文/明文切换 | ✓ | — | ✓ |
| AC-012 | 切换不清空密码 | ✓ | — | — |
| AC-013 | aria-label / 键盘 | ✓ | — | ✓ |
| AC-014 | CSS Port 无裸 Hex | — | — | ✓ |
| AC-015 | 服务端无密码明文 | — | ✓ | — |
| AC-016 | 登录校验无回归 | — | ✓ | ✓ |
| AC-017 | 左栏 refine 无回归 | — | — | ✓ |
| AC-018 | vitest 覆盖 | ✓ | — | — |
| AC-019 | build + vitest pass | — | — | ✓ |
| AC-020 | OpenSpec change | — | — | 流程 |
| AC-021 | spec 归档标题一致 | — | — | 流程 |

## 2. 建议测试文件

```text
src/web/src/features/auth/utils/login-credentials.test.ts
  - save / load / clear
  - corrupt JSON → clear + empty
  - remember=false → no autofill

src/web/src/features/auth/components/LoginForm.test.tsx
  - mount with stored credentials → fields filled
  - toggle password visibility
  - logout clears credentials (mock store)

src/web/src/features/auth/utils/auth-token.test.ts
  - 无变更；回归 remember token 行为
```

## 3. 手工用例（冒烟）

1. 勾选记住 → 登录成功 → 关闭浏览器 → 再开 `/admin/login` → 账号密码已填。
2. 取消勾选 → 登录成功 → 再开 → 表单空。
3. 登录后退出 → 再开 → 无预填密码。
4. 密码框点眼睛 → 明文 → 再点 → 密文。
5. 错误密码登录 → 本地旧凭证不变（若此前有保存）。

## 4. 执行命令

```bash
cd src/web && npx vitest run src/features/auth
cd src/web && npm run build
```
