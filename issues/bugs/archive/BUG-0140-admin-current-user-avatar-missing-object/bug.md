---
bug_id: BUG-0140-admin-current-user-avatar-missing-object
title: 当前登录用户头像引用缺失媒体对象
severity: high
status: done
owner:
discovered_at: 2026-08-25 14:36:24
environment: docker
related_requirement:
related_change: fix-admin-current-user-avatar-object-consistency
created_at: 2026-08-25 15:36:38
updated_at: 2026-08-25 17:41:27
---

# 缺陷说明

当前登录用户的 `avatar_object_key` 指向已不存在的媒体对象。管理后台通过 `/api/v1/profile/me` 获取当前用户资料后，会消费 `avatar_url` 并请求 `/media/images/default/user/avatars/*.png`，但该媒体读取返回 404，导致当前用户头像无法正常展示。

# 复现步骤

1. 启动 Docker 本地环境并登录管理后台。
2. 使用存在 `avatar_object_key` 的管理端账号访问任意后台页面。
3. 打开浏览器 Network，筛选 `/media/images/default/user/avatars/` 请求。
4. 进入侧边栏用户信息区域或个人资料页，观察当前登录用户头像加载结果。

# 期望结果

- 当前登录用户的 `avatar_object_key` 应指向可通过 `/media/{object_key}` 读取的对象。
- 当历史数据或对象存储出现漂移时，系统应避免展示破损图片，并提供可控降级。
- 用户更新头像时，后端应拒绝写入不存在的媒体对象 key。

# 实际结果

- `avatar_object_key` 指向的 `/media/images/default/user/avatars/*.png` 对象不存在。
- `/media/{avatar_object_key}` 返回 404。
- 个人资料页直接渲染头像 `img`，缺少加载失败后的 initials 降级展示。
- 侧边栏用户菜单已有图片 `onError` 降级，但仍会产生一次 404 请求。

# 影响范围

- 管理后台当前登录用户头像展示。
- 个人资料页基础资料区头像展示。
- 侧边栏用户菜单头像请求与降级行为。
- 用户资料数据与对象存储对象之间的一致性。

# 严重等级说明

严重等级为 high。该问题不阻断登录、商品维护或权限校验，但会稳定影响管理后台关键身份信息展示，并暴露历史数据与对象存储对象之间的一致性缺口；如果不在写入链路阻断无效 key，后续仍可能产生同类缺陷。

# 已知证据

- 本地 Docker 数据库中存在用户记录带 `images/default/user/avatars/*.png` 类型的 `avatar_object_key`。
- 访问 `localhost:3000/media/images/default/user/avatars/a255bbf6-b3f8-4eee-a559-ea7c76eb17ed.png` 返回 404。
- 后端直连 `localhost:8000/media/images/default/user/avatars/a255bbf6-b3f8-4eee-a559-ea7c76eb17ed.png` 返回 404。
- 后端日志出现 `media_read status=404`，同一环境中瓷砖图片 `/media/images/default/tiles/...` 可正常返回 200，说明不是媒体代理整体不可用。

# 修复策略

采用组合策略：数据修复、后端写入校验、前端展示兜底。

1. 数据修复：扫描当前用户头像字段，对确认缺失对象的 `avatar_object_key` 清空或补齐对象；本次优先清理脏字段，避免继续请求不存在对象。
2. 后端写入校验：在当前用户头像更新链路校验 `avatar_object_key` 对应媒体对象存在；不存在时拒绝写入并返回明确错误。
3. 前端展示兜底：个人资料页头像图片加载失败后 fallback 到用户 initials，避免 broken image。

# 验收要点

- [ ] 缺失头像对象的历史用户记录完成数据修复后，不再持续请求不存在的 `/media/images/default/user/avatars/*.png`。
- [ ] `PATCH /api/v1/profile/me` 传入不存在的 `avatar_object_key` 时返回明确失败，不写入用户资料。
- [ ] 用户上传头像后，使用上传返回的 `object_key` 更新资料成功，且 `/media/{object_key}` 可读。
- [ ] 个人资料页头像图片 404 时显示 initials 降级，不出现破损图片。
- [ ] 侧边栏用户菜单维持现有 fallback 行为。
openspec_changes:
  - change_id: fix-admin-current-user-avatar-object-consistency
    type: update
    status: archived
