---
requirement_id: REQ-0025-brand-logo-fst-favicon
title: 品牌区 Logo 与网页图标统一 - 业务流
status: pending_review
owner: product
created_at: 2026-07-01 20:56:22
updated_at: 2026-07-01 20:56:22
---

# 业务流

## 1. 管理端加载流

```text
用户打开管理端 URL
  ↓
浏览器加载 index.html
  ↓
浏览器读取 favicon / apple-touch-icon
  ↓
React 应用启动并完成登录态校验
  ↓
AdminLayout 渲染 Sidebar
  ↓
Sidebar 品牌区展示：
Logo + 菲尚特FST + 版本号 + 家居建材资料库 + 收起按钮
  ↓
用户继续进入当前管理端页面
```

## 2. 展开 / 收起交互流

```text
用户点击 Sidebar 收起按钮
  ↓
Sidebar 进入收起态
  ↓
Logo 保留为品牌识别
  ↓
品牌文字隐藏或按现有收起态策略处理
  ↓
用户点击展开按钮
  ↓
Sidebar 恢复展示 Logo、菲尚特FST、版本号与家居建材资料库
```

## 3. 范围边界

| 项目 | 处理方式 |
|---|---|
| 管理端 Sidebar 品牌区 | 本期改造 |
| 浏览器标签图标 | 本期替换 |
| 版本号来源 | 沿用现有机制 |
| 导航菜单、路由、权限 | 不改变 |
| 后端 API / SQLite | 不改变 |
| MinIO / 上传流程 | 不改变 |
| 店主 Web / 小程序品牌露出 | 本期不处理 |

## 4. 与既有需求关系

- `REQ-0010-product-version-display`：本需求复用其版本号展示能力，不改变版本维护方式。
- `REQ-0011-admin-sidebar-expand-collapse`：本需求复用其侧栏展开/收起能力，只调整品牌区内容和布局。
- `REQ-0016-banner-management`：现有原型承载页来自 Banner 管理列表，但 Banner 业务能力不是本需求范围。
