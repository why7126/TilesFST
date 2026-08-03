---
bug_id: BUG-0106-admin-brand-edit-logo-uploaded-text
acceptance_status: passed
created_at: 2026-08-03 08:22:25
updated_at: 2026-08-03 20:52:16
source_change: fix-admin-brand-edit-logo-uploaded-text
source_sprint: null
---

# 验收标准

## 回归 AC

### AC-001 品牌编辑弹窗不显示冗余成功态文案

- Given 管理后台存在已上传 Logo 的品牌
- When 管理员打开该品牌的编辑弹窗
- Then Logo 区域旁不显示 `已上传Logo`、`品牌Logo` 或等价冗余文案
- And 页面仍保留必要的 Logo 图片预览、上传或替换控件

### AC-002 已上传 Logo 仍可正常预览

- Given 品牌已有有效 Logo 图片
- When 管理员打开品牌编辑弹窗
- Then Logo 图片按现有预览规则正常展示
- And Logo 图片顶部与格式提示文字顶部视觉对齐
- And 不因移除冗余文案导致预览区域空白或布局错位

### AC-003 Logo 替换和重新上传交互保持正常

- Given 管理员在品牌编辑弹窗中操作 Logo 上传区域
- When 管理员选择替换、删除或重新上传 Logo
- Then 原有交互仍可完成
- And 上传成功后不展示 `已上传Logo` 冗余文案

### AC-004 错误与处理中状态提示仍可见

- Given 管理员上传不支持的文件或上传过程发生错误
- When Logo 上传组件进入错误、格式不支持或上传中状态
- Then 必要的错误提示、格式提示或上传中状态仍按原有规则展示
- And 不因隐藏 `已上传Logo` 文案而误删必要反馈

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-03 20:52:16
accepted_by: workflow-sync
source_change: fix-admin-brand-edit-logo-uploaded-text
source_sprint: sprint-018
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

