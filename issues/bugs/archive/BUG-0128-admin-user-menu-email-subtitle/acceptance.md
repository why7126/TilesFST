---
bug_id: BUG-0128-admin-user-menu-email-subtitle
acceptance_status: passed
created_at: 2026-08-11 22:02:01
updated_at: 2026-08-12 00:15:15
---

# Acceptance

## 回归验收标准

### AC-001 用户菜单栏不显示副标题

- Given 当前后台用户 `display_name` 非空
- When 用户进入管理后台并查看左侧底部用户菜单触发区
- Then 菜单栏仅显示用户昵称
- And 不显示邮箱、伪邮箱或其他副标题

### AC-002 用户菜单栏昵称为空时显示用户名

- Given 当前后台用户 `display_name` 为空且 `username` 非空
- When 用户进入管理后台并查看左侧底部用户菜单触发区
- Then 菜单栏显示用户名
- And 不显示邮箱、伪邮箱或其他副标题

### AC-003 菜单栏不展示真实邮箱

- Given 当前后台用户 `email` 非空
- When 用户进入管理后台并查看左侧底部用户菜单触发区
- Then 菜单栏仍只显示用户昵称或用户名
- And 不显示真实邮箱副标题

### AC-004 个人资料页顶部身份栏不拼接伪邮箱

- Given 当前后台用户 `email` 为空
- When 用户进入“个人资料”页面
- Then 顶部身份栏不显示 `${username}@tilesfst.com`
- And 不显示 `admin@tilesfst.com`
- And 邮箱片段应被省略或替换为非误导性展示

### AC-005 个人资料页顶部身份栏可显示真实邮箱

- Given 当前后台用户 `email` 非空
- When 用户进入“个人资料”页面
- Then 顶部身份栏可以显示该真实邮箱
- And 显示内容必须来自后端返回的 `profile.email`

### AC-006 联系邮箱编辑入口保留

- Given 用户进入“个人资料”页面
- When 查看基础资料表单
- Then “联系邮箱”输入框仍然存在
- And 空邮箱保持为空，不自动填入 `${username}@tilesfst.com`
- And 用户填写真实邮箱后仍可按现有校验保存

### AC-007 用户管理页邮箱能力不纳入本次修复

- Given 管理员进入“用户管理”页面
- When 查看用户列表或用户创建 / 编辑弹窗
- Then 本 BUG 不要求新增邮箱列或邮箱输入框
- And 若后续需要管理员维护用户联系邮箱，应另行创建需求

### AC-008 测试覆盖伪邮箱回归

- Given 修复完成
- When 运行 Web 前端相关测试
- Then `AdminUserMenu` 测试不再断言 `admin@tilesfst.com` 兜底
- And 应断言菜单栏不出现 `username@tilesfst.com` / `admin@tilesfst.com`
- And `ProfilePage` 测试应覆盖邮箱为空时顶部身份栏不拼接伪邮箱

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-12 00:15:15
accepted_by: workflow-sync
source_change: fix-admin-identity-fake-email-display
source_sprint: sprint-022
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

