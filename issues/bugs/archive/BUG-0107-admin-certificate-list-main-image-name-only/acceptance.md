---
bug_id: BUG-0107-admin-certificate-list-main-image-name-only
title: 管理后台证书列表证书字段额外显示图片或文件名称验收标准
acceptance_status: passed
source_change: fix-admin-certificate-list-main-image-name-only
source_sprint: sprint-018
created_at: 2026-08-03 08:22:37
updated_at: 2026-08-03 20:52:16
---

# 验收标准

## 回归验收

- [x] AC-0107-001：进入管理后台证书列表后，证书字段仅展示证书主图和证书名称。
- [x] AC-0107-002：证书字段不展示图片名称、文件名称、对象 key、原始 URL 或上传组件内部文案。
- [x] AC-0107-003：证书无主图时展示合理占位，证书名称仍清晰可读。
- [x] AC-0107-004：证书列表排序、筛选、分页和编辑入口保持可用。
- [x] AC-0107-005：修复不回归 `BUG-0089-admin-certificate-edit-image-filename-noise`，编辑弹窗不重新出现无意义文件名噪音。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-03 20:52:16
accepted_by: workflow-sync
source_change: fix-admin-certificate-list-main-image-name-only
source_sprint: sprint-018
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

