---
change_id: fix-admin-current-user-avatar-object-consistency
source_bug: BUG-0140-admin-current-user-avatar-missing-object
sprint: sprint-026
created_at: 2026-08-25 16:08:42
updated_at: 2026-08-25 17:22:18
---

# 设计

## 根因摘要

当前根因状态为 `confirmed`。`users.avatar_object_key` 保存了头像对象 key，但对象存储中对应 object 缺失；profile 服务仍按非空 key 返回 `/media/{object_key}`；个人资料页头像区域缺少图片加载失败后的 initials 兜底。

根本问题是头像 key 写入和历史数据修复没有与对象存储可读性闭环，导致数据库字段、对象、媒体 URL 和前端展示四个环节可以漂移。

## 修复方案

1. 数据修复
   - 提供受控流程扫描 `users.avatar_object_key` 非空记录。
   - 对每个头像 key 通过对象存储适配层或后端媒体读取能力判断 object 是否存在。
   - dry-run 输出缺失数量、跳过数量、脱敏 key 摘要和风险说明。
   - apply 仅清空已确认缺失对象的 `avatar_object_key`，不伪造统一占位 key。
   - apply 后再次 dry-run 应显示无待清理项，或列出明确 blocked 项。
2. 后端写入校验
   - `PATCH /api/v1/profile/me` 接收非空 `avatar_object_key` 时，必须校验 key 符合对象 key 安全边界且对象存在。
   - 对象不存在、权限异常或读取失败时返回统一错误响应，且不更新用户资料。
   - 清空头像应继续允许传入 `null` 或空值语义。
   - 合法头像上传返回的 `object_key` 应可成功写入，并继续返回 `/media/{object_key}`。
3. 前端展示兜底
   - 个人资料页头像图片加载成功时展示图片。
   - 图片加载失败时切换到当前用户 initials，占位尺寸保持稳定。
   - 侧边栏用户菜单现有 `onError` fallback 不回退。

## 测试设计

- 后端测试：
  - 不存在头像 key 写入 `PATCH /api/v1/profile/me` 返回业务错误，数据库保持原值。
  - 上传头像后使用返回 `object_key` 更新 profile 成功，`/media/{object_key}` 返回 200。
  - 清空头像 key 成功，不触发对象存在性误判。
- 前端测试：
  - 个人资料页存在 `avatar_url` 时先尝试渲染图片。
  - 触发图片 `error` 后显示 initials，且不显示破损图片。
  - 侧边栏用户菜单 fallback 行为保持。
- 数据修复测试：
  - dry-run 不写数据库。
  - apply 清理缺失对象 key。
  - 二次 dry-run 幂等。

## 安全边界

- 数据修复输出不得包含真实客户数据、密钥、Authorization header、Cookie、`.env` 内容、本机绝对路径或未脱敏对象存储凭据。
- 后端错误响应不得暴露对象存储 endpoint、bucket、access key、secret key 或底层 SDK 堆栈。
- 前端继续消费后端受控 `/media/{object_key}` 或 API 返回 URL，不直连对象存储。

## UI Contract

| 项 | 内容 |
|---|---|
| 事实源优先级 | BUG-0140 acceptance、Change delta spec、现有 `/admin/profile` CSS Port、`docs/standards/prototype-ui-acceptance.md`、`rules/ui-design.md`。本次不重做页面结构。 |
| 页面与入口 | `/admin/profile`，仅 `admin` 与 `employee` 可访问；通过现有 `AdminLayout` 与 profile API 数据渲染。 |
| 信息架构 | 仅调整基础资料卡片内头像展示状态；不新增卡片、弹窗、筛选、导航或保存 CTA。 |
| 视觉 token | 复用 `.profile-avatar` 既有尺寸、边框、背景、字体和 semantic CSS 变量；fallback 前后容器尺寸稳定。 |
| 交互状态 | `avatar_url` 非空时先渲染图片；图片 `error` 后切换 initials；`avatar_url` 变化时重置失败态。 |
| 图标与文案 | 无新增用户可见操作文案；fallback 使用既有 initials 规则。 |
| Mock/API 边界 | Vitest 使用 mock profile API 验证 render 状态；真实 API 行为由后端 profile 测试覆盖。 |
| 权限规则 | 不改变现有 profile 路由守卫和 `require_admin_access`。 |
| 一致性参照 | 侧边栏 `AdminUserMenu` 已有头像失败 fallback；本次保持该行为不回退。 |

## 验收方式

- 使用 BUG-0140 `acceptance.md` 中媒体四联验收项回填 key、object、URL、render 证据。
- 聚焦运行 profile、admin user avatar、ProfilePage 相关测试。
- 若新增错误码或响应 Schema 变化，运行 OpenAPI/Orval 生成并更新 API 文档。
