---
change_id: fix-user-modal-avatar-upload-display
bug_id: BUG-0019-user-modal-avatar-upload-display
created_at: 2026-06-27 13:14:25
updated_at: 2026-06-27 13:14:25
---

# 验收标准

映射 `issues/bugs/archive/BUG-0019-user-modal-avatar-upload-display/acceptance.md` AC-001～AC-012。

## 关键 Gate

- [ ] API 返回 `avatar_url` 且浏览器可加载
- [ ] 弹窗编辑回显 + 上传状态机 + 进度（对齐 BrandFormModal）
- [ ] 列表页头像图片回显
- [ ] pytest + Vitest 通过；Orval 已同步
- [ ] 无裸 Hex；用户管理其他功能不回归
