## Why

[BUG-0023-profile-duplicate-save-buttons](issues/bugs/archive/BUG-0023-profile-duplicate-save-buttons/) 已评审通过。REQ-0014 / `add-admin-profile-page` 交付后，个人资料页页头与表单底部各有一个「保存修改」按钮，功能相同但造成重复 CTA。根据项目规则，已交付能力上的 UX 缺口 MUST 使用新的 `fix-*` change 修复。

## What Changes

- 移除 `ProfilePage.tsx` 页头 `profile-page-head` 内的「保存修改」按钮。
- 保留「基础资料」卡片底部 `profile-form-actions` 内与「重置」并列的「保存修改」按钮（与 inline save-tip 同区）。
- 更新 `ProfilePage.test.tsx`：`getAllByRole` → `getByRole('button', { name: '保存修改' })`。
- 1440×1024 验收：页头无重复金色主按钮；表单 actions 与 save-tip 布局无回归。
- **不** 变更 PATCH 逻辑、API、SQLite、Orval、Docker、头像上传或账号安全卡片。

## Capabilities

### New Capabilities

（无新 capability 目录。）

### Modified Capabilities

- `admin-profile-page`：MODIFIED「管理端个人资料页面」— 页面 MUST 仅保留一处「保存修改」主 CTA（表单 actions 区）；MUST NOT 在页头与表单底重复渲染。

## Impact

| 影响面 | 说明 |
|---|---|
| Web 管理端 | `ProfilePage.tsx`、`ProfilePage.test.tsx` |
| 店主端 / 小程序 | 无 |
| 后端 / API / DB / Orval | 无 |
| 父需求 | REQ-0014-profile-page（已 archive `add-admin-profile-page`） |
| 关联 BUG | BUG-0022（同页 UX；本 change 仅 scope BUG-0023，可后续合并 apply） |
| 测试 | vitest ProfilePage；1440×1024 单 CTA 验收 |

## Rollback Plan

若移除页头按钮导致布局异常或测试失败，可回滚本 change 的前端改动：

1. 恢复 `ProfilePage.tsx`、`ProfilePage.test.tsx` 至 fix 前版本。
2. 运行 `cd src/web && pnpm vitest run src/pages/admin/ProfilePage && pnpm build` 确认通过。

回滚不涉及 API、数据库或部署配置。
