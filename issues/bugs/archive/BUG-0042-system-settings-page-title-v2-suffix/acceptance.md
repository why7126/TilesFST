---
bug_id: BUG-0042-system-settings-page-title-v2-suffix
status: pending_review
created_at: 2026-06-28 18:35:49
updated_at: 2026-06-28 18:35:49
related_requirement: REQ-0017-system-settings
related_bug: null
---

# 回归验收标准

> 修复本缺陷 MUST 使系统设置页眉标为 `SYSTEM / SYSTEM SETTINGS` 且 MUST NOT 回归 Tab 导航、保存、恢复默认或其它 Shell 能力。

## AC-001 眉标文案 MUST 去除 `/ V2`

**Given** `admin` 已登录并访问 `/admin/settings/basic`  
**When** 页面加载完成  
**Then** `.settings-page-hero .eyebrow` 文本 MUST 为 `SYSTEM / SYSTEM SETTINGS`  
**And** MUST NOT 含 `/ V2` 或任意版本号后缀

- [ ] AC-001

## AC-002 全部 Tab MUST 一致

**Given** 修复完成  
**When** 依次访问 basic / security / media / notification / audit  
**Then** 各 Tab 页头眉标 MUST 均为 `SYSTEM / SYSTEM SETTINGS`

- [ ] AC-002

## AC-003 页头其它元素 MUST 无回归

**Given** 修复完成  
**When** 查看 `settings-page-hero`  
**Then** MUST 仍展示 `h1.page-title`（含当前分组名）、说明文案、dirty badge、保存按钮（若尚未由 BUG-0043 移除）  
**And** 布局 MUST 无错位

- [ ] AC-003

## AC-004 样式 MUST 使用 semantic token

**Given** 修复完成  
**When** 检查 TSX/CSS  
**Then** MUST NOT 新增裸 Hex  
**And** `.eyebrow` 样式 MUST 沿用 `system-settings.css`

- [ ] AC-004

## AC-005 修复范围 MUST 为纯前端文案

**Given** 缺陷修复已合并  
**When** 检查变更范围  
**Then** MUST NOT 变更 API、SQLite、Orval、Docker  
**And** MUST NOT 影响店主端 / 小程序

- [ ] AC-005

## AC-006 REQ-0017 AC-006 delta（MODIFIED）

**Given** fix change 归档  
**When** 合并 delta spec  
**Then** AC-006 MUST 更新为：页头眉标 MUST 为 `SYSTEM / SYSTEM SETTINGS`，MUST NOT 含产品版本后缀

- [ ] AC-006
