---
title: 业务流程
purpose: REQ-0002 品牌与登录简化后的流程说明
content: 基于 requirement.md
source: 追溯补登
update_method: 需求变更时同步
owner: 产品负责人
status: resolved
note: REQ-0002-product-brand-login-simplify
---

# 业务流程

## 1. 变更摘要

```text
REQ-0001 登录主流程（账号密码 → API → 跳转 dashboard）
        │
        ├─ 移除：企业微信占位点击分支
        ├─ 移除：第三方登录分割 UI
        └─ 保留：语言切换 / 忘记密码占位（noop）
```

## 2. 管理端登录主流程（变更后）

```text
打开 /admin/login（视口锁定，无整页滚动）
  ↓
展示 TilesFST 品牌左栏 + 右栏表单
  ↓
用户输入账号、密码
  ↓
点击「登录」→ POST /api/v1/auth/login
  ↓
成功 → /admin/dashboard（顶栏显示 TilesFST）
```

## 3. 品牌展示触点

| 触点 | 展示文案 |
|---|---|
| 浏览器 `<title>` | TilesFST |
| 登录页左栏 Logo | TilesFST |
| 登录页左栏主标题 | TilesFST |
| 管理端顶栏 | TilesFST |
| OpenAPI `/docs` 标题 | TilesFST API |
| Web 首页 `/` 标题 | TilesFST |

Design System 内部命名（如 STONEX Design System 预览页）不在本需求强制变更范围内。

## 4. 与 REQ-0001 关系

- 认证 API、token、路由守卫 **不变**。
- REQ-0001 原型 HTML 仍作 CSS Port 参考，但 **产品名与企微入口** 以 REQ-0002 为准（Conflict Resolution：REQ-0002 > REQ-0001 原型中冲突项）。
