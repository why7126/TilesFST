---
title: 品牌区 Logo、菲尚特FST 文案与网页图标统一
purpose: 将 REQ-0025 转换为 OpenSpec Change
created_at: 2026-07-01 22:35:50
updated_at: 2026-07-01 22:35:50
owner: product
status: proposed
related_requirement: REQ-0025-brand-logo-fst-favicon
change_type: update
---

## Why

管理端 Sidebar 顶部品牌区仍以历史 `TILESFST` 文字品牌为主，浏览器标签图标也未统一展示菲尚特 Logo，导致用户在管理后台和多标签页场景中无法稳定识别「菲尚特FST 家居建材资料库」品牌。

REQ-0025 已评审并纳入 sprint-004，本 change 将该品牌露出统一为用户提供的 Logo、`菲尚特FST`、产品版本号、`家居建材资料库` 与网页 favicon。

## What Changes

- 更新管理端 Sidebar 顶部品牌区：
  - 展开态展示 Logo、`菲尚特FST`、现有产品版本号、`家居建材资料库` 与展开/收起按钮。
  - 收起态保留 Logo 作为品牌识别，保持展开/收起按钮可点击、可访问。
  - Logo 区域不新增独立卡片背景、边框、渐变底纹或阴影。
- 更新 Web 入口图标：
  - favicon / apple-touch-icon 使用菲尚特 Logo 或基于该 Logo 的 Web 优化图标。
  - 浏览器标签页不得继续显示 Vite、React 或默认图标。
- 保留既有管理端导航、权限、路由、版本号来源和业务页面主体结构。
- 不新增或修改后端 API、数据库、MinIO 上传流程、Orval 客户端或小程序能力。

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `admin-dashboard`: 修改管理端 Sidebar 品牌与导航 requirement，使品牌区从 `TILESFST + version pill` 更新为 `Logo + 菲尚特FST + version badge + 家居建材资料库`，并保持既有展开/收起与导航行为。
- `web-client`: 增补管理端 Web 入口图标 requirement，要求 favicon / apple-touch-icon 使用菲尚特 Logo 且不影响现有管理端路由守卫、权限和页面主体。

## Impact

- **Web / 管理端**：影响 `AdminSidebar` / `AdminLayout` 品牌区、静态 Logo 资产、`index.html` favicon 声明及相关前端测试。
- **Backend API**：无影响。
- **Database / SQLite / Pydantic**：无影响。
- **MinIO / object storage**：无影响；Logo 为前端静态资源，不走上传链路。
- **Orval**：无需执行。
- **小程序 / 店主 Web**：无影响。
- **Docker Compose**：运行时能力无影响；需要确认 Docker Web 构建后 favicon 静态资源可被正确引用。
