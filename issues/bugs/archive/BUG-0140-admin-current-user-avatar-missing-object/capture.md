---
bug_id: BUG-0140-admin-current-user-avatar-missing-object
status: done
created_at: 2026-08-25 14:36:24
updated_at: 2026-08-25 17:41:31
severity_hint: high
environment: docker
related_requirement:
related_bug:
lifecycle_stage: plan
---

# 现象

当前登录用户的头像字段 `avatar_object_key` 指向一个缺失的媒体对象，管理后台在 `localhost:3000` 加载 `/media/images/default/user/avatars/*.png` 时返回 404，导致当前登录用户头像无法正常显示。

# 复现步骤

1. 使用存在 `avatar_object_key` 的管理后台账号登录。
2. 进入管理后台任意包含当前登录用户头像的位置，例如侧边栏用户信息区域或个人资料页。
3. 打开浏览器 Network，筛选 `/media/images/default/user/avatars/` 请求。
4. 观察对应头像对象加载结果。

# 期望 vs 实际

- 期望：当前登录用户的 `avatar_object_key` 应指向已存在、可通过 `/media/...` 读取的对象；若对象缺失，应有可控的降级展示或数据修复策略。
- 实际：`avatar_object_key` 指向的 `/media/images/default/user/avatars/*.png` 对象不存在，Web 入口返回 404，头像资源加载失败。

# 影响范围

- 管理后台当前登录用户头像展示。
- 个人资料页、侧边栏用户菜单等消费 `avatar_url` 的位置。
- 本地 / Docker 演示数据或历史上传对象与用户资料字段的一致性。

# 初步线索

- 后端用户资料会根据 `avatar_object_key` 生成 `/media/{object_key}` URL。
- 当前问题表现为对象读取 404，倾向于用户表字段与对象存储 / 本地媒体文件之间存在数据漂移。
- 需进一步确认缺失对象是否来自历史上传清理、示例账号 seed 数据、头像上传失败后的脏字段，或媒体对象迁移遗漏。

# 建议验收或复现要点

- [ ] 确认当前登录用户记录中的 `avatar_object_key` 具体值。
- [ ] 确认对应对象在本地媒体存储 / MinIO 中是否存在。
- [ ] 确认 `/media/{avatar_object_key}` 返回 404 时前端是否稳定 fallback 到用户 initials。
- [ ] 明确修复策略：清理缺失 `avatar_object_key`、补齐对象、或在读取/展示链路增加缺失对象降级。

# 附件

- 用户描述：`当前登录用户头像 avatar_object_key 指向缺失对象，localhost:3000 加载 /media/images/default/user/avatars/*.png 返回 404`。
