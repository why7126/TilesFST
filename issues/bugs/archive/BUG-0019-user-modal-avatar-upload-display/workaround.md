---
bug_id: BUG-0019-user-modal-avatar-upload-display
status: pending_review
created_at: 2026-06-27 13:11:02
updated_at: 2026-06-27 13:11:02
---

# 临时规避方案

## 1. 操作规避

当前没有稳定的产品内规避方案可让用户在弹窗或列表中确认头像已上传或已更换。

在正式修复前，内部运营可临时采用：

1. 更换头像后点击「保存」，通过 Network 面板确认 `POST /api/v1/admin/uploads` 与 `PATCH /api/v1/admin/users/{id}` 均 200。
2. 通过数据库或 API 响应检查 `avatar_object_key` 是否已写入，**不得**依赖弹窗/列表视觉确认。
3. 暂不向业务方承诺头像在管理端可见；待 BUG-0019 修复后再验收。

## 2. 验收规避

在正式修复前，用户管理验收应拆分：

- 用户名、昵称、角色、状态、重置密码等字段可单独验收。
- 头像上传与展示 MUST 标记为本 BUG 未通过（含弹窗预览、列表回显、上传进度）。
- REQ-0005 AC-019、AC-011/AC-012 中与头像图片展示相关的项暂缓 sign-off。

## 3. 风险说明

该规避不能消除以下风险：

- 管理员误以为头像未上传而重复操作。
- 已入库头像无法在 UI 确认，影响运营信任。
- 与品牌 Logo 已修复体验不一致，造成「部分模块可用、用户模块不可用」的困惑。

因此建议 `/bug-review --approve` 后通过 `fix-user-modal-avatar-upload-display` OpenSpec Change 修复。
