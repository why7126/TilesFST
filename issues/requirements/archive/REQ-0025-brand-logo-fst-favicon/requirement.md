---
requirement_id: REQ-0025-brand-logo-fst-favicon
title: 品牌区 Logo、菲尚特FST 文案与网页图标统一
terminal: web-admin
version: v1
status: in_sprint
owner: product
source: capture.md
priority: P1
parent_requirement: REQ-0010-product-version-display
created_at: 2026-07-01 20:47:03
updated_at: 2026-07-01 22:25:00
---

# REQ-0025 品牌区 Logo、菲尚特FST 文案与网页图标统一

## 1. 背景

管理端已具备产品版本号展示与侧边栏展开/收起能力，但当前品牌区仍存在产品名称、Logo 展示与浏览器标签图标不统一的问题。用户已提供菲尚特家居建材 Logo 图片，并明确希望管理端品牌区参照 SoulKing 侧边栏结构展示：

```text
Logo + 菲尚特FST + 版本号 + 家居建材资料库
```

同时，浏览器标签图标也需要替换为同一品牌 Logo，保证管理后台从侧边栏到浏览器标签的品牌识别一致。

## 2. 目标用户

- **后台管理员 / 内部员工**：进入管理端后能快速识别当前系统为菲尚特FST家居建材资料库。
- **项目维护人员**：后续维护品牌资产、版本号和导航布局时，有明确的文案、图标和验收边界。

## 3. 本期范围

### 3.1 包含

- 管理端 Sidebar 顶部品牌区改为横向结构：Logo、品牌文字组、版本号、收起/展开按钮同一品牌行内稳定排布。
- 品牌主标题固定为 `菲尚特FST`。
- 品牌副标题固定为 `家居建材资料库`。
- 版本号继续沿用前端现有产品版本来源，视觉位置靠近主标题右上侧，不在需求中硬编码具体版本。
- Logo 使用用户提供的菲尚特图片资产，保持比例，不拉伸、不裁切关键图形。
- 浏览器标签图标 favicon / apple-touch-icon 使用同一品牌 Logo 或由其派生的网页图标资源。
- 保留现有侧边栏展开/收起交互、导航分组、路由和权限边界。

### 3.2 不包含

- 不新增后台接口、数据库字段、对象存储上传流程。
- 不实现管理端在线上传或配置 Logo。
- 不调整店主 Web、小程序的首页品牌露出。
- 不改变 Banner 管理、用户管理、品牌管理等业务页面主体结构。
- 不改变产品版本号维护机制。
- 不新增 Design System Token；若实现确需新增 Token，应另走 OpenSpec Change。

## 4. 原型与参考

本需求已有产品原型，开发与评审时按以下优先级参考：

1. `prototype/web/banner-management-list-logo.html`
2. `prototype/web/banner-management-list-logo.png`
3. `prototype/web/banner-management-list-logo-context.md`
4. `prototype/web/fs-logo-web.png`
5. `capture.md`
6. `rules/ui-design.md`

说明：现有原型承载在 Banner 管理列表页，仅用于验证管理端 Shell / Sidebar 品牌区视觉。页面主体 Banner 管理列表不是本需求范围。

## 5. UI / UE 要求

### 5.1 品牌区结构

```text
sidebar-brand
├── brand-logo              Logo 图标
├── brand-copy
│   ├── 菲尚特FST + version badge
│   └── 家居建材资料库
└── sidebar-collapse        展开/收起按钮
```

- Logo、品牌文字组、展开/收起按钮必须在同一行内，不得互相遮挡。
- Logo 区域不增加独立卡片背景、边框、渐变底纹或阴影。
- 品牌主标题使用 `font-brand` / `tracking-brand` 或现有品牌字重规则，文案为 `菲尚特FST`。
- 版本号使用现有版本号组件或同等语义结构，需保留弱边框、弱背景和紧凑高度。
- 副标题文案为 `家居建材资料库`，字号和颜色弱于主标题。
- 展开/收起按钮保持正方形热区，与侧边栏内边框留出安全间距，hover 后边框不得贴边。

### 5.2 浏览器标签图标

- `index.html` 或等效入口必须声明 favicon。
- favicon 与 apple-touch-icon 使用菲尚特 Logo 或基于该 Logo 的 Web 图标裁切资源。
- 标签图标在 Chrome / Safari 常规标签页中可见，不显示 Vite / React 默认图标。

### 5.3 收起态

- 侧边栏收起后，Logo 仍应作为主要品牌识别元素保留。
- 收起态不得出现品牌文案与导航图标重叠。
- 展开/收起按钮仍可点击，且保留可访问标签。

## 6. 数据、接口与权限

- **接口影响**：无。
- **数据库影响**：无。
- **Orval 影响**：无。
- **对象存储影响**：无，本期使用前端静态资源。
- **权限影响**：无，沿用管理端现有登录与路由守卫。

## 7. 验收摘要

- 管理端 Sidebar 顶部展示 Logo、`菲尚特FST`、版本号、`家居建材资料库`。
- 浏览器标签页图标展示菲尚特 Logo，不再展示默认图标。
- 展开态、收起态和 hover 态均无重叠、无裁切、无布局抖动。
- 业务页面主体、路由、接口、数据库与权限不发生行为变化。
