---
bug_id: BUG-0048-banner-modal-width-css-cascade-overridden
status: captured
created_at: 2026-06-28 18:10:30
updated_at: 2026-06-28 18:10:30
severity_hint: medium
environment: local|docker
related_requirement: REQ-0016-banner-management
related_bug: BUG-0040-banner-modal-width-too-narrow
follow_up_of: BUG-0040-banner-modal-width-too-narrow
---

# 现象

BUG-0040 在 `fix-banner-list-and-modal-ui` 中已将 `.banner-modal-card` 设为 880px，但 Banner 新增/编辑弹窗在浏览器中**实际宽度仍约 520px**（明显窄于瓷砖 SKU 弹窗 880px），880px 样式未生效。

# 复现步骤

1. 以 admin 登录 Web 管理端（本地 dev 或 Docker 构建产物均可）。
2. 进入「Banner 管理」，点击「新增 Banner」或「编辑」打开弹窗。
3. DevTools 选中 `.banner-modal-card`，查看 Computed → `width`（约 520px，非 880px）。
4. 对比「瓷砖 SKU 管理」新增/编辑弹窗 `.sku-modal-card` 的 `width`（880px）。

# 期望 vs 实际

| | 说明 |
|---|---|
| **期望** | Banner 弹窗外卡片 Computed width 为 880px（`max-width: 100%` 窄视口除外），与 SKU 弹窗并排视觉一致。 |
| **实际** | `banner-management.css` 虽声明 880px，但元素同时带 `modal-card` 类，被 bundle 中较晚出现的 `system-settings.css` → `.admin-shell .modal-card { width: 520px }` 覆盖。 |

# 初步根因（explore 结论，待 bug-complete 正式化）

- `BannerFormModal.tsx`：`className="modal-card banner-modal-card"`（SKU 仅用 `sku-modal-card`，无冲突）。
- 生产 CSS bundle 层叠顺序：`banner-modal-card` 880px 之后仍有 `.admin-shell .modal-card` 520px 规则生效。
- Vitest 仅断言源 CSS 文件含 880px，未覆盖全 bundle 层叠。

# 附件

- screenshots/（待补充：Banner vs SKU 弹窗并排对比）
- logs/
