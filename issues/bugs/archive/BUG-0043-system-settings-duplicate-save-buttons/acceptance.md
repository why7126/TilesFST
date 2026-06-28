---
bug_id: BUG-0043-system-settings-duplicate-save-buttons
status: pending_review
created_at: 2026-06-28 18:35:49
updated_at: 2026-06-28 18:35:49
related_requirement: REQ-0017-system-settings
related_bug: BUG-0023-profile-duplicate-save-buttons
---

# 回归验收标准

> 修复 MUST 使系统设置页仅保留一处「保存设置」主 CTA（底部 footer），且 MUST NOT 回归 PATCH、取消、恢复默认与 dirty 提示。

## AC-001 全页 MUST 仅有一处「保存设置」按钮

**Given** `admin` 访问 `/admin/settings/basic` 并修改字段使表单 dirty  
**When** 统计 accessible name 为「保存设置」的 button  
**Then** MUST 恰好为 **1** 个  
**And** `settings-hero-actions` MUST NOT 含「保存设置」

- [ ] AC-001

## AC-002 保留按钮 MUST 位于 panel footer

**Given** 修复完成  
**When** 查看 `settings-panel-footer`  
**Then** MUST 含「取消」「恢复默认」「保存设置」且顺序不变  
**And** 「保存设置」MUST 使用 `settings-btn primary`

- [ ] AC-002

## AC-003 页头 MUST 保留 dirty badge

**Given** 用户修改未保存字段  
**When** 查看 `settings-hero-actions`  
**Then** MUST 展示「有未保存修改」badge（若实现保留该 UX）  
**And** MUST NOT 因移除保存按钮导致 badge 布局破损

- [ ] AC-003

## AC-004 保存行为 MUST 无回归

**Given** 用户修改 basic 分组字段  
**When** 点击唯一「保存设置」  
**Then** MUST 调用 `PATCH /api/v1/admin/system-settings/basic`  
**And** 成功后 MUST 展示成功提示（文案与修复前一致）  
**And** dirty 态 MUST 清除

- [ ] AC-004

## AC-005 测试 MUST 单按钮断言

**Given** `/opsx-apply` 完成  
**When** 运行 `cd src/web && pnpm vitest run src/pages/admin/SystemSettingsPage`  
**Then** MUST 通过  
**And** 保存用例 MUST 使用 `getByRole('button', { name: '保存设置' })`

- [ ] AC-005

## AC-006 REQ-0017 AC-009 delta（MODIFIED）

**Given** fix change 归档  
**Then** AC-009 MUST 更新为：页面 **MUST** 仅在底部 footer 提供一处「保存设置」主 CTA，**MUST NOT** 页头与底部重复

- [ ] AC-006
