---
change_id: fix-admin-current-user-avatar-object-consistency
source_bug: BUG-0140-admin-current-user-avatar-missing-object
sprint: sprint-026
created_at: 2026-08-25 16:08:42
updated_at: 2026-08-25 16:08:42
---

# 修复当前登录用户头像对象一致性

## 背景

`BUG-0140-admin-current-user-avatar-missing-object` 已确认：当前登录用户的 `avatar_object_key` 指向 `images/default/user/avatars/...`，但对应对象在当前对象存储中不存在。`GET /api/v1/profile/me` 仍返回由该 key 拼出的 `avatar_url`，管理端个人资料页直接渲染图片后出现媒体 404 与破损头像风险。

该缺陷不阻断登录或资料编辑，但稳定影响管理后台当前用户身份展示，并暴露用户资料字段与对象存储对象之间缺少一致性保护的问题。

## 变更内容

- 对历史 `users.avatar_object_key` 执行受控数据修复，优先清空已确认缺失对象的头像 key，并保留 dry-run、apply 和幂等复查摘要。
- 在 `PATCH /api/v1/profile/me` 写入头像 key 前校验对象存在且可通过后端对象存储适配层读取；不存在时返回统一错误响应并拒绝写入。
- 在个人资料页头像图片加载失败时回退到当前用户 initials，避免破损图片展示。
- 保持侧边栏用户菜单既有 fallback 行为，并通过回归测试防止回退。

## 能力范围

### 修改能力

- `admin-profile-page`：补齐当前用户头像写入校验与个人资料页渲染兜底。
- `user-management`：明确用户头像字段不得指向不可读对象，列表和表单展示需稳定 fallback。
- `object-storage`：补充头像对象一致性修复和媒体四联验收要求。

### 非目标

- 不改变用户表结构，不新增数据库 migration。
- 不改变对象存储 Bucket、前缀策略、上传接口路径或 MinIO/COS/TOS 配置。
- 不让前端直连对象存储。
- 不扩大到小程序头像或店主端头像能力。

## 回滚计划

- 若后端校验导致合法头像误拒绝，可回退 profile 写入校验逻辑，并保留数据修复 dry-run 证据用于定位误判 key。
- 若前端兜底引入展示回退，可回退个人资料页头像渲染组件改动，侧边栏 fallback 不受影响。
- 数据修复默认应先 dry-run；apply 前记录受影响用户范围。若误清头像 key，使用对象存储备份或上传入口重新写回合法 key。
- 回滚不涉及 schema migration、Orval 生成或 Docker Compose 配置。

## 验证计划

- 运行后端 profile 聚焦测试，覆盖不存在 `avatar_object_key` 写入失败、合法上传 key 写入成功、`/media/{object_key}` 可读。
- 运行管理端个人资料页聚焦测试，覆盖头像图片 `error` 后显示 initials。
- 运行数据修复 dry-run/apply/二次 dry-run 或等价测试，确认缺失头像 key 被清理且过程幂等。
- 按媒体类 BUG 四联模板记录 key、object、URL、render 验收证据。

## 影响

- API：影响 `PATCH /api/v1/profile/me` 的错误分支；正常成功响应结构不变。若实现新增错误码，必须同步错误码文档与 OpenAPI/Orval。
- 数据库：不改表结构；会有受控数据修复操作清理缺失头像 key。
- Web：影响管理端个人资料页头像渲染兜底。
- 小程序：不影响。
- 管理端：影响当前用户头像展示与 profile 保存链路。
- Orval：仅在新增错误码或 Schema 变更时需要。
- Docker Compose：不需要。
- 测试：需要补充后端、前端与数据修复聚焦回归测试。
