---
bug_id: BUG-0023-profile-duplicate-save-buttons
status: pending_review
created_at: 2026-06-28 12:53:12
updated_at: 2026-06-28 12:53:12
related_requirement: REQ-0014-profile-page
related_bug: BUG-0022-profile-basic-info-redundant-role-status
---

# 回归验收标准

> 修复本缺陷 MUST 使个人资料页仅保留一处「保存修改」主 CTA，且 MUST NOT 回归 REQ-0014 表单校验、PATCH、inline save-tip、重置、头像上传与账号安全卡片。

## AC-001 页面 MUST 仅有一处「保存修改」按钮

**Given** `admin` 或 `employee` 已登录并访问 `/admin/profile`  
**When** 页面加载完成  
**Then** 全页 MUST 仅存在 **1** 个 `role="button"` 且 accessible name 为「保存修改」的按钮  
**And** 页头 `profile-page-head` MUST NOT 再渲染「保存修改」主按钮

- [ ] AC-001

## AC-002 保留的按钮 MUST 位于表单 actions 区

**Given** 修复完成  
**When** 查看「基础资料」卡片底部 `profile-form-actions`  
**Then** 「保存修改」MUST 与「重置」ghost 按钮并列  
**And** MUST 位于 inline `.save-tip` 同一操作行（布局与现网表单底 actions 一致）

- [ ] AC-002

## AC-003 保存行为 MUST 无回归（对齐 REQ-0014 AC-015 / AC-016）

**Given** 用户修改昵称等可写字段  
**When** 点击唯一的「保存修改」  
**Then** MUST 执行客户端校验并提交 `PATCH /api/v1/profile/me`（仅可写字段）  
**And** 成功后 MUST 在表单底部 inline 展示「资料已更新 · {timestamp}」（非 toast）  
**And** 操作记录 timeline MUST 刷新

- [ ] AC-003

## AC-004 重置与 disabled 态 MUST 无回归

**Given** 用户修改表单后点击「重置」  
**When** 重置完成  
**Then** MUST 恢复进入页面时的 GET 快照  

**Given** 正在提交保存或头像上传中  
**When** 查看「保存修改」按钮  
**Then** MUST 为 disabled 状态（与修复前逻辑一致）

- [ ] AC-004

## AC-005 页头 MUST 保留标题区且无布局回归

**Given** 移除页头保存按钮后  
**When** 查看 `profile-page-head`  
**Then** MUST 仍展示眉标 `SYSTEM / PROFILE`、标题「个人资料」、说明文案  
**And** 页头布局 MUST 无错位或多余空白占位

- [ ] AC-005

## AC-006 样式 MUST 使用 semantic token

**Given** 修复完成  
**When** 检查 `ProfilePage.tsx` 与 `profile-page.css`  
**Then** 保留的「保存修改」MUST 使用 `btn primary`（品牌金实底）  
**And** MUST NOT 新增裸 Hex

- [ ] AC-006

## AC-007 REQ-0014 其他能力 MUST 无回归

**Given** 修复完成  
**When** 执行 REQ-0014 核心场景  
**Then** 身份条、字段顺序、头像上传、账号安全卡片、操作记录 timeline MUST 行为不变  
**And** `employee` / `admin` 均可访问；`store_owner` 仍 forbidden

- [ ] AC-007

## AC-008 修复范围 MUST 为纯前端 UI

**Given** 缺陷修复已合并  
**When** 检查变更范围  
**Then** MUST NOT 变更 API、SQLite schema、Orval 生成物、Docker 部署  
**And** MUST NOT 影响店主端 / 小程序

- [ ] AC-008

## AC-009 测试 MUST 覆盖单按钮断言

**Given** 进入 `fix-profile-page-ux-refine`（或等价 fix-* Change）  
**When** 完成 `/opsx-apply`  
**Then** `ProfilePage.test.tsx` MUST 使用 `getByRole('button', { name: '保存修改' })`（或等价单入口断言）  
**And** 校验失败、重置、保存成功 save-tip 用例 MUST 仍通过  
**And** `cd src/web && pnpm vitest run src/pages/admin/ProfilePage` MUST 通过

- [ ] AC-009

## AC-010 视觉验收（SHOULD）

**Given** 修复完成  
**When** 1440×1024 查看 `/admin/profile`  
**Then** 页头无重复金色主按钮；表单底「重置 + 保存修改」与 save-tip 对齐  
**And** Change `trace.md` SHOULD 记录单 CTA 验收结论

- [ ] AC-010

## AC-011 REQ-0014 AC-017 delta（MODIFIED）

**Given** BUG-0023 修复并入 change delta spec  
**When** 归档时合并至 `admin-profile-page` spec  
**Then** AC-017 MUST 更新为：页面 **MUST** 仅保留一处「保存修改」主 CTA（推荐表单 actions 区），**MUST NOT** 在页头与表单底重复渲染相同主按钮

- [ ] AC-011
