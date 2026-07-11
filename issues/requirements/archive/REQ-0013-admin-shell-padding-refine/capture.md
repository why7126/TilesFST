---
req_id: REQ-0013-admin-shell-padding-refine
status: done
created_at: 2026-06-28 08:55:41
updated_at: 2026-07-11 17:18:39
recorded_by: product
source: 反馈
priority_hint: P1
parent_requirement: REQ-0004-admin-home
---

# 一句话

管理端 Shell 收窄内外边距并采用 fluid 内容宽：侧栏与主内容区减小水平/上 padding；`content-inner` 统一为软上限 1400px；提升宽屏列表信息密度。

# 原始描述

左侧栏减左右 padding，右侧内容区减左右 padding 以及上 padding。

反馈场景（瓷砖 SKU 列表页 `/admin/tile-skus`，宽屏）：侧栏菜单文字与列宽之间留白过多；主内容区 breadcrumb 上方、表格左右到窗口边缘存在明显对称暗区。当前实现源自 `admin-home.css`：

- `.sidebar { padding: 30px 18px 18px }` 及 nav-item / sidebar-head 多层水平 padding
- `.main-content { padding: 48px 56px 72px }`
- `.content-inner { max-width: 1080px; margin: 0 auto }`（SKU 页 override 为 1120px）

# 背景与关联

- 父需求：`REQ-0004-admin-home`（定义 264px 侧栏 + 1080px 内容上限的原型 port）
- 关联：`REQ-0011-admin-sidebar-expand-collapse`（侧栏宽 264↔72 契约，本需求不改动列宽；collapsed padding MODIFIED）
- 关联：`BUG-0021-sidebar-menu-icons-indistinguishable`（侧栏占位图标，可并行但不属本 REQ 范围）
- 影响范围：所有 `/admin/*` 页面共用 `AdminLayout` + `admin-home.css`

# 待澄清

- [x] 目标 padding 具体数值 — **已定**（见探索结论）；**MUST** prototype 定稿 Golden Reference
- [x] `content-inner` max-width / fluid — **策略 B**：`min(1400px, 100%)`；删除 SKU 页 1120px override
- [x] 收起态侧栏（72px）padding — **一并收紧**（与 expanded 6px 壳层对齐）
- [x] ≤1023px 响应式 breakpoint — **联动调整**（三档 token，tablet 勿沿用 desktop 6px）
- [x] 验收基准页 — **SKU 列表 / 用户管理 / Dashboard** 三页并排（1440×1024、1920×1080）
- [x] `main-content` 下 padding — **保持 72px 不改动**

# 探索结论（历史）

（/req-explore 2026-06-28；2026-06-28 09:04:54 决策确认；/req-complete 2026-06-28 已纳入 acceptance 与 prototype）

- **历史方案**：admin shell padding + content-inner fluid；曾建议 OpenSpec `fix-admin-shell-padding-refine`
- **历史 Padding**：main `32px 32px 72px`；sidebar expanded `30px 6px 18px`；collapsed `12px 6px 14px`
- **历史 Fluid 策略 B**：`min(1400px, 100%)`；删除 SKU 1120px override
- **验收页**：SKU / 用户管理 / Dashboard @ 1440 & 1920
- **Out**：列宽 264↔72、BUG-0021、bottom 72px 不变

详见 `acceptance.md` 与 `prototype/web/admin-shell-padding-refine-context.md`。

# 归档结论

2026-07-11 按用户指令以当前实际为准归档：本需求的原探索值已被 `BUG-0054-admin-content-padding-too-large` 修订，最终通过 `fix-admin-content-padding-too-large` 落地并归档。当前实现采用 `.main-content: 24px 24px 48px`、`.content-inner: min(1440px, 100%)`、expanded sidebar `30px 10px 18px`、collapsed sidebar `16px 10px 18px`；原 `32px 32px 72px` / `min(1400px, 100%)` / 6px 侧栏壳层仅保留为历史探索记录。
