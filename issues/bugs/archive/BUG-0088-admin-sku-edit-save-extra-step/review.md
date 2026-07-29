---
bug_id: BUG-0088-admin-sku-edit-save-extra-step
status: done
review_result: approved
reviewed_at: 2026-07-28 23:23:36
created_at: 2026-07-28 23:23:36
updated_at: 2026-07-29 08:05:05
---

# Review

## 结论

确认修复。

## 评审清单

- [x] 可复现或根因充分
- [x] 严重等级合理
- [x] 回归验收明确
- [x] 不需要 hotfix 路径

## 说明

该问题影响管理端 SKU 表单弹窗成功态交互。修复应限制在前端弹窗保存成功后的分支处理，确保编辑、创建和保存草稿成功后均直接关闭弹窗并刷新列表，不再显示弹窗内成功 tips、任务追踪反馈或复制追踪 ID 入口。
