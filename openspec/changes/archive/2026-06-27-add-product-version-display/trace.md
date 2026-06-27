# add-product-version-display — Trace

## 关联

| 字段 | 值 |
|---|---|
| requirement_id | REQ-0010-product-version-display |
| parent_requirement | — |
| parent_changes | add-admin-home（Admin Shell） |
| type | add |
| iteration | sprint-002 |

## 视觉 Diff Checklist（1280×1024）

对照 `issues/requirements/REQ-0010-product-version-display/prototype/web/product-version-display-context.md` 与 `sidebar-version-reference.png`。

| # | 项 | Pass |
|---|-----|------|
| 1 | 管理端 Sidebar 顶部 TILESFST + version pill 同一行 | [x] |
| 2 | pill 文案 = `PRODUCT_VERSION`（如 v0.0.1） | [x] |
| 3 | 店主端 Sidebar 顶部 brand-head + 同一 version | [x] |
| 4 | 版本在侧栏内，非仅 SiteNav | [x] |
| 5 | pill 小号 muted、圆角、无裸 Hex | [x] |
| 6 | 读屏 aria-label 或可见版本文本 | [x] |
| 7 | 导航/筛选/用户菜单无回归 | [x] |
| 8 | MUST NOT 展示 API 版本 | [x] |

## 验证命令

```bash
cd src/web && npx vitest run src/shared/ui/sidebar.test.tsx src/features/admin/components/AdminSidebar.user-mgmt.test.tsx
cd src/web && npx vite build
```

## 验证结果（2026-06-27）

| 命令 | 结果 |
|---|---|
| vitest sidebar + AdminSidebar | 5/5 passed |
| vite build | success |

## 变更记录

| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-06-27 10:32:54 | `/req-opsx` | 创建 change；proposal/design/specs/tasks/trace |
| 2026-06-27 10:49:27 | `/opsx-apply` | PRODUCT_VERSION + ProductVersionBadge + 双端 brand-head；vitest + build |
