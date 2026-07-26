---
created_at: 2026-06-28 18:45:00
updated_at: 2026-06-28 18:56:51
change_id: fix-banner-modal-width-css-cascade
linked_bug: BUG-0048-banner-modal-width-css-cascade-overridden
linked_req: REQ-0016-banner-management
status: archived
---

# Change 追溯

## 关联

| 项 | ID |
|---|---|
| BUG | BUG-0048-banner-modal-width-css-cascade-overridden |
| REQ | REQ-0016-banner-management |
| 父 BUG | BUG-0040-banner-modal-width-too-narrow |
| 前置 Change | fix-banner-list-and-modal-ui |

## 验收 Checklist

- [x] 移除 `modal-card` 双类名（`BannerFormModal.tsx` 仅 `banner-modal-card`）
- [x] Vitest import `user-management.css` + `banner-management.css` + `system-settings.css`；断言无 `modal-card` 类
- [x] Vitest 断言冲突栈含 `.modal-card { 520px }` 与 `.banner-modal-card { 880px }`
- [x] `vitest run BannerFormModal` 3/3 pass；`vite build` pass
- [ ] DevTools Computed `.banner-modal-card` width = 880px（archive 前人工冒烟推荐）
- [ ] Banner vs SKU 弹窗并排 880px（archive 前人工冒烟推荐）
- [x] BUG-0048 acceptance AC-001～AC-010 已勾选

## Apply 记录（2026-06-28 18:53:52）

**根因修复：** `BannerFormModal.tsx` L311 `className="modal-card banner-modal-card"` → `"banner-modal-card"`。

**层叠说明：** 元素不再匹配 `.admin-shell .modal-card { width: 520px }`（`user-management.css` / `system-settings.css`），仅命中 `.banner-modal-card { width: 880px }`。

**测试：** `BannerFormModal.test.tsx` — 完整 CSS 冲突栈 import + 单类名断言 + 520/880 源规则对照。

**未改：** API、Orval、DB、裸 Hex。

## 备注

- 本 change 已 `/opsx-archive fix-banner-modal-width-css-cascade`（2026-06-28 18:56:51）。
- Delta spec 已合并至 `openspec/specs/web-client/spec.md`。
- BUG-0048 已 promote → `issues/bugs/archive/`。
