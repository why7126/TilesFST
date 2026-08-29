---
bug_id: BUG-0140-admin-current-user-avatar-missing-object
title: 当前登录用户头像引用缺失媒体对象验收标准
acceptance_status: passed
template_ref: docs/standards/media-bug-four-point-acceptance-template.md
created_at: 2026-08-25 15:41:57
updated_at: 2026-08-28 16:21:48
---

# 验收目标

本 BUG 按 `docs/standards/media-bug-four-point-acceptance-template.md` 执行媒体类 BUG 四联验收，覆盖 `key`、`object`、`URL`、`render`。修复目标是闭环当前登录用户头像对象缺失导致 404 的问题，并阻止后续写入不可读头像 key。

# 回归验收项

## AC-0140-01 历史头像数据修复

Given 当前环境存在 `users.avatar_object_key` 指向缺失对象的管理端用户  
When 执行本 BUG 的数据修复策略  
Then 缺失对象对应的用户头像字段应被清空或对象被补齐  
And 管理后台不再持续请求已确认缺失的 `/media/images/default/user/avatars/*.png`

## AC-0140-02 后端拒绝写入不存在头像 key

Given 管理端用户已登录  
When 调用 `PATCH /api/v1/profile/me` 并传入不存在的 `avatar_object_key`  
Then API 应返回明确失败  
And 用户资料中的 `avatar_object_key` 不应被更新为该缺失 key

## AC-0140-03 上传头像后对象与 URL 可读

Given 管理端用户通过头像上传入口上传合法图片  
When 使用上传返回的 `object_key` 更新个人资料  
Then 更新应成功  
And `/media/{object_key}` 应返回 200  
And 返回的 `avatar_url` 应与受控媒体代理 URL 一致

## AC-0140-04 个人资料页头像加载失败兜底

Given `/api/v1/profile/me` 返回非空 `avatar_url`  
When 该 URL 图片加载失败  
Then 个人资料页应显示当前用户 initials  
And 不应显示破损图片占位

## AC-0140-05 侧边栏用户菜单保持兜底

Given 当前登录用户头像 URL 加载失败  
When 渲染侧边栏用户菜单  
Then 侧边栏应继续显示 initials fallback  
And 不应出现破损图片

# 媒体类 BUG 四联验收

## 原 BUG 场景

| 字段 | 内容 |
|---|---|
| BUG | BUG-0140-admin-current-user-avatar-missing-object |
| 标题 | 当前登录用户头像引用缺失媒体对象 |
| 严重等级 | high |
| 影响范围 | Web 管理端、后端接口、对象存储 |
| 复现入口 | 管理后台侧边栏用户信息区域、个人资料页、`/api/v1/profile/me`、`/media/{avatar_object_key}` |
| 受影响端 | admin、backend、storage |
| 环境 | docker-web-3000 |
| 媒体类型 | image |
| 业务资源 | 当前登录管理端用户头像 |
| 修复前实际结果 | `avatar_object_key` 指向缺失对象，`/media/images/default/user/avatars/*.png` 返回 404，个人资料页缺少图片失败兜底 |
| 修复后期望结果 | 历史缺失 key 被修复或清空；后端拒绝写入不存在 key；Web 头像渲染具备 initials fallback |

## 四联检查

| 维度 | 状态 | 证据 | 失败 / 阻塞处理 |
|---|---|---|---|
| key | pass | `tests/test_repair_user_avatar_objects.py` 覆盖缺失头像 key dry-run、apply 清空与二次 dry-run 幂等；`src/backend/tests/test_profile.py::test_patch_profile_rejects_missing_avatar_object_key` 验证不存在 key 不写入 | 若仍可写入任意不存在 key，视为 fail，需补后端校验 |
| object | pass | `src/backend/tests/test_profile.py::test_employee_can_upload_avatar` 覆盖上传头像 object 后使用返回 key 更新 profile 成功，并请求 `/media/{object_key}` 返回 200 | 若 object 缺失但字段仍非空，视为 fail，需执行数据修复 |
| URL | pass | 同一后端测试覆盖合法头像 `/media/{object_key}` 可读；缺失 key 写入返回 `40013` 且不更新用户资料 | 若仍出现保存后 `/media/...` 404，视为 fail |
| render | pass | `src/web/src/pages/admin/ProfilePage.test.tsx` 覆盖 `.profile-avatar img` error 后显示 initials；`AdminUserMenu.test.tsx` 既有侧边栏 fallback 测试通过 | 若用户可见破损图或空白头像，视为 fail |

## 媒体上传横切检查项

| Gate | 状态 | 验收要求 |
|---|---|---|
| 上传状态机 | pass | 既有个人资料上传流程保持，`test_employee_can_upload_avatar` 覆盖上传后保存成功；前端失败态未改动 |
| 同会话即时回显 | pass | ProfilePage 上传成功后继续 setProfile、刷新 activities 并触发 shell refetch；前端回归测试覆盖头像 render/fallback |
| Docker Web 边界 | pass | 用户补证截图显示 `http://localhost:3000` 入口下头像上传 `POST uploads`、profile `PATCH me`、头像媒体 `GET ...webp`、profile `GET me` 均为 200，页面头像正常渲染 |
| 媒体代理一致性 | pass | 后端上传后 `/media/{object_key}` 返回 200，前端继续消费 profile API 返回 URL，不直连对象存储 |
| 历史对象与审计 | pass | 新增 `scripts/repair_user_avatar_objects.py`，测试覆盖 dry-run、apply 和二次幂等复查摘要 |
| 小程序 evidence | n/a | 本 BUG 不影响小程序页面或组件 |

# 建议测试

- 后端集成测试：不存在头像 key 写入失败；上传返回 key 写入成功；`/media/{object_key}` 可读。
- 前端组件测试：个人资料页 `img` 触发 error 后显示 initials。
- 数据修复脚本或命令测试：dry-run 能列出缺失头像 key；apply 后再次 dry-run 为 0 或仅剩明确豁免项。

# 验收结论

当前状态：`passed`。核心 key/object/URL/render 自动化验收已通过；Docker Web `localhost:3000` 入口证据已由用户补证截图补齐，Change 已归档并回填最终验收结论。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-25 17:41:27
accepted_by: workflow-sync
source_change: fix-admin-current-user-avatar-object-consistency
source_sprint: sprint-026
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

