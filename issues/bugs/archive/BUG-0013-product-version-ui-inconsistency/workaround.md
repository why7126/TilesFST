---
bug_id: BUG-0013-product-version-ui-inconsistency
status: pending_review
created_at: 2026-06-27 10:59:01
updated_at: 2026-06-27 10:59:01
---

# 临时规避方案

## 1. 可用性规避

该缺陷不阻断产品版本号功能，当前可继续使用：

1. 管理端与店主端侧边栏顶部均已展示正确的产品版本文案（如 `v0.0.1`），与 `PRODUCT_VERSION` 常量一致。
2. 登录、导航、筛选、列表、CRUD 等核心功能均不受影响。
3. 读屏用户可通过 `aria-label="产品版本 v0.0.1"` 感知版本信息。

## 2. 验收规避

在正式修复前，验收 REQ-0010 时应明确标注：

- 版本 pill 视觉（AC-006、AC-013、AC-015）**暂不作为通过项**。
- 仅验证版本常量单一源、展示位置、文案一致性与 a11y 标签是否满足 FR-001～FR-003 功能项。
- `add-product-version-display` archive 后若视觉未达标，须以本 BUG 的 `fix-*` Change 闭环，不得视为 REQ-0010 全量验收通过。

## 3. 运营规避

内部用户报障或沟通时：

1. 可通过侧边栏顶部版本文案确认当前产品版本。
2. 若 pill 视觉难以辨认，以可见文字 `v0.0.1` 为准（功能正确，样式待修）。

## 4. 风险说明

该规避方案只能保证功能可用，不能消除以下问题：

- 侧边栏 brand-head 视觉层级与 Golden Reference / 原型不一致。
- Design System 徽章规范（§8）与管理端整体工业石材暗色旗舰风未对齐。
- 店主端与管理端共用 `ProductVersionBadge`，两端同步存在 pill 视觉偏差。

因此仍建议进入 `/bug-review BUG-0013 --approve`，评审通过后通过 `fix-product-version-ui-inconsistency` OpenSpec Change 修复。
