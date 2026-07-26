## Context

- **现状**：`.admin-shell { grid-template-columns: 264px 1fr }` 写死；`AdminSidebar` 无折叠 state；REQ-0010 `add-product-version-display` 可能已扩展 brand-head（产品名 + version pill）。
- **依赖**：REQ-0004 Admin Shell；REQ-0010 头部（建议同 Sprint 内 REQ-0010 先行或并行 apply）。
- **原型来源**（优先级，design.md 声明）：
  1. `issues/requirements/archive/REQ-0011-admin-sidebar-expand-collapse/prototype/web/admin-sidebar-expanded.html`
  2. `issues/requirements/archive/REQ-0011-admin-sidebar-expand-collapse/prototype/web/admin-sidebar-collapsed.html`
  3. `issues/requirements/archive/REQ-0011-admin-sidebar-expand-collapse/prototype/web/images/*.png`（Golden Reference — 待导出）
  4. SoulKing 参考图（`/req-capture` 附件）
  5. `issues/requirements/archive/REQ-0011-admin-sidebar-expand-collapse/prototype/web/admin-sidebar-collapse-context.md`
  6. `issues/requirements/archive/REQ-0011-admin-sidebar-expand-collapse/acceptance.md`
  7. `rules/ui-design.md`
  8. `openspec/specs/admin-dashboard/spec.md`、`openspec/specs/web-client/spec.md`

## Conflict Resolution

| 检查项 | admin-home.css / 现网 | expanded/collapsed HTML | REQ-0011 acceptance | openspec/specs | 决议 |
|--------|----------------------|-------------------------|----------------------|----------------|------|
| 侧栏宽度 | 固定 264px | 264 / 72 CSS var | FR-002 | Shell 264px 固定 | **MODIFIED** Shell 可变 `--admin-sidebar-width` |
| 头部 | `.logo` 或 REQ-0010 brand-head | `.sidebar-head` + chevron | FR-003/004 | 仅 TILESFST | **MODIFIED** 品牌与导航 + chevron |
| 收起裁剪 | 无 | 隐藏文案/版本/分区标题 | FR-005 | 无 | **MODIFIED** collapsed 规则 |
| 用户菜单 | 全量 trigger | collapsed 仅 avatar | FR-005/006 | 桌面全量 | **MODIFIED** collapsed avatar-only |
| ≤1023px | 顶栏双列 nav | 不展示 toggle | FR-007 Out | 现有 @media | **无变更** mobile |
| 店主端 Sidebar | — | Out | Out | — | 无变更 |

## Goals / Non-Goals

**Goals:**

- 桌面（>1023px）expanded ↔ collapsed；localStorage 持久化；chevron 头部右上；Vitest + HTML 并排验收。

**Non-Goals:**

- 店主端筛选 Sidebar；mobile drawer；flyout 子菜单；Lucide 真图标替换；REQ-0010 版本 pill 本身。

## Decisions

### D1：实现策略 — CSS Port + React Context（非整页 HTML Port）

- **决策**：在 `AdminLayout` 用 `useState` + `useEffect` 读写 `localStorage`；`.admin-shell` 设 `data-sidebar-state="expanded|collapsed"` 与 `--admin-sidebar-width`；`admin-home.css` 增加 collapsed 修饰类；chevron 用 Lucide `ChevronLeft`/`ChevronRight` 或等价 DS 图标。
- **理由**：与现有 `admin-home.css` Port 策略一致；改动面集中在 Layout + Sidebar + CSS。
- **备选**：纯 CSS `:has()` 无 state — 无法持久化；弃用。

### D2：宽度与动画 token

```css
.admin-shell {
  --admin-sidebar-width: 264px;
  grid-template-columns: var(--admin-sidebar-width) 1fr;
  transition: grid-template-columns 220ms ease;
}
.admin-shell[data-sidebar-state='collapsed'] {
  --admin-sidebar-width: 72px;
}
```

- `prefers-reduced-motion: reduce` 下 `transition: none`。

### D3：REQ-0010 兼容

- expanded：brand-head 行内右对齐 chevron；不遮挡 version pill。
- collapsed：隐藏 brand 文案与 pill，保留缩略 mark（如 `TF`）+ chevron。
- 若 REQ-0010 未 merge：`.logo` 行 + chevron；REQ-0010 apply 后仅调整头部 DOM，不改 toggle API。

### D4：无障碍

- chevron：`aria-expanded`、`aria-label`（收起/展开侧边栏）、键盘 Enter/Space。
- collapsed nav：`aria-label={item.label}`。

## Risks / Trade-offs

| 风险 | 缓解 |
|------|------|
| REQ-0010 头部 DOM 变更 | design D3；同 Sprint 顺序 |
| Grid transition 性能 | 仅 animating grid column；短 duration |
| PNG 未导出 | apply trace checklist；非阻塞 archive |

## Migration Plan

- 无数据/API 迁移；localStorage 新 key；回滚 revert 前端即可。

## Open Questions

- 无（REQ-0011 approved）。
