---
change_id: fix-admin-current-user-avatar-object-consistency
source_bug: BUG-0140-admin-current-user-avatar-missing-object
sprint: sprint-026
created_at: 2026-08-25 16:08:42
updated_at: 2026-08-25 17:22:18
---

# 任务

- [x] 梳理 `PATCH /api/v1/profile/me` 当前头像写入链路，确认可复用的对象存储适配层存在性检查入口。
- [x] 实现 profile 头像 key 写入校验：非空 `avatar_object_key` 必须对应可读 object，不存在时返回统一业务错误且不写入。
- [x] 实现或补齐历史头像 key 数据修复流程，支持 dry-run、apply 和二次幂等复查摘要。
- [x] 更新个人资料页头像渲染：图片加载失败后稳定 fallback 到当前用户 initials。
- [x] 确认侧边栏 `AdminUserMenu` 头像 fallback 行为不回退。
- [x] 补充后端回归测试：不存在头像 key 拒绝写入、合法上传 key 写入成功、清空头像 key 成功。
- [x] 补充前端回归测试：个人资料页图片加载失败后显示 initials。
- [x] 运行聚焦测试：`uv run pytest tests/test_profile.py tests/test_admin_users.py` 与相关 Vitest 测试。
- [x] 若新增错误码或 Schema 变更，同步错误码文档、OpenAPI、Orval 和 API 索引；若无变更，在 trace 中说明不需要。
- [x] 回填 BUG-0140 媒体四联验收证据：key、object、URL、render。
- [x] 评估是否需要在 `docs/knowledge-base/incidents/` 沉淀头像对象一致性事故复盘；若无新增可复用经验，记录不沉淀原因。
