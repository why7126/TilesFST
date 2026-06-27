---
bug_id: BUG-0019-user-modal-avatar-upload-display
title: 用户弹窗与列表头像上传后未回显且更换功能未生效
severity: high
status: draft
owner: product
discovered_at: 2026-06-27 13:02:22
environment: local|docker
related_requirement: REQ-0005-user-management
related_change: null
---

# 缺陷说明

## 1. 现象

管理端用户管理模块中，头像上传与展示链路未闭环：

- **用户弹窗**：头像区域始终显示 initials 占位（「默认头像」），编辑已有头像用户时不回显图片；点击「更换头像」选择图片后，弹窗内预览不更新，无上传进度或状态反馈。
- **用户列表**：用户列始终显示 initials，即使数据库已有 `avatar_object_key` 也不展示头像图片。

运行时验证表明：上传请求 Network 200，`avatar_object_key` 已入库，问题不在存储写入，而在前端预览/回显与 API 返回字段缺失。

## 2. 复现步骤

1. 以 admin 登录 Web 管理端。
2. 进入 `/admin/users` 用户管理列表页。
3. 打开某用户「编辑」弹窗，或点击「添加用户」。
4. 观察弹窗头像区：始终为 initials +「默认头像」文案。
5. 点击「更换头像」，选择 JPG/PNG 图片，等待 Network 200。
6. 观察弹窗：预览仍不变，无进度条/上传中状态。
7. 保存并关闭弹窗，再次打开编辑：仍无图片回显。
8. 返回列表页：该用户行头像仍为 initials，非上传图片。

## 3. 期望结果

与已修复的品牌 Logo 弹窗（`BrandFormModal`）行为对齐：

| 场景 | 期望 |
|---|---|
| 弹窗编辑回显 | 有 `avatar_object_key` 时 MUST 展示 `<img>` 预览；无头像时 initials 占位 |
| 更换头像 | 选择文件后 MUST 进入 uploading 状态，展示进度；成功后 MUST 更新预览为 uploaded |
| 上传失败 | MUST 进入 failed 状态并展示错误信息 |
| 保存后 | 列表页与弹窗 MUST 均可看到新头像 |
| 列表页 | 有头像时 MUST 渲染图片；无头像时 initials 占位（AC-011/AC-012） |
| API | 用户列表/详情 MUST 返回可访问 `avatar_url`（spec：`avatar_object_key` 或 `avatar_url`） |

## 4. 实际结果

- 弹窗内始终显示 initials，文案固定「默认头像」。
- 上传成功后 UI 无任何变化，无进度/状态机反馈。
- 列表页不展示已上传头像图片。
- 用户感知为「更换头像功能未生效」，尽管底层可能已持久化 `avatar_object_key`。

## 5. 影响范围

| 范围 | 影响 |
|---|---|
| Web 管理端用户弹窗 | 头像上传/更换无法被用户确认，编辑体验失效 |
| Web 管理端用户列表 | 已上传头像不可见，与 REQ-0005 列表展示要求不符 |
| 后端 API | `UserAdminItem` 缺 `avatar_url`，与 `openspec/specs/user-management/spec.md` 不一致 |
| 父需求验收 | REQ-0005 AC-019（头像上传）、requirement.md「头像允许更换」存在风险 |
| 小程序 / 店主端 | 不涉及 |

## 6. 严重等级说明

严重等级为 `high`。

原因：

- 头像为用户管理基础字段，弹窗与列表同时不可见，非单点 UI 问题。
- 上传链路已通但 UI 完全无反馈，导致管理员重复操作或误判功能损坏。
- 与品牌 Logo 同类缺陷（BUG-0004/0007）已在 Sprint-002 修复，用户模块未同步，形成能力不一致。

## 7. 关联信息

| 类型 | 编号 | 说明 |
|---|---|---|
| 父需求 | `REQ-0005-user-management` | 用户管理能力 |
| 参照 BUG | `BUG-0004-brand-logo-upload-progress-missing` | Logo 上传进度状态机 |
| 参照 BUG | `BUG-0007-brand-logo-not-displayed-after-storage-fix` | Logo/avatar_url 回显链路 |
| 修复参照 | `BrandFormModal` / `brand_admin_service._logo_url` | 实现模式 |

## 8. 修复范围（Scope）

本 BUG 修复 MUST 包含：

1. 后端 `UserAdminItem.avatar_url` 生成（`/media/{object_key}`）。
2. `UserFormModal` 头像预览 + 完整上传状态机（对齐 `BrandFormModal`）。
3. `UserManagementPage` 列表头像图片回显。
4. `uploadAvatar` 支持 `onUploadProgress`。
5. 相关后端/前端测试与 Orval 重新生成。
