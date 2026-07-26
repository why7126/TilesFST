## Why

[BUG-0022-profile-basic-info-redundant-role-status](issues/bugs/archive/BUG-0022-profile-basic-info-redundant-role-status/) 已评审通过。REQ-0014 / `add-admin-profile-page` 交付后，个人资料页「基础资料」表单内展示「所属角色」「账号状态」只读字段，与右侧「账号安全」卡片信息重复。产品 UX 定稿：角色/状态仅在账号安全卡片展示。根据项目规则，已交付能力上的 UX 缺口 MUST 使用新的 `fix-*` change 修复。

## What Changes

- 移除 `ProfilePage.tsx` `profile-form-grid` 内 `profile-role`、`profile-status` 只读 field。
- 保留「账号安全」卡片 info-list 中账号状态 badge 与所属角色（AC-022）。
- 同步 MODIFIED：`REQ-0014` acceptance AC-011、`requirement.md` FR-004、`profile-page.html`、`profile-page-context.md`（若 apply 时尚未合并）。
- 1440×1024 验收：表单无角色/状态 input；账号安全卡片完整。
- **不** 变更 identity-strip / card-head 摘要、PATCH 逻辑、API、SQLite、Orval、Docker；**不** scope BUG-0023 双保存按钮（见 `fix-profile-duplicate-save-buttons`）。

## Capabilities

### New Capabilities

（无新 capability 目录。）

### Modified Capabilities

- `admin-profile-page`：MODIFIED「管理端个人资料页面」— 主卡片表单 MUST NOT 含所属角色、账号状态只读字段；二者仅在账号安全卡片展示。

## Impact

| 影响面 | 说明 |
|---|---|
| Web 管理端 | `ProfilePage.tsx`；REQ-0014 prototype/acceptance 文档 delta |
| 店主端 / 小程序 | 无 |
| 后端 / API / DB / Orval | 无 |
| 父需求 | REQ-0014-profile-page（已 archive `add-admin-profile-page`） |
| 关联 BUG | BUG-0023（同页 UX；独立 change `fix-profile-duplicate-save-buttons`） |
| 测试 | vitest ProfilePage；1440×1024 表单字段验收 |

## Rollback Plan

若移除表单字段导致布局异常或验收失败，可回滚本 change 的前端与文档改动：

1. 恢复 `ProfilePage.tsx` 及 REQ-0014 prototype/acceptance 至 fix 前版本。
2. 运行 `cd src/web && pnpm vitest run src/pages/admin/ProfilePage && pnpm build` 确认通过。

回滚不涉及 API、数据库或部署配置。
