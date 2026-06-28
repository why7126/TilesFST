---
bug_id: BUG-0040-banner-modal-width-too-narrow
status: pending_review
created_at: 2026-06-28 17:43:07
updated_at: 2026-06-28 17:43:07
root_cause_type: design
---

# 根因分析

## 1. 直接原因

### 1.1 CSS 固定 Banner 弹窗宽度 640px

`banner-management.css`：

```css
.admin-shell .banner-modal-card {
  width: 640px;
  max-width: 100%;
  max-height: 92vh;
  ...
}
```

`BannerFormModal.tsx` 使用 `className="modal-card banner-modal-card"`，弹窗宽度由上述规则决定。

### 1.2 SKU 复杂表单弹窗已采用 880px 档位

`tile-sku-management.css`：

```css
.admin-shell .sku-modal-card {
  width: 880px;
  max-width: 100%;
  ...
}
```

瓷砖 SKU 弹窗（多图、多视频、双列 grid）在 `add-tile-sku-management` 中确立 880px 为管理端「大表单」基准。Banner 弹窗字段复杂度相近（双列 grid、图片区、Combobox、有效期区间），却使用更窄的 640px。

### 1.3 640px 为 REQ-0016 原型与现行 OpenSpec 的明确要求

- 四套 `banner-management-modal-*.html`：`.modal-card { width: 640px; … }`
- `openspec/specs/web-client/spec.md`：`BannerFormModal` **MUST** 宽 640px（`fix-banner-admin-ui` 归档写入）
- `add-banner-management` trace checklist #8 验收「640px + 无状态块」

因此当前实现 **符合当时规范**，与用户「对齐 SKU 880px」诉求形成 **规范层冲突**。

## 2. 根本原因

### 2.1 REQ-0016 弹窗宽度策略与 SKU 管理页策略未统一

Banner 与 SKU 分属不同 REQ/Change 交付，弹窗宽度分别绑定各自 HTML 原型（640 vs 880），未建立管理端「复杂表单弹窗」统一宽度 token 或组件约束。

### 2.2 交付后 UX 反馈要求跨模块一致性

运营在维护 Banner 与 SKU 时感知弹窗宽度不一致；Banner 在 640px 下图片上传区、双列字段与 Combobox 横向偏紧。属 **体验策略调整**，非 BUG-0033 滚动修复遗漏。

### 2.3 规范变更须走 OpenSpec delta

将 Banner 弹窗改为 880px 必须 MODIFIED `web-client` spec 中 Banner 640px 条款，并更新 acceptance（覆盖 BUG-0033 AC-005「MUST 保持 640px」在加宽场景下的 delta）。不能仅改 CSS 而不更新 spec。

## 3. 触发条件

满足以下条件可 **100% 稳定复现**：

1. 以 admin 或 employee 登录 Web 管理端。
2. 打开 Banner 新增/编辑弹窗与 SKU 新增/编辑弹窗。
3. 视口宽度 ≥ 880px，并排对比弹窗宽度。

Banner 弹窗稳定为 640px（至 `max-width: 100%` 断点）；SKU 为 880px。

## 4. 分类结论

| 维度 | 结论 |
|---|---|
| 缺陷分类 | design / frontend-ui |
| 是否接口缺陷 | 否 |
| 是否数据库缺陷 | 否 |
| 是否权限缺陷 | 否 |
| 是否回归 | 否（按 spec 有意 640px） |
| 主要修复面 | `banner-management.css`（`.banner-modal-card` width）；可选对齐 `.sku-modal-card` head/footer 规则 |
| 关联 BUG | BUG-0033（加宽后须回归滚动、textarea、footer） |
| 建议 Change | `fix-banner-modal-width`（可与 BUG-0039 合并） |

## 5. 后续修复建议

1. 将 `.banner-modal-card` `width` 改为 `880px`，保留 `max-width: 100%`。
2. 可选：对齐 `.sku-modal-card` 的 `border`、`box-shadow`、`modal-head` padding、`max-height` 规则以统一大弹窗体验。
3. 回归 BUG-0033：`.modal-body` 滚动、运营备注整行、footer 可达。
4. `/bug-opsx` MODIFIED `web-client`：Banner 弹窗宽度 640px → 880px（或与 SKU 同宽）。
5. 验收基准：与 SKU 弹窗并排对比，而非 640px modal PNG Golden。
6. SHOULD 补充 Vitest 或 CSS 断言：`.banner-modal-card` 宽度 880px。
