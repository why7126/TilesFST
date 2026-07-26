---
title: 品牌区 Logo 与网页图标统一设计
purpose: 说明 REQ-0025 的管理端品牌区与 favicon 实现策略
created_at: 2026-07-01 22:35:50
updated_at: 2026-07-01 22:35:50
owner: frontend
status: proposed
related_requirement: REQ-0025-brand-logo-fst-favicon
---

## Context

REQ-0025 已完成评审并纳入 sprint-004。当前管理端 Sidebar 品牌区由历史 `TILESFST` 文字品牌与 `PRODUCT_VERSION` pill 组成，且浏览器标签图标仍未统一为菲尚特 Logo。用户已提供品牌 Logo 图片与 SoulKing 风格参考，希望管理端品牌区固定展示：

```text
Logo + 菲尚特FST + 版本号 + 家居建材资料库
```

本 change 只建立 OpenSpec，不写 `src/`。后续实现由 `/opsx-apply update-brand-logo-fst-favicon` 执行。

## Goals / Non-Goals

**Goals:**

- 管理端 Sidebar 展开态展示菲尚特 Logo、`菲尚特FST`、`PRODUCT_VERSION` 与 `家居建材资料库`。
- Sidebar 收起态保留 Logo 品牌识别与展开/收起按钮可用性。
- Web 入口声明 favicon / apple-touch-icon，使用菲尚特 Logo 或派生图标。
- 使用现有 Design System semantic token 与 CSS Port 方式还原原型，不新增裸 Hex。
- 保持现有导航、权限、路由、版本号来源和业务页面主体行为不变。

**Non-Goals:**

- 不新增后端 API、数据库、Pydantic Schema、MinIO 上传或对象存储读取流程。
- 不提供管理端在线配置 Logo。
- 不修改店主 Web 或微信小程序品牌露出。
- 不改变 `PRODUCT_VERSION` 单一事实源。
- 不新增 Design System Token；若实现发现必须新增 Token，应另起 change。

## Decisions

### D1. UI strategy: CSS Port + DS semantic token + static asset

采用 CSS Port 还原现有 `prototype/web/banner-management-list-logo.html` 与 PNG 中的 Sidebar 品牌区布局，同时保持实现使用现有 AdminLayout / AdminSidebar 结构和 Design System semantic token。

理由：

- REQ-0025 是 Shell 品牌区视觉改造，不是新增业务页面。
- 原型已有 HTML/PNG，适合以 CSS Port 控制 Logo、文字组、版本 badge 与收起按钮同排布局。
- 现有 `AdminSidebar` 已承担展开/收起、localStorage、导航 active、权限过滤，复用它最稳。

备选：

- 纯 Tailwind 重写：会增加与既有 admin CSS 的割裂风险。
- 新建 Brand 配置 API：超出本期范围，也会引入后端/数据库/权限边界。

### D2. Conflict Resolution

原型与需求存在历史文案冲突，处理优先级如下：

```text
prototype/web/banner-management-list-logo.html
> prototype/web/banner-management-list-logo.png
> prototype/web/brand-logo-fst-favicon-context.md
> prototype/web/banner-management-list-logo-context.md
> acceptance.md
> rules/ui-design.md
> openspec/specs
```

冲突决议：

- 品牌区布局以 HTML/PNG 的三元素同行结构为准。
- 旧上下文中的 `家居建材管理后台` MUST 被 `家居建材资料库` 替换。
- 旧 spec 中的 `TILESFST` MUST 被 `菲尚特FST` 替换。
- 原型承载页是 Banner 管理列表页，但 Banner 业务主体不属于本 change。

### D3. Static asset placement

后续实现 SHOULD 将 Web 优化后的 Logo 图标放在 `src/web/public/` 下可被 Vite 和 Docker Web 静态服务直接访问的位置，并在入口 HTML 声明 favicon / apple-touch-icon。

理由：

- favicon 是入口 HTML 静态资源问题，不需要后端托管。
- 本期明确不走 MinIO 上传或后台配置。
- Docker Web 构建后 public 静态资源可随前端镜像发布。

### D4. Testing strategy

后续实现 MUST 至少补充前端测试覆盖：

- `AdminSidebar` 展开态品牌文案、版本 badge 与 Logo alt。
- 收起态仍保留 Logo/按钮可识别，不破坏 existing collapse tests。
- `index.html` 或等效入口包含 favicon / apple-touch-icon 指向菲尚特资源。

无需后端 pytest、OpenAPI、Orval 或数据库迁移测试。

## Risks / Trade-offs

- **Logo 原图白底或尺寸过大导致 40×40/50×50 下可读性差** → 使用 Web 优化版本或派生 favicon，但保持来源为用户提供 Logo。
- **品牌区三列布局挤压版本号或收起按钮** → 在 1366×768 与 1440×1024 验收，文本允许使用 `minmax(0, 1fr)` 与合理 truncation。
- **favicon 在 dev 与 Docker 路径不一致** → 使用 public 静态路径并在 Docker Web smoke 或静态构建检查中确认。
- **旧 CSS `.brand-head` / `.product-logo-*` 规则与新结构冲突** → 实现时优先复用或局部替换，避免新增全局裸 Hex 或破坏导航样式。

## Migration Plan

1. 将 Logo 静态资源加入 Web public 资产目录。
2. 更新 AdminSidebar 品牌区 DOM 与 CSS。
3. 更新入口 HTML favicon / apple-touch-icon 声明。
4. 补充前端测试与视觉验收记录。
5. 不执行数据库迁移、不执行 Orval。

Rollback：恢复入口 HTML 图标链接与 AdminSidebar 品牌区 DOM/CSS 即可，不涉及服务端数据回滚。

## Open Questions

- favicon 最终是否使用完整 Logo 缩略图还是从 Logo 派生的仅图形标识，由实现阶段根据 16×16 / 32×32 可读性决定。
