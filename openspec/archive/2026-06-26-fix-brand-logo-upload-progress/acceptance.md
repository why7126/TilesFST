---
change_id: fix-brand-logo-upload-progress
bug_id: BUG-0004-brand-logo-upload-progress-missing
status: proposed
created_at: 2026-06-26 09:39:00
---

# Acceptance Mapping

| BUG AC | Change 覆盖 |
|---|---|
| AC-001 | `web-client/spec.md` 选择 Logo 后触发上传；tasks §2 |
| AC-002 | `web-client/spec.md` 上传过程中展示进度反馈；tasks §2 |
| AC-003 | `web-client/spec.md` 上传成功后更新预览和保存对象 Key；tasks §3 |
| AC-004 | `web-client/spec.md` 上传失败可见且可重试；tasks §3 |
| AC-005 | `web-client/spec.md` 同一文件可重新选择；tasks §3 |
| AC-006 | `web-client/spec.md` 品牌管理功能不回退；tasks §5 |
| AC-007 | tasks §4 保持权限、MIME 与媒体安全 |
| AC-008 | tasks §5 测试覆盖上传进度与预览更新 |
| AC-009 | `web-client/spec.md` Design System 约束 |

## 验收清单

- [ ] 选择 Logo 后立即触发上传。
- [ ] 上传过程中能看到进度条、百分比或等价反馈。
- [ ] 上传成功后弹窗预览更新。
- [ ] 保存品牌后再次打开弹窗回显最新 Logo。
- [ ] 上传失败展示错误并允许重试。
- [ ] 重新选择同一文件可触发上传或明确提示。
- [ ] 品牌管理既有功能不回退。
- [ ] 新增或修改样式符合管理端 Design System。
