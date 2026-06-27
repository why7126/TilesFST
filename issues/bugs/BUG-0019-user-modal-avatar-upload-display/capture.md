---
bug_id: BUG-0019-user-modal-avatar-upload-display
status: captured
created_at: 2026-06-27 13:02:22
updated_at: 2026-06-27 13:09:15
severity_hint: high
environment: local|docker
related_requirement: REQ-0005-user-management
related_bug: BUG-0007-brand-logo-not-displayed-after-storage-fix
captured_via: capture
classification_rationale: 用户编辑弹窗已有头像上传与展示能力，但回显与更换未生效，属既有功能异常；与品牌 Logo 弹窗（BUG-0004/0007）同类媒体上传展示链路问题，非新需求。
---

# 现象

管理端用户新增/编辑弹窗中，头像区域始终显示默认 initials 占位（「默认头像」），未回显已上传头像；点击「更换头像」选择图片后，弹窗内预览不更新，用户无法确认上传是否成功或头像是否已更换。

# 复现步骤

1. 以 admin 登录 Web 管理端。
2. 进入「用户管理」列表页。
3. 点击「添加用户」或某行「编辑」，打开用户弹窗。
4. 观察弹窗内头像区域：编辑已有头像用户时，应显示已上传图片但实际仍为 initials 占位。
5. 点击「更换头像」，选择 JPG/PNG 图片。
6. 等待上传完成（或观察网络请求）。
7. 检查弹窗内头像预览是否更新；保存后再次打开编辑弹窗，检查头像是否持久回显。

# 期望 vs 实际

| | 说明 |
|---|---|
| **期望** | 与品牌 Logo 弹窗一致：已有头像 MUST 回显图片；选择新文件后 MUST 触发上传并更新预览；上传过程 SHOULD 有进度或状态反馈；保存后列表/弹窗均可看到新头像。 |
| **实际** | 弹窗内始终显示默认 initials，「更换头像」后预览不更新，功能未生效。 |

# 附件

- 暂无截图。

# 探索结论（/bug-explore）

## 运行时验证

- 上传请求 Network **200**，`avatar_object_key` **已入库**。
- 结论：上传与持久化链路正常，缺陷集中在 **前端预览/回显** 与 **API 缺 `avatar_url`**，非 MinIO/存储回归。

## Scope 决策

| 项 | 决策 |
|---|---|
| 列表页头像回显 | **纳入本 BUG** |
| 上传进度 UI | **对齐品牌 Logo 完整状态机**（idle → uploading → uploaded / failed） |

## 初步备注

- 参照已修复的品牌 Logo 问题处理方式：`BUG-0004-brand-logo-upload-progress-missing`、`BUG-0007-brand-logo-not-displayed-after-storage-fix`。
- 代码侧差异：`UserFormModal` 仅维护 `avatar_object_key`，未绑定可访问 `avatar_url` 预览；`BrandFormModal` 已实现 `logoUrl` 回显与上传进度状态。
- 后端 `UserAdminItem` 当前无 `avatar_url` 字段，可能与品牌 `logo_url` 解析链路同类。
- 列表页 `UserManagementPage` 同样仅渲染 initials，需同 Change 修复。
