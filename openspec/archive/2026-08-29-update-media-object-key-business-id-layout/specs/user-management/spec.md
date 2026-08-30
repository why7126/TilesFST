## MODIFIED Requirements

### Requirement: 管理端用户列表与筛选 API

系统 MUST 提供 `GET /api/v1/admin/users`，仅 `role=admin` 的用户可调用。接口 MUST 支持分页（默认 `page_size=10`，可选 10/20/50）、关键词模糊搜索（username、display_name、email、phone）、角色筛选、状态筛选（`active`/`disabled`/`deleted`）与登录情况筛选（从未登录、最近 7 天登录、超过 30 天未登录）。响应 MUST 包含用户列表与 summary（用户总数、当前筛选数、正常用户数、已冻结用户数）。每条用户记录 MUST 同时返回 `avatar_object_key` 与可访问的 `avatar_url`。当 `avatar_object_key` 非空时，`avatar_url` MUST 为 `/media/{object_key}` 或等价受控媒体 URL，且 SHOULD 对应可加载对象；若历史数据漂移导致对象缺失，系统 MUST 通过数据修复或安全 fallback 避免用户可见破损头像。

新上传用户头像在 `user_id` 已存在时 MUST 使用 `images/default/user-avatars/{user_id}/{uuid}.{ext}`。如存在用户创建前头像上传流程，头像 MUST 先进入用户头像 pending 目录，并在用户创建成功后 formalize 到 `user-avatars/{user_id}/`。历史头像 key MUST 保持读取兼容。

#### Scenario: 管理员查询用户列表

- **WHEN** `admin` 携带有效 token 请求 `GET /api/v1/admin/users`
- **THEN** 系统返回 HTTP 200，`data` 包含 `items`、`pagination` 与 `summary`
- **AND** 每条用户记录 MUST 包含 id、username、display_name、role、status、avatar_object_key、avatar_url、email、phone、last_login_at、created_at、is_protected、protected_reason
- **AND** 当 `avatar_object_key` 非空时 `avatar_url` MUST 非空且使用受控媒体 URL
- **AND** 新头像 key 在 `user_id` 已存在时 MUST 可追溯到 `images/default/user-avatars/{user_id}/`
- **AND** 历史头像 key 在迁移前 MUST 继续可读。
