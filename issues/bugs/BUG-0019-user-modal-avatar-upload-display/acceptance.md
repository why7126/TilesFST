---
bug_id: BUG-0019-user-modal-avatar-upload-display
status: pending_review
created_at: 2026-06-27 13:11:02
updated_at: 2026-06-27 13:11:02
related_requirement: REQ-0005-user-management
---

# 回归验收标准

## AC-001 用户 API 返回可访问 avatar_url

**Given** 用户记录存在非空 `avatar_object_key`  
**When** 调用 `GET /api/v1/admin/users` 或 `GET /api/v1/admin/users/{id}`  
**Then** 响应 MUST 包含可访问的 `avatar_url`（形如 `/media/{object_key}`）。  
**And** 无头像时 `avatar_url` MUST 为 `null`。  
**And** 浏览器 GET `avatar_url` MUST 返回 200 与图片内容。

## AC-002 编辑弹窗回显已有头像

**Given** 用户已有 `avatar_object_key`  
**When** admin 打开「编辑用户」弹窗  
**Then** 头像区 MUST 展示 `<img>` 预览，而非仅 initials。  
**And** 无头像用户 MUST 显示 initials 占位与「默认头像」或等价文案。

## AC-003 选择头像后必须触发上传

**Given** admin 已打开用户添加/编辑弹窗  
**When** 点击「更换头像」并选择 JPG/PNG/WebP  
**Then** 系统 MUST 立即触发 `POST /api/v1/admin/uploads` 上传。  
**And** 不得要求先保存用户后才开始上传。

## AC-004 上传过程中必须展示进度反馈（对齐品牌 Logo）

**Given** 用户已选择头像图片  
**When** 上传正在进行  
**Then** 弹窗内 MUST 展示进度条、百分比或等价进度反馈。  
**And** 状态 MUST 经过 `idle → uploading → uploaded / failed` 完整状态机。  
**And** 上传中「更换头像」入口 SHOULD 禁用或进入上传中态，避免重复触发。  
**And** 上传中 MUST 禁止提交保存（与 `BrandFormModal` 一致）。

## AC-005 上传成功后必须更新弹窗预览

**Given** 头像上传接口返回成功（含 `object_key` 与 `url`）  
**When** 上传完成  
**Then** 弹窗头像预览 MUST 立即更新为新图片。  
**And** 保存用户时 MUST 提交新的 `avatar_object_key`。  
**And** 保存后再次打开编辑弹窗 MUST 回显最新头像。

## AC-006 上传失败时必须展示错误和重试入口

**Given** 上传失败、网络异常或文件类型不合法  
**When** 上传流程结束  
**Then** 弹窗 MUST 进入 `failed` 状态并展示明确错误信息。  
**And** 用户 MUST 可重新选择图片重试。  
**And** 失败时不得静默覆盖旧头像预览为无效状态。

## AC-007 用户列表展示头像

**Given** `/admin/users` 列表中存在已上传头像的用户  
**When** 查看「用户」列  
**Then** MUST 渲染头像 `<img>`（使用 `avatar_url`）。  
**And** 无头像时 MUST 显示 initials 占位（REQ-0005 AC-012）。  
**And** 图片加载失败 MUST 稳定回退 initials，无布局跳动。

## AC-008 保存后列表与弹窗一致

**Given** 用户在弹窗中更换头像并保存成功  
**When** 返回列表或再次打开编辑弹窗  
**Then** 列表行与弹窗 MUST 均展示新头像。  
**And** 刷新页面后仍可见（持久化 + API 回传正确）。

## AC-009 修复不得破坏既有用户管理功能

**Given** admin 在用户管理页操作  
**When** 执行筛选、分页、添加、编辑、重置密码、冻结/解冻、删除  
**Then** 既有功能 MUST 保持可用。  
**And** 仅 admin 可访问用户管理 API 的权限边界 MUST 不变。

## AC-010 媒体与安全规范

**Given** 修复完成  
**When** 检查头像上传链路  
**Then** MUST 经后端鉴权、MIME 校验与对象 Key 安全处理。  
**And** 不得暴露密钥或未授权对象存储地址。  
**And** 不得前端绕过后端直连 MinIO。

## AC-011 测试覆盖

**Given** 完成 `fix-user-modal-avatar-upload-display`  
**When** 运行测试套件  
**Then** 后端 MUST 覆盖 `avatar_url` 可访问性（参照品牌 Logo URL 测试）。  
**And** 前端 MUST 覆盖弹窗上传状态机、预览更新、列表头像渲染。  
**And** OpenAPI 变更后 MUST 同步 Orval 并更新调用方。

## AC-012 Design System 约束

**Given** 修复修改 Web UI  
**When** 检查头像上传控件与列表头像  
**Then** MUST 使用既有 semantic token / 管理端样式，不得新增裸 Hex。  
**And** 进度条、错误文案、预览态 SHOULD 与 `BrandFormModal` 视觉模式一致。
