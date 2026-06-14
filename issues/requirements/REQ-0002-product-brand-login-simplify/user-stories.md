---
title: 用户故事
purpose: REQ-0002 产品品牌与登录页简化
content: 基于 requirement.md 提炼
source: 追溯补登
update_method: 需求变更时同步
owner: 产品负责人
status: resolved
note: REQ-0002-product-brand-login-simplify
---

# 用户故事

| 编号 | 角色 | 优先级 | 本期 |
|---|---|---|---|
| US-001 | 全体用户 | P0 | 是 |
| US-002 | 企业内部员工 | P0 | 是 |
| US-003 | 企业内部员工 | P1 | 是 |

## US-001 识别 TilesFST 产品名

**作为** 访问 Web 管理端的用户，  
**我希望** 在浏览器标题、登录页左栏 Logo/主标题、管理端顶栏看到 **TilesFST**，  
**以便** 明确当前产品身份。

**验收要点：**

- `index.html` 标题为 `TilesFST`。
- 登录页左栏 Logo 与主标题为 `TilesFST`。
- 管理端 `AdminLayout` 顶栏品牌为 `TilesFST`。
- FastAPI OpenAPI 标题为 `TilesFST API`。

## US-002 仅账号密码登录

**作为** 企业内部员工，  
**我希望** 登录页只提供账号与密码登录，  
**以便** 不被未实现的企业微信入口误导。

**验收要点：**

- 登录表单不包含「企业微信登录」按钮或「或使用企业身份登录」分割区。
- `LoginForm` 不渲染 `ThirdPartyLoginSection`。
- 单元测试断言企微入口不存在。

## US-003 登录页无页面级纵向滚动

**作为** 企业内部员工，  
**我希望** 在桌面视口（≥1024px，高度 ≥720px）打开 `/admin/login` 时页面不出现整页垂直滚动条，  
**以便** 一屏完成登录操作。

**验收要点：**

- `.login-shell` 固定视口且 `overflow: hidden`。
- `html:has(.login-shell)` 锁定 body 滚动。
- 1280×720 视口下 `document.documentElement.scrollHeight <= window.innerHeight`。
