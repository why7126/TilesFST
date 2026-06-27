# REQ-0011 管理端侧边栏展开/收起 — 原型上下文

## 1. 优先级（design.md / opsx-apply 引用）

1. `prototype/web/admin-sidebar-expanded.html`
2. `prototype/web/admin-sidebar-collapsed.html`
3. `prototype/web/images/*.png`（Golden Reference，待导出）
4. SoulKing 参考图（`/req-capture` 附件）
5. `acceptance.md`
6. `rules/ui-design.md`
7. `openspec/specs/web-client/spec.md`

## 2. 基线

- 管理端壳层与 nav 样式沿用 `REQ-0005-brand-management/prototype/web/brand-management.html` 侧栏结构。
- 本需求为 **增量**：在侧栏头部增加 `.sidebar-head` + `.sidebar-toggle`，并定义 `data-sidebar-state`。

## 3. 布局 token

| Token / 变量 | expanded | collapsed |
|---|---|---|
| `--admin-sidebar-width` | 264px | 72px |
| `.admin-shell` grid | `var(--admin-sidebar-width) 1fr` | 同左 |
| 侧栏 padding | 30px 18px 18px | 16px 8px（实现可微调，须容纳 34px avatar） |
| 头部 | brand + subtitle + version pill + chevron | logo 缩略块 + chevron |
| `.nav-title` | 可见 | `display: none` |
| nav label | 可见 | 视觉隐藏，保留 aria-label |
| `.user-trigger` | 三列 grid | 仅 `.avatar` 居中 |

## 4. Chevron

| 状态 | 图标 | aria-label |
|---|---|---|
| expanded | `‹` / ChevronLeft | 收起侧边栏 |
| collapsed | `›` / ChevronRight | 展开侧边栏 |

- 位置：`.sidebar-head` 内 `justify-content: space-between`，chevron 右对齐。
- 颜色：`var(--weak)` / hover `var(--text)`。

## 5. Active 项（collapsed）

- 保留 `.nav-item.active` 金色与左侧 2px bar；窄宽下 nav-item 可 `justify-content: center`。
- icon-only 时 bar 仍贴左缘或改为 bottom accent（实现择一，须在 trace PNG 验收中一致）。

## 6. 交互（HTML 原型）

- `admin-sidebar-expanded.html`：静态 expanded 态 + 可点击 chevron 跳转至 collapsed 页（或同页 query）。
- `admin-sidebar-collapsed.html`：静态 collapsed 态。
- 实现阶段：单页 React state + localStorage，无需双 HTML 路由。

## 7. 与 REQ-0010 头部

- expanded 头部示意：

```text
[TILESFST] [v0.0.1]                    [‹]
瓷砖信息管理平台
```

- collapsed 头部示意：

```text
[TF]                                   [›]
```

- 若 REQ-0010 未合并，原型可用 `.logo` 单行代替 product + badge。

## 8. 响应式

- 原型仅描述 **桌面 > 1023px**。
- ≤ 1023px 不展示 `.sidebar-toggle`（与 PRD FR-007 一致）。

## 9. PNG 导出清单（待人工 / opsx-apply）

| 文件 | 说明 |
|---|---|
| `images/admin-sidebar-expanded.png` | 1280×1024，expanded + 品牌页主内容 |
| `images/admin-sidebar-collapsed.png` | 1280×1024，collapsed + 主内容区变宽 |

## 10. 验收说明

- opsx-apply 时在 `/admin/brands` 或 `/admin/dashboard` 与两 HTML 原型并排 checklist。
- Vitest 覆盖 chevron、aria、localStorage，见 `acceptance.md` AC-026–AC-029。
