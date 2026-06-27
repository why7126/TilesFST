---
bug_id: BUG-0013-product-version-ui-inconsistency
status: pending_review
created_at: 2026-06-27 10:59:01
updated_at: 2026-06-27 10:59:01
root_cause_type: design
---

# 根因分析

## 1. 直接原因

### 1.1 `ProductVersionBadge` 为 ad-hoc 实现，未复用 Design System `Badge` 组件

`add-product-version-display` 新增独立组件 `src/web/src/shared/ui/product-version-badge.tsx`，使用手写 Tailwind class 组合，**未**基于既有 `src/web/src/shared/ui/badge.tsx` 的 `neutral` variant 扩展。

当前实现：

```tsx
'inline-flex h-[18px] items-center rounded-industrial border border-border-chip bg-surface/30 px-[7px] text-[10px] leading-none tracking-wide text-muted'
```

Design System `Badge` neutral variant 基准：

```tsx
'inline-flex items-center rounded-[1px] px-[7px] py-[2px] text-[9px] font-medium tracking-badge uppercase border border-border-chip bg-transparent text-muted'
```

二者在圆角（2px vs 1px）、字号（10px vs 9px）、字重（缺 `font-medium`）、字距（`tracking-wide` vs `tracking-badge`）、背景（`bg-surface/30` vs `bg-transparent`）上均不一致，导致 pill 形态偏离 DS §8 徽章规范与 `/design-system` 既有 Badge 预览。

### 1.2 样式规格在原型 context 与 ui-design §8 之间取「中间值」，未对齐任一权威源

| 属性 | 原型 `.version-pill` | ui-design §8 / Badge | 当前实现 |
|------|---------------------|----------------------|----------|
| 圆角 | 2px | 1px (`--radius-badge`) | `rounded-industrial` 2px |
| 字号 | 10px | 9px | 10px |
| padding | 2px 7px | 2px 7px | 仅 `px-[7px]` + `h-[18px]` |
| 字重 | — | 500 | 未设 |
| 字距 | 0.04em | `tracking-badge` | `tracking-wide` |
| 背景 | `rgba(255,255,255,0.03)` | 按 variant | `bg-surface/30` |
| 边框 | `--line-strong` (0.1) | `border-border-chip` | `border-border-chip` |

实现者在 D1 决策中选择「Tailwind DS + 共享组件」，但未在 apply 阶段完成与原型 HTML / Golden Reference 的并排视觉验收，也未强制对齐 `Badge` 组件。

### 1.3 管理端 brand-head 仅 port 了产品名 CSS，版本 pill 无 shell 级样式兜底

`admin-home.css` 为 `.brand-head .logo-text` 定义了 serif 金色品牌样式，但**未**为版本 pill 提供与原型 `.version-pill` 等价的 scoped CSS。pill 完全依赖 Tailwind utility；在 `.admin-shell { color: var(--admin-text) }` 继承环境下，若边框/背景对比度不足，版本号在视觉上退化为偏亮 sans-serif 主文字，缺乏 pill 容器感（与用户截图一致）。

### 1.4 测试仅断言文案存在，未覆盖视觉 class 与并排验收

- `AdminSidebar.user-mgmt.test.tsx` / `sidebar.test.tsx` 仅 `getByText(PRODUCT_VERSION)`，不校验 pill 边框、muted 色、圆角等 class。
- `add-product-version-display` tasks 7.2 将 1280×1024 并排验收标为完成，但 AC-015 要求的 admin/catalog HTML 原型 PNG 并排**未**作为阻塞项执行；REQ-0010 AC-006/AC-013/AC-015 视觉项未闭环。

## 2. 根本原因

### 2.1 功能优先、视觉验收门禁不足

`add-product-version-display` 以「常量 + 挂载 + Vitest 文案」为完成标准，apply 阶段缺少强制 PNG/HTML 并排 checklist（对比 BUG-0002、BUG-0009 等 UI fix 流程），导致 REQ-0010 功能 AC 通过但 FR-004 视觉 AC 未达标仍被标记 tasks complete。

### 2.2 组件选用优先级未执行

AGENTS.md 要求 Web UI **优先复用** `shared/ui/` 既有组件。版本 pill 语义上属于 DS §8 徽章，应扩展 `Badge`（neutral 或新增 `version` variant）而非新建平行组件；新建组件缺少与 Design System 验收页（`/design-system`）的同步展示与对照。

### 2.3 管理端 CSS Port 与 Tailwind 组件混用策略不一致

管理端 shell 大量样式在 `admin-home.css`（port 自 HTML），brand-head 产品名走 CSS class（`.logo-text`），版本 pill 却纯 Tailwind——同一 brand-head 区域内两种 styling 策略并存，pill 在 admin 渐变侧栏背景下难以达到原型 `.version-pill` 的可见度与层级。

## 3. 触发条件

满足以下条件时可稳定复现：

1. 以 admin 登录 Web 管理端（local 或 Docker）。
2. 访问任意 `/admin/*` 页面（经 `AdminLayout` + `AdminSidebar`）。
3. 观察侧边栏顶部 `TILESFST` 右侧 `v0.0.1`。
4. 与 `product-version-sidebar-admin.html`、Golden Reference PNG、用户截图 `screenshots/admin-sidebar-version-actual.png` 并排对比。
5. 可选：店主端 `Sidebar` brand-head 同样使用 `ProductVersionBadge`，存在相同 pill 偏差。

## 4. 分类结论

| 维度 | 结论 |
|---|---|
| 缺陷分类 | design / frontend-ui |
| 是否接口缺陷 | 否 |
| 是否数据库缺陷 | 否 |
| 是否权限缺陷 | 否 |
| 主要修复面 | `ProductVersionBadge`（或改为 `Badge` variant）+ 可选 `admin-home.css` brand-head pill 兜底 |
| 关联需求 AC | REQ-0010 AC-006、AC-013、AC-015 |
| 关联 Change | `add-product-version-display`（功能已交付，需 `fix-product-version-ui-inconsistency`） |

## 5. 后续修复建议

1. **优先**：重构 `ProductVersionBadge` 为 `Badge` 组件的 `version`/`neutral` variant 扩展，对齐 `rules/ui-design.md` §8（padding 2px 7px、font-weight 500、tracking-badge、semantic token）。
2. **管理端**：在 `admin-home.css` 为 `.brand-head` 内 pill 增加与原型 `.version-pill` 等价的 scoped 样式（或确保 Tailwind 组合在 admin shell 下可见度达标）。
3. **验收**：fix Change 的 `tasks.md` MUST 含 admin/catalog 原型 HTML + Golden Reference PNG 并排 checklist；`trace.md` 记录结论。
4. **测试**：Vitest 断言 pill 渲染含关键 class（如 `border-border-chip`、`text-muted`、`rounded-industrial` 或 Badge variant class）；可选 snapshot。
5. **Change 命名**：`fix-product-version-ui-inconsistency`。
6. **Design System**：在 `/design-system` 预览区展示 `ProductVersionBadge` 与原型并排说明。
