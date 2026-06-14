---
title: 验收标准
purpose: REQ-0002 产品品牌与登录页简化
content: 功能与 UI 验收清单
source: 追溯补登
update_method: 需求变更时同步
owner: 产品负责人
status: resolved
note: REQ-0002-product-brand-login-simplify
---

# 验收标准

## 1. 产品名称（TilesFST）

- [x] 浏览器标签标题为 `TilesFST`（`src/web/index.html`）。
- [x] Web 首页 `/` 主标题为 `TilesFST`（`App.tsx`）。
- [x] 登录页左栏 Logo 与主标题为 `TilesFST`（`AuthBrandPanel.tsx`）。
- [x] 管理端顶栏品牌为 `TilesFST`（`AdminLayout.tsx`）。
- [x] FastAPI 应用标题为 `TilesFST API`（`main.py`）。

## 2. 登录页简化

- [x] 登录表单仅含：账号、密码、记住我、忘记密码、登录按钮、安全说明、语言切换占位。
- [x] 不存在「企业微信登录」按钮。
- [x] 不存在「或使用企业身份登录」分割文案。
- [x] 已删除 `ThirdPartyLoginSection.tsx`、`WeComLoginButton.tsx`。
- [x] `LoginForm.test.tsx` 断言无企微入口。

## 3. 登录页无页面级纵向滚动

- [x] `.login-shell` 使用视口锁定（`position: fixed; inset: 0; overflow: hidden`）。
- [x] `html:has(.login-shell)` 与 `body` 设置 `overflow: hidden`。
- [x] 桌面 1280×720 视口下无 `document.documentElement` 纵向溢出（人工或自动化验收）。

## 4. 规范与追溯

- [x] `issues/requirements/REQ-0002-product-brand-login-simplify/` 五件套齐全。
- [x] OpenSpec change `update-tilesfst-login-simplify` 含 web-client delta spec（MODIFIED/REMOVED）。
- [x] `iterations/sprint-001/sprint.md` 登记 REQ-0002 与本 change。

## 5. 回归

- [x] 账号密码登录、路由守卫、退出登录行为与 REQ-0001 一致。
- [x] `python scripts/validate-design-system.py` 通过。
- [x] `vitest` 登录相关测试通过。

## 6. 本期不包含

- 企业微信 OAuth 接入。
- 全站 Design System 预览页 STONEX 文案替换。
- REQ-0001 原型 HTML/PNG 文件物理更新（以 delta spec 消化冲突）。
