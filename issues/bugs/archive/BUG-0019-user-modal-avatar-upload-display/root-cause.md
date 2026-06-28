---
bug_id: BUG-0019-user-modal-avatar-upload-display
status: pending_review
created_at: 2026-06-27 13:11:02
updated_at: 2026-06-27 13:11:02
root_cause_type: code
---

# 根因分析

## 1. 分类

| 项 | 值 |
|---|---|
| 缺陷类型 | **code**（前端 UI 未绑定 + 后端 API 字段缺失） |
| 引入阶段 | `add-user-management` apply（2026-06-20） |
| 责任模块 | `UserFormModal.tsx`、`UserManagementPage.tsx`、`user_admin_service.py` |
| 关联存储 | 无缺陷；上传 API 200，`avatar_object_key` 已入库 |

## 2. 直接原因

### 2.1 弹窗头像 UI 未绑定预览状态

`UserFormModal` 头像区**硬编码** initials，不读取 `avatarKey` 或任何 URL：

```tsx
<span className="avatar">{getUserInitials(displayName, username)}</span>
<span className="user-main">默认头像</span>
```

`handleAvatarChange` 上传成功后仅 `setAvatarKey(result.object_key)`，丢弃 API 返回的 `url`，且 UI 不响应 state 变化。

### 2.2 缺少上传状态机与进度反馈

对比已修复的 `BrandFormModal`：

| 能力 | BrandFormModal | UserFormModal |
|---|---|---|
| 预览 URL state | `logoUrl` | 无 |
| 上传状态 | idle/uploading/uploaded/failed | 无 |
| 进度回调 | `onUploadProgress` | 无 |
| 保存前校验 | 上传中禁止保存 | 无 |

### 2.3 列表页未渲染头像图片

`UserManagementPage` 用户列始终调用 `getUserInitials()`，未使用 `avatar_object_key` 或 `avatar_url` 渲染 `<img>`。

### 2.4 后端 API 缺 `avatar_url`

`UserAdminService.to_item()` 仅返回 `avatar_object_key`；`UserAdminItem` schema 无 `avatar_url` 字段。与 `openspec/specs/user-management/spec.md`（`avatar_object_key` 或 `avatar_url`）及品牌侧 `_logo_url()` 模式不一致，编辑回显无法获得可访问 URL。

## 3. 根本原因

1. **初始交付未完成展示闭环**：`add-user-management` 实现了上传 API、DB 字段与弹窗文件选择，但未完成预览绑定与列表展示，属于交付缺口而非运行时回归。
2. **品牌 Logo 修复未横向同步**：`fix-brand-logo-upload-progress`、`fix-brand-logo-display-after-storage-fix` 仅改品牌模块，用户模块未复用同一模式。
3. **验收与测试未覆盖头像回显**：`UserFormModal.test.tsx` 仅断言字段顺序；`test_admin_users.py` 无 avatar_url / 上传回显用例。

## 4. 触发条件

同时满足即可稳定复现：

- admin 登录 Web 管理端
- 访问 `/admin/users`
- 打开添加/编辑用户弹窗，或查看已有 `avatar_object_key` 的用户行

运行时验证：上传 Network 200 且 DB 已写入，UI 仍不变 — 排除 MinIO/存储层问题。

## 5. 非根因（排除）

| 假设 | 结论 |
|---|---|
| MinIO 写入失败 | 否；上传 200，object_key 已入库 |
| `/media/{object_key}` 不可读 | 否；品牌 Logo 同链路已修复可用 |
| 新需求缺失 | 否；REQ-0005 已要求头像上传与展示 |
| PATCH 未持久化 | 否；`update_user` 在 `avatar_object_key is not None` 时正确更新 |

## 6. 修复方向

参照 `BrandFormModal` + `brand_admin_service._logo_url`：

1. 后端：`UserAdminItem.avatar_url = f"/media/{object_key}"`（有 key 时）。
2. 前端弹窗：`avatarUrl` state、完整上传状态机、`<img>` 预览、`uploadAvatar` 进度回调。
3. 前端列表：有 `avatar_url` 时 `<img>`，否则 initials。
4. 测试 + Orval 同步。

建议 Change：`fix-user-modal-avatar-upload-display`。
