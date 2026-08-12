---
bug_id: BUG-0128-admin-user-menu-email-subtitle
status: done
lifecycle_stage: archive
created_at: 2026-08-11 21:43:22
updated_at: 2026-08-11 23:24:05
severity: low
related_requirement:
related_bug:
iteration: sprint-022
openspec_changes:
  - change_id: fix-admin-identity-fake-email-display
    type: fix
    status: archived
---

```yaml
bug_id: BUG-0128-admin-user-menu-email-subtitle
status: done
lifecycle_stage: review
severity: low
related_requirement:
related_bug:
iteration: sprint-022
openspec_changes:
  - change_id: fix-admin-identity-fake-email-display
    type: fix
    status: archived
```

# Trace

## 摘要

管理后台身份展示不应显示前端拼接的伪邮箱；用户菜单栏只显示用户昵称，昵称为空时显示用户名，个人资料页顶部身份栏也不得在邮箱为空时拼接伪邮箱。

## 线索

- `/explore` 只读排查确认，后端用户资料邮箱字段可为空且不生成默认邮箱。
- 前端菜单栏当前通过 `getUserEmail()` 在邮箱为空时拼接 `username@tilesfst.com`。
- 个人资料页顶部身份栏当前也存在邮箱为空时拼接 `${username}@tilesfst.com` 的展示逻辑。
- 用户已确认将个人资料页顶部身份栏的伪邮箱纳入同一修复范围。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-11 23:22:58 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-admin-identity-fake-email-display） |
| 2026-08-11 23:22:44 | /opsx-archive | Change `fix-admin-identity-fake-email-display` 已归档，状态同步完成。 |
| 2026-08-11 22:26:05 | /opsx-apply | Change `fix-admin-identity-fake-email-display` apply 完成，后续已归档。 |
| 2026-08-11 22:25:32 | /opsx-apply | Change `fix-admin-identity-fake-email-display` apply 进行中，后续已完成验收并归档。 |
| 2026-08-11 22:12:00 | /bug-opsx | 创建 OpenSpec 修复 Change `fix-admin-identity-fake-email-display`，后续已归档。 |
| 2026-08-11 22:08:09 | /sprint-propose | 纳入 sprint-022 正式范围。 |
| 2026-08-11 22:05:40 | lifecycle-stage-migrate | plan → review（/bug-review --approve） |
| 2026-08-11 22:05:07 | /bug-review --approve | 评审通过，确认进入后续 Sprint 与修复 Change 流程。 |
| 2026-08-11 22:02:01 | /bug-complete | 补齐 root-cause、workaround、acceptance，状态推进为 pending_review。 |
| 2026-08-11 21:54:38 | /bug-generate | 根据 capture、explore 结论与用户补充范围生成 bug.md，状态推进为 draft；同一修复范围纳入用户菜单栏和个人资料页顶部身份栏伪邮箱展示。 |
| 2026-08-11 21:43:22 | /bug-capture | 记录用户菜单栏显示伪邮箱副标题问题；来源为用户反馈与 `/explore` 只读排查结论。 |

- 2026-08-11 23:22:34 workflow-sync：状态同步为 done（Change archived）
