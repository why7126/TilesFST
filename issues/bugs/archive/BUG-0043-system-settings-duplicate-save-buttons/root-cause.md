---
bug_id: BUG-0043-system-settings-duplicate-save-buttons
status: pending_review
created_at: 2026-06-28 18:35:49
updated_at: 2026-06-28 18:35:49
root_cause_type: design
---

# 根因分析

## 1. 直接原因

### 1.1 页头与底部各渲染「保存设置」

`SystemSettingsPage.tsx` 在 `settings-hero-actions`（L806–813）与 `SettingsFooter`（L93–103）两处渲染相同文案、样式、行为的保存按钮，均调用 `handleSave()`，disabled 条件均为 `saving || !dirty`。

### 1.2 测试假设双按钮

`SystemSettingsPage.test.tsx` 使用 `getAllByRole('button', { name: '保存设置' })` 并点击 `[0]`，与双按钮实现一致。

## 2. 根本原因

### 2.1 OpenSpec / REQ 明确要求双入口

`add-system-settings` spec 与 REQ-0017 **AC-009** 规定页头与底部均提供「保存设置」且行为一致；实现按 spec 交付。

### 2.2 与用户反馈及 Profile 修复模式未对齐

`fix-profile-duplicate-save-buttons` 已将个人资料页收敛为表单底单入口；用户反馈系统设置页头按钮多余，需在 fix change 中 **MODIFIED AC-009** reconcile。

### 2.3 页头 CTA 与底部 footer 职责重叠

底部 `settings-panel-footer` 已含「取消 / 恢复默认 / 保存设置」完整操作链；页头保存按钮与 dirty badge 并存，形成重复主 CTA。

## 3. 触发条件

1. `admin` 访问 `/admin/settings/*`。
2. 修改任意可写字段使表单 dirty。
3. 页头与底部均出现可点击「保存设置」。

## 4. 分类结论

| 维度 | 结论 |
|---|---|
| 缺陷分类 | design / frontend-ui |
| 是否回归 | 否 |
| 主要修复面 | `SystemSettingsPage.tsx`、测试、OpenSpec delta |
| 关联 BUG | BUG-0023 |
| 建议 Change | `fix-system-settings-duplicate-save-buttons` |

## 5. 后续修复建议

1. 移除 `settings-hero-actions` 内保存按钮；保留 dirty badge。
2. 更新 vitest 为单按钮断言。
3. delta spec MODIFIED AC-009：仅保留底部一处「保存设置」。
