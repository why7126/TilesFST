---
title: 业务流程
purpose: 描述产品版本号展示与维护流程
content: 基于 requirement.md 提炼
source: AI 根据 PRD 生成，项目团队确认
update_method: PRD 变更时同步更新
owner: product
status: draft
created_at: 2026-06-27 10:21:38
updated_at: 2026-06-27 10:21:38
note: REQ-0010-product-version-display
---

# 业务流程

## 1. 与现有系统的差异

本需求 **不修改** 业务 API、权限、导航菜单项或页面主流程；仅在两端侧边栏头部 **增量展示** 产品版本 badge。

```text
变更前                              变更后
──────────────────────────────────────────────────────────────────
AdminSidebar: TILESFST（仅 logo）  →  TILESFST + v0.0.1 pill
店主端 Sidebar: 无品牌头           →  STONEX + v0.0.1 pill（筛选区之上）
版本维护: 无统一产品版本           →  src/shared/ 单一常量，发版人工更新
```

## 2. 运行时展示流程（无用户交互）

```text
应用启动 / 页面加载
  ↓
读取 src/shared/ PRODUCT_VERSION（例：v0.0.1）
  ↓
  ├─ 管理端 AdminLayout → AdminSidebar 头部渲染 产品名 + badge
  └─ 店主端 CatalogBody → Sidebar 头部渲染 品牌名 + badge
  ↓
用户浏览任意页面（版本常驻，无点击交互）
```

## 3. 发版维护流程

```text
产品 / 发布负责人决定新版本号（如 v0.0.2）
  ↓
手动修改 src/shared/ 产品版本常量
  ↓
  ├─ Web build（管理端 + 店主端自动引用同一常量）
  └─ release checklist 勾选「产品版本已更新」
  ↓
部署后两端侧边栏展示新版本
  ↓
MUST NOT 同步修改 package.json / FastAPI version 作为产品版本
```

## 4. 管理端布局（增量）

```text
AdminSidebar
  ├─ [新增] brand-head: TILESFST + version pill
  ├─ nav-scroll（不变）
  └─ sidebar-user（不变）
```

## 5. 店主端布局（增量）

```text
Sidebar
  ├─ [新增] brand-head: STONEX + version pill
  ├─ filter sections（不变）
  └─ footer slot（不变）
```

## 6. 依赖

| 依赖 | 说明 |
|---|---|
| REQ-0004-admin-home | `AdminLayout`、`AdminSidebar` 壳层 |
| 店主端 Landing / List 模板 | `Sidebar`、`CatalogBody` |
| `rules/ui-design.md` §8 徽章 | pill 字号、圆角、semantic token |
| `rules/release.md` | 发版 checklist 扩展项 |
