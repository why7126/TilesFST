---
change_id: fix-admin-identity-fake-email-display
status: applied
created_at: 2026-08-11 22:12:00
updated_at: 2026-08-11 22:25:00
type: fix
source_bug: BUG-0128-admin-user-menu-email-subtitle
sprint: sprint-022
---

# Trace

## 来源

- BUG：`BUG-0128-admin-user-menu-email-subtitle`
- Sprint：`sprint-022`
- 类型：修复

## 摘要

修复管理后台身份展示伪邮箱问题：用户菜单栏不显示邮箱副标题，个人资料页顶部身份栏不再在邮箱为空时拼接伪邮箱，同时保留个人资料联系邮箱编辑入口。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-11 22:12:00 | /bug-opsx | 创建 OpenSpec 修复 Change，待执行 `/opsx-apply BUG-0128-admin-user-menu-email-subtitle`。 |
| 2026-08-11 22:25:00 | /opsx-apply | 已移除用户菜单栏邮箱副标题和伪邮箱兜底；个人资料页顶部身份栏仅在存在真实联系邮箱时展示邮箱；联系邮箱输入框保留且空值不自动填充。 |

## 验证

- `pnpm --dir src/web exec vitest run src/features/admin/components/AdminUserMenu.test.tsx src/pages/admin/ProfilePage.test.tsx`
- `openspec validate fix-admin-identity-fake-email-display --strict`
- `python scripts/validate-openspec-language.py`
- `python scripts/validate-directory-structure.py`

## 知识库判断

本次修复为局部展示兜底移除，根因与修复方式已在 BUG 与 Change trace 中闭环；暂不新增 `docs/knowledge-base/incidents/` 经验沉淀。
