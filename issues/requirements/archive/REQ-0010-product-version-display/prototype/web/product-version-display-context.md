# REQ-0010 产品版本号展示 — 原型上下文

## 1. 优先级（design.md 引用）

```text
1. prototype/web/*.html
2. prototype/web/images/sidebar-version-reference.png（Golden Reference — 布局参照）
3. prototype/web/product-version-display-context.md（本文件）
4. issues/.../acceptance.md
5. rules/ui-design.md §8 徽章与状态标签
```

## 2. Golden Reference

| 文件 | 说明 |
|------|------|
| `images/sidebar-version-reference.png` | 产品提供的 SoulKing 竞品参考：侧边栏顶部产品名 + 右侧 `v0.0.6` pill |
| `product-version-sidebar-admin.html` | 管理端增量原型：`.logo` 区扩展为产品名 + version pill |
| `product-version-sidebar-catalog.html` | 店主端增量原型：Sidebar 顶部 brand-head + version pill |

实现时 **布局语义** 对齐参考图；**品牌色与字体** 对齐 TilesFST Design System（管理端 gold `TILESFST`，店主端 `STONEX`）。

## 3. 管理端 brand-head

| 元素 | 内容 / 样式 |
|------|-------------|
| 容器 | `.brand-head` — flex 横排、align-items center、gap 8px；位于 `.sidebar` 内 `.nav-scroll` 之上 |
| 产品名 | `TILESFST` — 沿用 `.logo` 品牌字体、金色、`letter-spacing: 0.16em` |
| 版本 pill | `v0.0.1` — 高度约 18–20px，`padding: 2px 7px`，`border-radius: 2px`，边框 `var(--line-strong)`，文字 10px muted |
| 交互 | 纯展示，无 hover 跳转 |

## 4. 店主端 brand-head

| 元素 | 内容 / 样式 |
|------|-------------|
| 容器 | Sidebar 顶部，`padding-bottom: 16px`，`border-bottom: 0.5px solid border-default`，位于第一个 filter section 之上 |
| 品牌名 | `STONEX` — `font-brand text-sm tracking-brand`，金色强调 `ONE` 可选 |
| 版本 pill | 与管理端同一 pill 规格；值来自同一 `PRODUCT_VERSION` |
| 副标题 | 可选「瓷砖信息库」类 muted 副文案（非阻塞，实现时可省略） |

## 5. 版本常量

- 原型 HTML 中写死 `v0.0.1` 仅作视觉参考。
- 实现 MUST 使用 `src/shared/` 导出常量；发版人工更新。

## 6. 验收说明

- 管理端基线侧栏结构参考 `REQ-0006-tile-sku-management/prototype/web/tile-sku-management-list.html`；本需求仅增量描述 brand-head。
- 店主端基线参考 `LandingPage` + `Sidebar`；本需求在侧栏顶部新增 brand-head。
- 实现 PNG 导出（admin/catalog 各一）为 **Partially Ready 非阻塞项**；有 HTML + 参考 PNG 即可 req-opsx。
