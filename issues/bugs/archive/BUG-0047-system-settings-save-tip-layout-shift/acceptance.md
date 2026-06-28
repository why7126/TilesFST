---
bug_id: BUG-0047-system-settings-save-tip-layout-shift
status: pending_review
created_at: 2026-06-28 18:35:49
updated_at: 2026-06-28 18:35:49
related_requirement: REQ-0017-system-settings
related_bug: BUG-0015-admin-list-status-tips-layout-shift
---

# 回归验收标准

> 修复 MUST 消除保存/恢复成功提示导致的 layout shift，且 MUST NOT 回归 PATCH/reset 功能。推荐对齐 `AdminToast`（BUG-0015 模式）。

## AC-001 保存成功 MUST NOT 推挤主内容

**Given** `admin` 在 `/admin/settings/basic`  
**When** 修改字段并点击「保存设置」成功  
**Then** `settings-layout` 顶部位置 MUST NOT 相对保存前发生垂直位移（layout shift CLS ≈ 0）  
**And** 用户 MUST 仍能感知成功（toast 或 reserved 占位 tip）

- [ ] AC-001

## AC-002 恢复默认成功 MUST NOT 推挤主内容

**Given** 用户确认恢复默认并成功  
**When** 成功反馈展示  
**Then** MUST 满足 AC-001 无推挤要求

- [ ] AC-002

## AC-003 成功文案 MUST 保持语义

**Given** 保存成功  
**Then** 提示 MUST 含「设置已保存并立即生效」或等价  
**Given** 恢复默认成功  
**Then** 提示 MUST 含「已恢复默认配置」或等价

- [ ] AC-003

## AC-004 若使用 AdminToast MUST 对齐列表页

**Given** 采用 AdminToast 方案  
**When** 保存成功  
**Then** MUST 在 `.admin-toast-region` 展示  
**And** 样式 MUST 与品牌/用户列表页 status toast 一致  
**And** `settings-save-tip` 条件块 SHOULD 移除或不再插入文档流

- [ ] AC-004

## AC-005 error tip 与 dirty badge MUST 无回归

**Given** 保存失败或加载失败  
**When** 展示 `settings-error-tip`  
**Then** 行为 MAY 保持现状（本 BUG 不强制改 error 展示）  
**And** dirty badge MUST 仍正常工作

- [ ] AC-005

## AC-006 REQ-0017 AC-012 delta（MODIFIED）

**Given** fix change 归档  
**Then** AC-012 MUST 更新为：保存成功提示 MUST 使用非推挤模式（AdminToast 或 reserved 占位），MUST NOT 因 tip 出现导致主内容 layout shift

- [ ] AC-006

## AC-007 测试 MUST 通过

**Given** `/opsx-apply` 完成  
**When** `pnpm vitest run src/pages/admin/SystemSettingsPage`  
**Then** MUST 通过

- [ ] AC-007
