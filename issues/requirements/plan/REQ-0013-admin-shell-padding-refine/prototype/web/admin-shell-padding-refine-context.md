---
title: REQ-0013 Shell padding 原型说明
purpose: admin-shell-padding-refine 原型优先级与 token 定稿
content: Golden Reference for fix-admin-shell-padding-refine
source: /req-complete REQ-0013
update_method: PRD 或 acceptance 变更时同步
owner: product
status: draft
created_at: 2026-06-28 09:20:59
updated_at: 2026-06-28 09:20:59
note: REQ-0013-admin-shell-padding-refine
---

# admin-shell-padding-refine-context

## 1. 原型优先级（apply / 验收）

```text
1. prototype/web/admin-shell-padding-refine-expanded.html
2. prototype/web/admin-shell-padding-refine-collapsed.html
3. prototype/web/admin-shell-padding-refine-tablet.html
4. prototype/web/admin-shell-padding-refine-context.md（本文件）
5. issues/.../acceptance.md
6. rules/ui-design.md
7. openspec/specs/（已归档 admin-home / sidebar）
```

## 2. CSS Token 定稿（>1023px desktop）

| Token / 选择器 | 变更前 | 定稿值 |
|---|---|---|
| `--admin-sidebar-width` expanded | 264px | **264px**（不变） |
| `--admin-sidebar-width` collapsed | 72px | **72px**（不变） |
| `.sidebar` padding expanded | `30px 18px 18px` | **`30px 6px 18px`** |
| `.sidebar` padding collapsed | `16px 8px 18px` | **`12px 6px 14px`** |
| `.sidebar-head` | `0 8px 28px 14px` | **`0 6px 20px 8px`**（实现可 ±2px） |
| `.nav-title` | `0 14px` | **`0 8px`** |
| `.nav-item` | `0 12px` | **`0 8px`** |
| `.main-content` | `48px 56px 72px` | **`32px 32px 72px`** |
| `.content-inner` | `1080px` | **`min(1400px, 100%)`** |

建议实现变量：

```css
--admin-content-max-width: min(1400px, 100%);
--admin-main-padding-block: 32px 72px;
--admin-main-padding-inline: 32px;
--admin-sidebar-padding-inline: 6px;
```

## 3. 响应式 Token

| 断点 | `.sidebar` padding | `.main-content` padding |
|---|---|---|
| ≤1023px | **`18px 16px`** | **`24px 20px 56px`** |
| ≤639px | （结构同 REQ-0011） | **`24px 16px 40px`** |

## 4. Gutter 验收阈值（acceptance AC-018～020）

| 视口 | 侧栏态 | 指标 |
|---|---|---|
| 1920×1080 | expanded | 侧栏右缘 → content-inner 左缘 **≤128px** |
| 1920×1080 | expanded | content-inner 右缘 → 视口右缘 **≤128px** |
| 1440×1024 | expanded | 侧栏右缘 → content-inner 左缘 **≤32px** |
| 1920×1080 | expanded | content-inner 宽度 **=1400px** |
| 1440×1024 | expanded | content-inner 宽度 **≥1110px** |

## 5. HTML 文件说明

| 文件 | 用途 |
|---|---|
| `admin-shell-padding-refine-expanded.html` | Golden：expanded + SKU 表格示意 + gutter 标注 |
| `admin-shell-padding-refine-collapsed.html` | Golden：72px + 6px 壳层 |
| `admin-shell-padding-refine-tablet.html` | Golden：≤1023 全宽侧栏 + main padding |

## 6. PNG Golden（待导出，非阻塞 req-opsx）

| 文件 | 尺寸 |
|---|---|
| `prototype/web/images/admin-shell-padding-1440-expanded.png` | 1440×1024 |
| `prototype/web/images/admin-shell-padding-1920-expanded.png` | 1920×1080 |
| `prototype/web/images/admin-shell-padding-collapsed-sku.png` | 1920×1080 collapsed |
| `prototype/web/images/admin-shell-padding-tablet-1023.png` | 1023×768 |

## 7. MODIFIED 关系

- **REQ-0004-admin-home**：1080 cap / 56px main / 18px sidebar → 本 token 表
- **REQ-0011-admin-sidebar-expand-collapse**：collapsed padding MODIFIED；列宽与 chevron **不变**
- **REQ-0006-tile-sku-management**：删除页级 `1120px` override

## 8. 验收基准页（生产路由）

- `/admin/tile-skus`
- `/admin/users`
- `/admin/dashboard`
