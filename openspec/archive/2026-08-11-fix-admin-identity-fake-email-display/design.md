# 设计：管理后台身份展示伪邮箱修复

## 根因

管理后台前端把真实资料字段 `email` 和身份展示兜底混用：

- `AdminUserMenu` 使用 `getUserEmail(user?.username, profileEmail)` 生成副标题。
- `getUserEmail()` 在邮箱为空时拼接 `${username}@tilesfst.com`，无用户名时返回 `admin@tilesfst.com`。
- `ProfilePage` 顶部身份栏使用 `profile.email?.trim() || `${profile.username}@tilesfst.com``，邮箱为空时同样展示伪邮箱。

后端个人资料响应中的 `email` 字段可为空，服务层原样返回 `user.email`，不会生成默认邮箱。因此伪邮箱完全来自 Web 前端展示逻辑。

## 修复方案

### 用户菜单栏

- `AdminUserMenu` 保留头像、昵称 / 用户名和 chevron。
- 移除邮箱副标题渲染。
- 移除或废弃 `getUserEmail()` 在菜单栏的调用。
- `AdminSidebar` / `AdminLayout` 可不再向用户菜单传递 `profileEmail`；若保留取 profile shell 的逻辑，也不得用于菜单副标题展示。

### 个人资料页顶部身份栏

- 顶部身份栏构造 meta 片段时只拼接真实字段。
- `profile.email?.trim()` 非空时显示该真实邮箱。
- `profile.email` 为空时省略邮箱片段，避免伪邮箱和多余分隔符。
- “联系邮箱”输入框继续绑定 `form.email`，空值保持空字符串，保存时沿用现有 `form.email.trim() || null`。

### 用户管理页边界

- 本修复不新增用户管理列表邮箱列。
- 本修复不新增用户创建 / 编辑弹窗联系邮箱输入框。
- 若后续需要管理员维护用户联系邮箱，应另行创建需求。

## 测试方案

- 更新 `AdminUserMenu.test.tsx`：
  - 昵称非空时显示昵称，不显示邮箱副标题。
  - 昵称为空时显示用户名，不显示邮箱副标题。
  - 传入真实 `profileEmail` 时仍不显示邮箱。
  - 不出现 `admin@tilesfst.com` 或 `${username}@tilesfst.com`。
- 更新 `ProfilePage.test.tsx`：
  - 邮箱为空时顶部身份栏不拼接伪邮箱。
  - 邮箱非空时顶部身份栏显示真实邮箱。
  - 联系邮箱输入框仍存在且空邮箱不自动填充伪邮箱。
- 保持用户管理页现有测试不展示 `hidden@example.com` 的预期。

## 验证范围

- Web 前端相关 Vitest。
- 视需要运行 `pnpm --dir src/web test -- AdminUserMenu ProfilePage` 或项目既有等价命令。
- 不需要后端 pytest、OpenAPI、Orval、数据库迁移或 Docker Compose 验证。
