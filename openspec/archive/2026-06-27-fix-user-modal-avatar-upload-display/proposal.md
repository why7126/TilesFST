# Proposal: fix-user-modal-avatar-upload-display

## Why

`BUG-0019-user-modal-avatar-upload-display` 已评审通过（REV-BUG-0019-001）。管理端用户弹窗与列表的头像上传/展示链路未闭环：弹窗始终显示 initials 占位，「更换头像」后预览不更新；列表页不渲染已上传头像。

运行时验证表明 `POST /api/v1/admin/uploads` 返回 200 且 `avatar_object_key` 已入库，问题不在 MinIO 写入，而在 **API 缺 `avatar_url`** 与 **前端未绑定预览/上传状态机**。与已修复的品牌 Logo（BUG-0004、BUG-0007）同类，用户模块未同步 `BrandFormModal` 模式。

父需求：`REQ-0005-user-management`（AC-011、AC-012、AC-019）。

## What Changes

- 后端 `UserAdminItem` 增加 `avatar_url`（有 `avatar_object_key` 时生成 `/media/{object_key}`），对齐 `brand_admin_service._logo_url`。
- `UserFormModal`：头像预览 `<img>`、完整上传状态机（idle/uploading/uploaded/failed）、进度反馈、上传中禁止保存，对齐 `BrandFormModal`。
- `UserManagementPage`：列表用户列有 `avatar_url` 时渲染头像图片，无则 initials。
- `uploadAvatar` 支持 `onUploadProgress`；OpenAPI 变更后同步 Orval。
- 补充后端 avatar_url 可访问性测试与前端 Vitest 回归。

## Impact

| 影响面 | 说明 |
|---|---|
| Web 管理端 | `/admin/users` 列表 + 用户添加/编辑弹窗头像展示与上传交互 |
| 后端 API | `UserAdminItem` 新增 `avatar_url`；需 OpenAPI + Orval |
| 数据库 | 不变更 schema |
| MinIO | 复用既有 avatars 前缀与 `/media` 受控读取 |
| 小程序 / 店主端 | 不涉及 |
| 测试 | pytest + Vitest |
| Design System | 进度条/错误态复用管理端 semantic token，禁止裸 Hex |

## Out of Scope

- 不新增 MinIO Bucket 或上传端点。
- 不修改 Sidebar `AdminUserMenu` 当前用户头像（除非共享组件必须同步且 tasks 明确）。
- 不重做用户管理页整体 UI 或 PNG port CSS。

## Rollback Plan

1. 回滚 `UserAdminItem.avatar_url` 生成与前端预览/状态机改动。
2. 保留既有上传 API 与 `avatar_object_key` 持久化能力。
3. 若已执行 Orval，回滚 generated 客户端至修复前版本。
4. 回滚后重新标记 `BUG-0019` 未修复，保留验收失败记录。
