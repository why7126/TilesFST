---
bug_id: BUG-0140-admin-current-user-avatar-missing-object
title: 当前登录用户头像引用缺失媒体对象根因分析
root_cause_document_status: completed
root_cause_status: confirmed
root_cause_category: data_consistency
created_at: 2026-08-25 15:41:57
updated_at: 2026-08-25 15:41:57
---

# 根因结论

根因状态：`confirmed`

当前登录用户头像展示异常的直接原因是 `users.avatar_object_key` 保存了 `images/default/user/avatars/...` 媒体对象 key，但对应对象在当前对象存储中不存在；后端资料接口仍根据该 key 返回 `/media/{object_key}`，个人资料页收到 `avatar_url` 后直接渲染图片，导致媒体代理返回 404 后出现头像展示异常。

根本原因是用户资料字段与对象存储对象之间缺少一致性保护：历史数据可残留已失效的头像 key，当前用户头像更新链路也缺少对象存在性校验；前端个人资料页缺少图片加载失败后的 initials 兜底。

# 直接原因

1. `users.avatar_object_key` 中存在头像对象 key。
2. `/media/{avatar_object_key}` 经后端媒体代理读取对象存储时找不到对应 object。
3. 个人资料页头像区域直接渲染 `img`，没有 `onError` 后切换 initials。

# 触发条件

- 管理端账号存在非空 `avatar_object_key`。
- 该 key 对应对象在当前对象存储中缺失、被清理、迁移遗漏或环境切换后不可读。
- 用户访问管理后台侧边栏或个人资料页，前端请求 `/api/v1/profile/me` 并消费返回的 `avatar_url`。

# 影响范围

- Web 管理端当前登录用户头像展示。
- 个人资料页基础资料区。
- 侧边栏用户菜单头像请求与降级体验。
- 用户资料数据与对象存储对象一致性。

# 证据链

| 证据 | 类型 | 摘要 | 结论 |
|---|---|---|---|
| `issues/bugs/archive/BUG-0140-admin-current-user-avatar-missing-object/bug.md` | 缺陷记录 | 记录 `avatar_object_key` 指向 `/media/images/default/user/avatars/*.png` 且资源 404 | 原始现象成立 |
| `data/sqlite/tilesfst.db` 只读查询摘要 | 数据样本 | `admin` 等账号存在 `images/default/user/avatars/...` 形式的 `avatar_object_key` | 用户表存在头像 key |
| `curl` 复现摘要 | 复现 | `localhost:3000/media/images/default/user/avatars/a255bbf6-b3f8-4eee-a559-ea7c76eb17ed.png` 返回 `404 application/json` | Web 入口媒体 URL 不可读 |
| `curl` 复现摘要 | 复现 | `localhost:8000/media/images/default/user/avatars/a255bbf6-b3f8-4eee-a559-ea7c76eb17ed.png` 返回 `404 application/json` | 后端媒体代理直连同样不可读 |
| Docker 后端日志摘要 | 日志 | `media_read status=404` 命中头像 key；同一环境瓷砖图片 `/media/images/default/tiles/...` 返回 200 | 不是媒体代理整体不可用，而是目标头像 object 缺失 |
| `src/backend/app/services/profile_service.py` | 代码定位 | `_avatar_url()` 对非空 key 直接返回 `/media/{object_key}` | 接口输出不会校验 object 存在性 |
| `src/web/src/pages/admin/ProfilePage.tsx` | 代码定位 | 个人资料页头像 `img` 未设置加载失败 fallback | 端侧缺少展示兜底 |
| `src/web/src/features/admin/components/AdminUserMenu.tsx` | 代码定位 | 侧边栏菜单已有 `onError` fallback | 兜底能力已有局部实现，可作为个人资料页修复参照 |
| `src/backend/tests/test_admin_users.py::test_user_list_returns_accessible_avatar_url` | 回归测试现状 | 已覆盖新上传头像在用户列表中 URL 可读 | 上传后对象可读路径存在，但 profile 写入缺少缺失 key 防护 |

# 已排除项

- 排除媒体代理整体故障：同一后端日志中存在瓷砖图片 `/media/images/default/tiles/...` 读取 200。
- 排除单纯前端路由问题：后端直连 `localhost:8000/media/...` 同样返回 404。
- 不将对象缺失来源限定为某一次上传、清理或迁移操作；当前证据足以确认数据与对象存储不一致，但无法从现有记录还原最初导致对象缺失的历史动作。

# 验证方式

修复前验证：

1. 查询用户表中非空 `avatar_object_key`。
2. 访问 `/media/{avatar_object_key}`，确认返回 404。
3. 打开个人资料页，确认头像图片加载失败时没有稳定 fallback。

修复后验证：

1. 对历史缺失头像 key 执行数据修复，确认不再持续请求缺失对象。
2. `PATCH /api/v1/profile/me` 传入不存在的头像 key 时返回明确错误且不写入用户资料。
3. 用户上传头像后用返回 `object_key` 更新资料成功，`/media/{object_key}` 返回 200。
4. 个人资料页头像图片 404 时显示 initials 兜底，不出现破损图片。

# 人工补证

若后续需要追溯最初对象缺失来源，可补充以下证据，但不阻塞当前根因成立：

1. 对象存储审计日志：查找目标头像 key 是否曾存在、何时删除或迁移。
2. 历史上传日志：确认头像上传是否成功写入 object、是否存在后续清理任务。
3. 部署环境记录：确认当前数据库与对象存储 bucket 是否来自同一环境快照。
