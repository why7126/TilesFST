---
title: 业务流程
purpose: 描述管理端 Shell padding 与 content fluid 变更影响
content: 基于 requirement.md 提炼
source: AI 根据 PRD 生成，项目团队确认
update_method: PRD 变更时同步更新
owner: product
status: done
created_at: 2026-06-28 09:20:59
updated_at: 2026-07-11 17:18:39
note: REQ-0013-admin-shell-padding-refine
---

# 业务流程

## 1. 与父需求 REQ-0004 的差异

| 维度 | REQ-0004（admin-home port） | REQ-0013（本需求） |
|---|---|---|
| 侧栏水平 padding | 18px | **10px**（expanded，当前实际） |
| 主内容 padding | `48px 56px 72px` | **`24px 24px 48px`**（当前实际） |
| content-inner | `max-width: 1080px` 居中 | **`min(1440px, 100%)`**（当前实际） |
| 列宽 | 264px | **不变** |
| 交互 | 无折叠 | 继承 REQ-0011 折叠（本 REQ 不改） |

```text
REQ-0004 Golden                    REQ-0013 MODIFIED
────────────────────────────────────────────────────────────
1080px 固定 cap            →      1440px 软 cap + fluid
56px main 左右 gutter      →      24px
18px sidebar 内边距        →      10px
SKU 1120px 页级 override   →      删除，统一 shell token
```

说明：REQ-0013 原探索值为 `32px 32px 72px`、`min(1400px, 100%)`、expanded sidebar 6px。后续 `BUG-0054-admin-content-padding-too-large` 明确修订为当前更紧凑的内容区策略，并已通过 `fix-admin-content-padding-too-large` 归档。

## 2. 与 REQ-0011 的差异

| 维度 | REQ-0011 | REQ-0013 |
|---|---|---|
| 侧栏宽度 | 264 ↔ 72 | **不变** |
| chevron / localStorage | In scope | **Out** |
| collapsed padding | `16px 8px 18px` | **`16px 10px 18px`**（当前实际） |
| ≤1023px 结构 | 双列 nav 等 | **结构不变，仅 padding 数值** |

## 3. 壳层渲染（无新增用户操作）

本需求 **不引入新交互**；用户进入 `/admin/*` 时自动应用新 spacing。

```text
用户进入 /admin/*（已登录）
  ↓
AdminLayout 挂载（与现网相同）
  ↓
.admin-shell 应用 CSS token：
  ├─ --admin-sidebar-width: 264 | 72（REQ-0011，不变）
  ├─ sidebar padding: 30px 10px 18px（expanded）| 16px 10px 18px（collapsed）
  ├─ .main-content: 24px 24px 48px（>1023px）
  └─ .content-inner: min(1440px, 100%)
  ↓
Outlet 渲染业务页（SKU / 用户 / Dashboard …）
  ↓
业务页 MUST NOT 再 override content-inner max-width
```

## 4. 视口断点切换

```text
视口宽度变化
  ↓
  ├─ > 1023px（desktop）
  │     ├─ expanded / collapsed padding token（FR-002/003）
  │     └─ content-inner fluid cap 1440px
  │
  ├─ ≤ 1023px（tablet）
  │     ├─ sidebar 全宽 grid；padding 22px 20px（非 desktop 紧凑值）
  │     ├─ main 20px 16px 40px
  │     └─ REQ-0011：chevron 隐藏、user menu 隐藏
  │
  └─ ≤ 639px（mobile）
        └─ main 16px 12px 32px
```

## 5. 侧栏折叠（REQ-0011 行为保持）

```text
用户点击 chevron（>1023px）
  ↓
--admin-sidebar-width: 264 → 72（REQ-0011，不变）
  ↓
padding 同步切换：
  expanded  30px 10px 18px
  collapsed 16px 10px 18px
  ↓
.main-content 列宽增加 ~192px
  ↓
.content-inner 仍 min(1440px, 100%) — 列表更宽
```

## 6. 实施与回归流

```text
/fix-admin-content-padding-too-large apply
  ↓
admin-home.css：spacing + content-inner max-width 当前策略
  ↓
删除 tile-sku-management.css content-inner override
  ↓
Vitest：AdminSidebar.collapse + AdminLayout
  ↓
三页人工验收：/admin/tile-skus | /admin/users | /admin/dashboard
  ↓
1440 / 1920 PNG 与 prototype HTML 并排
```
