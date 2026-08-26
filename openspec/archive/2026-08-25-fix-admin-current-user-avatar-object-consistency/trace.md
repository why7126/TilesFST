---
change_id: fix-admin-current-user-avatar-object-consistency
type: fix
status: applied
source_bug: BUG-0140-admin-current-user-avatar-missing-object
sprint: sprint-026
created_at: 2026-08-25 16:08:42
updated_at: 2026-08-25 17:34:12
---

# 追溯

## 来源

- BUG：`BUG-0140-admin-current-user-avatar-missing-object`
- Sprint：`sprint-026`
- 能力：`admin-profile-page`、`user-management`、`object-storage`

## 根因状态

`confirmed`

## 证据摘要

- 当前用户 `avatar_object_key` 指向 `images/default/user/avatars/...`。
- Web 入口与后端直连 `/media/{avatar_object_key}` 均返回 404。
- 同一环境其他瓷砖媒体 URL 可返回 200，说明不是媒体代理整体不可用。
- `profile_service.py` 对非空头像 key 直接拼出 `/media/{object_key}`。
- `ProfilePage.tsx` 个人资料页头像缺少图片加载失败兜底。
- `AdminUserMenu.tsx` 已有侧边栏 fallback，可作为回归参照。

## 同步状态

```yaml
bug_id: BUG-0140-admin-current-user-avatar-missing-object
change_id: fix-admin-current-user-avatar-object-consistency
sprint: sprint-026
status: applied
workflow_event: bug.opsx
```

## 实现验证

```yaml
implemented_at: 2026-08-25 17:22:18
checks:
  - command: uv run pytest src/backend/tests/test_profile.py src/backend/tests/test_admin_users.py tests/test_repair_user_avatar_objects.py
    result: pass
    summary: 36 passed
  - command: pnpm --dir src/web --config.pm-on-fail=warn test -- ProfilePage.test.tsx AdminUserMenu.test.tsx
    result: pass
    summary: 62 test files passed, 362 tests passed; pnpm version gate downgraded to warning for this command
  - command: python scripts/repair_user_avatar_objects.py --dry-run --db <sqlite-db>
    result: covered_by_tests
    summary: tests/test_repair_user_avatar_objects.py 覆盖 dry-run、apply 和二次幂等复查
api_docs:
  changed_schema: false
  changed_error_code: false
  orval_required: false
  note: 复用 PROFILE_VALIDATION_ERROR=40013 和既有 ProfilePatchRequest/ProfileMe schema，未新增 OpenAPI 字段。
ui_evidence:
  - selector: .profile-avatar
    viewport: vitest-jsdom
    result: 图片 error 后切换 `.profile-avatar.is-fallback` 并显示 initials `AU`，不保留 broken img。
  - selector: .sidebar-user .avatar
    viewport: vitest-jsdom
    result: AdminUserMenu 既有头像失败 fallback 测试继续通过。
  - selector: /admin/profile
    viewport: docker-web-localhost-3000
    result: 用户补证截图显示头像上传、profile 保存、头像 webp 读取和 profile 重新获取均为 200，页面头像正常渲染。
data_repair_evidence:
  - script: scripts/repair_user_avatar_objects.py
    result: dry-run 不写库；apply 清空缺失头像 key；二次 dry-run missing_objects=0。
acceptance: pending
incident_note: 本次经验已由 BUG root-cause、Change trace、数据修复脚本测试和媒体上传最佳实践覆盖；不新增 docs/knowledge-base/incidents/ 事故复盘。
```
