---
bug_id: BUG-0022-profile-basic-info-redundant-role-status
status: pending_review
created_at: 2026-06-28 12:54:36
updated_at: 2026-06-28 12:54:36
related_requirement: REQ-0014-profile-page
related_bug: BUG-0023-profile-duplicate-save-buttons
note: UX 定稿已 MODIFIED REQ-0014 AC-011；工作区可能已有先行修复，正式验收以 fix-* Change apply + archive 为准
---

# 回归验收标准

> 修复本缺陷 MUST 移除基础资料表单内重复的「所属角色」「账号状态」只读字段；MUST 保留账号安全卡片展示（AC-022）；MUST NOT 回归资料 PATCH、校验、重置、头像上传、操作记录与 semantic token 规范。

## AC-001 表单 MUST NOT 含角色/状态只读 input

**Given** 已登录 `admin` 或 `employee` 访问 `/admin/profile`  
**When** 检查「基础资料」`profile-form-grid`  
**Then** MUST NOT 存在 `profile-role`、`profile-status` 或 label 为「所属角色」「账号状态」的表单字段  
**And** 表单 MUST 按顺序含：用户名（只读）、昵称、联系邮箱、手机、备注

- [ ] AC-001

## AC-002 账号安全卡片 MUST 继续展示角色与状态

**Given** 同上  
**When** 检查右侧「账号安全」`side-card`  
**Then** MUST 展示登录账号、账号状态（badge）、所属角色、最后登录  
**And** 状态 badge MUST 使用 semantic class（如 `status on`），非裸 Hex

- [ ] AC-002

## AC-003 资料编辑与保存 MUST 无回归

**Given** 用户修改昵称并点击「保存修改」  
**When** PATCH 成功  
**Then** MUST 展示 inline save-tip「资料已更新」  
**And** PATCH payload MUST NOT 含 role/status  
**And** 「重置」MUST 恢复 GET 快照

- [ ] AC-003

## AC-004 校验规则 MUST 无回归

**Given** 昵称长度不符或邮箱/手机格式错误  
**When** 点击保存  
**Then** MUST 展示既有校验文案（2–32 字、邮箱、手机、备注 200 字）  
**And** MUST NOT 提交 PATCH

- [ ] AC-004

## AC-005 REQ-0014 MODIFIED AC-011 MUST 对齐

**Given** 修复完成  
**When** 对照 `issues/requirements/archive/REQ-0014-profile-page/acceptance.md` AC-011  
**Then** 实现 MUST 符合「表单不含角色/状态；二者仅在账号安全卡片」  
**And** `profile-page.html` 原型 MUST 已移除表单内两字段

- [ ] AC-005

## AC-006 OpenSpec MUST 同步

**Given** fix-* Change 归档  
**When** 检查 `openspec/specs/admin-profile-page/spec.md` Scenario「表单字段与只读规则」  
**Then** MUST 含 MUST NOT 在主卡片表单展示角色/状态  
**And** MUST NOT 要求表单 grid 内 role/status input

- [ ] AC-006

## AC-007 修复范围 MUST 为纯前端 + 文档 delta

**Given** 缺陷修复已合并  
**When** 检查变更范围  
**Then** MUST NOT 变更 profile API、SQLite schema、Orval 生成物、Docker 部署  
**And** 店主端 / 小程序 MUST NOT 受影响

- [ ] AC-007

## AC-008 测试 MUST 通过

**Given** 进入 `fix-profile-page-ux-refine`（或等价 fix-* Change）并完成 apply  
**When** 运行 `cd src/web && pnpm vitest run src/pages/admin/ProfilePage.test.tsx`  
**Then** 全部用例 MUST pass  
**And** `pnpm build` MUST pass

- [ ] AC-008

## AC-009 视觉验收（SHOULD）

**Given** 修复完成  
**When** 1440×1024 并排对比 `/admin/profile` 与更新后的 `profile-page.html`  
**Then** 表单区 MUST 无角色/状态 input；账号安全卡片信息完整  
**And** Change `trace.md` SHOULD 记录并排结论

- [ ] AC-009
